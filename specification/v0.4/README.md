# v0.4 — JSON Schemas

## Status

Exploratory draft. These schemas test the v0.1 concepts, v0.2 relationships, and v0.3 semantic conventions and cannot freeze before them.

## Artifacts

- [Workflow Schema](schemas/workflow.schema.json) describes reusable definitions.
- [Run Schema](schemas/run.schema.json) describes runtime evidence and execution graphs.
- [Common Schema](schemas/common.schema.json) contains shared identifiers, references, relationships, events, and measurements.
- [Conformance](conformance.md) defines structural and semantic validation requirements.
- [Examples](examples.md) explains the validation fixtures.
- [Acceptance criteria](acceptance-criteria.md) records review gates.

The schemas use JSON Schema Draft 2020-12. Draft alignment requires both schema validation and the semantic checks in the conformance document. Validation proves contract alignment, not truth, quality, safety, or operational success.

## Version marker

Every artifact uses `spec_version: "0.4-draft"` while this milestone remains under review. It MUST change when v0.4 is frozen.
