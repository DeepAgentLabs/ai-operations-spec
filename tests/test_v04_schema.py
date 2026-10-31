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
    return [message for _, message in semantic_issues(artifact)]


def semantic_issues(artifact: dict) -> list[tuple[str, str]]:
    """Return `(rule_id, message)` pairs citing `specification/v0.4/conformance-rules.json`."""
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

    errors: list[tuple[str, str]] = []
    ids = [object_id for object_id, _ in objects]
    if len(ids) != len(set(ids)):
        errors.append(("AIOS-0.4-P02", "object identities must be unique within a Run artifact"))
    object_types = dict(objects)
    occurrence_by_id = {item["id"]: item for item in artifact.get("occurrences", [])}
    evidence_by_id = {item["id"]: item for item in artifact.get("evidence", [])}

    relationships = artifact.get("relationships", [])
    relationship_ids = [item["id"] for item in relationships]
    if len(relationship_ids) != len(set(relationship_ids)):
        errors.append(("AIOS-0.4-P03", "relationship identities must be unique"))

    event_ids = [item["event_id"] for item in artifact.get("events", [])]
    if len(event_ids) != len(set(event_ids)):
        errors.append(("AIOS-0.4-P03", "event identities must be unique"))

    def parse_time(value: str) -> datetime:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))

    if artifact.get("ended_at"):
        if parse_time(artifact["ended_at"]) < parse_time(artifact["started_at"]):
            errors.append(("AIOS-0.4-P04", "ended_at must not precede started_at"))
    for step in artifact.get("steps", []):
        if step.get("started_at") and step.get("ended_at"):
            if parse_time(step["ended_at"]) < parse_time(step["started_at"]):
                errors.append(("AIOS-0.4-P04", f"Step {step['id']} ended_at must not precede started_at"))

    for relationship in relationships:
        source, target = relationship["source"], relationship["target"]
        if source["id"] == target["id"]:
            errors.append(("AIOS-0.4-P11", f"{relationship['id']} cannot relate an object to itself"))
        for endpoint in (source, target):
            if endpoint.get("external"):
                continue
            actual_type = object_types.get(endpoint["id"])
            if actual_type is None:
                errors.append(("AIOS-0.4-P05", f"{relationship['id']} references missing object {endpoint['id']}"))
            elif actual_type != endpoint["type"]:
                errors.append(("AIOS-0.4-P05", f"{relationship['id']} declares the wrong type for {endpoint['id']}"))

    def count_edges(edge_type: str, source_id: str | None = None, target_id: str | None = None) -> int:
        return sum(
            item["type"] == edge_type
            and (source_id is None or item["source"]["id"] == source_id)
            and (target_id is None or item["target"]["id"] == target_id)
            for item in relationships
        )

    for step in artifact.get("steps", []):
        if count_edges("contains", artifact["id"], step["id"]) != 1:
            errors.append(("AIOS-0.4-P06", f"Step {step['id']} must be contained by its Run exactly once"))
    for occurrence in artifact.get("occurrences", []):
        if count_edges("observed-in", occurrence["id"]) != 1:
            errors.append(("AIOS-0.4-P07", f"Occurrence {occurrence['id']} must be observed in exactly one Step"))
    for evidence in artifact.get("evidence", []):
        if evidence["type"] == "evaluation" and count_edges("evaluates", evidence["id"]) < 1:
            errors.append(("AIOS-0.4-P08", f"Evaluation {evidence['id']} must identify a target"))

    workflow_id = artifact.get("workflow_id")
    if workflow_id and not any(
        item["type"] == "run-of" and item["source"]["id"] == artifact["id"]
        and item["target"]["id"] == workflow_id for item in relationships
    ):
        errors.append(("AIOS-0.4-P09", "workflow_id must be supported by a matching run-of relationship"))

    for event in artifact.get("events", []):
        if object_types.get(event["object_id"]) != event["object_type"]:
            errors.append(("AIOS-0.4-P10", f"Event {event['event_id']} must target an object of its declared type"))

    attempt_signal_targets: dict[str, list[tuple[int, str]]] = {}
    for relationship in relationships:
        if relationship["type"] != "signals-on":
            continue
        source = evidence_by_id.get(relationship["source"]["id"])
        if not source or source.get("type") != "reliability_event":
            continue
        attempt = source.get("attributes", {}).get("attempt")
        if not isinstance(attempt, int):
            continue
        target_id = relationship["target"]["id"]
        attempt_signal_targets.setdefault(target_id, []).append((attempt, source["id"]))
        occurrence = occurrence_by_id.get(target_id)
        if occurrence:
            occurrence_attempt = occurrence.get("attributes", {}).get("attempt")
            if isinstance(occurrence_attempt, int) and occurrence_attempt != attempt:
                errors.append((
                    "AIOS-0.4-P12",
                    f"Retry evidence {source['id']} must target attempt {attempt}, not occurrence attempt {occurrence_attempt}",
                ))
    for target_id, attempts in attempt_signal_targets.items():
        if len(attempts) > 1:
            ordered_attempts = ", ".join(str(attempt) for attempt, _ in sorted(attempts))
            errors.append((
                "AIOS-0.4-P12",
                f"Retry attempts {ordered_attempts} must not all signal the same occurrence {target_id}",
            ))

    retry_groups: dict[str, dict[int, str]] = {}
    for occurrence in artifact.get("occurrences", []):
        attributes = occurrence.get("attributes", {})
        logical_activity_id = attributes.get("logical_activity_id")
        attempt = attributes.get("attempt")
        if not isinstance(logical_activity_id, str) or not isinstance(attempt, int):
            continue
        retry_groups.setdefault(logical_activity_id, {})
        if attempt in retry_groups[logical_activity_id]:
            errors.append(("AIOS-0.4-P12", f"Retry activity {logical_activity_id} duplicates attempt {attempt}"))
            continue
        retry_groups[logical_activity_id][attempt] = occurrence["id"]
    for logical_activity_id, attempts in retry_groups.items():
        ordered_attempts = sorted(attempts.items())
        if len(ordered_attempts) < 2:
            continue
        for index in range(len(ordered_attempts) - 1):
            _, source_id = ordered_attempts[index]
            next_attempt, target_id = ordered_attempts[index + 1]
            if not (
                count_edges("follows", source_id, target_id)
                or count_edges("caused", source_id, target_id)
            ):
                errors.append((
                    "AIOS-0.4-P12",
                    f"Retry activity {logical_activity_id} must link attempt {index + 1} to attempt {next_attempt}",
                ))

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
            errors.append(("AIOS-0.4-P11", f"relationship graph {sorted(edge_types)} must be acyclic"))

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


def test_semantic_issues_cite_cataloged_semantic_rules() -> None:
    catalog = load(V04 / "conformance-rules.json")
    semantic_rules = {rule["id"] for rule in catalog["rules"] if rule["check"] == "semantic"}
    for path in sorted((V04 / "examples" / "semantic-invalid").glob("*.json")):
        issues = semantic_issues(load(path))
        assert issues, path.name
        assert {rule_id for rule_id, _ in issues} <= semantic_rules, path.name
