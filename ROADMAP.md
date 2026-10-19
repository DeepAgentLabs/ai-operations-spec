# AI Operations Specification Roadmap

> An evidence-based audit of this roadmap against the actual contents of
> `specification/`, `drafts/`, and `reviews/` is recorded in
> [ROADMAP_AUDIT.md](ROADMAP_AUDIT.md). It found the Release Status badges
> below still accurate, but the "Next Steps" and "Cross-Project Dependencies"
> sections stale relative to review evidence already committed under
> `reviews/`.

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

- Machine-readable conformance and compatibility catalogs shipped in the
  `v0.5.1` repository release (2026-10-13):
  `specification/v0.4/conformance-rules.json` and
  `specification/v0.5/compatibility.json`. `deep-agentic-core-mcp` consumes
  them for rule-cited conformance reports and `spec_version`-routed
  validation. No milestone's review status changes.
- Close external review decision `D-001` in
  [reviews/decision-log.md](reviews/decision-log.md): every milestone from
  v0.1 through v0.4 still needs review from at least one party with no
  DeepAgentLabs authorship, funding, or editorial role. A ready-to-send
  outreach packet already exists at
  [reviews/EXTERNAL_REVIEW_INVITE.md](reviews/EXTERNAL_REVIEW_INVITE.md); this
  is the actual blocker, not further internal drafting.
- Two DeepAgentLabs-owned framework mappings
  ([agenticlens](reviews/framework-mappings/agenticlens.md),
  [agentic-chaos](reviews/framework-mappings/agentic-chaos.md)) and two
  sibling-repo-derived run artifacts that pass v0.4 schema and semantic
  conformance (`reviews/artifacts/`) are already committed. They are real
  evidence but do not close the "independent implementations" gates in
  [reviews/evidence-matrix.md](reviews/evidence-matrix.md), because neither
  producer is outside DeepAgentLabs — a non-DeepAgentLabs producer/consumer
  is still needed to prove the v0.4 draft.
- Define compatibility/versioning policy before claiming stable consumption
  guarantees.
- Promote provenance, evidence, and conformance fixtures from implementation
  practice into spec-standard artifacts once the underlying model settles.
  v0.4's `evidence` object family is an early precursor but not yet the
  dedicated v0.6.x concept.
- Keep the Release Status badges as-is until `D-001` closes; do not treat a
  closed internal decision (e.g. `D-002`, `D-003`, `D-004` in
  [reviews/decision-log.md](reviews/decision-log.md)) as equivalent to
  independent review.

## Cross-Project Dependencies

AIOS is the normative specification, not an implementation package, but its
roadmap still depends on evidence from sibling projects and independent
implementers.

- `agenticlens`
  Provides real producer/consumer evidence for traces, findings, conformance
  tooling, and schema usage. Delivered so far:
  [framework mapping](reviews/framework-mappings/agenticlens.md) and a
  passing v0.4 conformance artifact
  (`reviews/artifacts/agenticlens-support-run.aios.json`). AgenticLens 0.7.0
  consumes `specification/v0.4/conformance-rules.json`: every conformance
  issue cites its `AIOS-0.4-*` rule, each applicable rule is reported as
  pass / fail / not checked, and artifacts declaring another `spec_version`
  are rejected per `AIOS-0.5-V03`. Still a DeepAgentLabs-owned repo, so this
  evidence does not by itself satisfy an "independent implementation"
  acceptance gate.
- `agentic-chaos`
  Provides resilience and fault evidence that tests whether the model can
  represent degraded, failed, and recovered behavior. Delivered so far:
  [framework mapping](reviews/framework-mappings/agentic-chaos.md) and a
  passing v0.4 conformance artifact
  (`reviews/artifacts/agentic-chaos-customer-support.aios.json`). The
  0.6.0 addendum records the additive call log and contract verdicts, which
  stay producer-native and are not AIOS evaluation objects. Same independence
  caveat as above.
- `deep-agentic-core-mcp`
  Provides a consumer/control-plane view that exercises artifact validation and
  interoperability across tools.
- `agentic-sidecar`
  Provides future decision, intent, and governance artifacts that test whether
  the shared model can represent pre-action supervision cleanly.
