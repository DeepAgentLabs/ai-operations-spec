import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).parents[1]
SCHEMA = json.loads((ROOT / "schemas" / "workflow.schema.json").read_text())
VALIDATOR = Draft202012Validator(SCHEMA, format_checker=FormatChecker())


def load(path: Path) -> dict:
    return json.loads(path.read_text())


@pytest.mark.parametrize("path", sorted((ROOT / "examples" / "valid").glob("*.json")))
def test_valid_examples(path: Path) -> None:
    VALIDATOR.validate(load(path))


@pytest.mark.parametrize("path", sorted((ROOT / "examples" / "invalid").glob("*.json")))
def test_invalid_examples(path: Path) -> None:
    assert list(VALIDATOR.iter_errors(load(path)))


def test_example_references_resolve() -> None:
    artifact = load(ROOT / "examples" / "valid" / "customer-support.json")
    step_ids = [step["id"] for step in artifact["steps"]]
    assert len(step_ids) == len(set(step_ids))
    references = [item["step_id"] for key in ("chaos_events", "evaluations") for item in artifact.get(key, []) if item.get("step_id")]
    assert all(reference in step_ids for reference in references)
