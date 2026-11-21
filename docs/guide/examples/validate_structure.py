"""Offline structure-only tutorial; this is not a conformance CLI or SDK.

Run from a source checkout after `uv sync --extra dev`:
    uv run python docs/guide/examples/validate_structure.py path/to/artifact.json
"""
import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
from referencing.exceptions import NoSuchResource

ROOT = Path(__file__).resolve().parents[3]


def no_remote_retrieval(uri):
    raise NoSuchResource(ref=uri)


def validate_structure(path):
    document = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        raise ValueError("Expected a JSON object")
    catalog = json.loads((ROOT / "specification/v0.5/compatibility.json").read_text())
    schema_set = catalog["published_schema_sets"].get(document.get("spec_version"))
    artifact_type = document.get("artifact_type")
    if schema_set is None or artifact_type not in schema_set["artifact_types"]:
        raise ValueError("Unsupported marker/artifact_type pair; no fallback is permitted")
    resources = []
    for published in catalog["published_schema_sets"].values():
        for source in sorted((ROOT / published["schema_directory"]).glob("*.schema.json")):
            schema = json.loads(source.read_text(encoding="utf-8"))
            resources.append((schema["$id"], Resource.from_contents(schema)))
    registry = Registry(retrieve=no_remote_retrieval).with_resources(resources)
    schema_path = ROOT / schema_set["schema_directory"] / f"{artifact_type}.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator(schema, registry=registry, format_checker=FormatChecker()).validate(document)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path)
    args = parser.parse_args()
    validate_structure(args.artifact)
    print("Structure valid. Semantic and consumer-process checks are still required.")