- `agenticops-control-tower`
  Provides future inventory, status, configuration, and control-plane artifact
  needs that test whether the shared model can support operator-facing
  operations semantics without collapsing into one package's implementation.

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
                 |-- Agentic Sidecar
                 |-- DeepAgent MCP
                 `-- AgenticOps Control Tower
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

**Status: exploratory draft; blocked from freeze by v0.1–v0.4 review.**

Define artifact version markers, additive and breaking change rules, deprecation, compatibility behavior, and extension expectations. See [specification/v0.5/versioning.md](specification/v0.5/versioning.md) for the current draft text and decision `D-005` in [reviews/decision-log.md](reviews/decision-log.md) for the closed-vocabulary-growth classification it depends on.

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
|   |-- v0.4/
|   `-- v0.5/
|-- drafts/
|   `-- v0.4/
`-- reviews/
    |-- decision-log.md
    |-- evidence-matrix.md
    |-- framework-mappings/
    |-- scenarios/
    `-- artifacts/
```

Specification milestone documents live under `specification/` and clearly state their maturity. Premature implementation research lives under `drafts/` and must state that it is non-normative. `reviews/` holds the acceptance-gate evidence scaffolding (decision log, evidence matrix, framework mappings, shared scenarios, and validated review artifacts) described in
[MILESTONE_CLOSEOUT_PLAN.md](MILESTONE_CLOSEOUT_PLAN.md) and audited in
[ROADMAP_AUDIT.md](ROADMAP_AUDIT.md). Stable release layout will be decided before v1.0.

## Package roles

- `ai-operations-spec` defines the standard.
- `agenticlens` instruments and exports the standard, and may provide
  user-facing conformance tooling over AIOS-defined rules.
- `agentic-chaos` adds resilience and fault-testing evidence using the same model.
- `deep-agentic-core-mcp` reads, exposes, and transforms conforming artifacts.

The specification remains above every implementation.

## Contributor test

A contribution belongs here when it makes the shared runtime model, relationships, semantic conventions, schemas, compatibility, examples, or extensions clearer for independent implementers. Package-specific behavior belongs in the implementation repository.

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

## Evals 0.7.2 report contract

Agentic Evals 0.7.2 publishes native report (`schema_version: "1.0"`) and
gate-decision JSON Schemas, with offline `report_schema()` and
`gate_decision_schema()` accessors. Contract 1.x evolves additively; readers
should tolerate unknown fields. These package-local schemas are not normative AIOS contracts and do not establish AIOS conformance. The future evaluation-evidence mapping remains Evals v0.10 work.

