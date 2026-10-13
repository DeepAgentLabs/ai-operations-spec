from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).parents[1]
V05 = ROOT / "specification" / "v0.5"

VERSION_PATTERN = re.compile(r"^(0\.[1-9][0-9]*|[1-9][0-9]*\.(0|[1-9][0-9]*))(-draft)?$")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def fenced_block(markdown: str, heading: str) -> list[str]:
    pattern = rf"## {re.escape(heading)}\n\n```text\n([\s\S]*?)\n```"
    match = re.search(pattern, markdown)
    assert match, f"Missing fenced block for heading: {heading}"
    return [line for line in match.group(1).splitlines() if line.strip()]


def test_versioning_doc_states_the_pattern_this_suite_enforces() -> None:
    versioning = read(V05 / "versioning.md")
    assert VERSION_PATTERN.pattern in versioning


def test_valid_version_markers_match_the_grammar() -> None:
    examples = read(V05 / "examples.md")
    for marker in fenced_block(examples, "Valid version markers"):
        assert VERSION_PATTERN.match(marker), f"expected valid marker: {marker}"


def test_invalid_version_markers_do_not_match_the_grammar() -> None:
    examples = read(V05 / "examples.md")
    for marker in fenced_block(examples, "Invalid version markers"):
        assert not VERSION_PATTERN.match(marker), f"expected invalid marker: {marker}"


def test_existing_schema_spec_versions_conform_to_v05_grammar() -> None:
    schemas_dir = ROOT / "specification" / "v0.4" / "schemas"
    found_any = False
    for schema_path in schemas_dir.glob("*.schema.json"):
        text = read(schema_path)
        for value in re.findall(r'"spec_version":\s*\{"const":\s*"([^"]+)"\}', text):
            found_any = True
            assert VERSION_PATTERN.match(value), f"{schema_path.name} spec_version const {value!r} fails v0.5 grammar"
    assert found_any, "expected at least one spec_version const in the v0.4 schemas"


def test_decision_d005_is_recorded() -> None:
    decision_log = read(ROOT / "reviews" / "decision-log.md")
    assert "D-005" in decision_log
    assert "closed-vocabulary growth" in decision_log.lower()
