# AI Operations Specification

The **AI Operations Specification (AIOS)** is a vendor-neutral contract for describing what happens when an AI or agentic system runs.

It gives instrumentation, observability, evaluation, safety, and reliability tools a shared vocabulary and portable JSON artifacts for Runs, Steps, model interactions, tool calls, retrieval, memory, evaluations, signals, and incidents.

This repository defines the contract. It does **not** run agents, collect telemetry, host dashboards, or provide an SDK.
It also does **not** own the primary end-user CLI for conformance checks;
implementation repositories may provide that convenience on top of the
normative rules defined here.

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

DeepAgentLabs stewards the specification today and is its sole editor.
AgenticLens, Agentic Chaos, Agentic Sidecar, DeepAgent MCP, and
AgenticOps Control Tower may implement or consume it, but none of them owns
the contract. Vendor-neutrality is the design goal, not yet an established
fact: several acceptance gates — independent implementer review, validation
against artifacts from at least two unrelated producers — remain open (see
each milestone's acceptance criteria and the [roadmap](ROADMAP.md)). Treat
"vendor-neutral" as the intended end state until those gates close.

## Current maturity

**Pre-release draft. Do not claim stable conformance.**

## Release Status

- **v0.1** 🏗️ In review — Core runtime concepts and boundaries
- **v0.2** 🚧 Exploratory draft — Relationships and execution graphs
- **v0.3** 🚧 Exploratory draft — Transport-neutral semantic events
- **v0.4** 🚧 Exploratory draft — JSON Schema artifacts
- **v0.5** 🚧 Exploratory draft — Versioning and compatibility rules
- **v0.6** 🚧 Planned — Canonical examples and extension model
- **v0.6.x** 🚧 Planned — Provenance, evidence, and operational artifacts
- **v1.0** 🚧 Planned — Stable specification

## Next Steps

- Close the remaining v0.1 external review gate so later layers can move
  toward freeze.
- Validate the v0.4 draft artifacts against at least two independent
  implementations.
- Validate the v0.5 compatibility rules against a real version transition
  once one exists; the version-marker grammar and change classification are
  drafted, but no frozen version has yet been superseded.
- Standardize provenance/evidence concepts and publish producer-independent
  conformance fixtures and rules.

The work is cumulative, not five competing formats:

| Layer | Defines | Status |
|---|---|---|
| [v0.1](specification/v0.1/README.md) | Core runtime concepts and boundaries | Draft; external review pending |
| [v0.2](specification/v0.2/README.md) | Relationships and execution graphs | Exploratory draft |
| [v0.3](specification/v0.3/README.md) | Transport-neutral semantic events | Exploratory draft |
| [v0.4](specification/v0.4/README.md) | JSON Schema artifacts | Exploratory draft |
| [v0.5](specification/v0.5/README.md) | Versioning and compatibility rules | Exploratory draft |

Later layers depend on earlier ones. They are available for design feedback and prototype implementations; acceptance of a later layer does not bypass open review gates in an earlier layer.

Conformance should be understood in two layers:

- **AIOS defines the normative rules**: schemas, conformance requirements,
  canonical fixtures, and expected validation behavior
- **implementations may provide tooling**: for example, AgenticLens can expose
  a practical `conformance` CLI over those rules without owning the standard

Two machine-readable catalogs mirror the normative text for tooling, so
validators can cite the rule an issue violates instead of inventing their own
labels:

- [`specification/v0.4/conformance-rules.json`](specification/v0.4/conformance-rules.json)
  — stable IDs for each v0.4 producer/consumer requirement (`AIOS-0.4-P01` …)
- [`specification/v0.5/compatibility.json`](specification/v0.5/compatibility.json)
  — the `spec_version` grammar, the schema set behind each published marker,
  and IDs for each consumer compatibility rule (`AIOS-0.5-V01` …)

The Markdown documents stay normative; tests fail if a catalog drifts from them.

## Choose a path

- **Understand the model:** read the [v0.1 overview](specification/v0.1/README.md), [core concepts](specification/v0.1/core-concepts.md), and [conceptual examples](specification/v0.1/examples.md).
- **Represent execution graphs:** read [v0.2 relationships](specification/v0.2/relationships.md).
- **Instrument runtime events:** read [v0.3 semantic conventions](specification/v0.3/semantic-conventions.md).
- **Prototype a producer or consumer:** read the [v0.4 schema guide](specification/v0.4/README.md) and [validated Run example](specification/v0.4/examples/valid/run.json).
- **Decide whether you may safely consume an artifact:** read the [v0.5 versioning and compatibility rules](specification/v0.5/versioning.md).
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

That same boundary applies to conformance: the specification owns the rules
and expected behavior, while implementation repositories may offer user-facing
commands that execute those checks.

See [SPECIFICATION.md](SPECIFICATION.md) for the complete reading order and maturity rules, or [CONTRIBUTING.md](CONTRIBUTING.md) to propose a change.

## What's Next

Upcoming specification work (see [ROADMAP.md](ROADMAP.md)):

- **Provenance and evidence concepts** — standardize source references,
  evidence lineage, and derived findings as first-class spec objects
- **Conformance test suite** — producers can validate artifacts against the
  spec independently, while implementation repositories can expose convenient
  CLIs on top
- **Naming conventions** — lock down field naming rules, casing, and
  abbreviation policy
- **Migration guides** — clear upgrade paths between spec versions

## Control Tower integration boundary

AgenticOps Control Tower owns deployment registration, heartbeat, fleet
inventory and operator workflows. AgenticLens owns observability and analysis;
Agentic Evals owns scoring and release-gate computation; Agentic Sidecar owns
decision supervision (SUPERVISE); Agentic Chaos owns fault injection and
resilience experiments. AI Operations Specification owns shared semantics and
is currently draft.

Tower's native artifact readers consume existing producer outputs using an
explicit deployment/evidence link. They do not change producer behavior or
convert a failed run, failed gate, blocked action or injected fault into fleet
health. This link is a Tower-local contract, not a normative AIOS schema.
See [Control Tower's evidence contract](https://github.com/DeepAgentLabs/agenticops-control-tower/blob/main/docs/ecosystem-alignment.md).
Tower 0.6.0 adds pushed evidence posture, cited investigation and approved
deterministic staging recovery. Pull collection and production runtime adapters
remain planned; native interoperability does not establish stable AIOS conformance.

## Sidecar 0.8 interoperability

The native sidecar.correlation/1 convention is recorded in
[drafts/sidecar-correlation-v1](drafts/sidecar-correlation-v1/README.md), with a
validated producer/consumer fixture. This is non-normative and does not promote
AIOS maturity or add a runtime dependency.

Sidecar 0.8 provides Shared/Exclusive context-only, guardrails-only or combined
configuration, explicit host context delivery and mandatory guardrail composition.
Exclusive rules cannot weaken shared restrictions. Cross-framework privacy,
revocation and delegated authority remain v0.9 validation; stable schemas remain
v1.0. Native correlated Lens readback requires Lens 0.7.1. All sibling packages
stay optional; no dependency floor is increased without a runtime requirement.
See the [Sidecar integration contract](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/docs/integrations.md).

## Control Tower 0.6.0 integration

Tower Phase 6 and 6A ship together in 0.6.0 with MCP 0.3.6: evidence-cited
investigation, exact-preview human approval and verified deterministic staging
recovery. Native producer outcomes and package ownership remain unchanged.
See [compatibility, examples and dependency matrix](docs/control-tower-0.6.md).
This is documentation alignment; no package release or dependency bump is needed.
