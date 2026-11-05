# Audit events

Exploratory draft. An audit event records an observed action or request with
actor attribution and a target. It does not authorize an action or attest that
all calls, actions or journal entries were captured.

[Schema](schemas/audit_event.schema.json) · [Example](examples/audit_event.json)

In addition to the envelope, required fields are occurred_at, actor, action,
target, outcome and native_outcome. created_at is the recording time;
occurred_at is the observation time, not a scheduled future execution.
A projector without an observed occurrence time cannot invent one.

| Field | Meaning |
| --- | --- |
| actor.kind | human, service, agent, unknown; all known kinds require id |
| action | Producer-defined operation name; retain its original meaning |
| target | Source-attributed reference; a logical id is not an authenticated principal |
| outcome | requested, denied, started, succeeded, failed, partial, unknown |
| native_outcome | Original source format and outcome/event value |
| correlation_id | Optional source correlation handle |
| causal_event_ids | Optional unique predecessor event ids; no self-reference |

MCP dispatch maps to started; denial and revocation_acknowledged map to denied
for that attempted dispatch. Completion maps to succeeded or failed only when
the native result supports it; otherwise unknown. A request or acknowledgement
does not prove that running calls stopped. Preserve the source correlation id.

Sidecar BLOCK maps to denied for the decision boundary. ALLOW records a decision,
not executed work, so it cannot establish succeeded. Some Sidecar audit records
lack actor attribution; use unknown rather than invent an operator identity.
Do not copy AuditRecord.trigger.arguments or execution_context into this shape.
Tower operator actions preserve the operator and native timeline event.

Unknown free text, attributes and extensions are not a redaction mechanism.
See [conformance](conformance.md) for required privacy and interpretation rules.
