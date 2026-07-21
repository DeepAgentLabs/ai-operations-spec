from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).parents[1]
SPEC_DIR = ROOT / "specification" / "v0.1"


CORE_CONCEPTS = [
    "Workflow",
    "Run",
    "Request",
    "Step",
    "Agent",
    "Model Interaction",
    "Prompt",
    "Context",
    "Tool Invocation",
    "RAG Retrieval",
    "Memory Operation",
    "Evaluation",
    "Safety Signal",
    "Reliability Event",
    "Incident",
]


REQUIRED_SECTIONS = [
    "Purpose.",
    "Identity and lifecycle.",
    "Owns.",
    "References.",
    "Must not represent.",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def local_markdown_links(markdown: str) -> list[str]:
    return [
        match.group("target")
        for match in re.finditer(r"\[[^\]]+\]\((?P<target>[^)#][^)]*)\)", markdown)
        if "://" not in match.group("target")
    ]


def concept_section(markdown: str, concept: str) -> str:
    pattern = rf"^## {re.escape(concept)}\s*$([\s\S]*?)(?=^## |\Z)"
    match = re.search(pattern, markdown, re.MULTILINE)
    assert match, f"Missing core concept heading: {concept}"
    return match.group(1)


def test_specification_markdown_links_resolve() -> None:
    markdown_files = [
        ROOT / "README.md",
        ROOT / "SPECIFICATION.md",
        ROOT / "ROADMAP.md",
        ROOT / "CONTRIBUTING.md",
        *sorted((ROOT / "specification").glob("v*/*.md")),
    ]

    for markdown_file in markdown_files:
        for target in local_markdown_links(read(markdown_file)):
            linked_path = (markdown_file.parent / target).resolve()
            assert linked_path.exists(), f"{markdown_file.relative_to(ROOT)} links to missing {target}"


def test_v01_core_concepts_are_defined_with_required_boundaries() -> None:
    core = read(SPEC_DIR / "core-concepts.md")

    for concept in CORE_CONCEPTS:
        section = concept_section(core, concept)
        for required_section in REQUIRED_SECTIONS:
            assert required_section in section, f"{concept} is missing {required_section}"


def test_v01_overview_and_acceptance_criteria_cover_the_same_concepts() -> None:
    overview = read(SPEC_DIR / "README.md")
    acceptance = read(SPEC_DIR / "acceptance-criteria.md")

    for concept in CORE_CONCEPTS:
        assert concept in overview, f"{concept} missing from v0.1 overview"
        assert concept in acceptance, f"{concept} missing from v0.1 acceptance criteria"


def test_v04_draft_does_not_claim_v01_schema_identity() -> None:
    schema = read(ROOT / "drafts" / "v0.4" / "schemas" / "workflow.schema.json")

    assert "v0.1/workflow.schema.json" not in schema
    assert '"const": "0.1"' not in schema


def test_every_milestone_has_review_and_navigation_documents() -> None:
    for milestone in (ROOT / "specification").glob("v*"):
        assert (milestone / "README.md").exists()
        assert (milestone / "examples.md").exists()
        assert (milestone / "acceptance-criteria.md").exists()


def test_legacy_llm_interaction_name_is_not_used_as_a_core_object() -> None:
    specification = "\n".join(read(path) for path in (ROOT / "specification").rglob("*.md"))
    assert "LLM Interaction" not in specification
