# AI Operations Specification developer guide

Use this simple guide to choose a capability and prototype a producer or consumer. The [API Reference (detailed)](api-reference.md) lists every field, constraint and rule of each artifact family. The [AI Readable Documentation](https://deepagentlabs.io/ai-operations-spec/docs/llms-full.md) includes the full capability index, maintained specification/profile text, schema sets, rule catalogs, canonical examples and portable fixtures with a source/checksum manifest.

AIOS defines a language-neutral contract; runtimes, SDKs and exporters implement it. Repository release **1.0.0** ships every artifact family with its schemas, rule catalogs, canonical examples and the portable conformance suite.

[Capability index](#capability-index) · [Quickstart](#quickstart) · [Artifact markers](#artifact-markers) · [Troubleshooting](#troubleshooting)

## Capability index

| Capability | What you can do |
| --- | --- |
| [Runtime model](#runtime-model) | Distinguish all fifteen runtime concepts and their boundaries. |
| [Execution graphs](#execution-graphs) | Represent containment, ordering, causality, participation and evidence links. |
| [Retries and recovery evidence](#retries) | Preserve separate attempts and link observed recovery. |
| [Semantic events](#semantic-events) | Record canonical lifecycle events and producer event names. |
| [Measurements](#measurements) | Preserve units, currency and observed/estimated/derived meaning. |
| [Run and Workflow artifacts](#artifacts) | Exchange execution artifacts and reusable workflow definitions. |
| [Offline structural validation](#structural-validation) | Route to the declared schema and register local dependencies. |
| [Semantic conformance](#semantic-conformance) | Check identity, references, timestamps and graph invariants. |
| [Version routing and compatibility](#compatibility) | Separate repository releases, artifact markers and consumer support. |
| [Extensions and preservation](#extensions) | Publish reusable metadata contracts without changing core meaning. |
| [Naming conventions](#naming) | Apply field, vocabulary, event and rule-ID grammars. |
| [Provenance and lineage](#provenance) | Link subjects, sources and findings in a separate companion. |
| [Cross-artifact resolution](#resolution) | Resolve subject identity, held bytes, digests and typed object references. |
| [Portable validator suite](#portable-suite) | Compare schema, semantic, unsupported and resolution outcomes offline. |
| [Verification signals](#verification) | Represent second opinions, grounding, safety and unavailable assessments. |
| [Audit events](#audit) | Record attributed actions, observation times, targets and native outcomes. |
| [Investigation reports](#investigations) | Summarize incidents, citations, uncertainty, timelines and recovery. |
| [Operational conformance and privacy](#operational-conformance) | Apply companion semantic rules and separate process obligations. |
| [OpenTelemetry mapping](#opentelemetry) | Project observed events with explicit timing, identities and losses. |
| [Migration, rollout and rollback](#migration) | Adopt cumulative layers and companion families without rewriting markers. |
| [Access-evidence profile](#access-evidence) | Embed individual dispatch, completion, denial and revocation observations. |
| [Sidecar correlation profile](#sidecar-correlation) | Preserve native decision identity and explicit host correlation. |
| [Sidecar candidate contracts](#sidecar-contracts) | Inspect native intent, decision, audit, scope and transfer mappings. |
| [Ecosystem adoption and ownership](#ecosystem) | Map Lens, Evals, Chaos, Sidecar, MCP and Tower evidence explicitly. |
| [Review gates and maturity](#review) | Assess draft claims and independent implementation evidence. |
| [Documentation and contribution workflow](#maintenance) | Build both sites, refresh the reference and keep coverage complete. |

## Quickstart

Use a source checkout with Python 3.10 or newer and uv installed. From the repository root:

```bash
uv sync --extra dev
uv run pytest tests/test_v04_schema.py tests/test_v06_conformance_suite.py
```

Open the [minimal Run](../specification/v0.6/examples/minimal-run.json), then the [customer-support Run](../specification/v0.4/examples/valid/run.json). The latter records retrieval and model Steps, an evaluation and explicit graph edges. These are synthetic fixtures, not live operational evidence. The structural-validation tutorial below accepts your own JSON file; full draft alignment also requires semantic and consumer-process checks.

## Artifact markers

| Artifact family | Exact marker | Schema |
| --- | --- | --- |
| Run, Workflow | `0.4-draft` | [Run](../specification/v0.4/schemas/run.schema.json), [Workflow](../specification/v0.4/schemas/workflow.schema.json) |
| Provenance | `0.6-draft` | [Provenance](../specification/v0.6/schemas/provenance.schema.json) |
| Verification signal | `0.8-draft` | [Verification](../specification/v0.8/schemas/verification_signal.schema.json) |
| Audit event | `0.8-draft` | [Audit](../specification/v0.8/schemas/audit_event.schema.json) |
| Investigation report | `0.8-draft` | [Investigation](../specification/v0.8/schemas/investigation_report.schema.json) |

There is no `0.7-draft` family. Versioned layers are cumulative design milestones, not successive Run wire formats. JSON Schema files reuse common definitions; register them by full `$id`, never filename alone.

## Runtime model

Use a Workflow for a reusable process, a Run for one execution, a Request for incoming work and a Step for an activity boundary. Agents participate in work; a model interaction is one model call, not an Agent. Prompt and Context describe inputs. Tool Invocation, RAG Retrieval and Memory Operation describe distinct occurrences. Evaluation, Safety Signal, Reliability Event and Incident record evidence or operational conditions, not interchangeable execution states. Use the [terminology](../specification/v0.1/terminology.md) when mapping a framework's names.

Detailed reference: [Core runtime concepts](../specification/v0.1/core-concepts.md).

## Execution graphs

Choose a directional relationship from the thirteen defined types: `run-of`, `contains`, `parent-of`, `caused`, `follows`, `depends-on`, `performed-by`, `delegated-to`, `handed-off-to`, `observed-in`, `evaluates`, `signals-on` and `evidence-for`. In the [customer-support Run](../specification/v0.4/examples/valid/run.json), the Run contains two Steps; `depends-on` orders their dependency, and each occurrence has an `observed-in` Step. Parallel branches, joins, handoffs and cross-Run links need explicit evidence; array order does not establish causality.

Detailed reference: [Relationships and execution structure](../specification/v0.2/relationships.md).

<a id="retries"></a>

## Retries and recovery evidence

Start from the [retry Run](../specification/v0.6/examples/retry-run.json). Retain separate occurrence IDs for the failed lookup and successful retry, link the retry to its prior attempt with `follows` or `caused`, and connect both to their Step. Do not overwrite failure with the final success or invent missing events. The advanced examples also cover delegation, parallel work and incident evidence.

Detailed reference: [Canonical examples and negative controls](../specification/v0.6/examples.md).

## Semantic events

Use the complete `aiops.*` event catalog for observed Run, Request, Step, Agent, model, prompt/context, tool, retrieval, memory, evaluation, safety, reliability and incident transitions. An event carries its own `event_id`, `occurred_at`, `object_id` and `object_type`. For example, `aiops.tool.authorized` records authorization; only an observed completion supports `aiops.tool.completed`. Custom events use a permitted reverse-domain name outside `aiops`, targeting an existing object type.

Detailed reference: [Semantic event conventions](../specification/v0.3/semantic-conventions.md).

## Measurements

Represent quantities using `name`, `value`, `unit` and `kind`. For example, `{"name":"duration","value":25,"unit":"ms","kind":"observed"}` means an observed 25 milliseconds. Keep `observed`, `estimated` and `derived` distinct, and carry currency where required. An absent quantity is unknown; it is not zero. A derived resilience measurement is not an Evals gate or deployment-health verdict.

Detailed reference: [Semantic event conventions](../specification/v0.3/semantic-conventions.md).

<a id="artifacts"></a>

## Run and Workflow artifacts

Use `artifact_type: "run"` for execution evidence and `artifact_type: "workflow"` for a reusable definition, both with `spec_version: "0.4-draft"`. Start with the [Run example](../specification/v0.4/examples/valid/run.json) or [Workflow example](../specification/v0.4/examples/valid/workflow.json). A Run with `workflow_id` also needs a matching `run-of` relationship; mark its endpoint `external: true` when the Workflow is outside this artifact.

Detailed reference: [JSON Schema artifacts](../specification/v0.4/README.md).

<a id="structural-validation"></a>

## Offline structural validation

Run the downloadable [structural-validation example](guide/examples/validate_structure.py) from the repository root:

```bash
uv run python docs/guide/examples/validate_structure.py specification/v0.4/examples/valid/run.json
```

It reads the compatibility catalog, rejects unsupported marker/type pairs, registers published schemas by full `$id`, enables format checking and disables remote retrieval. It checks structure only; use the semantic rules and portable suite before claiming draft alignment. It is tutorial code, not a supported SDK or conformance CLI.

Detailed reference: [JSON Schema artifacts](../specification/v0.4/README.md).

## Semantic conformance

After structural validation, check the [producer and consumer rules](../specification/v0.4/conformance-rules.json): unique object/relationship/event IDs, timestamp order, typed endpoint resolution, exact Step containment and occurrence membership, evaluation targets, Workflow consistency, event targets, acyclicity and distinct retry identities. An external endpoint must be marked external; report it unresolved until actually resolved. Preserve unknown attributes and extensions. JSON Schema validation alone cannot establish these graph or process obligations.

Detailed reference: [Run and Workflow conformance](../specification/v0.4/conformance.md).

<a id="compatibility"></a>

## Version routing and compatibility

Repository version **1.0.0** does not turn the artifacts into `1.0` schemas. Route each artifact using the [compatibility catalog](../specification/v0.5/compatibility.json), its exact `spec_version` and `artifact_type`. Unsupported means unsupported; never retry against a different draft schema. The versioning guide also defines breaking/additive/editorial changes, deprecation, frozen-version compatibility and allowed draft-alignment claims.

Detailed reference: [Versioning and compatibility](../specification/v0.5/versioning.md).

<a id="extensions"></a>

## Extensions and preservation

Use an existing core field when its meaning matches. Put local metadata in permitted `attributes`, or reusable structured data in permitted `extensions`, for example `{"org.example.support":{"version":"1","queue":"refunds"}}`. Use a namespace you control in production. Consumers preserve unknown nested values, arrays and nulls; extensions cannot add closed-enum members or weaken core invariants. Publish payload schemas, examples, version handling, migration and privacy rules. Validate an understood extension separately from core alignment.

Detailed reference: [Extension model](../specification/v0.6/extension-model.md).

<a id="naming"></a>

## Naming conventions

Use `snake_case` core fields and object types, `kebab-case` relationship verbs, `_id` identifiers and `_at` date-time fields. Arrays use plural nouns except the documented mass nouns `evidence` and `lineage`. Boolean names describe true state without `is_`/`has_`. Only `id`, `uri` and `rag` are allowed core abbreviations. Catalog rules use `AIOS-<milestone>-<letter><two digits>`. Producer-defined keys remain open; these naming rules do not justify rejecting otherwise valid extensions.

Detailed reference: [Naming conventions](../specification/v0.6/naming-conventions.md).

<a id="provenance"></a>

## Provenance and lineage

Keep the original Run/Workflow intact and emit a separate `0.6-draft` `provenance` artifact. The [support finding](../specification/v0.6/examples/provenance/support-finding.provenance.json) demonstrates subject artifacts, object/document/human-input sources, targeted findings and `derived-from`, `supports`, `contradicts` and `supersedes` lineage. Preserve source identity and uncertainty. A finding's provenance identifies its origin; it does not prove the finding true.

Detailed reference: [Provenance records](../specification/v0.6/provenance.md).

<a id="resolution"></a>

## Cross-artifact resolution

Use held subject bytes keyed by the provenance subject's local `id`; compare the held artifact's ID, type and marker with the subject's declared artifact identity. Hash the exact original bytes for a declared `sha-256` digest, not reserialized JSON or a code block copied from the reference. Report unavailable, invalid, identity mismatch, digest mismatch and unresolved/missing/type-mismatched references distinctly. Do not fetch a subject URI automatically. The suite's `resolution_cases` supplies expected reports for these states.

Detailed reference: [Portable conformance suite](../specification/v0.6/conformance-suite/README.md).

<a id="portable-suite"></a>

## Portable validator suite

Read [suite.json](../specification/v0.6/conformance-suite/suite.json). The current snapshot has **66 outcome cases and 5 resolution cases**. Compare `valid`, `schema-invalid`, `semantic-invalid` or `unsupported`, plus the expected rule-ID sets for semantic/unsupported cases. Register schema dependencies offline. Run the repository reference checks with:

```bash
uv run pytest tests/test_v06_conformance_suite.py
```

An independent implementation should run the same fixtures using its own validator. Passing fixtures does not demonstrate extension preservation, exhaustive capture, factual accuracy or independent acceptance.

Detailed reference: [Portable conformance suite](../specification/v0.6/conformance-suite/README.md).

<a id="verification"></a>

## Verification signals

Emit `artifact_type: "verification_signal"` with `spec_version: "0.8-draft"` and a native source, subject and versioned method. Compare the [completed](../specification/v0.8/examples/verification_signal.json) and [unavailable](../specification/v0.8/examples/verification_unavailable.json) examples. Non-completed results retain null verdict/confidence and `not_checked` grounding/safety. Completed inconclusive assessments differ from unavailable judges. Confidence is not a calibrated probability; a Sidecar ALLOW is not a verification verdict.

Detailed reference: [Verification signals](../specification/v0.8/verification-signals.md).

<a id="audit"></a>

## Audit events

Use the [audit example](../specification/v0.8/examples/audit_event.json) with a required native source, actor, action, target, `occurred_at`, recording `created_at`, outcome and native outcome. Preserve optional correlation and causal-event IDs. Map dispatch to started; denied dispatch to denied; completion to succeeded/failed only when supported. Use unknown attribution where identity is absent. A request, ALLOW or stop acknowledgement is not proof of execution or stopped in-flight work. Omit privileged arguments and context.

Detailed reference: [Audit events](../specification/v0.8/audit-events.md).

<a id="investigations"></a>

## Investigation reports

Start from the [investigation example](../specification/v0.8/examples/investigation_report.json). Preserve incident/native status, affected targets, evidence-local citation IDs, summary, findings, observed timeline, missing inputs and recovery state. Observed and contradictory claims require citations; hypotheses may lack them. Verified recovery requires citations and actual native recovery observations. An incident marked resolved does not itself establish recovery; an empty missing-input list does not establish completeness.

Detailed reference: [Investigation reports](../specification/v0.8/investigation-reports.md).

<a id="operational-conformance"></a>

## Operational conformance and privacy

Validate companions against their individual `0.8-draft` schemas and the [operational rule catalog](../specification/v0.8/operational-rules.json), including local identity/citation scopes, timestamps, grounding and assessment consistency. Register v0.4 shared definitions too. Native references are citation handles, not authenticated or automatically fetched sources. Privacy, source retention and honest outcome interpretation require separate implementation checks beyond fixture validation.

Detailed reference: [Operational companion conformance](../specification/v0.8/conformance.md).

<a id="opentelemetry"></a>

## OpenTelemetry mapping

Pin the non-normative `aios.otel/1` profile and its OpenTelemetry semantic-conventions **v1.37.0** baseline. The [mapping catalog](../specification/v0.6/otel/mapping.json) covers every canonical event; the [paired example](../specification/v0.6/otel/example.json) preserves two retry attempts and explicit units. AIOS Run IDs are not OTel trace IDs; graph edges do not all become parent spans. Retain original artifacts and conversion losses. The readable projection is not OTLP JSON and no exporter SDK ships here.

Detailed reference: [OpenTelemetry companion binding](../specification/v0.6/otel-binding.md).

<a id="migration"></a>

## Migration, rollout and rollback

Pin a repository snapshot for producer and validator, inventory native identities, preserve originals and record unmapped fields. Add graphs/events only when observed. Introduce provenance and operational companions separately while retaining Run/Workflow markers. Compare readers before rollout, deduplicate dual-written native/projected evidence, and roll back adapters without rewriting stored markers. `drafts/v0.4` is a superseded experiment; do not migrate it by changing only its marker.

Detailed reference: [Migration and rollout](../specification/v0.6/migration-guide.md).

<a id="access-evidence"></a>

## Access-evidence profile

The exploratory `io.deepagentlabs.access` extension uses `format: "access/1"` in existing `0.4-draft` Runs. Its [embedding example](../drafts/access-evidence-v1/run-example.json) preserves producer/task/correlation identity and omits arguments and credentials. The schema validates one observation. Ordered-stream authentication, coverage and containment scoring belong to implementations; no observation proves exhaustive capture or that already-running calls stopped.

Detailed reference: [Non-normative access evidence profile](../drafts/access-evidence-v1/README.md).

<a id="sidecar-correlation"></a>

## Sidecar correlation profile

Read the native `sidecar.correlation/1` [example](../drafts/sidecar-correlation-v1/example.json). Preserve decision status/rationale, causal link, policy fingerprint, journal source and host-supplied run/trace/span IDs. Logical scope is not granted authority. Verify native journal links before correlation and authorize/redact reader access. A decision projection is not an execution receipt or a verifiable full journal.

Detailed reference: [Non-normative Sidecar correlation](../drafts/sidecar-correlation-v1/README.md).

<a id="sidecar-contracts"></a>

## Sidecar candidate contracts

Use the native candidate schemas under [drafts/sidecar-contracts-v1](../drafts/sidecar-contracts-v1/README.md) for their stated `/1` wrappers. Preserve intent and decision identities, native outcomes, exact scope and parent-grant links. Receivers need live registry validation; a wire claim does not grant authority. These schema copies are implementation drafts, not additional AIOS artifact families. Explicit wrapping must preserve existing IDs and times.

Detailed reference: [Non-normative Sidecar candidate contracts](../drafts/sidecar-contracts-v1/README.md).

<a id="ecosystem"></a>

## Ecosystem adoption and ownership

AIOS defines shared meaning. Lens owns instrumentation/analysis, Evals scoring/release gates, Chaos faults/resilience, Sidecar supervision/governance, MCP transport/composition and Tower fleet/operator workflows. Consult [operational adoption](v0.8.0-ecosystem.md) and [source mappings](../reviews/operational-artifact-mappings.md) before projecting native evidence. Native report versions, package versions and AIOS markers are independent. Historical compatibility notes describe their named releases; they are not guarantees about today's runtime behavior.

Detailed reference: [Coordinated engineering readiness](coordinated-v1-readiness.md).

<a id="review"></a>

## Review gates and maturity

All current schema families remain drafts despite repository 1.0.0. Use a dated/snapshot-specific draft-alignment claim and disclose validation limits. Read the [decision log](../reviews/decision-log.md), [evidence matrix](../reviews/evidence-matrix.md) and [external review tasks](../reviews/EXTERNAL_REVIEW_TASKS.md). Internal tests and sibling adoption do not close independent-review, independent-implementation, deployment/live-provider or stable-freeze gates.

Detailed reference: [Specification reading order and maturity](../SPECIFICATION.md).

<a id="maintenance"></a>

## Documentation and contribution workflow

Run `make check` for repository validation and `make docs` for the strict documentation build; it publishes the site with the shared DeepAgentLabs theme, like every product. New user-facing capabilities need a row in both capability indexes and detailed maintained sources. Refresh/check the robust pack from this repository root:

```bash
python3 ../deepagentlabs.github.io/scripts/build_ai_docs.py --sources .. --project ai-operations-spec
python3 ../deepagentlabs.github.io/scripts/build_ai_docs.py --sources .. --project ai-operations-spec --check
```

The builder needs Python 3.11 or newer. Keep published specification/profile Markdown and JSON selected in `docs/ai-docs.json`; generated outputs must not select themselves. Follow [CONTRIBUTING](../CONTRIBUTING.md), preserve realistic examples and add fixtures for spec behavior changes. `make check` does not include the separate strict site build.

Detailed reference: [Documentation build and publication](documentation-site.md).

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Unsupported marker or type | Read the exact pair from compatibility.json; repository version is not a schema marker. |
| Missing `$ref` or network lookup | Register all local schemas by full `$id`, including v0.4 dependencies. |
| Structure passes but alignment fails | Check typed references, containment, retry edges, cycles and citations using the relevant rule catalog. |
| Provenance digest mismatch | Use exact held source bytes; do not hash parsed/reformatted JSON. |
| New page missing from `make docs` | The repository staging script selects tracked paths; add intended files to Git before a normal build. |
| Robust reference is stale | Regenerate after changing any selected source, schema, catalog or fixture, then run `--check`. |
| Verification is unavailable | Preserve unknown/null states; never turn missing assessment into a pass. |
