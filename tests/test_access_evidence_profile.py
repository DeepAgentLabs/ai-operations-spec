"""Exploratory extension contract; no new normative AIOS version marker."""

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1] / "drafts" / "access-evidence-v1"


def test_example_and_required_correlation():
    schema = json.loads((ROOT / "access.schema.json").read_text())
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    example = json.loads((ROOT / "example.json").read_text())
    validator.validate(example)
    for field in schema["required"]:
        broken = {k: v for k, v in example.items() if k != field}
        assert list(validator.iter_errors(broken)), field
    for kind in ["stop_requested", "allowed", "BLOCK"]:
        assert list(validator.iter_errors({**example, "kind": kind}))
