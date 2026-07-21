# v0.3 Semantic Conventions

## Naming rules

Canonical event names use lowercase dot-separated segments: `aiops.<area>.<action>`. Producers MUST NOT place provider, framework, or organization names in the canonical namespace. Extensions MUST use a reverse-domain namespace such as `io.deepagentlabs.agenticlens.*`.

## Common attributes

Every event MUST provide `event_id`, `event_name`, `occurred_at`, `object_id`, and `object_type`. It SHOULD provide `run_id`, producer identity, specification version, and correlation information when known. Unknown values MUST NOT be fabricated.

Sensitive content MUST be optional. Producers SHOULD support references, hashes, summaries, classifications, and redaction metadata.

## Lifecycle events

- `aiops.run.started`, `aiops.run.completed`, `aiops.run.failed`, `aiops.run.cancelled`
- `aiops.request.received`, `aiops.request.completed`, `aiops.request.rejected`
- `aiops.step.started`, `aiops.step.completed`, `aiops.step.failed`, `aiops.step.cancelled`
- `aiops.agent.started`, `aiops.agent.waiting`, `aiops.agent.completed`, `aiops.agent.failed`

Lifecycle events describe transitions, not state snapshots. A completion event MUST identify its outcome.

## Model, Prompt, and Context

- `aiops.model.requested`, `aiops.model.responded`, `aiops.model.failed`
- `aiops.prompt.rendered`
- `aiops.context.assembled`

Model events SHOULD include provider, model, modality, usage, finish reason, provider request identity, and latency when observed. Each retry has a distinct interaction identity. Prompt template identity and revision MUST remain distinguishable from a rendered Prompt. Context SHOULD retain source and redaction evidence.

## Tools, retrieval, and memory

- `aiops.tool.requested`, `aiops.tool.authorized`, `aiops.tool.completed`, `aiops.tool.failed`
- `aiops.retrieval.started`, `aiops.retrieval.completed`, `aiops.retrieval.failed`
- `aiops.memory.read`, `aiops.memory.written`, `aiops.memory.updated`, `aiops.memory.deleted`, `aiops.memory.failed`

Transport success MUST NOT imply tool application success. Retrieval completion MUST NOT imply selection, use, correctness, or groundedness. Memory events SHOULD identify the persistence boundary without requiring private values.

## Evaluation, safety, and reliability

- `aiops.evaluation.completed`, `aiops.evaluation.failed`
- `aiops.safety.detected`, `aiops.safety.reviewed`, `aiops.safety.mitigated`
- `aiops.reliability.detected`, `aiops.reliability.recovered`

Evaluation events MUST identify method, criterion, target, and result. Safety events MUST distinguish detection from confirmation and enforcement. Reliability events SHOULD identify the affected target and operational effect.

## Incidents

- `aiops.incident.opened`, `aiops.incident.updated`, `aiops.incident.mitigated`, `aiops.incident.resolved`

A failure, failed Evaluation, or Safety Signal MUST NOT automatically become an Incident.

## Measurements and compatibility

Durations use non-negative milliseconds. Token counts use non-negative integers. Cost MUST include a currency code. Scores MUST declare their scale or categorical domain. A measurement MUST state whether it is observed, estimated, or derived.

Consumers MUST ignore unrecognized extension attributes unless configured to reject them. Producers MUST NOT reuse a canonical name with incompatible meaning.
