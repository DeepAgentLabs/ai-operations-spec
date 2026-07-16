# AI Operations Specification

## Status

Draft `v0`

This document defines the first draft of the AI Operations Specification, a
shared operational data model for production AI systems.

## Purpose

The specification provides a common contract for representing AI execution in a
portable, inspectable form. It is intended to make interoperability possible
between:

- frameworks and orchestration runtimes
- observability and telemetry tooling
- resilience and chaos testing systems
- local analysis, audits, and CI workflows

Rather than starting from hundreds of disconnected metrics and fields, the
specification should start from the **operational objects** that make up a real
AI application. Tools can then attach fields, events, metrics, and extensions
to those objects in a consistent way.

## Primary Artifact

The primary reference JSON representation is `workflow.json`.

This JSON artifact is a serialization of the AI Operations Specification, not
the definition of the specification itself.

## AI Runtime Model

The specification should model the runtime of an AI application.

```text
AI Runtime
│
├── Workflow
├── Request
├── Agent
├── LLM
├── Prompt
├── Context
├── RAG
├── Memory
├── Tool
├── MCP
├── Evaluation
├── Safety
├── Reliability
└── Incident
```

Each operational object owns the fields that naturally belong to it.

This keeps the specification understandable, additive, and useful across
frameworks instead of turning it into a flat list of unrelated counters.

## Operational Objects

### Workflow

A workflow is one complete execution of an AI system or AI-assisted task.

Examples:

- a customer support run
- a RAG answer generation flow
- a multi-agent planning and execution cycle
- a degraded or chaos-tested execution

Developer questions:

- what ran
- how long did it take
- did it succeed

### Request

A request is the triggering interaction that starts or advances a workflow.

Examples:

- a user chat message
- an API request
- a scheduled job input
- an agent-to-agent delegated request

Developer questions:

- what input triggered this run
- how is it correlated with the rest of the workflow

### Agent

An agent is an autonomous or semi-autonomous runtime participant that plans,
decides, invokes tools, and produces intermediate or final work.

Developer questions:

- what was the goal
- what plan did it make
- which actions did it take
- did it loop, hand off, or finish

### LLM

An LLM object represents one model interaction within the runtime.

Developer questions:

- which model was used
- what prompt was sent
- what response came back
- how many tokens were used
- how much did it cost

### Prompt

A prompt object captures the prompt template and the rendered prompt that was
actually sent.

Developer questions:

- which prompt version ran
- what changed
- what variables were rendered

### Context

A context object captures the information injected around a prompt, including
conversation history, retrieved knowledge, and memory.

Developer questions:

- what context was injected
- how large was it
- was anything truncated or compressed

### RAG

A RAG object captures retrieval and grounding behavior.

Developer questions:

- what was retrieved
- which chunks were used
- were they relevant and grounded

### Memory

A memory object captures state read and written by the runtime.

Developer questions:

- what memories were read
- what memories were written
- did stale or conflicting memory affect the run

### Tool

A tool object captures an external action taken by the runtime.

Developer questions:

- which tool ran
- what inputs were passed
- what outputs came back
- how long did it take
- did it fail

### MCP

An MCP object captures actions performed through the Model Context Protocol.

Developer questions:

- which MCP server and tool were used
- what request was sent
- what response came back

### Evaluation

An evaluation object captures judgments about output quality, correctness,
groundedness, policy, or readiness.

Developer questions:

- was the answer good
- what score did it get
- what did human or model-based evaluators say

### Safety

A safety object captures guardrails, policy, and privacy-relevant signals.

Developer questions:

- was there prompt injection
- was PII detected
- was any output blocked or redacted

### Reliability

A reliability object captures runtime stability behavior.

Developer questions:

- were there retries, timeouts, or fallbacks
- what errors occurred
- did the system recover cleanly

### Incident

An incident object captures notable degradations, anomalies, failures, or
operational events.

Developer questions:

- what failed
- how serious was it
- what evidence should be retained

### Step

A step is a meaningful unit within a workflow.

Examples:

- planner step
- retriever step
- tool call
- LLM call
- memory step
- final response step

### Extensions

Extensions allow additional structured data to be attached without breaking core
interoperability, provided the base contract remains valid.

## Semantic Events

Operational objects should emit AI-native semantic events that are stable across
frameworks.

Examples include:

- `workflow.run`
- `request.start`
- `request.end`
- `agent.run`
- `agent.plan`
- `agent.step`
- `llm.call`
- `prompt.render`
- `context.inject`
- `rag.retrieve`
- `memory.read`
- `memory.write`
- `tool.call`
- `mcp.call`
- `evaluation.run`
- `judge.score`
- `guardrail.block`
- `incident.detected`

These events are the semantic backbone of the specification. Individual tools
may export them as JSON records, OpenTelemetry spans/logs/metrics, or other
transport-specific representations.

## Export Model

Telemetry is an export mechanism, not an operational object.

The same operational objects and semantic events should be exportable to:

- `workflow.json`
- JSON
- CSV
- Markdown
- OpenTelemetry traces
- OpenTelemetry logs
- OpenTelemetry metrics
- OTLP
- future sinks such as Kafka or webhooks

## Design Principles

- The specification must remain framework-agnostic.
- The specification must remain language-neutral.
- The specification should be additive by default.
- The specification should support local files and CI workflows.
- The specification should support interoperability without requiring a hosted
  control plane.
- The specification should model operational objects before low-level fields.
- The specification should support "instrument once, export everywhere."

## Compatibility

Compatibility should follow these rules:

- additive fields are preferred over destructive renames
- unknown extension fields should not invalidate otherwise valid artifacts
- changes that break existing consumers should require a new major version

## Ownership

DeepAgentLabs stewards the specification.

Individual tools such as `agenticlens` may implement, extend, validate, and
export artifacts that conform to it, but no single tool owns the contract.

## Near-Term Follow-Up

This draft should eventually be expanded with:

- a machine-readable JSON Schema
- canonical example artifacts
- extension conventions
- object-level definitions and required/optional rules
- semantic event conventions
- explicit version markers inside the artifact
