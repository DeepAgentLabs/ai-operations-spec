# v0.1 — Core Concepts and Runtime Object Model

## Status

Foundation draft. Internal terminology decisions are recorded; independent-framework review remains open.

## Goal

v0.1 defines a shared language for describing what exists during the operation of an AI system. It establishes conceptual identity and boundaries before the specification chooses JSON fields or package APIs.

## Central distinction

The model separates reusable design from runtime evidence:

```text
Workflow (reusable definition)
    └── Run (one execution)
          ├── Request (work entering or advancing the run)
          ├── Step (bounded execution activity)
          ├── Agent (runtime participant)
          ├── Evaluation / Safety / Reliability evidence
          └── Incident (managed operational occurrence)
```

A Workflow is not a trace. A Run is not a reusable workflow definition. A Request is not necessarily the entire Run. A Step is not automatically an Agent.

## Core concepts

v0.1 defines:

- Workflow
- Run
- Request
- Step
- Agent
- Model Interaction
- Prompt
- Context
- Tool Invocation
- RAG Retrieval
- Memory Operation
- Evaluation
- Safety Signal
- Reliability Event
- Incident

The roadmap originally used shortened labels such as `LLM`, `Tool`, `RAG`, `Memory`, `Safety`, and `Reliability`. v0.1 gives runtime occurrences precise names while retaining those labels as capability-area shorthand. An LLM call is represented by the broader Model Interaction concept.

## What v0.1 does not define

v0.1 does not standardize:

- property names or required JSON fields
- containment arrays or graph serialization
- semantic event names
- telemetry span mapping
- Python or other language classes
- schema validation
- extension namespaces

Those belong to later milestones. Conceptual examples in this milestone demonstrate meaning, not wire format.

## Documents

- [Core concepts](core-concepts.md) is the normative vocabulary.
- [Terminology](terminology.md) defines cross-cutting terms and disambiguations.
- [Examples](examples.md) test whether the model describes realistic systems.
- [Acceptance criteria](acceptance-criteria.md) defines when v0.1 is ready to freeze.
- [Design decisions](decisions.md) records resolved vocabulary choices.
