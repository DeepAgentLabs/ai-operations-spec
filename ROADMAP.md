# AI Operations Specification Roadmap

## Release Status

- **v0.1** 🏗️ In review — Core runtime concepts and boundaries
- **v0.2** 🚧 Exploratory draft — Relationships and execution graphs
- **v0.3** 🚧 Exploratory draft — Transport-neutral semantic events
- **v0.4** 🚧 Exploratory draft — JSON Schema artifacts
- **v0.5** 🚧 Planned — Versioning and compatibility rules
- **v0.6** 🚧 Planned — Canonical examples and extension model
- **v0.6.x** 🚧 Planned — Provenance, evidence, and operational artifacts
- **v1.0** 🚧 Planned — Stable specification

## Next Steps

- Resolve the remaining v0.1 review gate and keep later milestones clearly
  labeled as draft until those dependencies close.
- Prove the v0.4 draft against at least two independent producers and
  consumers.
- Define compatibility/versioning policy before claiming stable consumption
  guarantees.
- Promote provenance, evidence, and conformance fixtures from implementation
  practice into spec-standard artifacts once the underlying model settles.

## Cross-Project Dependencies

AIOS is the normative specification, not an implementation package, but its
roadmap still depends on evidence from sibling projects and independent
implementers.

- `agenticlens`
  Provides real producer/consumer evidence for traces, findings, conformance
  tooling, and schema usage.
- `agentic-chaos`
  Provides resilience and fault evidence that tests whether the model can
  represent degraded, failed, and recovered behavior.
- `deep-agentic-core-mcp`
  Provides a consumer/control-plane view that exercises artifact validation and
  interoperability across tools.

For roadmap planning, distinguish:

- `Depends on`: an earlier AIOS layer that must freeze first.
- `Evidence from`: sibling repos or independent implementers that should
  validate the design in practice.
- `Coordinate with`: implementation repos that may need doc, fixture, or
  terminology updates when the spec changes.

## Definition of Done

A roadmap item is done only when all applicable work is complete:

- normative text is written with scope, boundaries, and maturity clearly
  stated
- examples, fixtures, and schema changes are added or updated together
- tests validate the intended structure or document invariants
- `README.md` and this roadmap are updated when milestone status or user
  guidance changes
- dependent milestone documents are updated when an earlier layer changes
- implementation evidence or independent review is recorded for any acceptance
  gate that requires it
- draft, reviewed, and stable claims remain consistent across all milestone
  documents

## Direction

DeepAgentLabs builds the AI Operations Specification **specification-first**. The standard defines meaning before SDK ergonomics, exporter fields, dashboards, or integrations.

```text
AI Operations Specification
    |-- Core concepts
    |-- Relationships and execution graph
    |-- Semantic conventions
    |-- JSON Schemas
    |-- Versioning and compatibility
    `-- Examples and extension model
             |
             `-- Reference implementations
                 |-- AgenticLens
                 |-- Agentic Chaos
                 `-- DeepAgent MCP
