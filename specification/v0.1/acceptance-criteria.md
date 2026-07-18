# v0.1 Acceptance Criteria

v0.1 is ready to freeze only when all criteria below are satisfied.

## Vocabulary completeness

- [x] Workflow is defined as a reusable definition.
- [x] Run is defined as one execution instance.
- [x] Request and Step have distinct boundaries.
- [x] Agent, LLM Interaction, Prompt, Context, Tool Invocation, RAG Retrieval, and Memory Operation are defined.
- [x] Evaluation, Safety Signal, Reliability Event, and Incident are defined.
- [x] Each concept states purpose, identity/lifecycle, ownership, references, and exclusions.

## Coherence

- [x] Definition objects and runtime occurrences are distinguished.
- [x] Runtime completion, quality, safety, reliability, and incident management are not collapsed into one status.
- [x] Sensitive content is not required to be embedded.
- [x] Sequential, parallel, nested, retrying, and graph-shaped execution are acknowledged without prematurely specifying serialization.

## Scope discipline

- [x] v0.1 does not standardize JSON fields.
- [x] v0.1 does not standardize semantic event names.
- [x] v0.1 does not define SDK classes or transport mappings.
- [x] Premature schema work is labeled non-normative and preserved for v0.4.

## Review gates

The following require maintainer review before v0.1 is frozen:

- [ ] Confirm whether **Run** becomes a named roadmap object or is called `WorkflowRun`.
- [ ] Confirm whether MCP needs a core runtime concept; the current draft treats MCP as a transport/integration used by Tool Invocations.
- [ ] Confirm whether model interactions should use the general name `Model Interaction` with LLM as a subtype.
- [ ] Review definitions against at least two independent frameworks.
- [ ] Record decisions and update all v0.1 documents consistently.

## Exit condition

v0.1 is complete when the review gates are resolved and two independent implementers can classify the same example runtime objects without package-specific knowledge. Only then should normative v0.2 relationship work begin.
