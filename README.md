# AI Operations Specification

The **AI Operations Specification (AIOS)** is a vendor-neutral contract for describing what happens when an AI or agentic system runs.

It gives instrumentation, observability, evaluation, safety, and reliability tools a shared vocabulary and portable JSON artifacts for Runs, Steps, model interactions, tool calls, retrieval, memory, evaluations, signals, and incidents.

This repository defines the contract. It does **not** run agents, collect telemetry, host dashboards, or provide an SDK.

## Why it exists

Without a shared contract, every framework exports different names and structures for the same runtime behavior. AIOS separates the standard from its implementations so producers and consumers can interoperate without importing a DeepAgentLabs package.

```text
AI frameworks and instrumentation
              |
              v
   AI Operations Specification
              |
              v
observability, evaluation, safety, and operations tools
```

DeepAgentLabs stewards the specification. AgenticLens, Agentic Chaos, and DeepAgent MCP may implement or consume it, but none of them owns the contract.

## Current maturity

**Pre-release draft. Do not claim stable conformance.**

The work is cumulative, not four competing formats:

| Layer | Defines | Status |
|---|---|---|
| [v0.1](specification/v0.1/README.md) | Core runtime concepts and boundaries | Draft; external review pending |
| [v0.2](specification/v0.2/README.md) | Relationships and execution graphs | Exploratory draft |
| [v0.3](specification/v0.3/README.md) | Transport-neutral semantic events | Exploratory draft |
| [v0.4](specification/v0.4/README.md) | JSON Schema artifacts | Exploratory draft |

Later layers depend on earlier ones. They are available for design feedback and prototype implementations; acceptance of a later layer does not bypass open review gates in an earlier layer.

## Choose a path

- **Understand the model:** read the [v0.1 overview](specification/v0.1/README.md), [core concepts](specification/v0.1/core-concepts.md), and [conceptual examples](specification/v0.1/examples.md).
- **Represent execution graphs:** read [v0.2 relationships](specification/v0.2/relationships.md).
- **Instrument runtime events:** read [v0.3 semantic conventions](specification/v0.3/semantic-conventions.md).
- **Prototype a producer or consumer:** read the [v0.4 schema guide](specification/v0.4/README.md) and [validated Run example](specification/v0.4/examples/valid/run.json).
- **Contribute to the design:** review the open acceptance gates in each milestone and the [roadmap](ROADMAP.md).

## Minimal artifact

```json
{
  "spec_version": "0.4-draft",
  "artifact_type": "run",
  "id": "run-001",
  "started_at": "2026-07-21T06:00:00Z",
  "status": "completed",
  "requests": [],
  "steps": [],
  "relationships": []
}
```

Schema validation establishes structural validity only. It does not prove that recorded claims are true, safe, reliable, or high quality.

## Repository layout

```text
specification/   current milestone drafts
drafts/          superseded or premature experiments
tests/           document, schema, fixture, and graph checks
```

The early workflow schema under [`drafts/v0.4/`](drafts/v0.4/README.md) is retained for history and is not the current v0.4 design.

## Validation

A `Makefile` provides shorthand for common tasks:

```bash
make install     # install dependencies
make test        # run schema validation tests
make check       # run all quality gates
make help        # list all available targets
```

Or run directly:

```bash
uv sync --extra dev
uv run pytest
```

## Scope

AIOS defines shared meaning, relationships, events, and exchange artifacts. SDK behavior, dashboards, provider catalogs, recommendation logic, storage, and transport exporters belong in implementation repositories.

See [SPECIFICATION.md](SPECIFICATION.md) for the complete reading order and maturity rules, or [CONTRIBUTING.md](CONTRIBUTING.md) to propose a change.

## What's Next

Upcoming specification work (see [ROADMAP.md](ROADMAP.md)):

- **Provenance and evidence concepts** — standardize source references,
  evidence lineage, and derived findings as first-class spec objects
- **Conformance test suite** — producers can validate artifacts against the
  spec independently
- **Naming conventions** — lock down field naming rules, casing, and
  abbreviation policy
- **Migration guides** — clear upgrade paths between spec versions
