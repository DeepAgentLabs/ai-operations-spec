# API Reference (detailed)

**Repository version:** 1.0.2

AIOS is a contract: its public interface is the set of JSON artifacts that producers emit and
consumers accept. This page lists every field, type, constraint and conformance rule of each
artifact family.

All six artifact families ship with JSON Schemas, rule catalogs, canonical examples and the
portable conformance suite. Each artifact declares its family's version marker exactly as shown
(`0.4-draft`, `0.6-draft` or `0.8-draft`). The specification prose and rule catalogs define the
full requirements: schemas check structure, and the conformance suite checks the semantic rules.

This page is generated from the schemas and rule catalogs by `scripts/build_api_reference.py`.
Edit those sources, then run `make api-reference`; a test fails if this page is stale.
For a guided path, start with the [Developer Guide](developer-guide.md).

## Artifact families

| Family | Artifact type | Version marker | Schema | Example | Rules |
| --- | --- | --- | --- | --- | --- |
| [Run](#v04-run) | `run` | `0.4-draft` | [run.schema.json](../specification/v0.4/schemas/run.schema.json) | [run.json](../specification/v0.4/examples/valid/run.json) | 23 ([catalog](#v04-conformance-rules)) |
| [Workflow](#v04-workflow) | `workflow` | `0.4-draft` | [workflow.schema.json](../specification/v0.4/schemas/workflow.schema.json) | [workflow.json](../specification/v0.4/examples/valid/workflow.json) | 12 ([catalog](#v04-conformance-rules)) |
| [Provenance record](#v06-provenance) | `provenance` | `0.6-draft` | [provenance.schema.json](../specification/v0.6/schemas/provenance.schema.json) | [support-finding.provenance.json](../specification/v0.6/examples/provenance/support-finding.provenance.json) | 18 ([catalog](#v06-provenance-rules)) |
| [Verification signal](#v08-verification-signal) | `verification_signal` | `0.8-draft` | [verification_signal.schema.json](../specification/v0.8/schemas/verification_signal.schema.json) | [verification_signal.json](../specification/v0.8/examples/verification_signal.json) | 10 ([catalog](#v08-operational-rules)) |
| [Audit event](#v08-audit-event) | `audit_event` | `0.8-draft` | [audit_event.schema.json](../specification/v0.8/schemas/audit_event.schema.json) | [audit_event.json](../specification/v0.8/examples/audit_event.json) | 10 ([catalog](#v08-operational-rules)) |
| [Investigation report](#v08-investigation-report) | `investigation_report` | `0.8-draft` | [investigation_report.schema.json](../specification/v0.8/schemas/investigation_report.schema.json) | [investigation_report.json](../specification/v0.8/examples/investigation_report.json) | 12 ([catalog](#v08-operational-rules)) |

How to read the field tables: a dotted name (`grounding.status`) is a field of an inline object,
and `[]` marks the items of an array. Linked types are definitions listed under the family or
under the shared definitions. To validate offline, register both shared schemas by `$id`; see
[Offline structural validation](developer-guide.md#structural-validation).

<a id="v04-run"></a>

## Artifact: Run

`artifact_type: run` · `spec_version: 0.4-draft` · schema `https://deepagentlabs.github.io/ai-operations-spec/v0.4/run.schema.json`

Normative text: [README.md](../specification/v0.4/README.md). Example: [run.json](../specification/v0.4/examples/valid/run.json).

Rules that apply (23): [AIOS-0.4-P01](#aios-0.4-p01), [AIOS-0.4-P02](#aios-0.4-p02), [AIOS-0.4-P03](#aios-0.4-p03), [AIOS-0.4-P04](#aios-0.4-p04), [AIOS-0.4-P05](#aios-0.4-p05), [AIOS-0.4-P06](#aios-0.4-p06), [AIOS-0.4-P07](#aios-0.4-p07), [AIOS-0.4-P08](#aios-0.4-p08), [AIOS-0.4-P09](#aios-0.4-p09), [AIOS-0.4-P10](#aios-0.4-p10), [AIOS-0.4-P11](#aios-0.4-p11), [AIOS-0.4-P12](#aios-0.4-p12), [AIOS-0.4-X01](#aios-0.4-x01), [AIOS-0.4-X02](#aios-0.4-x02), [AIOS-0.4-C01](#aios-0.4-c01), [AIOS-0.4-C02](#aios-0.4-c02), [AIOS-0.4-C03](#aios-0.4-c03), [AIOS-0.4-C04](#aios-0.4-c04), [AIOS-0.4-U01](#aios-0.4-u01), [AIOS-0.4-U02](#aios-0.4-u02), [AIOS-0.4-E01](#aios-0.4-e01), [AIOS-0.4-D01](#aios-0.4-d01), [AIOS-0.4-K01](#aios-0.4-k01).

### Run fields

| Field | Type | Required | Constraints |
| --- | --- | --- | --- |
| `spec_version` | const | yes | always `0.4-draft` |
| `artifact_type` | const | yes | always `run` |
| `id` | [`id`](#v04-common-id) | yes |  |
| `workflow_id` | [`id`](#v04-common-id) |  |  |
| `started_at` | [`time`](#v04-common-time) | yes |  |
| `ended_at` | [`time`](#v04-common-time) |  |  |
| `status` | enum | yes | one of `created`, `running`, `completed`, `failed`, `cancelled` |
| `requests` | array of [`object`](#v04-run-object) | yes |  |
| `steps` | array of [`step`](#v04-run-step) | yes |  |
| `agents` | array of [`object`](#v04-run-object) |  |  |
| `occurrences` | array of [`occurrence`](#v04-run-occurrence) |  |  |
| `evidence` | array of [`evidence`](#v04-run-evidence) |  |  |
| `incidents` | array of [`object`](#v04-run-object) |  |  |
| `relationships` | array of [`relationship`](#v04-common-relationship) | yes |  |
| `events` | array of [`event`](#v04-common-event) |  |  |
| `measurements` | array of [`measurement`](#v04-common-measurement) |  |  |
| `extensions` | [`extensions`](#v04-common-extensions) |  |  |

Other fields: not allowed (`additionalProperties: false`).

<a id="v04-run-object"></a>

#### `object`

| Field | Type | Required | Constraints |
| --- | --- | --- | --- |
| `id` | [`id`](#v04-common-id) | yes |  |
| `name` | string |  |  |
| `status` | string |  |  |
| `attributes` | object |  |  |
| `extensions` | [`extensions`](#v04-common-extensions) |  |  |

Other fields: not allowed (`additionalProperties: false`).

<a id="v04-run-step"></a>

#### `step`

| Field | Type | Required | Constraints |
| --- | --- | --- | --- |
| `id` | [`id`](#v04-common-id) | yes |  |
| `category` | string | yes | min length 1 |
| `name` | string |  |  |
| `status` | string |  |  |
| `started_at` | [`time`](#v04-common-time) |  |  |
| `ended_at` | [`time`](#v04-common-time) |  |  |
| `attributes` | object |  |  |
| `extensions` | [`extensions`](#v04-common-extensions) |  |  |

Other fields: not allowed (`additionalProperties: false`).

<a id="v04-run-occurrence"></a>

#### `occurrence`

| Field | Type | Required | Constraints |
| --- | --- | --- | --- |
| `id` | [`id`](#v04-common-id) | yes |  |
| `type` | enum | yes | one of `model_interaction`, `prompt`, `context`, `tool_invocation`, `rag_retrieval`, `memory_operation` |
| `name` | string |  |  |
| `status` | string |  |  |
| `attributes` | object |  |  |
| `extensions` | [`extensions`](#v04-common-extensions) |  |  |

Other fields: not allowed (`additionalProperties: false`).

<a id="v04-run-evidence"></a>

#### `evidence`

| Field | Type | Required | Constraints |
| --- | --- | --- | --- |
| `id` | [`id`](#v04-common-id) | yes |  |
| `type` | enum | yes | one of `evaluation`, `safety_signal`, `reliability_event` |
| `name` | string |  |  |
| `status` | string |  |  |
| `attributes` | object |  |  |
| `extensions` | [`extensions`](#v04-common-extensions) |  |  |

Other fields: not allowed (`additionalProperties: false`).

<a id="v04-workflow"></a>

## Artifact: Workflow

`artifact_type: workflow` · `spec_version: 0.4-draft` · schema `https://deepagentlabs.github.io/ai-operations-spec/v0.4/workflow.schema.json`

Normative text: [README.md](../specification/v0.4/README.md). Example: [workflow.json](../specification/v0.4/examples/valid/workflow.json).

Rules that apply (12): [AIOS-0.4-P01](#aios-0.4-p01), [AIOS-0.4-X01](#aios-0.4-x01), [AIOS-0.4-X02](#aios-0.4-x02), [AIOS-0.4-C01](#aios-0.4-c01), [AIOS-0.4-C02](#aios-0.4-c02), [AIOS-0.4-C03](#aios-0.4-c03), [AIOS-0.4-C04](#aios-0.4-c04), [AIOS-0.4-U01](#aios-0.4-u01), [AIOS-0.4-U02](#aios-0.4-u02), [AIOS-0.4-E01](#aios-0.4-e01), [AIOS-0.4-D01](#aios-0.4-d01), [AIOS-0.4-K01](#aios-0.4-k01).

### Workflow fields

| Field | Type | Required | Constraints |
| --- | --- | --- | --- |
| `spec_version` | const | yes | always `0.4-draft` |
| `artifact_type` | const | yes | always `workflow` |
| `id` | [`id`](#v04-common-id) | yes |  |
| `name` | string | yes | min length 1 |
| `description` | string |  |  |
| `revision` | string |  | min length 1 |
| `status` | enum |  | one of `draft`, `active`, `retired` |
| `declared_structure` | object |  |  |
| `references` | array of [`reference`](#v04-common-reference) |  |  |
| `extensions` | [`extensions`](#v04-common-extensions) |  |  |

Other fields: not allowed (`additionalProperties: false`).

<a id="v06-provenance"></a>

## Artifact: Provenance record

`artifact_type: provenance` · `spec_version: 0.6-draft` · schema `https://deepagentlabs.github.io/ai-operations-spec/v0.6/provenance.schema.json`

Normative text: [provenance.md](../specification/v0.6/provenance.md). Example: [support-finding.provenance.json](../specification/v0.6/examples/provenance/support-finding.provenance.json).

Exploratory 0.6-draft companion artifact recording the sources and evidence lineage behind derived findings about AIOS artifacts. Shared definitions come from the 0.4-draft common schema.

Rules that apply (18): [AIOS-0.6-R01](#aios-0.6-r01), [AIOS-0.6-R02](#aios-0.6-r02), [AIOS-0.6-R03](#aios-0.6-r03), [AIOS-0.6-R04](#aios-0.6-r04), [AIOS-0.6-R05](#aios-0.6-r05), [AIOS-0.6-R06](#aios-0.6-r06), [AIOS-0.6-R07](#aios-0.6-r07), [AIOS-0.6-C01](#aios-0.6-c01), [AIOS-0.6-C02](#aios-0.6-c02), [AIOS-0.6-C03](#aios-0.6-c03), [AIOS-0.6-C04](#aios-0.6-c04), [AIOS-0.6-C05](#aios-0.6-c05), [AIOS-0.6-C06](#aios-0.6-c06), [AIOS-0.6-C07](#aios-0.6-c07), [AIOS-0.6-C08](#aios-0.6-c08), [AIOS-0.6-D01](#aios-0.6-d01), [AIOS-0.6-K01](#aios-0.6-k01), [AIOS-0.6-S01](#aios-0.6-s01).

### Provenance record fields

| Field | Type | Required | Constraints |
| --- | --- | --- | --- |
| `spec_version` | const | yes | always `0.6-draft` |
| `artifact_type` | const | yes | always `provenance` |
| `id` | [`id`](#v04-common-id) | yes |  |
| `created_at` | [`time`](#v04-common-time) | yes |  |
| `producer` | [`producer`](#v06-provenance-producer) | yes |  |
| `subjects` | array of [`subject`](#v06-provenance-subject) | yes | min items 1 |
| `sources` | array of [`source`](#v06-provenance-source) | yes |  |
| `findings` | array of [`finding`](#v06-provenance-finding) | yes |  |
| `lineage` | array of [`lineage_edge`](#v06-provenance-lineage-edge) | yes |  |
| `attributes` | object |  |  |
| `extensions` | [`extensions`](#v04-common-extensions) |  |  |

Other fields: not allowed (`additionalProperties: false`).

<a id="v06-provenance-id"></a>

#### `id`

Type: [`id`](#v04-common-id).

<a id="v06-provenance-subject-object"></a>

#### `subject_object`

A v0.4 reference to an object inside the subject artifact; it can never be external.

| Field | Type | Required | Constraints |
| --- | --- | --- | --- |
| `external` | const |  | always `false` |

<a id="v06-provenance-producer"></a>

#### `producer`

| Field | Type | Required | Constraints |
| --- | --- | --- | --- |
| `name` | string | yes | min length 1 |
| `version` | string |  | min length 1 |
| `uri` | string |  | format `uri` |

Other fields: not allowed (`additionalProperties: false`).

<a id="v06-provenance-digest"></a>

#### `digest`

| Field | Type | Required | Constraints |
| --- | --- | --- | --- |
| `algorithm` | enum | yes | one of `sha-256`, `sha-384`, `sha-512` |
| `value` | string | yes | pattern `^[0-9a-f]+$` |

Other fields: not allowed (`additionalProperties: false`).

Conditional requirements:

- If `algorithm` is `sha-256`: `value` is exactly 64 characters.
- If `algorithm` is `sha-384`: `value` is exactly 96 characters.
- If `algorithm` is `sha-512`: `value` is exactly 128 characters.

<a id="v06-provenance-subject"></a>

#### `subject`

| Field | Type | Required | Constraints |
| --- | --- | --- | --- |
| `id` | [`id`](#v06-provenance-id) | yes |  |
| `artifact_id` | [`id`](#v06-provenance-id) | yes |  |
| `artifact_type` | enum | yes | one of `workflow`, `run` |
| `spec_version` | string | yes | pattern `^(0\.[1-9][0-9]*\|[1-9][0-9]*\.(0\|[1-9][0-9]*))(-draft)?$` |
| `uri` | string |  | format `uri` |
| `digest` | [`digest`](#v06-provenance-digest) |  |  |

Other fields: not allowed (`additionalProperties: false`).

<a id="v06-provenance-source"></a>

#### `source`

| Field | Type | Required | Constraints |
| --- | --- | --- | --- |
| `id` | [`id`](#v06-provenance-id) | yes |  |
| `kind` | enum | yes | one of `aios_object`, `artifact`, `document`, `dataset`, `log`, `tool_output`, `human_input` |
| `description` | string |  | min length 1 |
| `subject` | [`id`](#v06-provenance-id) |  |  |
| `object` | [`subject_object`](#v06-provenance-subject-object) |  |  |
| `uri` | string |  | format `uri` |
| `digest` | [`digest`](#v06-provenance-digest) |  |  |
| `captured_at` | [`time`](#v04-common-time) |  |  |
| `attributes` | object |  |  |
| `extensions` | [`extensions`](#v04-common-extensions) |  |  |

Other fields: not allowed (`additionalProperties: false`).

Conditional requirements:

- If `kind` is `aios_object`: `subject` is present; `object` is present.
- If `kind` is `artifact`: `subject` is present; `object` is absent.
- If `kind` is one of `document`, `dataset`, `log`, `tool_output`, `human_input`: at least one of `uri`, `description` is present; `object` is absent.

<a id="v06-provenance-method"></a>

#### `method`

| Field | Type | Required | Constraints |
| --- | --- | --- | --- |
| `kind` | enum | yes | one of `rule`, `model`, `human`, `statistical`, `heuristic` |
| `name` | string | yes | min length 1 |
| `version` | string |  | min length 1 |

Other fields: not allowed (`additionalProperties: false`).

<a id="v06-provenance-finding-target"></a>

#### `finding_target`

| Field | Type | Required | Constraints |
| --- | --- | --- | --- |
| `subject` | [`id`](#v06-provenance-id) | yes |  |
| `object` | [`subject_object`](#v06-provenance-subject-object) | yes |  |

Other fields: not allowed (`additionalProperties: false`).

<a id="v06-provenance-finding"></a>

#### `finding`

| Field | Type | Required | Constraints |
| --- | --- | --- | --- |
| `id` | [`id`](#v06-provenance-id) | yes |  |
| `statement` | string | yes | min length 1 |
| `category` | string |  | min length 1 |
| `status` | enum | yes | one of `open`, `confirmed`, `disputed`, `retracted` |
| `severity` | enum |  | one of `info`, `low`, `medium`, `high`, `critical` |
| `confidence` | number |  | ≥ 0; ≤ 1 |
| `method` | [`method`](#v06-provenance-method) | yes |  |
| `targets` | array of [`finding_target`](#v06-provenance-finding-target) |  |  |
| `attributes` | object |  |  |
| `extensions` | [`extensions`](#v04-common-extensions) |  |  |

Other fields: not allowed (`additionalProperties: false`).

<a id="v06-provenance-lineage-edge"></a>

#### `lineage_edge`

| Field | Type | Required | Constraints |
| --- | --- | --- | --- |
| `id` | [`id`](#v06-provenance-id) | yes |  |
| `type` | enum | yes | one of `derived-from`, `supports`, `contradicts`, `supersedes` |
| `source` | [`id`](#v06-provenance-id) | yes |  |
| `target` | [`id`](#v06-provenance-id) | yes |  |
| `extensions` | [`extensions`](#v04-common-extensions) |  |  |

Other fields: not allowed (`additionalProperties: false`).

<a id="v08-verification-signal"></a>

## Artifact: Verification signal

`artifact_type: verification_signal` · `spec_version: 0.8-draft` · schema `https://deepagentlabs.github.io/ai-operations-spec/v0.8/verification_signal.schema.json`

Normative text: [verification-signals.md](../specification/v0.8/verification-signals.md). Example: [verification_signal.json](../specification/v0.8/examples/verification_signal.json).

Rules that apply (10): [AIOS-0.8-R01](#aios-0.8-r01), [AIOS-0.8-R02](#aios-0.8-r02), [AIOS-0.8-R05](#aios-0.8-r05), [AIOS-0.8-P01](#aios-0.8-p01), [AIOS-0.8-S01](#aios-0.8-s01), [AIOS-0.8-C01](#aios-0.8-c01), [AIOS-0.8-C02](#aios-0.8-c02), [AIOS-0.8-C03](#aios-0.8-c03), [AIOS-0.8-C04](#aios-0.8-c04), [AIOS-0.8-D01](#aios-0.8-d01).

### Verification signal fields

| Field | Type | Required | Constraints |
| --- | --- | --- | --- |
| `spec_version` | const | yes | always `0.8-draft` |
| `artifact_type` | const | yes | always `verification_signal` |
| `id` | string | yes | min length 1 |
| `created_at` | string | yes | format `date-time` |
| `producer` | [`producer`](#v08-common-producer) | yes |  |
| `subject` | [`reference`](#v08-common-reference) | yes |  |
| `method` | [`method`](#v08-common-method) | yes |  |
| `status` | enum | yes | one of `completed`, `unavailable`, `error`, `skipped` |
| `verdict` | enum | yes | one of `supports`, `partially_supports`, `contradicts`, `inconclusive`, `null` |
| `confidence` | number or null | yes | ≥ 0; ≤ 1 |
| `rationale` | string | yes | min length 1 |
| `evidence` | array of [`reference`](#v08-common-reference) | yes | min items 0 |
| `grounding` | object | yes |  |
| `grounding.status` | enum | yes | one of `grounded`, `partial`, `ungrounded`, `not_checked` |
| `grounding.unsupported_claims` | array of string | yes | min items 0; each item: min length 1 |
| `grounding.missed_evidence_items` | array of string | yes | min items 0; each item: min length 1 |
| `safety` | object | yes |  |
| `safety.status` | enum | yes | one of `concerns`, `no_concerns`, `not_checked` |
| `safety.concerns` | array of string | yes | min items 0; each item: min length 1 |
| `native_outcome` | [`native_outcome`](#v08-common-native-outcome) | yes |  |
| `attributes` | object |  |  |
| `extensions` | [`extensions`](#v08-common-extensions) |  |  |
| `source` | [`reference`](#v08-common-reference) | yes |  |

Other fields: not allowed (`additionalProperties: false`).

Conditional requirements:

- If `status` is `completed`: `verdict` is string. Otherwise: `verdict` is null; `confidence` is null; `grounding.status` is `not_checked`; `grounding.unsupported_claims` is empty; `grounding.missed_evidence_items` is empty; `safety.status` is `not_checked`; `safety.concerns` is empty.
- If `safety.status` is `concerns`: `safety.concerns` has at least 1 item. Otherwise: `safety.concerns` is empty.
- If `grounding.status` is `grounded`: `grounding.unsupported_claims` is empty; `grounding.missed_evidence_items` is empty.

<a id="v08-audit-event"></a>

## Artifact: Audit event

`artifact_type: audit_event` · `spec_version: 0.8-draft` · schema `https://deepagentlabs.github.io/ai-operations-spec/v0.8/audit_event.schema.json`

Normative text: [audit-events.md](../specification/v0.8/audit-events.md). Example: [audit_event.json](../specification/v0.8/examples/audit_event.json).

Rules that apply (10): [AIOS-0.8-R01](#aios-0.8-r01), [AIOS-0.8-R04](#aios-0.8-r04), [AIOS-0.8-R07](#aios-0.8-r07), [AIOS-0.8-P01](#aios-0.8-p01), [AIOS-0.8-S01](#aios-0.8-s01), [AIOS-0.8-C01](#aios-0.8-c01), [AIOS-0.8-C02](#aios-0.8-c02), [AIOS-0.8-C03](#aios-0.8-c03), [AIOS-0.8-C04](#aios-0.8-c04), [AIOS-0.8-D01](#aios-0.8-d01).

### Audit event fields

| Field | Type | Required | Constraints |
| --- | --- | --- | --- |
| `spec_version` | const | yes | always `0.8-draft` |
| `artifact_type` | const | yes | always `audit_event` |
| `id` | string | yes | min length 1 |
| `created_at` | string | yes | format `date-time` |
| `producer` | [`producer`](#v08-common-producer) | yes |  |
| `occurred_at` | string | yes | format `date-time` |
| `actor` | [`actor`](#v08-common-actor) | yes |  |
| `action` | string | yes | min length 1 |
| `target` | [`reference`](#v08-common-reference) | yes |  |
| `outcome` | enum | yes | one of `requested`, `denied`, `started`, `succeeded`, `failed`, `partial`, `unknown` |
| `native_outcome` | [`native_outcome`](#v08-common-native-outcome) | yes |  |
| `correlation_id` | string |  | min length 1 |
| `causal_event_ids` | array of string |  | min items 0; unique items; each item: min length 1 |
| `attributes` | object |  |  |
| `extensions` | [`extensions`](#v08-common-extensions) |  |  |
| `source` | [`reference`](#v08-common-reference) | yes |  |

Other fields: not allowed (`additionalProperties: false`).

<a id="v08-investigation-report"></a>

## Artifact: Investigation report

`artifact_type: investigation_report` · `spec_version: 0.8-draft` · schema `https://deepagentlabs.github.io/ai-operations-spec/v0.8/investigation_report.schema.json`

Normative text: [investigation-reports.md](../specification/v0.8/investigation-reports.md). Example: [investigation_report.json](../specification/v0.8/examples/investigation_report.json).

Rules that apply (12): [AIOS-0.8-R01](#aios-0.8-r01), [AIOS-0.8-R02](#aios-0.8-r02), [AIOS-0.8-R03](#aios-0.8-r03), [AIOS-0.8-R04](#aios-0.8-r04), [AIOS-0.8-R06](#aios-0.8-r06), [AIOS-0.8-P01](#aios-0.8-p01), [AIOS-0.8-S01](#aios-0.8-s01), [AIOS-0.8-C01](#aios-0.8-c01), [AIOS-0.8-C02](#aios-0.8-c02), [AIOS-0.8-C03](#aios-0.8-c03), [AIOS-0.8-C04](#aios-0.8-c04), [AIOS-0.8-D01](#aios-0.8-d01).

### Investigation report fields

| Field | Type | Required | Constraints |
| --- | --- | --- | --- |
| `spec_version` | const | yes | always `0.8-draft` |
| `artifact_type` | const | yes | always `investigation_report` |
| `id` | string | yes | min length 1 |
| `created_at` | string | yes | format `date-time` |
| `producer` | [`producer`](#v08-common-producer) | yes |  |
| `incident` | object | yes |  |
| `incident.id` | string | yes | min length 1 |
| `incident.status` | enum | yes | one of `open`, `investigating`, `resolved`, `escalated`, `unknown` |
| `incident.native_state` | string | yes | min length 1 |
| `incident.detected_at` | string | yes | format `date-time` |
| `incident.affected_targets` | array of [`reference`](#v08-common-reference) | yes | min items 1 |
| `summary` | object | yes |  |
| `summary.statement` | string | yes | min length 1 |
| `summary.certainty` | [`certainty`](#v08-common-certainty) | yes |  |
| `summary.evidence_ids` | array of string | yes | min items 0; unique items; each item: min length 1 |
| `evidence` | array of [`reference`](#v08-common-reference) | yes | min items 0 |
| `timeline_entries` | array of object | yes | min items 0 |
| `timeline_entries[].id` | string | yes | min length 1 |
| `timeline_entries[].occurred_at` | string | yes | format `date-time` |
| `timeline_entries[].evidence_ids` | array of string | yes | min items 0; unique items; each item: min length 1 |
| `findings` | array of object | yes | min items 0 |
| `findings[].id` | string | yes | min length 1 |
| `findings[].statement` | string | yes | min length 1 |
| `findings[].certainty` | [`certainty`](#v08-common-certainty) | yes |  |
| `findings[].evidence_ids` | array of string | yes | min items 0; unique items; each item: min length 1 |
| `missing_evidence_items` | array of string | yes | min items 0; each item: min length 1 |
| `recovery` | object | yes |  |
| `recovery.status` | enum | yes | one of `not_attempted`, `pending`, `verified`, `failed`, `unknown` |
| `recovery.evidence_ids` | array of string | yes | min items 0; unique items; each item: min length 1 |
| `attributes` | object |  |  |
| `extensions` | [`extensions`](#v08-common-extensions) |  |  |
| `source` | [`reference`](#v08-common-reference) | yes |  |

Other fields: not allowed (`additionalProperties: false`).

## Shared definitions: 0.4-draft

Schema `https://deepagentlabs.github.io/ai-operations-spec/v0.4/common.schema.json` ([common.schema.json](../specification/v0.4/schemas/common.schema.json)).

<a id="v04-common-id"></a>

### `id`

Type: string. Constraints: pattern `.*\S.*`; min length 1.

<a id="v04-common-time"></a>

### `time`

Type: string. Constraints: format `date-time`.

<a id="v04-common-extension-name"></a>

### `extension_name`

Type: string. Constraints: pattern `^(?!aiops(?:\.\|$))[a-z0-9]+(?:[_-][a-z0-9]+)*(?:\.[a-z0-9]+(?:[_-][a-z0-9]+)*){2,}$`.

<a id="v04-common-extensions"></a>

### `extensions`

Type: object. Constraints: keys: [`extension_name`](#v04-common-extension-name).

<a id="v04-common-reference"></a>

### `reference`

| Field | Type | Required | Constraints |
| --- | --- | --- | --- |
| `id` | [`id`](#v04-common-id) | yes |  |
| `type` | enum | yes | one of `workflow`, `run`, `request`, `step`, `agent`, `model_interaction`, `prompt`, `context`, `tool_invocation`, `rag_retrieval`, `memory_operation`, `evaluation`, `safety_signal`, `reliability_event`, `incident` |
| `external` | boolean |  | default `false` |

Other fields: not allowed (`additionalProperties: false`).

<a id="v04-common-relationship"></a>

### `relationship`

| Field | Type | Required | Constraints |
| --- | --- | --- | --- |
| `id` | [`id`](#v04-common-id) | yes |  |
| `type` | enum | yes | one of `run-of`, `contains`, `parent-of`, `caused`, `follows`, `depends-on`, `performed-by`, `delegated-to`, `handed-off-to`, `observed-in`, `evaluates`, `signals-on`, `evidence-for` |
| `source` | [`reference`](#v04-common-reference) | yes |  |
| `target` | [`reference`](#v04-common-reference) | yes |  |
| `extensions` | [`extensions`](#v04-common-extensions) |  |  |

Other fields: not allowed (`additionalProperties: false`).

<a id="v04-common-measurement"></a>

### `measurement`

| Field | Type | Required | Constraints |
| --- | --- | --- | --- |
| `name` | string | yes | min length 1 |
| `value` | number | yes | ≥ 0 |
| `unit` | string |  | min length 1 |
| `currency` | string |  | pattern `^[A-Z]{3}$` |
| `kind` | enum | yes | one of `observed`, `estimated`, `derived` |

Other fields: not allowed (`additionalProperties: false`).

Conditional requirements:

- If `name` is present and `name` is `cost`: `currency` is present.

<a id="v04-common-canonical-event-name"></a>

### `canonical_event_name`

Type: enum. Constraints: one of `aiops.run.started`, `aiops.run.completed`, `aiops.run.failed`, `aiops.run.cancelled`, `aiops.request.received`, `aiops.request.completed`, `aiops.request.rejected`, `aiops.step.started`, `aiops.step.completed`, `aiops.step.failed`, `aiops.step.cancelled`, `aiops.agent.started`, `aiops.agent.waiting`, `aiops.agent.completed`, `aiops.agent.failed`, `aiops.model.requested`, `aiops.model.responded`, `aiops.model.failed`, `aiops.prompt.rendered`, `aiops.context.assembled`, `aiops.tool.requested`, `aiops.tool.authorized`, `aiops.tool.completed`, `aiops.tool.failed`, `aiops.retrieval.started`, `aiops.retrieval.completed`, `aiops.retrieval.failed`, `aiops.memory.read`, `aiops.memory.written`, `aiops.memory.updated`, `aiops.memory.deleted`, `aiops.memory.failed`, `aiops.evaluation.completed`, `aiops.evaluation.failed`, `aiops.safety.detected`, `aiops.safety.reviewed`, `aiops.safety.mitigated`, `aiops.reliability.detected`, `aiops.reliability.recovered`, `aiops.incident.opened`, `aiops.incident.updated`, `aiops.incident.mitigated`, `aiops.incident.resolved`.

<a id="v04-common-event"></a>

### `event`

| Field | Type | Required | Constraints |
| --- | --- | --- | --- |
| `event_id` | [`id`](#v04-common-id) | yes |  |
| `event_name` | [`canonical_event_name`](#v04-common-canonical-event-name) or [`extension_name`](#v04-common-extension-name) | yes |  |
| `occurred_at` | [`time`](#v04-common-time) | yes |  |
| `object_id` | [`id`](#v04-common-id) | yes |  |
| `object_type` | enum | yes | one of `run`, `request`, `step`, `agent`, `model_interaction`, `prompt`, `context`, `tool_invocation`, `rag_retrieval`, `memory_operation`, `evaluation`, `safety_signal`, `reliability_event`, `incident` |
| `attributes` | object |  |  |
| `extensions` | [`extensions`](#v04-common-extensions) |  |  |

Other fields: not allowed (`additionalProperties: false`).

## Shared definitions: 0.8-draft

Schema `https://deepagentlabs.github.io/ai-operations-spec/v0.8/common.schema.json` ([common.schema.json](../specification/v0.8/schemas/common.schema.json)).

<a id="v08-common-producer"></a>

### `producer`

| Field | Type | Required | Constraints |
| --- | --- | --- | --- |
| `name` | string | yes | min length 1 |
| `version` | string | yes | min length 1 |

Other fields: not allowed (`additionalProperties: false`).

<a id="v08-common-reference"></a>

### `reference`

| Field | Type | Required | Constraints |
| --- | --- | --- | --- |
| `id` | string | yes | min length 1 |
| `producer` | string | yes | min length 1 |
| `artifact_id` | string | yes | min length 1 |
| `format` | string | yes | min length 1 |
| `object_id` | string |  | min length 1 |
| `uri` | string |  | format `uri` |

Other fields: not allowed (`additionalProperties: false`).

<a id="v08-common-method"></a>

### `method`

| Field | Type | Required | Constraints |
| --- | --- | --- | --- |
| `kind` | enum | yes | one of `rule`, `model`, `human`, `statistical`, `heuristic` |
| `name` | string | yes | min length 1 |
| `version` | string | yes | min length 1 |

Other fields: not allowed (`additionalProperties: false`).

<a id="v08-common-native-outcome"></a>

### `native_outcome`

| Field | Type | Required | Constraints |
| --- | --- | --- | --- |
| `format` | string | yes | min length 1 |
| `value` | string | yes | min length 1 |

Other fields: not allowed (`additionalProperties: false`).

<a id="v08-common-actor"></a>

### `actor`

| Field | Type | Required | Constraints |
| --- | --- | --- | --- |
| `kind` | enum | yes | one of `human`, `service`, `agent`, `unknown` |
| `id` | string |  | min length 1 |

Other fields: not allowed (`additionalProperties: false`).

Conditional requirements:

- If `kind` is one of `human`, `service`, `agent`: `id` is present.

<a id="v08-common-extensions"></a>

### `extensions`

Type: [`extensions`](#v04-common-extensions).

<a id="v08-common-certainty"></a>

### `certainty`

Type: enum. Constraints: one of `observed`, `hypothesis`, `contradictory`, `inconclusive`.

## Conformance rules

Each rule has a stable ID that validators report. **Check** says how a rule is decided:
`schema` and `semantic` from one artifact, `cross_artifact` across held artifacts, `process`
from implementation behavior that no single artifact can show.

<a id="v04-conformance-rules"></a>

### Rules: Run and Workflow (0.4-draft)

Source: [conformance.md](../specification/v0.4/conformance.md) · catalog [conformance-rules.json](../specification/v0.4/conformance-rules.json)

| ID | Role | Level | Check | Applies to | Requirement |
| --- | --- | --- | --- | --- | --- |
| <a id="aios-0.4-p01"></a>`AIOS-0.4-P01` | producer | MUST | schema | workflow, run | Emit an artifact that validates against the schema selected by artifact_type. |
| <a id="aios-0.4-p02"></a>`AIOS-0.4-P02` | producer | MUST | semantic | run | Preserve globally unique object identities within a Run artifact. |
| <a id="aios-0.4-p03"></a>`AIOS-0.4-P03` | producer | MUST | semantic | run | Preserve unique relationship and event identities. |
| <a id="aios-0.4-p04"></a>`AIOS-0.4-P04` | producer | MUST | semantic | run | Ensure an end timestamp does not precede its start timestamp. |
| <a id="aios-0.4-p05"></a>`AIOS-0.4-P05` | producer | MUST | semantic | run | Resolve every non-external relationship endpoint to an object in the artifact with the declared type. |
| <a id="aios-0.4-p06"></a>`AIOS-0.4-P06` | producer | MUST | semantic | run | Contain every Step in its Run exactly once. |
| <a id="aios-0.4-p07"></a>`AIOS-0.4-P07` | producer | MUST | semantic | run | Connect every runtime occurrence to exactly one Step using observed-in. |
| <a id="aios-0.4-p08"></a>`AIOS-0.4-P08` | producer | MUST | semantic | run | Give every Evaluation at least one evaluates target. |
| <a id="aios-0.4-p09"></a>`AIOS-0.4-P09` | producer | MUST | semantic | run | Support workflow_id with a matching run-of relationship. |
| <a id="aios-0.4-p10"></a>`AIOS-0.4-P10` | producer | MUST | semantic | run | Ensure event targets resolve with the declared object type. |
| <a id="aios-0.4-p11"></a>`AIOS-0.4-P11` | producer | MUST | semantic | run | Reject self-relationships and cycles in structural, causal, and ordering graphs. |
| <a id="aios-0.4-p12"></a>`AIOS-0.4-P12` | producer | MUST | semantic | run | When representing retries, preserve distinct occurrence identities for each attempt and link each retry attempt to the prior attempt with an explicit recoverability edge such as follows or caused. |
| <a id="aios-0.4-x01"></a>`AIOS-0.4-X01` | producer | MUST | semantic | workflow, run | Mark every reference to an object outside the artifact with external: true. |
| <a id="aios-0.4-x02"></a>`AIOS-0.4-X02` | consumer | MUST NOT | process | workflow, run | Do not report an external reference as verified unless it was resolved. |
| <a id="aios-0.4-c01"></a>`AIOS-0.4-C01` | consumer | MUST | process | workflow, run | Perform schema and semantic validation before treating an artifact as aligned. |
| <a id="aios-0.4-c02"></a>`AIOS-0.4-C02` | consumer | MUST | process | workflow, run | Preserve unknown namespaced extensions. |
| <a id="aios-0.4-c03"></a>`AIOS-0.4-C03` | consumer | MUST NOT | process | workflow, run | Do not interpret structural validity as factual accuracy. |
| <a id="aios-0.4-c04"></a>`AIOS-0.4-C04` | consumer | MUST | process | workflow, run | Preserve unrecognized attributes keys and namespaced extensions entries, and do not treat their presence as a validation failure. |
| <a id="aios-0.4-u01"></a>`AIOS-0.4-U01` | consumer | MUST | schema | workflow, run | Reject an artifact that contains a value outside a closed vocabulary rather than guessing its meaning (decision D-004). |
| <a id="aios-0.4-u02"></a>`AIOS-0.4-U02` | producer | MUST NOT | schema | workflow, run | Do not invent new members of a closed vocabulary (decision D-004). |
| <a id="aios-0.4-e01"></a>`AIOS-0.4-E01` | producer | MUST | schema | workflow, run | Name namespaced extensions with a reverse-domain name outside the aiops namespace. |
| <a id="aios-0.4-d01"></a>`AIOS-0.4-D01` | implementation | MUST | process | workflow, run | Describe the implementation as aligned with the v0.4 draft, not stably conformant. |
| <a id="aios-0.4-k01"></a>`AIOS-0.4-K01` | implementation | SHOULD | process | workflow, run | Include the draft marker and observation date in an alignment claim. |

<a id="v06-provenance-rules"></a>

### Rules: Provenance (0.6-draft)

Source: [provenance.md](../specification/v0.6/provenance.md) · catalog [provenance-rules.json](../specification/v0.6/provenance-rules.json)

| ID | Role | Level | Check | Applies to | Requirement |
| --- | --- | --- | --- | --- | --- |
| <a id="aios-0.6-r01"></a>`AIOS-0.6-R01` | producer | MUST | schema | provenance | Emit a record that validates against the provenance record schema. |
| <a id="aios-0.6-r02"></a>`AIOS-0.6-R02` | producer | MUST | semantic | provenance | Preserve unique identities across subjects, sources, findings, and lineage edges within the record. |
| <a id="aios-0.6-r03"></a>`AIOS-0.6-R03` | producer | MUST | semantic | provenance | Resolve every source subject and every finding target subject to a subject declared in the record. |
| <a id="aios-0.6-r04"></a>`AIOS-0.6-R04` | producer | MUST | semantic | provenance | Resolve every lineage endpoint to a source or finding in the record with an endpoint kind the lineage type permits. |
| <a id="aios-0.6-r05"></a>`AIOS-0.6-R05` | producer | MUST | semantic | provenance | Give every finding at least one derived-from edge. |
| <a id="aios-0.6-r06"></a>`AIOS-0.6-R06` | producer | MUST | semantic | provenance | Keep every lineage edge free of self-reference, and derived-from and supersedes lineage free of cycles. |
| <a id="aios-0.6-r07"></a>`AIOS-0.6-R07` | producer | MUST | semantic | provenance | Not record a source captured_at later than the record created_at. |
| <a id="aios-0.6-c01"></a>`AIOS-0.6-C01` | consumer | MUST | process | provenance | Perform schema and semantic validation of the record before treating it as aligned. |
| <a id="aios-0.6-c02"></a>`AIOS-0.6-C02` | consumer | MUST | process | provenance | Validate a subject artifact against the schema its own spec_version names before resolving references into it. |
| <a id="aios-0.6-c03"></a>`AIOS-0.6-C03` | consumer | MUST NOT | cross_artifact | provenance | Do not report an aios_object source or finding target as resolved unless the subject contains an object with that id and declared type. |
| <a id="aios-0.6-c04"></a>`AIOS-0.6-C04` | consumer | MUST NOT | cross_artifact | provenance | Do not use a held artifact whose own id, artifact_type or spec_version differs from the subject entry's artifact_id, artifact_type or spec_version to resolve that entry. |
| <a id="aios-0.6-c05"></a>`AIOS-0.6-C05` | consumer | MUST NOT | cross_artifact | provenance | Do not report a digest as verified unless it was recomputed over the subject bytes actually held. |
| <a id="aios-0.6-c06"></a>`AIOS-0.6-C06` | consumer | MUST NOT | process | provenance | Do not treat a finding's status, severity, confidence or lineage as evidence that the finding is true. |
| <a id="aios-0.6-c07"></a>`AIOS-0.6-C07` | consumer | MUST NOT | process | provenance | Do not fetch a uri or execute content merely because a record contains it. |
| <a id="aios-0.6-c08"></a>`AIOS-0.6-C08` | consumer | MUST | process | provenance | Preserve unknown attributes and namespaced extensions entries in the record. |
| <a id="aios-0.6-d01"></a>`AIOS-0.6-D01` | implementation | MUST | process | provenance | Describe support for provenance records as aligned with the 0.6-draft, not stably conformant. |
| <a id="aios-0.6-k01"></a>`AIOS-0.6-K01` | implementation | SHOULD | process | provenance | Include the draft marker and observation date in a provenance alignment claim. |
| <a id="aios-0.6-s01"></a>`AIOS-0.6-S01` | producer | SHOULD | process | provenance | Reference personal data, credentials or proprietary content by uri or digest rather than copying it into description or statement, and document any redaction applied. |

<a id="v08-operational-rules"></a>

### Rules: Operational artifacts (0.8-draft)

Source: [conformance.md](../specification/v0.8/conformance.md) · catalog [operational-rules.json](../specification/v0.8/operational-rules.json)

| ID | Role | Level | Check | Applies to | Requirement |
| --- | --- | --- | --- | --- | --- |
| <a id="aios-0.8-r01"></a>`AIOS-0.8-R01` | producer | MUST | schema | verification_signal, audit_event, investigation_report | An operational artifact MUST validate against the schema selected by its declared marker and artifact type. |
| <a id="aios-0.8-r02"></a>`AIOS-0.8-R02` | producer | MUST | semantic | verification_signal, investigation_report | Evidence, finding and timeline entry identities MUST be unique across those collections within an artifact. |
| <a id="aios-0.8-r03"></a>`AIOS-0.8-R03` | producer | MUST | semantic | investigation_report | Every investigation summary, finding, timeline and recovery citation MUST name an evidence entry declared in that report. |
| <a id="aios-0.8-r04"></a>`AIOS-0.8-R04` | producer | MUST NOT | semantic | audit_event, investigation_report | An audit occurred_at, incident detected_at or timeline occurred_at MUST NOT be later than the enclosing artifact created_at. |
| <a id="aios-0.8-r05"></a>`AIOS-0.8-R05` | producer | MUST | semantic | verification_signal | A verification signal with grounded or partial grounding MUST contain at least one evidence reference. |
| <a id="aios-0.8-r06"></a>`AIOS-0.8-R06` | producer | MUST | semantic | investigation_report | Observed or contradictory investigation claims and verified recovery MUST cite at least one declared evidence entry. |
| <a id="aios-0.8-r07"></a>`AIOS-0.8-R07` | producer | MUST NOT | semantic | audit_event | An audit event MUST NOT name its own identity in causal_event_ids. |
| <a id="aios-0.8-p01"></a>`AIOS-0.8-P01` | producer | MUST | process | verification_signal, audit_event, investigation_report | A projection MUST preserve the source producer, native identity, native format and outcome meaning without inventing absent observations. |
| <a id="aios-0.8-s01"></a>`AIOS-0.8-S01` | producer | MUST NOT | process | verification_signal, audit_event, investigation_report | Producers MUST NOT copy credentials, credential hashes, raw tool arguments or privileged context into operational artifacts, including free text, attributes and extensions. |
| <a id="aios-0.8-c01"></a>`AIOS-0.8-C01` | consumer | MUST | process | verification_signal, audit_event, investigation_report | A consumer MUST perform both schema and semantic validation before describing an operational artifact as draft-aligned. |
| <a id="aios-0.8-c02"></a>`AIOS-0.8-C02` | consumer | MUST NOT | process | verification_signal, audit_event, investigation_report | A consumer MUST NOT fetch a reference URI or execute its content merely because it appears in an artifact. |
| <a id="aios-0.8-c03"></a>`AIOS-0.8-C03` | consumer | MUST | process | verification_signal, audit_event, investigation_report | A consumer MUST preserve unknown attributes and namespaced extensions when forwarding an artifact. |
| <a id="aios-0.8-c04"></a>`AIOS-0.8-C04` | consumer | MUST NOT | process | verification_signal, audit_event, investigation_report | A consumer MUST NOT treat citation presence, a native outcome, confidence or schema validity as proof of factual truth, authorization, safety, containment or successful recovery. |
| <a id="aios-0.8-d01"></a>`AIOS-0.8-D01` | implementation | MUST NOT | process | verification_signal, audit_event, investigation_report | An implementation MUST NOT describe this exploratory draft as stable AIOS conformance. |

## Companion profiles (non-normative)

These profiles extend the families above for access evidence and Sidecar integration. Each has
its own schema and guide; they add no conformance rules and do not change the core families.

| Profile | Schema | Guide |
| --- | --- | --- |
| Access evidence | [access.schema.json](../drafts/access-evidence-v1/access.schema.json) | [README](../drafts/access-evidence-v1/README.md) |
| Sidecar correlation | [schema.json](../drafts/sidecar-correlation-v1/schema.json) | [README](../drafts/sidecar-correlation-v1/README.md) |
| Sidecar intent | [intent.schema.json](../drafts/sidecar-contracts-v1/intent.schema.json) | [README](../drafts/sidecar-contracts-v1/README.md) |
| Sidecar decision | [decision.schema.json](../drafts/sidecar-contracts-v1/decision.schema.json) | [README](../drafts/sidecar-contracts-v1/README.md) |
| Sidecar audit | [audit.schema.json](../drafts/sidecar-contracts-v1/audit.schema.json) | [README](../drafts/sidecar-contracts-v1/README.md) |
| Sidecar scope | [scope.schema.json](../drafts/sidecar-contracts-v1/scope.schema.json) | [README](../drafts/sidecar-contracts-v1/README.md) |
| Sidecar transfer | [transfer.schema.json](../drafts/sidecar-contracts-v1/transfer.schema.json) | [README](../drafts/sidecar-contracts-v1/README.md) |
