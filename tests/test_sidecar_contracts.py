"""Portable, non-normative Sidecar v1 candidate schema acceptance."""

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker, ValidationError

ROOT = Path(__file__).parents[1] / "drafts" / "sidecar-contracts-v1"


@pytest.mark.parametrize("kind", ["intent", "decision", "audit", "scope", "transfer"])
def test_candidate_schema_examples_and_negative_markers(kind):
    schema = json.loads((ROOT / f"{kind}.schema.json").read_text())
    example = json.loads((ROOT / f"{kind}.example.json").read_text())
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    validator.validate(example)
    example.pop("schema_version")
    with pytest.raises(ValidationError):
        validator.validate(example)
    example["schema_version"] = f"sidecar.{kind}/999"
    with pytest.raises(ValidationError):
        validator.validate(example)
    example["schema_version"] = f"sidecar.{kind}/1"
    example["authorization"] = True
    with pytest.raises(ValidationError):
        validator.validate(example)


def test_draft_mapping_keeps_native_and_normative_boundaries():
    guide = (ROOT / "README.md").read_text()
    assert "Non-normative" in guide
    assert "not new normative AIOS artifact families" in guide
    assert "io.deepagentlabs.agentic-sidecar" in guide
