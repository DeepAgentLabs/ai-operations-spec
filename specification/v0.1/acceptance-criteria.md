# v0.1 Acceptance Criteria

v0.1 is ready to freeze only when all criteria below are satisfied.

## Vocabulary completeness

- [x] Workflow is defined as a reusable definition.
- [x] Run is defined as one execution instance.
- [x] Request and Step have distinct boundaries.
- [x] Agent, Model Interaction, Prompt, Context, Tool Invocation, RAG Retrieval, and Memory Operation are defined.
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
- [x] The premature schema experiment is labeled historical and separated from the current v0.4 exploratory design.

## Review gates

The following require maintainer review before v0.1 is frozen:

- [x] Use **Run**, because ad hoc execution need not reference a Workflow.
- [x] Treat MCP as an integration protocol used by Tool Invocations, not a core runtime concept.
- [x] Use the general name **Model Interaction**, with LLM calls represented as a model family or operation.
- [ ] Review definitions against at least two independent frameworks.
- [ ] Record decisions and update all v0.1 documents consistently.

## Exit condition

v0.1 is complete when the remaining external review gate is resolved and two independent implementers can classify the same example runtime objects without package-specific knowledge. Exploratory later-layer work MAY proceed to test the model, but no later milestone can freeze before its dependencies.
