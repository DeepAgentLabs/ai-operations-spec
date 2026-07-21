# v0.4 Draft Conformance

Because v0.4 is pre-release, implementations MUST describe themselves as **aligned with the v0.4 draft**, not stably conformant.

## Producer requirements

A producer claiming draft alignment MUST:

1. Emit an artifact that validates against the schema selected by `artifact_type`.
2. Preserve globally unique object identities within a Run artifact.
3. Preserve unique relationship and event identities.
4. Ensure an end timestamp does not precede its start timestamp.
5. Resolve every non-external relationship endpoint to an object in the artifact with the declared type.
6. Contain every Step in its Run exactly once.
7. Connect every runtime occurrence to exactly one Step using `observed-in`.
8. Give every Evaluation at least one `evaluates` target.
9. Support `workflow_id` with a matching `run-of` relationship.
10. Ensure event targets resolve with the declared object type.
11. Reject self-relationships and cycles in structural, causal, and ordering graphs.

An external reference MUST set `external: true`. External resolution is the consumer's responsibility and MUST NOT be reported as verified unless it was resolved.

## Consumer requirements

A consumer claiming draft alignment MUST perform schema and semantic validation before treating an artifact as aligned. It MUST preserve unknown namespaced extensions and MUST NOT interpret structural validity as factual accuracy.

## Claim format

A claim SHOULD include the draft marker and observation date, for example:

```text
Aligned with AI Operations Specification v0.4-draft as observed on 2026-07-21.
```

No compatibility across different draft snapshots is promised.
