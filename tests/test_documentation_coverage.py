"""Check reference freshness and coverage without requiring a sibling checkout."""
import hashlib
import importlib.util
import json
import re
from pathlib import Path

import pytest
from jsonschema import ValidationError

ROOT = Path(__file__).parents[1]
DOCS = ROOT / "docs"


def test_ai_reference_covers_maintained_sources_and_is_fresh():
    config = json.loads((DOCS / "ai-docs.json").read_text())
    manifest = json.loads((DOCS / "ai-docs-manifest.json").read_text())
    selected = {entry["path"] for entry in config["references"]}
    expected_markdown = {
        path.relative_to(ROOT).as_posix()
        for directory in ("specification", "docs", "drafts", "reviews")
        for path in (ROOT / directory).rglob("*.md")
        if path.name != "llms-full.md"
    }
    assert expected_markdown <= selected, expected_markdown - selected
    recorded = {entry["path"]: entry for entry in manifest["sources"]}
    required = selected | {"pyproject.toml", "docs/ai-docs.json"}
    required |= {
        path.relative_to(ROOT).as_posix()
        for pattern in config["schemas"] + config["data"]
        for path in ROOT.glob(pattern)
    }
    required |= {path.relative_to(ROOT).as_posix() for path in (DOCS / "guide/examples").glob("*") if path.is_file()}
    assert required == set(recorded)
    for relative, source in recorded.items():
        normalized = (ROOT / relative).read_text(encoding="utf-8").encode("utf-8")
        assert hashlib.sha256(normalized).hexdigest() == source["sha256"], f"Regenerate AI reference: {relative} changed"
    reference = (DOCS / "llms-full.md").read_bytes()
    assert hashlib.sha256(reference).hexdigest() == manifest["sha256"]


def test_capability_indexes_match_and_link_to_included_sections():
    guide = (DOCS / "developer-guide.md").read_text()
    index = (DOCS / "ai-reference-index.md").read_text()
    simple_table = guide.split("## Capability index\n", 1)[1].split("\n## ", 1)[0]
    robust_table = index.split("## Capability index\n", 1)[1].split("\n## ", 1)[0]
    simple = re.findall(r"^\| \[([^]]+)\]\(#([^)]+)\) \|", simple_table, re.M)
    robust = re.findall(r"^\| ([^|]+?) \| [^\n]+<a href=\"#([^\"]+)\">", robust_table, re.M)
    assert [name for name, _ in simple] == [name.strip() for name, _ in robust]
    assert len(simple) >= 26
    slug = lambda text: re.sub(r"[^\w\- ]", "", text.lower()).replace(" ", "-")
    guide_anchors = {slug(title) for title in re.findall(r"^## (.+)$", guide, re.M)}
    guide_anchors |= set(re.findall(r'<a id="([^"]+)">', guide))
    assert {anchor for _, anchor in simple} <= guide_anchors
    reference = (DOCS / "llms-full.md").read_text()
    included = {slug(title) for title in re.findall(r"^## (.+)$", reference, re.M)}
    assert {anchor for _, anchor in robust} <= included
    # Full-reference jumps must reach one detailed source, not a short guide heading.
    all_headings = [slug(title) for title in re.findall(r"^## (.+)$", reference, re.M)]
    for _, anchor in robust:
        assert all_headings.count(anchor) == 1
    suite = json.loads((ROOT / "specification/v0.6/conformance-suite/suite.json").read_text())
    assert f"{len(suite['cases'])} outcome cases and {len(suite['resolution_cases'])} resolution cases" in guide
    for source in (DOCS / "developer-guide.md", DOCS / "ai-reference-index.md"):
        for target in re.findall(r"\[[^]]*\]\(([^\s)]+)\)", source.read_text()):
            if ":" not in target and not target.startswith("#"):
                assert (source.parent / target.split("#")[0]).exists(), target


def test_api_reference_is_generated_from_current_schemas_and_catalogs():
    spec = importlib.util.spec_from_file_location("api_reference", ROOT / "scripts/build_api_reference.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    reference = (DOCS / "api-reference.md").read_text(encoding="utf-8")
    assert reference == module.render(), "Regenerate with: make api-reference"
    # Every published family, shared definition and rule must be reachable.
    for _, schema, *_ in module.FAMILIES:
        properties = json.loads((ROOT / schema).read_text())["properties"]
        assert f'<a id="{module.anchor(schema)}"></a>' in reference
        for field in properties:
            assert f"| `{field}` |" in reference, (schema, field)
    for _, catalog in module.CATALOGS:
        for rule in json.loads((ROOT / catalog).read_text())["rules"]:
            assert f'<a id="{rule["id"].lower()}"></a>' in reference
    for target in re.findall(r"\]\(#([^)]+)\)", reference):
        assert f'<a id="{target}"></a>' in reference, target
    for target in re.findall(r"\]\((\.\./[^)#]+)", reference):
        assert (DOCS / target).resolve().is_file(), target


def test_unrendered_schema_keywords_fail_generation():
    spec = importlib.util.spec_from_file_location("api_reference", ROOT / "scripts/build_api_reference.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with pytest.raises(ValueError, match="Unrendered schema keywords"):
        module.Renderer().check({"dependentRequired": {}}, "fixture")


def tutorial():
    source = DOCS / "guide/examples/validate_structure.py"
    spec = importlib.util.spec_from_file_location("structure_tutorial", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("relative", [
    "specification/v0.4/examples/valid/run.json",
    "specification/v0.4/examples/valid/workflow.json",
    "specification/v0.6/examples/provenance/support-finding.provenance.json",
    "specification/v0.8/examples/verification_signal.json",
    "specification/v0.8/examples/audit_event.json",
    "specification/v0.8/examples/investigation_report.json",
])
def test_structural_tutorial_supports_each_published_artifact_family(relative):
    tutorial().validate_structure(ROOT / relative)


def test_structural_tutorial_distinguishes_structure_from_semantics(tmp_path):
    module = tutorial()
    # A dangling typed graph reference must still be checked by a semantic validator.
    module.validate_structure(ROOT / "specification/v0.4/examples/semantic-invalid/dangling-reference.json")
    invalid = tmp_path / "input.json"
    invalid.write_text('{"spec_version":"0.4-draft","artifact_type":"run"}')
    with pytest.raises(ValidationError):
        module.validate_structure(invalid)
    invalid.write_text('{"spec_version":"1.0","artifact_type":"run"}')
    with pytest.raises(ValueError, match="Unsupported"):
        module.validate_structure(invalid)
    invalid.write_text('{"spec_version":"0.4-draft","artifact_type":"audit_event"}')
    with pytest.raises(ValueError, match="Unsupported"):
        module.validate_structure(invalid)
