# Scenario 01: Customer Support Answer

## Narrative

A customer asks whether a refund is still possible for an order that arrived damaged. The system starts a run, classifies the request, retrieves policy passages, drafts an answer with a model interaction, and evaluates whether the answer is grounded in retrieved policy.

## Minimum expected objects

- one `Run`
- one initiating `Request`
- at least two `Step` occurrences:
  - classification
  - answer generation
- one or more `Model Interaction` occurrences
- one `RAG Retrieval`
- one `Prompt`
- one `Context`
- one `Evaluation`

## v0.1 review questions

- Is the `Request` distinct from the `Run`?
- Is retrieval modeled as `RAG Retrieval` instead of a generic tool by default?
- Is the evaluation distinct from runtime completion?

## v0.2 review questions

- Does the answer step depend on retrieval?
- Are retrieval and answer represented as separate observed occurrences?

## v0.3 expected event areas

- run lifecycle
- step lifecycle
- prompt rendering
- context assembly
- model request and response
- retrieval activity
- evaluation result

## v0.4 artifact expectations

- references resolve cleanly between run, request, steps, retrieval, and evaluation
- schema allows optional sensitive content omission
