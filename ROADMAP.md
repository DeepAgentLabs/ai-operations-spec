# AI Operations Specification Roadmap

## Direction

The AI Operations Specification should be built **specification-first**.

It should come before SDK ergonomics, package-specific abstractions,
exporter-specific design, or Python implementation details.

The goal is not to define "the JSON format that one package exports."

The goal is to define:

> **The open standard for representing the execution, evaluation, and
> operational behavior of AI and agentic systems.**

That makes the specification the foundation of the ecosystem:

```text
AI Operations Specification
        │
        ├── Core Concepts
        ├── Runtime Object Model
        ├── Relationships
        ├── Semantic Conventions
        ├── JSON Schemas
        ├── Versioning
        ├── Examples
        └── Extension Model
                 │
                 ▼
     Reference Implementations
        ├── AgenticLens
        ├── Agentic Chaos
        └── DeepAgent MCP
```

## Build Order

The specification should be developed in this order.

### Phase 1 — Core Concepts and Runtime Object Model

Goal: define the language of AI operations before building SDKs or exporters.

Questions to answer:

- what is a workflow
- what is a request
- what is a step
- what is an agent
- what is an LLM call
- what is a prompt
- what is a context object
- what is a tool call
- what is a memory operation
- what is a RAG retrieval
- what is an evaluation
- what is a safety signal
- what is a reliability event
- what is an incident

Initial runtime objects:

- `Workflow`
- `Request`
- `Step`
- `Agent`
- `LLM`
- `Prompt`
- `Context`
- `Tool`
- `Memory`
- `RAG`
- `Evaluation`
- `Safety`
- `Reliability`
- `Incident`

At this phase, the focus is on definitions and boundaries, not on low-level
field catalogs.

### Phase 2 — Relationships and Execution Structure

Goal: define how the runtime objects connect.

Examples:

- `Workflow` contains `Request`, `Step`, `Evaluation`, and `Incident`
- `Step` may represent or contain `LLM`, `Tool`, `RAG`, `Memory`, or other
  runtime activity
- workflows may have parent-child relationships
- execution may be sequential, parallel, or graph-shaped
- agent handoffs and delegation should have a portable representation

This phase should define the execution graph model clearly enough that multiple
tools can represent the same run consistently.

### Phase 3 — Semantic Conventions

Goal: define canonical AI-native event names and meanings.

Examples:

- `workflow.started`
- `workflow.completed`
- `request.started`
- `request.completed`
- `agent.started`
- `agent.step`
- `llm.call`
- `prompt.rendered`
- `context.injected`
- `tool.called`
- `memory.read`
- `memory.write`
- `rag.retrieved`
- `evaluation.run`
- `judge.scored`
- `incident.created`

This is where the specification starts to play a role analogous to
OpenTelemetry semantic conventions, but for AI runtimes.

### Phase 4 — JSON Schemas

Goal: make specification artifacts validatable and portable.

Examples:

- `schemas/workflow.schema.json`
- `schemas/llm.schema.json`
- `schemas/prompt.schema.json`
- `schemas/tool.schema.json`
- `schemas/evaluation.schema.json`

At this point the repository should provide both written rules and
machine-readable validation.

### Phase 5 — Versioning and Compatibility

Goal: define how the standard evolves without fragmenting implementations.

This phase should establish:

- version markers
- additive change guidance
- breaking change policy
- extension compatibility expectations
- deprecation guidance

### Phase 6 — Examples and Extension Model

Goal: make adoption easier for both humans and tools.

This phase should provide:

- canonical example artifacts
- minimal and advanced examples
- extension conventions
- guidance for third-party interoperability

## Repository Shape

The repository should evolve toward a structure like:

```text
ai-operations-spec/
├── README.md
├── SPECIFICATION.md
├── ROADMAP.md
├── schemas/
├── semantic-conventions/
├── examples/
└── extensions/
```

This repository is the home of the standard itself, not a Python SDK.

## Milestones

### v0.1 — Core Concepts

Define:

- `Workflow`
- `Request`
- `Step`
- `Agent`
- `LLM`
- `Prompt`
- `Tool`
- `RAG`
- `Memory`
- `Evaluation`
- `Incident`

Success criteria:

- written definitions exist
- object boundaries are clear
- the spec reads like a coherent runtime model rather than a metric list

### v0.2 — Relationships

Define:

- workflow-to-step structure
- parent-child runs
- execution graph model
- step-to-object relationships
- agent handoff and delegation concepts

Success criteria:

- two different tools could represent the same run shape consistently

### v0.3 — Semantic Conventions

Define:

- canonical event names
- event meaning and lifecycle
- basic naming rules

Success criteria:

- event producers and consumers can agree on stable AI-native event semantics

### v0.4 — JSON Schemas

Deliver:

- initial machine-readable schemas
- validation examples

Success criteria:

- artifacts can be validated outside the Python packages

### v0.5 — Versioning

Define:

- artifact versioning rules
- compatibility and extension policy

Success criteria:

- the spec can evolve without creating ambiguity for implementers

### v1.0 — Stable Specification

Deliver:

- stable core object model
- stable semantic conventions
- stable schema set
- examples and extension guidance

Success criteria:

- third parties can implement the specification without depending on DeepAgentLabs
  packages directly

## Relationship To The Packages

The package roles should stay clear:

- `ai-operations-spec` defines the standard
- `agenticlens` is the flagship Python instrumentation and export
  implementation
- `agentic-chaos` extends the same standard with resilience and fault-testing
  evidence
- `deep-agentic-core-mcp` reads, exposes, and transforms the same artifacts

The specification should remain above any one package.

## Contributor Question

Anyone contributing to this repository should be able to ask:

`Does this make the AI runtime model, semantic conventions, schemas, versioning,
or extension model clearer and easier to implement?`

If the answer is no, it probably belongs in one of the implementation
repositories instead.
