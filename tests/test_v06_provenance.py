"""Provenance records: schema, rule catalog, semantics and cross-artifact resolution."""
from __future__ import annotations

import copy
import json
import re
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from aios_reference import check, resolve, validator
from test_conformance_catalogs import normalize

ROOT = Path(__file__).parents[1]
V06 = ROOT / "specification" / "v0.6"
DOCUMENT = (V06 / "provenance.md").read_text(encoding="utf-8")
CATALOG = json.loads((V06 / "provenance-rules.json").read_text(encoding="utf-8"))
SCHEMA = json.loads((V06 / "schemas" / "provenance.schema.json").read_text(encoding="utf-8"))
EXAMPLE_PATH = V06 / "examples" / "provenance" / "support-finding.provenance.json"
SUBJECT_BYTES = (V06 / "examples" / "advanced-support-run.json").read_bytes()
PRODUCER_LEAD_IN = "A producer claiming draft alignment for a provenance record MUST:"


def example() -> dict:
    return json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))


def producer_requirements() -> list[str]:
    section = DOCUMENT.split("## Producer requirements", 1)[1].split("\n## ", 1)[0]
    items = re.findall(r"^\d+\.\s+(.*?)(?=^\d+\.\s|^\S|\Z)", section, flags=re.M | re.S)
    return [normalize(item) for item in items]


def test_schema_is_valid_and_declares_its_marker() -> None:
    Draft202012Validator.check_schema(SCHEMA)
    assert SCHEMA["properties"]["spec_version"] == {"const": CATALOG["spec_version"]}
    assert SCHEMA["properties"]["artifact_type"] == {"const": "provenance"}


def test_catalog_identifiers_and_kinds() -> None:
    ids = [rule["id"] for rule in CATALOG["rules"]]
    assert len(ids) == len(set(ids))
    for rule in CATALOG["rules"]:
        assert re.fullmatch(r"AIOS-0\.6-[RCDKS]\d{2}", rule["id"]), rule["id"]
        assert rule["check"] in CATALOG["check_kinds"], rule["id"]
        assert rule["applies_to"] == ["provenance"], rule["id"]


def test_producer_rules_mirror_the_numbered_requirements() -> None:
    documented = producer_requirements()
    catalog = [rule for rule in CATALOG["rules"] if rule["id"].startswith("AIOS-0.6-R")]
    assert [rule["id"] for rule in catalog] == [f"AIOS-0.6-R{n:02d}" for n in range(1, len(documented) + 1)]
    for rule, text in zip(catalog, documented):
        assert normalize(rule["requirement"]) == text, rule["id"]
        assert normalize(rule["source_text"]) == text, rule["id"]


def test_every_normative_keyword_is_cataloged() -> None:
    document = normalize(DOCUMENT)
    quoted = [normalize(rule["source_text"]) for rule in CATALOG["rules"]] + [PRODUCER_LEAD_IN]
    for text in quoted:
        assert text in document, text
    covered = [(document.find(text), document.find(text) + len(text)) for text in quoted]
    for match in re.finditer(r"\b(MUST|SHOULD)\b", document):
        assert any(start <= match.start() < end for start, end in covered), document[
            max(0, match.start() - 60) : match.start() + 60
        ]


def test_claim_template_matches_the_documented_claim() -> None:
    assert CATALOG["claim_template"].replace("{date}", "2026-10-31") in DOCUMENT


def test_documented_vocabularies_match_the_schema() -> None:
    definitions = SCHEMA["$defs"]
    source_kinds = set(re.findall(r"^\| `([a-z_]+)` \|", DOCUMENT.split("### Source reference", 1)[1].split("###", 1)[0], re.M))
    lineage_types = set(re.findall(r"^\| `([a-z-]+)` \|", DOCUMENT.split("### Evidence lineage", 1)[1].split("##", 1)[0], re.M))
    source_kinds.discard("kind")  # table header
    lineage_types.discard("type")
    assert source_kinds == set(definitions["source"]["properties"]["kind"]["enum"])
    assert lineage_types == set(definitions["lineage_edge"]["properties"]["type"]["enum"])
    for value in lineage_types:
        assert re.fullmatch(r"[a-z]+(-[a-z]+)*", value), value


def test_example_is_valid_and_resolves_against_its_subject() -> None:
    record = example()
    assert check(record) == ("valid", [])
    report = resolve(record, {"subject-run": SUBJECT_BYTES})
    assert report["subjects"]["subject-run"] == {
        "available": True, "valid": True, "identity": "match", "digest": "verified",
    }
    assert set(report["references"].values()) == {"resolved"}


