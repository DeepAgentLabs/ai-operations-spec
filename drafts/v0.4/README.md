# Unreleased v0.4 schema experiment

This directory preserves the workflow JSON Schema, fixtures, and validation tests created before the conceptual model was complete.

It is **non-normative** and **not a v0.1 artifact format**. It remains useful implementation research for the planned v0.4 schema milestone.

Known gaps include:

- the schema conflates Workflow and Run
- Request and Agent are not first-class objects
- several core concepts have no representation
- relationship semantics have not passed through v0.2
- event naming has not passed through v0.3

Do not update reference implementations to claim conformance to this draft. When v0.1 through v0.3 are accepted, this material should be revised against those decisions.

To run its experimental validation suite:

```bash
uv sync --project drafts/v0.4 --extra dev
uv run --project drafts/v0.4 pytest
```
