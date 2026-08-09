import json
from pathlib import Path

from test_v04_schema import semantic_errors, validator


ROOT = Path(__file__).parents[1]
REVIEW_ARTIFACTS = ROOT / "reviews" / "artifacts"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_review_aios_artifacts_validate() -> None:
    for path in sorted(REVIEW_ARTIFACTS.glob("*.aios.json")):
        artifact = load(path)
        validator(artifact).validate(artifact)
        assert not semantic_errors(artifact), f"{path.name} has semantic errors"
