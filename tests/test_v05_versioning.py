from __future__ import annotations

import re
from pathlib import Path

import pytest


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


def parse_version(marker: str) -> tuple[int, int, bool]:
    assert VERSION_PATTERN.match(marker), f"not a valid v0.5 marker: {marker}"
    is_draft = marker.endswith("-draft")
    core = marker[: -len("-draft")] if is_draft else marker
    major_str, minor_str = core.split(".")
    return int(major_str), int(minor_str), is_draft


def decide_compatibility(consumer: str, producer: str, extension_only: bool | None = None) -> str:
    """Reference implementation of the "Consumer compatibility behavior" table
    in specification/v0.5/versioning.md. Exists so the matrix has an
    executable, regression-tested counterpart, not only prose."""
    if consumer == producer:
        _, _, draft = parse_version(producer)
        return "accept_informal" if draft else "accept"

    c_major, c_minor, c_draft = parse_version(consumer)
    p_major, p_minor, p_draft = parse_version(producer)

    if p_draft or c_draft:
        # different draft snapshots (or a draft vs. a frozen marker) are never assumed compatible
        return "reject"
    if p_major != c_major:
        return "reject"
    if p_minor > c_minor:
        return "accept" if extension_only else "reject"
    if p_minor < c_minor:
        return "accept_as_older"
    raise AssertionError("unreachable: equal major/minor/draft implies equal markers")


@pytest.mark.parametrize(
    ("consumer", "producer", "extension_only", "expected"),
    [
        ("1.0", "1.0", None, "accept"),
        ("0.4-draft", "0.4-draft", None, "accept_informal"),
        ("0.4-draft", "0.5-draft", None, "reject"),
        ("1.0", "1.0-draft", None, "reject"),
        ("1.0", "1.1", True, "accept"),
        ("1.0", "1.1", False, "reject"),
        ("1.0", "2.0", True, "reject"),
        ("1.1", "1.0", None, "accept_as_older"),
    ],
)
def test_compatibility_matrix_decisions(consumer: str, producer: str, extension_only: bool | None, expected: str) -> None:
    assert decide_compatibility(consumer, producer, extension_only) == expected