See the [contract, examples and compatibility policy](https://github.com/DeepAgentLabs/agentic-evals/blob/main/docs/report-contract.md). Existing dependency
ranges remain sufficient; using the new accessors directly requires
`agentic-evals>=0.7.2`. This documentation alignment needs no sibling patch release.

## AgenticLens 0.8.0 suite management

AgenticLens 0.8.0 delivers its v0.6 milestone: `agenticlens.suites` and
`agenticlens suite` build regression suites from CSV/JSON imports, production
traces and user feedback. It masks PII by default before storage (`--no-mask`
opts out), detects duplicates and
conflicting labels, adds synthetic variations and stable splits, records
reviews, and approves suites into immutable, hash-verified versions that CI
verifies, exports and evaluates. Suites stay plain agentic-evals `TestSuite`
files.

The suite-version, feedback-batch, duplicate-report and masking-report schemas
are Lens-local (`schemas/suites/` in AgenticLens), not AIOS objects, and make
no conformance claim. No normative change or spec release is needed; a shared
evaluation-dataset object would be proposed here first.

See the [suite management guide](https://github.com/DeepAgentLabs/agenticlens/blob/v0.8.0/docs/suite-management.md).

## AgenticLens 0.9.0 ModelFit

AgenticLens 0.9.0 delivers its v0.7 milestone: `agenticlens.modelfit` and
`agenticlens modelfit` recommend a model per task category from recorded
experiment reports, under hard quality, cost, latency, safety, provider and
deployment constraints that fail closed. Each recommendation carries a
confidence level with reasons, an explanation, alternatives, a fallback
(on a different provider when one is feasible), savings against a reference variant tied to the
experiment evidence, and quality risks, plus a task-level model matrix.

The ModelFit config and report schemas are Lens-local (`schemas/modelfit/` in
AgenticLens), not AIOS objects, and make no conformance claim. No normative
change or spec release is needed; a shared model-selection or routing-decision
object would be proposed here first, alongside Lens v0.8 advisory routing.

See the [ModelFit guide](https://github.com/DeepAgentLabs/agenticlens/blob/v0.9.0/docs/modelfit.md).

## Evals 0.8.0 CLI interoperability

Evals 0.8.0 adds a declarative evaluation and release-gate CLI with native JSON, JUnit and Markdown output. These outputs are package-local artifacts, not AIOS evaluation evidence or conformance claims. Normative evaluation evidence export remains Evals v0.10 work; no specification or schema change is required.

See [CLI usage and compatibility](docs/evals-0.8-cli.md).

## Chaos 0.7.0 interoperability

Chaos 0.7.0 adds sequential fault cascades, deterministic monotonic breaking-point
search, synthetic response poisoning (including prompt/tool-response instruction
and policy-bypass payloads), and explicit-price retry cost estimates. Native
child event IDs and fault types remain intact; cascade IDs/stages and poisoning
strategy/payload/seed are additive event detail. Existing report readers and
AIOS exports remain compatible.

See the [v0.7 guide and offline synthetic example](https://github.com/DeepAgentLabs/agentic-chaos/blob/v0.7.0/docs/v0.7.md).
The example includes observed synthetic dispatches and a bypassed negative
control. Injection or recovery alone does not prove containment. No new shared
schema, automatic adapter, hosted execution capability or containment guarantee
is introduced.

These are producer-local extensions, not normative concepts or schema changes. Existing AIOS Run mappings preserve native evidence; specification maturity and conformance claims remain unchanged. No spec release is needed.

## Control Tower 0.7.0 fleet operations

Tower 0.7.0 adds frozen environment/capability targeting, bulk desired settings,
separate approval, durable per-target results and bounded stop/MCP-revocation
acknowledgement through Python, HTTP and CLI. No fleet atomicity or automatic
rollback/resume is claimed. Timed-out/requested commands need host reconciliation.

Bulk selectors, approvals, command IDs and receipts remain Tower-local implementation contracts. This integration creates no normative AIOS schema or conformance claim; shared command semantics remain draft.

Existing optional dependency ranges remain sufficient. No sibling runtime or
native evidence schema changes are required; this documentation alignment needs
no patch release. See the [operator guide](https://github.com/DeepAgentLabs/agenticops-control-tower/blob/v0.7.0/docs/fleet-operations.md).

See the [local Tower compatibility guide](docs/tower-0.7-fleet-operations.md) for the operator workflow and package boundaries.

## AgenticLens 0.10.0 routing compatibility

See the [local integration boundary guide](docs/lens-0.10-routing.md).

AgenticLens 0.10.0 implements roadmap v0.8: evidence-based runtime model
selection, fail-closed routing constraints, bounded provider failover,
confidence/escalation handoffs, shadow/canary modes and a local routing journal.
The default is advisory; execution uses explicit caller-owned callbacks.
MCP 0.3.12 exposes read-only `lens.routing_decide` and pins hosted Lens 0.10.0.
See the [routing guide](https://github.com/DeepAgentLabs/agenticlens/blob/v0.10.0/docs/routing.md)
and [offline example](https://github.com/DeepAgentLabs/agenticlens/blob/v0.10.0/examples/routing_demo.py).

Lens routing decisions/results/policies and schema version 1.0 are package-local
implementation artifacts, not a normative AIOS extension or conformance claim.
No shared event meaning, schema version or reviewed specification layer changes.
There is no Python dependency or specification release required for this alignment.

## Chaos 0.8.0 interoperability

Chaos 0.8.0 adds:

- multi-stage chaos workflows: steps, steady-state health checks, parallel
  branches, approval gates that can be resumed, and reusable templates
- declarative YAML/JSON/TOML experiments, with validation that never executes
  targets and cron schedule previews
- `Scope` explosion-radius control (steps, providers and exclusions) on every
  fault
- a topology fuzzer that weights fault placement by fan-out

Native event IDs and fault types are unchanged. Workflow provenance
(`detail.workflow`) and an optional `ChaosReport.workflow` summary are
additive. A workflow's steps merge into one native report for contracts and
AIOS export.

See the [v0.8 guide](https://github.com/DeepAgentLabs/agentic-chaos/blob/v0.8.0/docs/v0.8.md)
and the [offline examples](https://github.com/DeepAgentLabs/agentic-chaos/tree/v0.8.0/examples/workflows).
Workflow statuses, health checks and fuzz outcomes are resilience evidence.
They are not scores, release gates or proof of containment. No new shared
schema, automatic adapter or hosted execution capability is introduced.

Merged workflow exports validate against the v0.4 Run schema and semantic checker. The workflow summary is a producer-local extension member, not a normative Workflow object or a schema change. Specification maturity and conformance claims are unchanged. No spec release is needed.
