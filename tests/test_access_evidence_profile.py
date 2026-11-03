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


def test_all_kinds_and_malformed_observations():
    schema = json.loads((ROOT / "access.schema.json").read_text())
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    example = json.loads((ROOT / "example.json").read_text())
    for kind in schema["properties"]["kind"]["enum"]:
        validator.validate({**example, "kind": kind})
    for fields in [{"occurred_at": "yesterday"}, {"task_id": ""}, {"secret": "forbidden"}]:
        assert list(validator.iter_errors({**example, **fields}))


def test_run_embedding_preserves_existing_aios_schema_and_namespace():
    from test_v04_schema import semantic_errors, validator

    artifact = json.loads((ROOT / "run-example.json").read_text())
    validator(artifact).validate(artifact)
    assert not semantic_errors(artifact)
    event = artifact["events"][0]
    assert event["event_name"].startswith("io.deepagentlabs.access.")
    assert event["object_id"] == artifact["id"]
    Draft202012Validator(json.loads((ROOT / "access.schema.json").read_text())).validate(
        event["extensions"]["io.deepagentlabs.access"]
    )
