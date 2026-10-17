"""Native Sidecar fixture is validated without promoting normative AIOS layers."""

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker, ValidationError


def test_native_sidecar_draft_fixture() -> None:
    root = Path(__file__).resolve().parents[1] / "drafts/sidecar-correlation-v1"
    schema = json.loads((root / "schema.json").read_text())
    fixture = json.loads((root / "example.json").read_text())
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(fixture)
    assert fixture["contract_version"] == "sidecar.correlation/1"
    assert "Non-normative" in (root / "README.md").read_text()


@pytest.mark.parametrize("missing_id,bad_timestamp", [(True, False), (False, True)])
def test_native_draft_rejects_missing_identity_and_bad_time(missing_id: bool, bad_timestamp: bool) -> None:
    root = Path(__file__).resolve().parents[1] / "drafts/sidecar-correlation-v1"
    schema = json.loads((root / "schema.json").read_text())
    fixture = json.loads((root / "example.json").read_text())
    if missing_id:
        del fixture["decision"]["decision_id"]
    if bad_timestamp:
        fixture["timestamp"] = "not-a-date"
    with pytest.raises(ValidationError):
        Draft202012Validator(schema, format_checker=FormatChecker()).validate(fixture)
