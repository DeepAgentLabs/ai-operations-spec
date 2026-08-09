# v0.2 Relationships and Execution Structure

This document defines normative relationship semantics. Relationship serialization is deferred to v0.4.

## General rules

Every relationship has a source, a target, and a type. Implementations MUST preserve object identity across references. They MUST NOT infer causation from timestamps, containment, or correlation alone.

A relationship MAY carry implementation-specific evidence, but extensions MUST NOT change its normative direction or meaning.

## Structural relationships

### `run-of`

Connects a Run to the Workflow definition it executes. A Run has at most one direct `run-of` relationship and MAY have none for ad hoc execution. Many Runs may reference one Workflow.

### `contains`

States that a Run is the operational boundary for a Request or Step. Containment does not imply order or causation. Every Step MUST be contained by exactly one Run.

### `parent-of`

Connects structurally nested Requests, Steps, or Runs of the same kind. A child MUST NOT have more than one direct structural parent of that kind. Parent relationships MUST be acyclic.

## Causal relationships

### `caused`

States that the source occurrence directly produced or initiated the target occurrence. A causal edge is stronger than correlation and MUST be supported by producer evidence.

### `follows`

States that the target is constrained to occur after the source in the intended execution order. `follows` does not by itself claim that the source caused the target.

### `depends-on`

States that the source requires the target's result, state, or completion. Dependency graphs MUST be acyclic unless a loop boundary explicitly scopes the cycle.

## Participation relationships

### `performed-by`

Connects a Step to the Agent responsible for selecting or coordinating its action. A Step MAY be performed without an Agent. Deterministic execution MUST NOT be assigned an Agent merely to satisfy this relationship.

### `delegated-to`

Connects a delegating Agent occurrence or Step to the Agent receiving a bounded objective. Delegation transfers responsibility for work; it does not necessarily create a child Run.

### `handed-off-to`

Connects one Agent participation occurrence to another when primary responsibility moves. A handoff differs from delegation because the sender need not retain responsibility.

## Evidence relationships

### `observed-in`

Connects a Model Interaction, Tool Invocation, RAG Retrieval, or Memory Operation to the Step in which it occurred. Each such runtime occurrence MUST be observed in exactly one Step.

### `evaluates`

Connects an Evaluation to its target. Every Evaluation MUST have at least one target and MUST state which criterion applies to each multi-target judgment.

### `signals-on`

Connects a Safety Signal or Reliability Event to the occurrence or content reference that produced the concern.

### `evidence-for`

Connects operational evidence to an Incident. Incident association MUST NOT change the original evidence or imply that every linked signal was confirmed.

## Execution shapes

- **Sequential:** Steps are connected by `follows` or `depends-on` edges.
- **Parallel:** sibling Steps have no ordering edge and their lifecycles may overlap.
- **Branch:** one occurrence causes or enables multiple alternatives; recorded branch evidence identifies the selected path.
- **Join:** a Step depends on multiple predecessor Steps.
- **Retry:** a new attempt refers to the prior attempt and the shared logical activity; attempts retain distinct identities. The failed occurrence and the retry attempt MUST be linked by an explicit recoverability edge (for example `caused` or `follows`) so consumers can reconstruct the retry path without inferring it from timing or naming alone (decision `D-002`).
- **Loop:** repeated occurrences have distinct identities and a shared loop identity plus iteration position.
- **Delegation:** Agent responsibility is represented separately from Step structure.

Ordering fields such as sequence numbers MAY assist presentation but MUST NOT replace explicit graph relationships when non-sequential structure matters.

## Cross-run relationships

A Run MAY create a child Run. The child remains an independent execution boundary with its own Requests and Steps. Cross-run causation MUST be explicit, and implementations MUST NOT flatten child Runs in a way that loses their identity.

## Graph integrity

- Every referenced identity MUST resolve within the artifact or through an explicit external reference.
- Structural parent graphs MUST be acyclic.
- An occurrence MUST NOT be its own ancestor or causal predecessor.
- Missing telemetry MUST be represented as unknown, not reconstructed as fact.
- Producers SHOULD preserve enough evidence for consumers to distinguish structure, order, causation, and correlation.
