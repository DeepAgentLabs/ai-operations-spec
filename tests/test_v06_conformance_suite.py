"""Run the portable conformance suite with the repository's reference checks."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from aios_reference import check, resolve

ROOT = Path(__file__).parents[1]
SUITE_DIR = ROOT / "specification" / "v0.6" / "conformance-suite"
SUITE = json.loads((SUITE_DIR / "suite.json").read_text(encoding="utf-8"))
CATALOGS = [
    ROOT / "specification" / "v0.4" / "conformance-rules.json",
    ROOT / "specification" / "v0.6" / "provenance-rules.json",
]


def load(relative: str) -> object:
    return json.loads((SUITE_DIR / relative).read_text(encoding="utf-8"))


def catalog_rules() -> list[dict]:
    return [rule for path in CATALOGS for rule in json.loads(path.read_text(encoding="utf-8"))["rules"]]


@pytest.mark.parametrize("case", SUITE["cases"], ids=lambda case: case["id"])
def test_outcome_case(case: dict) -> None:
    assert check(load(case["path"])) == (case["expected"], case["rules"])


@pytest.mark.parametrize("case", SUITE["resolution_cases"], ids=lambda case: case["id"])
def test_resolution_case(case: dict) -> None:
    record = load(case["record"])
    assert check(record) == ("valid", [])
    held = {subject: (SUITE_DIR / path).read_bytes() for subject, path in case["subjects"].items()}
    assert resolve(record, held) == case["expected"]


def test_manifest_lists_every_file_once() -> None:
    ids = [case["id"] for case in SUITE["cases"] + SUITE["resolution_cases"]]
    assert len(ids) == len(set(ids))
    paths = [case["path"] for case in SUITE["cases"]]
    assert len(paths) == len(set(paths))
    assert set(paths) == {f"cases/{path.name}" for path in (SUITE_DIR / "cases").glob("*.json")}
    used = {path for case in SUITE["resolution_cases"] for path in case["subjects"].values()}
    assert used == {f"subjects/{path.name}" for path in (SUITE_DIR / "subjects").glob("*.json")}
    assert {case["expected"] for case in SUITE["cases"]} == set(SUITE["outcomes"])
    for case in SUITE["cases"]:
        assert case["id"] == Path(case["path"]).stem
        assert (case["expected"] == "valid") == (not case["rules"]), case["id"]


def test_every_decidable_rule_has_a_case() -> None:
    cited = {rule for case in SUITE["cases"] for rule in case["rules"]}
    exercised = {rule for case in SUITE["resolution_cases"] for rule in case["rules"]}
    for rule in catalog_rules():
        if rule["check"] in {"schema", "semantic"} and rule["role"] == "producer":
            described = any(rule["id"] in case["description"] for case in SUITE["cases"])
            assert rule["id"] in cited or described, rule["id"]
        if rule["check"] == "cross_artifact":
            assert rule["id"] in exercised, rule["id"]
    assert "AIOS-0.5-V03" in cited
    known = {rule["id"] for rule in catalog_rules()} | {"AIOS-0.5-V03"}
    assert cited | exercised <= known


def test_suite_snapshot_matches_the_repository_release() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert f'version = "{SUITE["snapshot"].removeprefix("v")}"' in pyproject
