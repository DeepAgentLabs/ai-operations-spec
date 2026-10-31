"""Enforce specification/v0.6/naming-conventions.md over every published schema."""
from __future__ import annotations

import json
import re
from collections.abc import Iterator
from pathlib import Path

ROOT = Path(__file__).parents[1]
SCHEMA_PATHS = sorted((ROOT / "specification").glob("v*/schemas/*.schema.json"))
CATALOG_PATHS = [
    ROOT / "specification" / "v0.4" / "conformance-rules.json",
    ROOT / "specification" / "v0.5" / "compatibility.json",
    *sorted((ROOT / "specification" / "v0.6").glob("*-rules.json")),
]

FIELD = re.compile(r"^[a-z][a-z0-9]*(_[a-z0-9]+)*$")
SNAKE_VALUE = re.compile(r"^[a-z][a-z0-9]*(_[a-z0-9]+)*$")
KEBAB_VALUE = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")
MASS_NOUNS = {"evidence", "lineage"}
ABBREVIATIONS = {"id", "uri", "rag"}
FORBIDDEN_ABBREVIATIONS = {"ts", "msg", "obj", "rel", "attr", "attrs", "ext", "cfg", "num", "info", "desc"}


def properties(node: object, path: str = "") -> Iterator[tuple[str, str, dict]]:
    """Yield (location, field name, field schema) for every declared property."""
    if isinstance(node, dict):
        for name, schema in node.get("properties", {}).items():
            yield f"{path}.{name}", name, schema
        for key, value in node.items():
            yield from properties(value, f"{path}/{key}")
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from properties(value, f"{path}[{index}]")


def is_time(schema: dict) -> bool:
    return schema.get("format") == "date-time" or schema.get("$ref", "").endswith("/$defs/time")


def is_array(schema: dict) -> bool:
    return schema.get("type") == "array"


def all_fields() -> list[tuple[str, str, dict]]:
    fields = []
    for path in SCHEMA_PATHS:
        schema = json.loads(path.read_text(encoding="utf-8"))
        fields.extend((f"{path.name}{location}", name, field) for location, name, field in properties(schema))
    return fields


def test_schemas_are_discovered() -> None:
    assert {path.parent.parent.name for path in SCHEMA_PATHS} >= {"v0.4"}
    assert all_fields()


def test_field_names_are_snake_case_words() -> None:
    for location, name, _ in all_fields():
        assert FIELD.fullmatch(name), location
        assert not set(name.split("_")) & FORBIDDEN_ABBREVIATIONS, location


def test_time_fields_and_suffixes_agree() -> None:
    for location, name, schema in all_fields():
        assert is_time(schema) == name.endswith("_at"), location


def test_arrays_are_plural_and_scalars_singular() -> None:
    for location, name, schema in all_fields():
        if is_array(schema):
            assert name.endswith("s") or name in MASS_NOUNS, location
        elif name.endswith("s") and name not in {"status", "attributes", "extensions"}:
            raise AssertionError(f"{location} looks plural but is not an array")


def test_booleans_are_positive_adjectives() -> None:
    for location, name, schema in all_fields():
        if schema.get("type") == "boolean":
            assert not name.startswith(("is_", "has_", "not_", "un")), location


def enum_values(field: str) -> set[str]:
    values: set[str] = set()
    for location, name, schema in all_fields():
        if name == field:
            values.update(value for value in schema.get("enum", []) if isinstance(value, str))
    return values


def test_vocabulary_values_follow_their_documented_form() -> None:
    common = json.loads((ROOT / "specification" / "v0.4" / "schemas" / "common.schema.json").read_text())
    relationship_types = set(common["$defs"]["relationship"]["properties"]["type"]["enum"])
    object_types = set(common["$defs"]["reference"]["properties"]["type"]["enum"])
    for value in relationship_types:
        assert KEBAB_VALUE.fullmatch(value), value
    for value in object_types | enum_values("object_type") | enum_values("kind") | enum_values("status"):
        assert SNAKE_VALUE.fullmatch(value), value
    for event in common["$defs"]["canonical_event_name"]["enum"]:
        assert re.fullmatch(r"aiops\.[a-z]+\.[a-z]+", event), event


def test_catalog_rule_identifiers_follow_the_documented_grammar() -> None:
    seen: set[str] = set()
    for path in CATALOG_PATHS:
        catalog = json.loads(path.read_text(encoding="utf-8"))
        for rule in catalog.get("rules", []) + catalog.get("consumer_rules", []):
            assert re.fullmatch(r"AIOS-0\.[1-9][0-9]*-[A-Z]\d{2}", rule["id"]), rule["id"]
            assert rule["id"] not in seen, rule["id"]
            seen.add(rule["id"])


def test_documented_abbreviation_and_mass_noun_lists_match_this_test() -> None:
    document = (ROOT / "specification" / "v0.6" / "naming-conventions.md").read_text(encoding="utf-8")
    abbreviations = document.split("## Abbreviations", 1)[1].split("\n## ", 1)[0]
    assert set(re.findall(r"`([a-z]+)`", abbreviations.split("Acronyms", 1)[0])) == ABBREVIATIONS
    plural = document.split("## Singular and plural", 1)[1].split("\n## ", 1)[0]
    assert set(re.findall(r"`([a-z]+)`", plural.split("Mass nouns", 1)[1])) == MASS_NOUNS
