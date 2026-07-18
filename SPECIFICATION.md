# AI Operations Specification v0.1

## Status

Draft `v0.1`. This version is suitable for experimentation and interoperability
testing. It is not a stable `1.0` contract.

## Purpose

The AI Operations Specification (AIOps) defines a portable JSON representation
of an AI workflow run. It lets runtimes, observability tools, evaluation tools,
and resilience systems exchange operational data without sharing implementation
code or requiring a hosted control plane.

Normative terms such as **MUST**, **SHOULD**, and **MAY** are interpreted as in
RFC 2119.

## Conformance

An artifact conforms to v0.1 when it:

1. validates against [`schemas/workflow.schema.json`](schemas/workflow.schema.json),
2. uses RFC 3339 timestamps with a timezone,
3. uses identifiers that are unique within the artifact, and
4. preserves the meaning and units defined below.

Schema validation checks structure. Producers and consumers SHOULD also enforce
semantic requirements such as unique step IDs and valid `parent_step_id`
references.

## Workflow artifact

A workflow artifact represents one execution of an AI system or AI-assisted
task. The canonical media type is JSON and the conventional filename is
`workflow.json`.

### Required fields

| Field | Type | Meaning |
| --- | --- | --- |
| `spec_version` | string | Specification version. This draft requires `0.1`. |
| `id` | string | Stable identifier for this run. |
| `name` | string | Human-readable workflow name. |
| `start_time` | timestamp | Time execution began. |
| `steps` | array | Ordered execution steps; it MAY be empty. |

### Optional fields

| Field | Type | Meaning |
| --- | --- | --- |
| `workflow_id` | string | Stable identity shared by runs of the same workflow. |
| `end_time` | timestamp or null | Time execution ended. |
| `status` | enum | `running`, `completed`, `failed`, or `cancelled`. |
| `metrics` | object | Run-level aggregate metrics. |
| `chaos_events` | array | Fault-injection events correlated to this run. |
| `evaluations` | array | Quality or policy judgments for the run or a step. |
| `agent_topology` | object | Implementation-defined agent graph. |
| `metadata` | object | Producer-defined, non-normative data. |
| `extensions` | object | Namespaced structured extensions. |

## Step

A step is an ordered, meaningful unit of execution. Common types are `planner`,
`retriever`, `tool_call`, `llm_call`, `memory`, and `final_response`. Producers
MAY use another non-empty type string; consumers MUST tolerate unknown types.

Every step MUST have `id`, `name`, `type`, and `metrics`. A step MAY identify an
agent, provider, model, parent step, or handoff. `parent_step_id` MUST refer to a
step in the same artifact when present.

## Metrics and units

Metrics have consistent units throughout the specification:

| Field | Unit |
| --- | --- |
| `prompt_tokens`, `completion_tokens`, `total_tokens` | token count |
| `latency` | seconds |
| `ttft` | seconds |
| `cost` | US dollars |

Counts and durations MUST be non-negative. `cost` MAY be `null` when unknown.
Producers SHOULD set `total_tokens` to the sum of prompt and completion tokens
when both are known.

## Chaos events

A chaos event records one injected fault occurrence. It MUST include `id`,
`fault_type`, `timestamp`, `outcome`, and `message`. `outcome` is one of
`errored`, `degraded`, `delayed`, or `looped`. `step_id` SHOULD be used when the
event can be correlated with a step.

## Evaluations

An evaluation records a judgment associated with the run or a step. It MUST
contain an `id`, `name`, and `status`. A numeric `score`, optional bounds, a
human-readable explanation, and implementation-defined detail MAY be included.

## Extensions

The `extensions` object is the safe location for portable vendor or project
extensions. Keys MUST use reverse-domain notation, for example:

```json
{
  "extensions": {
    "io.deepagentlabs.agenticlens": {"reducible_tokens": 420}
  }
}
```

Consumers MUST ignore extension keys they do not understand. Producers SHOULD
not place data required to interpret core fields inside an extension.

`metadata` is intended for local annotations and is not governed by the same
portability guarantee.

## Versioning and compatibility

- `0.x` versions may change as implementations converge.
- Additive optional fields SHOULD be introduced in minor versions.
- Removing fields, changing their meaning, or changing units requires a major
  version after `1.0`.
- Consumers SHOULD reject unsupported major versions and MAY accept newer minor
  versions when unknown fields can be ignored safely.
- Unknown fields are allowed to support forward-compatible producers.

Artifacts produced before v0.1 that omit `spec_version` are legacy artifacts,
not conforming v0.1 artifacts. Tools MAY support them through an explicit
compatibility mode.

## Stewardship

DeepAgentLabs stewards this specification. No individual SDK or product owns
the contract. Changes should be proposed with a schema update, examples, and a
clear compatibility statement.
