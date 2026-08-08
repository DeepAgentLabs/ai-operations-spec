import json
import re
from datetime import datetime
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource


ROOT = Path(__file__).parents[1]
V04 = ROOT / "specification" / "v0.4"
SCHEMAS = V04 / "schemas"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


SCHEMA_DOCUMENTS = {path.name: load(path) for path in SCHEMAS.glob("*.schema.json")}
REGISTRY = Registry().with_resources(
    (schema["$id"], Resource.from_contents(schema)) for schema in SCHEMA_DOCUMENTS.values()
)


def validator(artifact: dict) -> Draft202012Validator:
    schema = SCHEMA_DOCUMENTS[f"{artifact['artifact_type']}.schema.json"]
    return Draft202012Validator(schema, registry=REGISTRY, format_checker=FormatChecker())


def semantic_errors(artifact: dict) -> list[str]:
    if artifact.get("artifact_type") != "run":
        return []

    objects: list[tuple[str, str]] = [(artifact["id"], "run")]
    groups = [
        ("requests", "request"), ("steps", "step"), ("agents", "agent"),
        ("incidents", "incident"),
    ]
    for key, object_type in groups:
        objects.extend((item["id"], object_type) for item in artifact.get(key, []))
    objects.extend((item["id"], item["type"]) for item in artifact.get("occurrences", []))
    objects.extend((item["id"], item["type"]) for item in artifact.get("evidence", []))

    errors: list[str] = []
    ids = [object_id for object_id, _ in objects]
    if len(ids) != len(set(ids)):
        errors.append("object identities must be unique within a Run artifact")
    object_types = dict(objects)

    relationships = artifact.get("relationships", [])
    relationship_ids = [item["id"] for item in relationships]
    if len(relationship_ids) != len(set(relationship_ids)):
        errors.append("relationship identities must be unique")

    event_ids = [item["event_id"] for item in artifact.get("events", [])]
    if len(event_ids) != len(set(event_ids)):
        errors.append("event identities must be unique")

    if artifact.get("ended_at"):
        started = datetime.fromisoformat(artifact["started_at"].replace("Z", "+00:00"))
        ended = datetime.fromisoformat(artifact["ended_at"].replace("Z", "+00:00"))
        if ended < started:
            errors.append("ended_at must not precede started_at")

    for relationship in relationships:
        source, target = relationship["source"], relationship["target"]
        if source["id"] == target["id"]:
            errors.append(f"{relationship['id']} cannot relate an object to itself")
        for endpoint in (source, target):
            if endpoint.get("external"):
                continue
            actual_type = object_types.get(endpoint["id"])
            if actual_type is None:
                errors.append(f"{relationship['id']} references missing object {endpoint['id']}")
            elif actual_type != endpoint["type"]:
                errors.append(f"{relationship['id']} declares the wrong type for {endpoint['id']}")

    def count_edges(edge_type: str, source_id: str | None = None, target_id: str | None = None) -> int:
        return sum(
            item["type"] == edge_type
            and (source_id is None or item["source"]["id"] == source_id)
            and (target_id is None or item["target"]["id"] == target_id)
            for item in relationships
        )

    for step in artifact.get("steps", []):
        if count_edges("contains", artifact["id"], step["id"]) != 1:
            errors.append(f"Step {step['id']} must be contained by its Run exactly once")
    for occurrence in artifact.get("occurrences", []):
        if count_edges("observed-in", occurrence["id"]) != 1:
            errors.append(f"Occurrence {occurrence['id']} must be observed in exactly one Step")
    for evidence in artifact.get("evidence", []):
        if evidence["type"] == "evaluation" and count_edges("evaluates", evidence["id"]) < 1:
            errors.append(f"Evaluation {evidence['id']} must identify a target")

    workflow_id = artifact.get("workflow_id")
    if workflow_id and not any(
        item["type"] == "run-of" and item["source"]["id"] == artifact["id"]
        and item["target"]["id"] == workflow_id for item in relationships
    ):
        errors.append("workflow_id must be supported by a matching run-of relationship")

    for event in artifact.get("events", []):
        if object_types.get(event["object_id"]) != event["object_type"]:
            errors.append(f"Event {event['event_id']} must target an object of its declared type")

    for edge_types in ({"parent-of"}, {"caused", "follows", "depends-on"}):
        graph: dict[str, set[str]] = {}
        for item in relationships:
            if item["type"] in edge_types:
                graph.setdefault(item["source"]["id"], set()).add(item["target"]["id"])
        visiting: set[str] = set()
        visited: set[str] = set()

        def has_cycle(node: str) -> bool:
            if node in visiting:
                return True
            if node in visited:
                return False
            visiting.add(node)
            cycle = any(has_cycle(target) for target in graph.get(node, set()))
            visiting.remove(node)
            visited.add(node)
            return cycle

        if any(has_cycle(node) for node in list(graph)):
            errors.append(f"relationship graph {sorted(edge_types)} must be acyclic")

    return errors


def test_v04_schemas_are_valid() -> None:
    for schema in SCHEMA_DOCUMENTS.values():
        Draft202012Validator.check_schema(schema)


def test_v03_event_catalog_matches_v04_schema() -> None:
    conventions = (ROOT / "specification" / "v0.3" / "semantic-conventions.md").read_text(encoding="utf-8")
    documented = set(re.findall(r"`(aiops\.[a-z0-9.]+)`", conventions))
    schema_events = set(SCHEMA_DOCUMENTS["common.schema.json"]["$defs"]["canonical_event_name"]["enum"])
    assert documented == schema_events


@pytest.mark.parametrize("path", sorted((V04 / "examples" / "valid").glob("*.json")))
def test_valid_v04_examples(path: Path) -> None:
    artifact = load(path)
    validator(artifact).validate(artifact)
    assert not semantic_errors(artifact)


@pytest.mark.parametrize("path", sorted((V04 / "examples" / "invalid").glob("*.json")))
def test_invalid_v04_examples(path: Path) -> None:
    artifact = load(path)
    assert list(validator(artifact).iter_errors(artifact))


@pytest.mark.parametrize("path", sorted((V04 / "examples" / "semantic-invalid").glob("*.json")))
def test_semantically_invalid_v04_examples(path: Path) -> None:
    artifact = load(path)
    validator(artifact).validate(artifact)
    assert semantic_errors(artifact)
