# Review Decision Log

Use this file to record milestone-level review outcomes.

## Open decisions

### D-001: External framework set for acceptance review

- Status: open
- Applies to: `v0.1`, `v0.2`, `v0.3`, `v0.4`
- Question:
  Which two independent frameworks or implementations will be used for formal comparison?
- Suggested candidates:
  - `agenticlens`
  - `agentic-chaos`
  - one non-DeepAgentLabs implementation or external reviewer
- Evidence needed:
  committed framework mapping notes and scenario results
- Current state (2026-08-08):
  `agenticlens` and `agentic-chaos` mappings are committed
  (`reviews/framework-mappings/`), but both are DeepAgentLabs-owned repos.
  Per `README.md`, vendor-neutrality is not established until review includes
  a party outside DeepAgentLabs. This decision cannot close on repo-internal
  work alone.
- Definition of "independent" for this gate:
  a reviewer or implementation with no DeepAgentLabs authorship, funding, or
  editorial control over AIOS, reviewing the scenario pack without being
  briefed on the intended "correct" answer beforehand.
- Next action (external, not repo work):
  identify and engage at least one such reviewer/implementer, run
  `reviews/scenarios/` against their framework, and commit the result as
  `reviews/framework-mappings/<name>.md` using
  `reviews/framework-mappings/external-reviewer-template.md`. A ready-to-send
  outreach message is in `reviews/EXTERNAL_REVIEW_INVITE.md`.

### D-002: v0.2 retry and ordering semantics

- Status: accepted
- Applies to: `v0.2`
- Question:
  Are retry attempts represented as repeated occurrences within one logical activity, and what minimal ordering guarantees are required for equivalent graph reconstruction?
- Decision:
  Retry attempts should remain distinct runtime occurrences with their own identities, while still being attributable to one logical activity or step. Equivalent graph reconstruction requires at least explicit attempt ordering and a recoverability link between the failed occurrence and the subsequent retry path.
- Evidence:
  `reviews/framework-mappings/agenticlens.md`
  `reviews/framework-mappings/agentic-chaos.md`
- Follow-up:
  Closed: `specification/v0.2/relationships.md` now requires an explicit
  recoverability edge (`caused` or `follows`) between a failed occurrence and
  its retry attempt.

### D-003: v0.3 transport-boundary policy

- Status: accepted
- Applies to: `v0.3`
- Question:
  Should transport mappings remain outside the core spec and be published as separate non-normative profiles?
- Decision:
  Yes. Core AIOS semantics should remain transport-neutral. Transport mappings such as OpenTelemetry bindings should live as separate non-normative profiles or companion documents.
- Evidence:
  `reviews/framework-mappings/agenticlens.md`
  `reviews/framework-mappings/agentic-chaos.md`
- Follow-up:
  Closed: `specification/v0.3/semantic-conventions.md` now states the
  transport-boundary rule under "Transport boundary".

### D-004: v0.4 unknown-value behavior

- Status: accepted (proposed by editor pass on 2026-08-08; maintainer should
  confirm rather than treat as externally reviewed)
- Applies to: `v0.4`
- Question:
  What unknown enum, extension, and forward-compatibility behavior should consumers preserve or reject?
- Decision:
  Closed vocabularies (`object_type`, reference/relationship/occurrence/evidence
  `type`, canonical `event_name`) are fixed by the schema; an out-of-enum value
  is a schema violation and MUST be rejected, not tolerated as unknown. Forward
  compatibility is scoped to the two existing open extension points instead:
  freeform `attributes` objects and reverse-domain-namespaced `extensions`
  objects. Consumers MUST preserve unrecognized keys in both rather than
  discarding them.
- Evidence:
  `specification/v0.4/conformance.md` ("Unknown-value behavior" section)
  `specification/v0.4/examples/invalid/run-unknown-relationship-type.json`
  `specification/v0.4/examples/invalid/run-unknown-object-type.json`
  `specification/v0.4/examples/valid/run-namespaced-extensions.json`
- Follow-up:
  This is a repo-internal design decision, not independent-implementer
  evidence. It closes the "review identifier/reference/extension/unknown-value
  behavior" row on its own merits but does not substitute for the still-open
  independent-implementation validation gate.

## Accepted decisions

### D-100: `Run` remains broader than `Workflow`

- Status: accepted
- Applies to: `v0.1`
- Notes:
  Ad hoc execution may exist without a reusable workflow definition.

### D-101: MCP is not a core runtime concept

- Status: accepted
- Applies to: `v0.1`
- Notes:
  MCP is treated as an integration protocol used by tool invocations.

### D-102: `Model Interaction` is the general runtime concept

- Status: accepted
- Applies to: `v0.1`
- Notes:
  LLM calls are represented as a model family or operation, not as a separate core concept.

## Review template

Copy this block for each new decision:

```text
### D-XXX: Short title

- Status: open | accepted | rejected
- Applies to: v0.x
- Question:
  ...
- Decision:
  ...
- Evidence:
  ...
- Follow-up:
  ...
```