```

The goal is an open standard for representing the execution, evaluation, safety, reliability, and operational behavior of AI systems.

## Build order

### Phase 1 / v0.1 — Core concepts

**Status: foundation draft; internal terminology decisions resolved, independent review pending.**

Define the meaning and boundaries of:

- Workflow and Run
- Request and Step
- Agent
- Model Interaction
- Prompt and Context
- Tool Invocation
- RAG Retrieval
- Memory Operation
- Evaluation
- Safety Signal
- Reliability Event
- Incident

No normative JSON field catalog, SDK model, or event namespace belongs in this phase.

Success means two independent implementers can classify the same runtime occurrences consistently.

### Phase 2 / v0.2 — Relationships and execution structure

**Status: exploratory draft; blocked from freeze by v0.1 review.**

Define:

- Workflow-to-Run and Run-to-Request structure
- step parent-child and causal relationships
- sequential, parallel, branch, join, retry, and loop representation
- parent-child Runs
- Agent participation, handoff, and delegation
- Step relationships to model, tool, retrieval, and memory occurrences

Success means two tools can represent the same execution graph consistently.

### Phase 3 / v0.3 — Semantic conventions

**Status: exploratory draft; blocked from freeze by v0.1 and v0.2 review.**

Define canonical event names, lifecycle meaning, naming rules, and the minimum attributes needed to interpret events. Candidate areas include workflow/run lifecycle, requests, Agent activity, model interactions, prompts, context assembly, tools, memory, retrieval, evaluations, safety, reliability, and incidents.

Candidate names are non-normative until v0.3 is reviewed.

Success means producers and consumers agree on stable AI-native event semantics independent of transport.

### Phase 4 / v0.4 — JSON Schemas

**Status: exploratory schemas and fixtures; blocked from freeze by v0.1–v0.3 review.**

Deliver machine-readable schemas and validation fixtures derived from v0.1–v0.3. Object-specific schemas may be introduced where independent reuse justifies them.

Success means artifacts can be validated without a DeepAgentLabs package.

The repository preserves an [early non-normative schema experiment](drafts/v0.4/README.md) for history. The current v0.4 design under `specification/v0.4/` supersedes that experiment but remains a draft until earlier milestones are accepted.

### Phase 5 / v0.5 — Versioning and compatibility

Define artifact version markers, additive and breaking change rules, deprecation, compatibility behavior, and extension expectations.

Success means implementers can determine whether they may safely consume an artifact.

### Phase 6 — Examples and extension model

Publish minimal and advanced canonical artifacts, namespace rules, third-party extension guidance, and conformance expectations.

The specification should define what conformance means, but it should not
require the specification repository itself to be the primary end-user entry
point for running those checks. Implementation repositories may expose
convenient CLIs as long as they follow the normative rules defined here.

### Phase 6.x — Provenance, Evidence & Operational Artifacts

Formalize concepts proven in implementation repositories.

**Implement now (after implementation evidence settles):**

- provenance/evidence concepts — standardize source references, evidence
  lineage, and derived findings as first-class spec objects
- conformance test suite — so producers can validate their artifacts against
  the spec without importing a DeepAgentLabs package
- conformance requirements, canonical fixtures, and expected validation
  behavior — so implementations such as AgenticLens can offer user-facing
  `conformance` commands without owning the standard
- naming conventions document — lock down field naming rules, casing,
  singular/plural, abbreviation policy

**Implement next:**

- migration guides between spec versions (v0.1→v0.2→v0.3→v0.4)
- hosted documentation site for browsable spec (MkDocs)
- optional report/investigation artifact schemas (if implementation usage
  proves the need)
- incident context and operator-facing summary semantics
- OpenTelemetry GenAI semantic convention binding — a non-normative mapping
  document from canonical `aiops.*` events and common attributes to OTel
  spans, span events, and resource attributes, so producers already emitting
  OTel do not need to invent their own bridge independently
- verification-signal schema — a standard shape for second-opinion/judge
  results (verdict, confidence, evidence-grounding, safety concerns) as a
  first-class signal object, once judge-output shapes stabilize across
  implementation repos; candidate prior art: `devops-open-agent`'s
  LLM-as-a-Judge verifier output
- audit-event schema — a standard shape for who-did-what operational events
  (actor, action, target artifact reference, timestamp, no secret values),
  feeding the incident-context/operator-facing summary semantics above;
  candidate prior art: `devops-open-agent`'s structured audit log

Success means implementations can attach provenance to findings using
spec-standard objects, and producers can run conformance checks independently.

### v1.0 — Stable specification

Freeze the reviewed core model, relationships, semantic conventions, schemas, versioning, examples, and extension model.

Success means third parties can implement the standard without importing DeepAgentLabs packages.

## Repository organization

```text
ai-operations-spec/
|-- README.md
|-- SPECIFICATION.md
|-- ROADMAP.md
|-- specification/
|   |-- v0.1/
|   |-- v0.2/
|   |-- v0.3/
|   `-- v0.4/
`-- drafts/
    `-- v0.4/
```

Specification milestone documents live under `specification/` and clearly state their maturity. Premature implementation research lives under `drafts/` and must state that it is non-normative. Stable release layout will be decided before v1.0.

## Package roles

- `ai-operations-spec` defines the standard.
- `agenticlens` instruments and exports the standard, and may provide
  user-facing conformance tooling over AIOS-defined rules.
- `agentic-chaos` adds resilience and fault-testing evidence using the same model.
- `deep-agentic-core-mcp` reads, exposes, and transforms conforming artifacts.

The specification remains above every implementation.

## Contributor test

A contribution belongs here when it makes the shared runtime model, relationships, semantic conventions, schemas, compatibility, examples, or extensions clearer for independent implementers. Package-specific behavior belongs in the implementation repository.
