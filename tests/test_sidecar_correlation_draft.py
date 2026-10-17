"""Native Sidecar fixture is validated without promoting normative AIOS layers."""

import json
from pathlib import Path

from jsonschema import Draft202012Validator


def test_native_sidecar_draft_fixture() -> None:
    root = Path(__file__).resolve().parents[1] / "drafts/sidecar-correlation-v1"
    schema = json.loads((root / "schema.json").read_text())
    fixture = json.loads((root / "example.json").read_text())
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(fixture)
    assert fixture["contract_version"] == "sidecar.correlation/1"
    assert "Non-normative" in (root / "README.md").read_text()
