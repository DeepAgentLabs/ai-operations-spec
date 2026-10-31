"""Reference checks the repository runs over its own fixtures and conformance suite.

Routing follows `specification/v0.5/compatibility.json` (AIOS-0.5-V03): a document
is validated only against the schema set its own `spec_version` names. Run and
Workflow semantics come from `test_v04_schema.semantic_issues`; provenance record
semantics and cross-artifact resolution are defined in
`specification/v0.6/provenance.md`. This is repository test code, not an SDK.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

from test_v04_schema import semantic_issues as run_semantic_issues

ROOT = Path(__file__).parents[1]
COMPATIBILITY = json.loads((ROOT / "specification" / "v0.5" / "compatibility.json").read_text(encoding="utf-8"))
SCHEMA_SETS = COMPATIBILITY["published_schema_sets"]


def _schemas(marker: str) -> dict[str, dict]:
    directory = ROOT / SCHEMA_SETS[marker]["schema_directory"]
    return {path.name: json.loads(path.read_text(encoding="utf-8")) for path in directory.glob("*.schema.json")}


def _registry(marker: str) -> Registry:
    documents: dict[str, dict] = {}
    for dependency in [*SCHEMA_SETS[marker].get("depends_on", []), marker]:
        documents.update(_schemas(dependency))
    return Registry().with_resources(
        (schema["$id"], Resource.from_contents(schema)) for schema in documents.values()
    )


def route(document: object) -> str | None:
    """Return the published marker that validates `document`, or None to reject it."""
    if not isinstance(document, dict):
        return None
    marker = document.get("spec_version")
    entry = SCHEMA_SETS.get(marker) if isinstance(marker, str) else None
    if entry is None or document.get("artifact_type") not in entry["artifact_types"]:
        return None
    return marker


def validator(document: dict) -> Draft202012Validator:
    marker = route(document)
    if marker is None:
        raise LookupError("no published schema set validates this spec_version and artifact_type")
    schema = _schemas(marker)[f"{document['artifact_type']}.schema.json"]
    return Draft202012Validator(schema, registry=_registry(marker), format_checker=FormatChecker())


def semantic_issues(document: dict) -> list[tuple[str, str]]:
    if document.get("artifact_type") == "provenance":
        return provenance_issues(document)
    return run_semantic_issues(document)


def check(document: object) -> tuple[str, list[str]]:
    """Return (outcome, cited rule IDs) for one document read on its own."""
    if route(document) is None:
        return "unsupported", ["AIOS-0.5-V03"]
    assert isinstance(document, dict)
    if any(True for _ in validator(document).iter_errors(document)):
        rule = "AIOS-0.6-R01" if document["artifact_type"] == "provenance" else "AIOS-0.4-P01"
        return "schema-invalid", [rule]
    issues = semantic_issues(document)
    if issues:
        return "semantic-invalid", sorted({rule for rule, _ in issues})
    return "valid", []


LINEAGE_ENDPOINTS = {
    "derived-from": ({"finding"}, {"source", "finding"}),
    "supports": ({"source", "finding"}, {"finding"}),
    "contradicts": ({"source", "finding"}, {"finding"}),
    "supersedes": ({"finding"}, {"finding"}),
}


def provenance_issues(record: dict) -> list[tuple[str, str]]:
    """Semantic checks AIOS-0.6-R02 through R07 for a schema-valid provenance record."""
    issues: list[tuple[str, str]] = []
    subjects = {item["id"] for item in record["subjects"]}
    kinds = {item["id"]: "source" for item in record["sources"]}
    kinds.update({item["id"]: "finding" for item in record["findings"]})

    identities = [
        item["id"] for group in ("subjects", "sources", "findings", "lineage") for item in record[group]
    ]
    if len(identities) != len(set(identities)):
        issues.append(("AIOS-0.6-R02", "identities must be unique within a provenance record"))

    for source in record["sources"]:
        if "subject" in source and source["subject"] not in subjects:
            issues.append(("AIOS-0.6-R03", f"Source {source['id']} names undeclared subject {source['subject']}"))
    for finding in record["findings"]:
        for target in finding.get("targets", []):
            if target["subject"] not in subjects:
                issues.append(("AIOS-0.6-R03", f"Finding {finding['id']} targets undeclared subject {target['subject']}"))

    for edge in record["lineage"]:
        allowed_sources, allowed_targets = LINEAGE_ENDPOINTS[edge["type"]]
        for endpoint, allowed in ((edge["source"], allowed_sources), (edge["target"], allowed_targets)):
            kind = kinds.get(endpoint)
            if kind is None:
                issues.append(("AIOS-0.6-R04", f"Lineage {edge['id']} references missing {endpoint}"))
            elif kind not in allowed:
                issues.append(("AIOS-0.6-R04", f"Lineage {edge['id']} cannot use {kind} {endpoint} with {edge['type']}"))
        if edge["source"] == edge["target"]:
            issues.append(("AIOS-0.6-R06", f"Lineage {edge['id']} cannot relate {edge['source']} to itself"))

    derived = {edge["source"] for edge in record["lineage"] if edge["type"] == "derived-from"}
    for finding in record["findings"]:
        if finding["id"] not in derived:
            issues.append(("AIOS-0.6-R05", f"Finding {finding['id']} has no derived-from lineage"))

    for edge_type in ("derived-from", "supersedes"):
        graph: dict[str, set[str]] = {}
        for edge in record["lineage"]:
            if edge["type"] == edge_type and edge["source"] != edge["target"]:
                graph.setdefault(edge["source"], set()).add(edge["target"])
        if _has_cycle(graph):
            issues.append(("AIOS-0.6-R06", f"{edge_type} lineage must be acyclic"))

    created = _time(record["created_at"])
    for source in record["sources"]:
        if "captured_at" in source and _time(source["captured_at"]) > created:
            issues.append(("AIOS-0.6-R07", f"Source {source['id']} was captured after the record was created"))
    return issues


def resolve(record: dict, subject_bytes: dict[str, bytes]) -> dict:
    """Resolve a valid record against the subject artifacts a consumer actually holds.

    Returns `{"subjects": {id: {...}}, "references": {key: state}}` where a reference key
    is a source id or `<finding id>/targets/<index>` and its state is `resolved`,
    `unresolved` (subject unavailable or unusable), `missing` or `type_mismatch`.
    """
    subjects: dict[str, dict] = {}
    objects: dict[str, dict[str, str] | None] = {}
    for subject in record["subjects"]:
        raw = subject_bytes.get(subject["id"])
        state = {"available": raw is not None, "valid": None, "identity": None, "digest": "absent"}
        if "digest" in subject:
            state["digest"] = "unchecked"
        objects[subject["id"]] = None
        if raw is not None:
            if "digest" in subject:
                actual = hashlib.new(subject["digest"]["algorithm"].replace("-", ""), raw).hexdigest()
                state["digest"] = "verified" if actual == subject["digest"]["value"] else "mismatch"
            artifact = json.loads(raw)
            outcome, _ = check(artifact)
            state["valid"] = outcome == "valid"
            matches = (
                isinstance(artifact, dict)
                and artifact.get("id") == subject["artifact_id"]
                and artifact.get("artifact_type") == subject["artifact_type"]
                and artifact.get("spec_version") == subject["spec_version"]
            )
            state["identity"] = "match" if matches else "mismatch"
            if state["valid"] and matches:
                objects[subject["id"]] = _objects(artifact)
        subjects[subject["id"]] = state

    references: dict[str, str] = {}

    def lookup(subject_id: str, reference: dict) -> str:
        index = objects.get(subject_id)
        if index is None:
            return "unresolved"
        actual = index.get(reference["id"])
        if actual is None:
            return "missing"
        return "resolved" if actual == reference["type"] else "type_mismatch"

    for source in record["sources"]:
        if source["kind"] == "aios_object":
            references[source["id"]] = lookup(source["subject"], source["object"])
    for finding in record["findings"]:
        for position, target in enumerate(finding.get("targets", [])):
            references[f"{finding['id']}/targets/{position}"] = lookup(target["subject"], target["object"])
    return {"subjects": subjects, "references": references}


def _objects(artifact: dict) -> dict[str, str]:
    if artifact["artifact_type"] == "workflow":
        return {artifact["id"]: "workflow"}
    index = {artifact["id"]: "run"}
    for key, object_type in (("requests", "request"), ("steps", "step"), ("agents", "agent"), ("incidents", "incident")):
        index.update((item["id"], object_type) for item in artifact.get(key, []))
    for key in ("occurrences", "evidence"):
        index.update((item["id"], item["type"]) for item in artifact.get(key, []))
    return index


def _time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _has_cycle(graph: dict[str, set[str]]) -> bool:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        cycle = any(visit(target) for target in graph.get(node, set()))
        visiting.remove(node)
        visited.add(node)
        return cycle

    return any(visit(node) for node in list(graph))