def test_unavailable_subject_leaves_references_unresolved_not_invalid() -> None:
    record = example()
    report = resolve(record, {})
    assert report["subjects"]["subject-run"]["digest"] == "unchecked"
    assert set(report["references"].values()) == {"unresolved"}
    assert check(record) == ("valid", [])


def test_changed_bytes_fail_digest_verification_without_changing_resolution() -> None:
    reformatted = json.dumps(json.loads(SUBJECT_BYTES)).encode()
    report = resolve(example(), {"subject-run": reformatted})
    assert report["subjects"]["subject-run"]["digest"] == "mismatch"
    assert set(report["references"].values()) == {"resolved"}


def test_mismatched_or_invalid_subject_is_not_used_for_resolution() -> None:
    other = json.loads(SUBJECT_BYTES)
    other["id"] = "run-other"
    report = resolve(example(), {"subject-run": json.dumps(other).encode()})
    assert report["subjects"]["subject-run"]["identity"] == "mismatch"
    assert set(report["references"].values()) == {"unresolved"}
    broken = json.loads(SUBJECT_BYTES)
    broken["steps"].append({"id": "step-orphan", "category": "model"})
    report = resolve(example(), {"subject-run": json.dumps(broken).encode()})
    assert report["subjects"]["subject-run"]["valid"] is False
    assert set(report["references"].values()) == {"unresolved"}


def test_missing_and_mistyped_objects_are_distinguished() -> None:
    record = example()
    record["sources"][0]["object"]["id"] = "eval-missing"
    record["sources"][1]["object"]["type"] = "tool_invocation"
    references = resolve(record, {"subject-run": SUBJECT_BYTES})["references"]
    assert references["source-evaluation"] == "missing"
    assert references["source-retrieval"] == "type_mismatch"


def mutate(change) -> dict:
    record = copy.deepcopy(example())
    change(record)
    return record


SEMANTIC_MUTATIONS = {
    "AIOS-0.6-R02": lambda r: r["lineage"][1].update(id="lineage-grounded-evaluation"),
    "AIOS-0.6-R03": lambda r: r["sources"][0].update(subject="subject-missing"),
    "AIOS-0.6-R04": lambda r: r["lineage"][2].update(target="source-review"),
    "AIOS-0.6-R05": lambda r: r.update(lineage=[e for e in r["lineage"] if e["source"] != "finding-stale-source"]),
    "AIOS-0.6-R06": lambda r: r["lineage"].append(
        {"id": "lineage-loop", "type": "derived-from", "source": "finding-grounded", "target": "finding-grounded"}
    ),
    "AIOS-0.6-R07": lambda r: r["sources"][3].update(captured_at="2026-07-21T06:06:00Z"),
}


@pytest.mark.parametrize("rule_id", sorted(SEMANTIC_MUTATIONS))
def test_each_semantic_rule_rejects_its_violation(rule_id: str) -> None:
    record = mutate(SEMANTIC_MUTATIONS[rule_id])
    assert check(record) == ("semantic-invalid", [rule_id])


@pytest.mark.parametrize(
    "change",
    [
        lambda r: r["sources"][0].pop("object"),
        lambda r: r["sources"][0]["object"].update(external=True),
        lambda r: r["findings"][1]["targets"][0]["object"].update(external=True),
        lambda r: r["sources"][2].update(kind="artifact"),
        lambda r: r["sources"][3].pop("description"),
        lambda r: r["subjects"][0]["digest"].update(value="abc"),
        lambda r: r["findings"][0].update(confidence=1.5),
        lambda r: r["lineage"][0].update(type="cites"),
        lambda r: r.update(subjects=[]),
        lambda r: r.update(extensions={"aiops.provenance.extra": {}}),
        lambda r: r.update(run_id="run-001"),
    ],
)
def test_schema_rejections(change) -> None:
    record = mutate(change)
    assert check(record) == ("schema-invalid", ["AIOS-0.6-R01"])


def test_routing_follows_the_declared_marker() -> None:
    record = example()
    record["spec_version"] = "0.4-draft"
    assert check(record) == ("unsupported", ["AIOS-0.5-V03"])
    record["spec_version"] = "0.7-draft"
    assert check(record) == ("unsupported", ["AIOS-0.5-V03"])
    run = json.loads(SUBJECT_BYTES)
    run["spec_version"] = "0.6-draft"
    assert check(run) == ("unsupported", ["AIOS-0.5-V03"])
    validator(example()).validate(example())
