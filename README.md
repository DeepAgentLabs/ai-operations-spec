# AI Operations Specification

The **AI Operations Specification** is DeepAgentLabs' language-neutral contract for exchanging operational data about AI workflow runs.

It gives observability, evaluation, resilience, local tooling, and CI systems a shared representation of runs, steps, metrics, chaos events, and evaluations. It is a data contract, not a Python package or hosted service.

## Current release

Draft **v0.1** includes the normative [specification](SPECIFICATION.md), a [JSON Schema](schemas/workflow.schema.json), valid and invalid examples, and automated validation tests.

AgenticLens is the observability and optimization reference implementation. Agentic Chaos produces compatible fault-injection data. DeepAgentLabs MCP is a consumer and control surface over these artifacts.

## Validate the examples

```bash
uv sync --extra dev
uv run pytest
```

## Minimal artifact

```json
{
  "spec_version": "0.1",
  "id": "run_01",
  "name": "Customer support",
  "start_time": "2026-07-17T15:00:00Z",
  "status": "completed",
  "steps": []
}
```

See [the complete example](examples/valid/customer-support.json).

## Contribution policy

Changes to normative fields should include a written specification update, a matching schema change, fixtures demonstrating the behavior, and a compatibility note.
