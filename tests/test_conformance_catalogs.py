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
    """Drop Markdown code ticks and collapse whitespace for prose comparison."""
    return " ".join(text.replace("`", "").split())


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
        assert re.fullmatch(r"AIOS-0\.4-[PXCU]\d{2}", rule_id), rule_id
    for rule in RULES["rules"]:
        assert rule["check"] in RULES["check_kinds"]
        assert rule["role"] in {"producer", "consumer"}
        assert set(rule["applies_to"]) <= {"workflow", "run"}


def test_producer_rules_mirror_the_numbered_producer_requirements() -> None:
    documented = producer_requirements()
    catalog = [rule for rule in RULES["rules"] if rule["id"].startswith("AIOS-0.4-P")]
    assert len(documented) == 12
    assert [rule["id"] for rule in catalog] == [f"AIOS-0.4-P{n:02d}" for n in range(1, 13)]
    for rule, text in zip(catalog, documented):
        assert normalize(rule["requirement"]) == text, rule["id"]


def test_consumer_and_external_rules_quote_the_conformance_document() -> None:
    conformance = normalize((V04 / "conformance.md").read_text(encoding="utf-8")).lower()
    for rule in RULES["rules"]:
        if rule["id"][len("AIOS-0.4-")] not in {"X", "C"}:
            continue
        assert normalize(rule["requirement"]).rstrip(".").lower() in conformance, rule["id"]
    unknown_value = next(rule for rule in RULES["rules"] if rule["id"] == "AIOS-0.4-U01")
    assert "D-004" in unknown_value["requirement"]
    assert "rather than guessing its meaning" in conformance


def test_claim_template_matches_the_documented_claim_format() -> None:
    conformance = (V04 / "conformance.md").read_text(encoding="utf-8")
    example = RULES["claim_template"].replace("{date}", "2026-07-21")
    assert example in conformance


def test_compatibility_pattern_is_the_versioning_grammar() -> None:
    versioning = (V05 / "versioning.md").read_text(encoding="utf-8")
    assert COMPATIBILITY["spec_version_pattern"] in versioning


def test_consumer_rules_mirror_the_compatibility_table() -> None:
    rows = compatibility_rows()
    rules = COMPATIBILITY["consumer_rules"]
    assert len(rows) == len(rules) == 6
    assert [rule["id"] for rule in rules] == [f"AIOS-0.5-V{n:02d}" for n in range(1, 7)]
    for rule, row in zip(rules, rows):
        assert normalize(rule["requirement"]) == row[-1], rule["id"]


def test_published_schema_sets_resolve_and_declare_their_marker() -> None:
    pattern = re.compile(COMPATIBILITY["spec_version_pattern"])
    for marker, entry in COMPATIBILITY["published_schema_sets"].items():
        assert pattern.match(marker), marker
        schema_dir = ROOT / entry["schema_directory"]
        schemas = sorted(schema_dir.glob("*.schema.json"))
        assert schemas, f"no schemas under {schema_dir}"
        for path in schemas:
            text = path.read_text(encoding="utf-8")
            for value in re.findall(r'"spec_version":\s*\{"const":\s*"([^"]+)"\}', text):
                assert value == marker, f"{path.name} declares {value}, catalog says {marker}"
        rules_path = ROOT / entry["conformance_rules"]
        assert json.loads(rules_path.read_text(encoding="utf-8"))["spec_version"] == marker
        assert entry["frozen"] == (not marker.endswith("-draft")), marker
