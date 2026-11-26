# AI Operations Specification

What happened when an AI agent ran, described in one format that every tool can read?

## What it does

A shared contract for AI runs, evidence and incidents, grouped by area below. Each area links to its detailed guide. For runnable steps, see the [developer guide](developer-guide.md); for every field and rule, see the [API reference](api-reference.md).

### 1. Runtime model

- **Fifteen runtime concepts**
    - Workflow, Run, Request, Step and Agent
    - Model interaction, Prompt, Context, Tool invocation, RAG retrieval and Memory operation
    - Evaluation, Safety signal, Reliability event and Incident
- **Clear boundaries**
    - A Workflow is a reusable definition; a Run is one execution of it
    - Each concept has one meaning, whichever framework produced it

Guides: [Core concepts](../specification/v0.1/core-concepts.md) ·
[Terminology](../specification/v0.1/terminology.md)

### 2. Execution graphs

- **Thirteen relationship types**
    - Containment and ordering: `contains`, `parent-of`, `follows`, `run-of`
    - Causality and dependency: `caused`, `depends-on`
    - Participation: `performed-by`, `delegated-to`, `handed-off-to`, `observed-in`
    - Evidence: `evaluates`, `signals-on`, `evidence-for`
- **Retries and recovery**
    - Each attempt keeps its own identity, linked to the attempt before it
    - Observed recovery is recorded as evidence, not inferred

Guides: [Relationships and execution structure](../specification/v0.2/relationships.md) ·
[Canonical examples](../specification/v0.6/examples.md)

### 3. Semantic events and measurements

- **Events**
    - 43 canonical `aiops.*` lifecycle events, from `aiops.run.started` to `aiops.incident.resolved`
    - Producer-specific events under a reverse-domain name
- **Measurements**
    - Units and ISO currency codes; cost always carries its currency
    - Each value is marked `observed`, `estimated` or `derived`

Guides: [Semantic conventions](../specification/v0.3/semantic-conventions.md)

### 4. Artifacts and schemas

- **Run and Workflow artifacts**
    - Portable JSON documents, one schema per `artifact_type`
    - JSON Schema 2020-12, validated offline by registering schemas by `$id`
- **Six artifact families**
    - Run, Workflow, Provenance record, Verification signal, Audit event and Investigation report

Guides: [Artifact schemas](../specification/v0.4/README.md) ·
[API reference](api-reference.md#artifact-families)

### 5. Conformance

- **Rule catalogs**
    - 55 rules with stable IDs (for example `AIOS-0.4-P05`) that validators report
    - Producer, consumer and implementation obligations
    - Each rule is decided by schema, semantic, cross-artifact or process checks
- **Portable conformance suite**
    - 66 outcome cases and 5 resolution cases with expected rule IDs
    - Valid, schema-invalid, semantic-invalid and unsupported-marker examples

Guides: [Conformance rules](../specification/v0.4/conformance.md) ·
[Portable conformance suite](../specification/v0.6/conformance-suite/README.md)

### 6. Versioning and compatibility

- **Version markers**
    - Every artifact declares its `spec_version`; consumers route by it
    - Repository releases, artifact markers and consumer support are versioned separately
- **Migration**
    - Adopt layers and companion families one at a time, without rewriting existing artifacts
    - Rollout and rollback guidance

Guides: [Versioning and compatibility](../specification/v0.5/versioning.md) ·
[Migration and rollback](../specification/v0.6/migration-guide.md)

### 7. Extensions and naming

- **Extensions**
    - Reverse-domain names outside the reserved `aiops` namespace
    - Consumers preserve extensions they do not recognize
- **Naming**
    - Grammars for fields, vocabularies, event names and rule IDs

Guides: [Extension model](../specification/v0.6/extension-model.md) ·
[Naming conventions](../specification/v0.6/naming-conventions.md)

### 8. Provenance and lineage

- **Provenance records**
    - Subjects, sources, findings and lineage edges in a separate companion artifact
    - Lineage types: `derived-from`, `supports`, `contradicts`, `supersedes`
- **Cross-artifact resolution**
    - Subject identity, held bytes and SHA-256/384/512 digests
    - Typed references into the subject artifact

Guides: [Provenance](../specification/v0.6/provenance.md)

### 9. Operational artifacts

- **Verification signals**
    - Second opinions with verdict, confidence, grounding and safety assessment
- **Audit events**
    - Attributed actions with actor, target, occurrence time and native outcome
- **Investigation reports**
    - Incident context, operator summary, cited findings, timeline and recovery state
- **Privacy**
    - Credentials and privileged context stay out of every artifact

Guides: [Verification signals](../specification/v0.8/verification-signals.md) ·
[Audit events](../specification/v0.8/audit-events.md) ·
[Investigation reports](../specification/v0.8/investigation-reports.md) ·
[Operational conformance](../specification/v0.8/conformance.md)

### 10. OpenTelemetry mapping

- **Projection to OTel**
    - Complete mapping of AIOS events to OpenTelemetry spans and events
    - Explicit timing, identities and any information lost in the projection
    - A tested retry example

Guides: [OpenTelemetry companion](../specification/v0.6/otel-binding.md)

### 11. Companion profiles

- **Access evidence**: dispatch, completion, denial and revocation observations
- **Sidecar correlation**: native decision identity with explicit host correlation
- **Sidecar contracts**: intent, decision, audit, scope and transfer mappings

Guides: [Access evidence](../drafts/access-evidence-v1/README.md) ·
[Sidecar correlation](../drafts/sidecar-correlation-v1/README.md) ·
[Sidecar contracts](../drafts/sidecar-contracts-v1/README.md)

### 12. Ecosystem interoperability

- **AgenticLens**: instrumentation and analysis
- **Agentic Evals**: scoring and release gates
- **Agentic Chaos**: fault injection and resilience
- **Agentic Sidecar**: supervision and governance
- **MCP Server**: transport and composition
- **Control Tower**: fleet and operator workflows

Guides: [Operational adoption](v0.8.0-ecosystem.md) ·
[Source mappings](../reviews/operational-artifact-mappings.md)

## What you need

A JSON Schema 2020-12 validator in any language, and runtime data from your agent or framework to describe.

## Start here

Validate the customer-support Run example and read its graph: [follow the quickstart](developer-guide.md#quickstart).

## Limits

- AIOS defines the artifacts. Running agents, collecting telemetry and hosting dashboards are done by the products that implement it.
- Schemas check structure. Semantic rules are checked by the conformance suite and the rule catalogs.
- Each artifact family keeps its own version marker (`0.4-draft`, `0.6-draft` or `0.8-draft`).

See [Limitations](limitations.md).

## Documentation

- [Developer Guide (simple)](developer-guide.md): short task workflows and a capability index
- [API Reference (detailed)](api-reference.md): every field, constraint and conformance rule of each artifact family
- [AI Readable Documentation](https://deepagentlabs.io/ai-operations-spec/docs/llms-full.md): the full reference as one file for AI tools, with schemas, rule catalogs and fixtures
