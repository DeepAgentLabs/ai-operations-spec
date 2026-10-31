"""Keep the machine-readable conformance catalogs in sync with the normative prose.

`specification/v0.4/conformance-rules.json` and `specification/v0.5/compatibility.json`
only assign stable identifiers to requirements the Markdown documents already
state. These checks fail if a rule is added, removed, or reworded on one side
without the other.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).parents[1]
V04 = ROOT / "specification" / "v0.4"
V05 = ROOT / "specification" / "v0.5"

RULES = json.loads((V04 / "conformance-rules.json").read_text(encoding="utf-8"))
COMPATIBILITY = json.loads((V05 / "compatibility.json").read_text(encoding="utf-8"))


def normalize(text: str) -> str:
    """Drop Markdown emphasis/code markers and collapse whitespace for prose comparison."""
    return " ".join(text.replace("`", "").replace("**", "").split())


# The obligation the numbered producer rules (P01-P12) share.
PRODUCER_LEAD_IN = "A producer claiming draft alignment MUST:"


def producer_requirements() -> list[str]:
    conformance = (V04 / "conformance.md").read_text(encoding="utf-8")
    section = conformance.split("## Producer requirements", 1)[1].split("\n## ", 1)[0]
    items = re.findall(r"^\d+\.\s+(.*?)(?=^\d+\.\s|^\S|\Z)", section, flags=re.M | re.S)
    return [normalize(item) for item in items]


def compatibility_rows() -> list[list[str]]:
    versioning = (V05 / "versioning.md").read_text(encoding="utf-8")
    section = versioning.split("## Consumer compatibility behavior", 1)[1].split("\n## ", 1)[0]
    rows = [line for line in section.splitlines() if line.startswith("| ")]
    # Skip the header row; the separator row starts with "| ---" and is excluded too.
    return [
        [normalize(cell) for cell in row.strip("|").split(" | ")]
        for row in rows[1:]
        if not row.startswith("| ---")
    ]


def test_rule_ids_are_unique_and_well_formed() -> None:
    ids = [rule["id"] for rule in RULES["rules"]]
    assert len(ids) == len(set(ids))
    for rule_id in ids:
        assert re.fullmatch(r"AIOS-0\.4-[PXCUEDK]\d{2}", rule_id), rule_id
    for rule in RULES["rules"]:
        assert rule["check"] in RULES["check_kinds"]
        assert rule["role"] in {"producer", "consumer", "implementation"}
        assert rule["level"] in {"MUST", "MUST NOT", "SHOULD"}
        assert set(rule["applies_to"]) <= {"workflow", "run"}


def test_producer_rules_mirror_the_numbered_producer_requirements() -> None:
    documented = producer_requirements()
    catalog = [rule for rule in RULES["rules"] if rule["id"].startswith("AIOS-0.4-P")]
    assert len(documented) == 12
    assert [rule["id"] for rule in catalog] == [f"AIOS-0.4-P{n:02d}" for n in range(1, 13)]
    for rule, text in zip(catalog, documented):
        assert normalize(rule["requirement"]) == text, rule["id"]


def test_every_rule_quotes_its_normative_sentence() -> None:
    conformance = normalize((V04 / "conformance.md").read_text(encoding="utf-8"))
    for rule in RULES["rules"]:
        assert normalize(rule["source_text"]) in conformance, rule["id"]
        if rule["id"].startswith("AIOS-0.4-P"):
            continue  # numbered items inherit MUST from PRODUCER_LEAD_IN
        # The quoted sentence must carry the rule's own obligation keyword.
        assert rule["level"].split()[0] in rule["source_text"], rule["id"]


def test_every_normative_keyword_in_the_document_is_cataloged() -> None:
    """Each MUST/MUST NOT/SHOULD occurrence must fall inside some rule's quoted text."""
    conformance = normalize((V04 / "conformance.md").read_text(encoding="utf-8"))
    quoted = [normalize(rule["source_text"]) for rule in RULES["rules"]] + [PRODUCER_LEAD_IN]
    covered = [(conformance.find(text), conformance.find(text) + len(text)) for text in quoted]
    for match in re.finditer(r"\b(MUST|SHOULD)\b", conformance):
        position = match.start()
        assert any(start <= position < end for start, end in covered), conformance[
            max(0, position - 60) : position + 60
        ]

def test_claim_template_matches_the_documented_claim_format() -> None:
    conformance = (V04 / "conformance.md").read_text(encoding="utf-8")
    example = RULES["claim_template"].replace("{date}", "2026-07-21")
    assert example in conformance


def test_compatibility_pattern_is_the_versioning_grammar() -> None:
    versioning = (V05 / "versioning.md").read_text(encoding="utf-8")
    assert COMPATIBILITY["spec_version_pattern"] in versioning


EXPECTED_DECISIONS = [
    "accept",
    "accept_informal",
    "validate_against_declared_schema",
    "accept_extension_only",
    "reject",
    "accept_as_older",
]


def test_consumer_rules_mirror_the_compatibility_table() -> None:
    rows = compatibility_rows()
    rules = COMPATIBILITY["consumer_rules"]
    assert len(rows) == len(rules) == 6
    assert [rule["id"] for rule in rules] == [f"AIOS-0.5-V{n:02d}" for n in range(1, 7)]
    assert [rule["decision"] for rule in rules] == EXPECTED_DECISIONS
    for rule, (producer, consumer, requirement) in zip(rules, rows):
        assert rule["producer"] == producer, rule["id"]
        assert rule["consumer"] == consumer, rule["id"]
        assert normalize(rule["requirement"]) == requirement, rule["id"]


def test_published_schema_sets_resolve_and_declare_their_marker() -> None:
    pattern = re.compile(COMPATIBILITY["spec_version_pattern"])
    published = COMPATIBILITY["published_schema_sets"]
    for marker, entry in published.items():
        assert pattern.match(marker), marker
        schema_dir = ROOT / entry["schema_directory"]
        declared: set[str] = set()
        for path in sorted(schema_dir.glob("*.schema.json")):
            schema = json.loads(path.read_text(encoding="utf-8"))
            if "artifact_type" not in schema.get("properties", {}):
                continue  # shared definitions such as common.schema.json
            declared.add(schema["properties"]["artifact_type"]["const"])
            assert path.name == f"{schema['properties']['artifact_type']['const']}.schema.json", path.name
            assert schema["properties"]["spec_version"] == {"const": marker}, path.name
        assert declared == set(entry["artifact_types"]), marker
        for dependency in entry.get("depends_on", []):
            assert dependency in published and dependency != marker, marker
        rules_path = ROOT / entry["conformance_rules"]
        assert json.loads(rules_path.read_text(encoding="utf-8"))["spec_version"] == marker
        assert entry["frozen"] == (not marker.endswith("-draft")), marker


def test_each_artifact_type_has_exactly_one_published_marker() -> None:
    owners: dict[str, list[str]] = {}
    for marker, entry in COMPATIBILITY["published_schema_sets"].items():
        for artifact_type in entry["artifact_types"]:
            owners.setdefault(artifact_type, []).append(marker)
    assert owners == {"workflow": ["0.4-draft"], "run": ["0.4-draft"], "provenance": ["0.6-draft"]}
