# v0.1 Conceptual Examples

These examples are non-serializable narratives. They test the vocabulary without defining JSON structure.

## Example 1: Customer-support answer

A reusable **Workflow** describes how support questions are classified, grounded in policy, and answered.

A customer message creates a **Request** and starts a **Run**. A classification **Step** contains an **LLM Interaction** using a rendered **Prompt**. A **RAG Retrieval** searches the policy index; selected passages contribute to **Context** for an answer Step. An **Evaluation** judges groundedness.

If the model endpoint times out and the system retries, each invocation attempt is a distinct LLM Interaction and the timeout and retry are **Reliability Events**. The retry does not automatically create an Incident.

## Example 2: Multi-agent research

A research **Workflow** is executed as one **Run**. A coordinator **Agent** receives the initiating Request and delegates work to researcher Agents. Each delegation creates or advances work and will receive a portable relationship representation in v0.2.

Searches are Tool Invocations. Retrieved documents processed for grounding are RAG Retrieval evidence. Notes persisted for later turns use Memory Operations. An Agent is not the same object as the Steps it performs.

Two research Steps execute in parallel. v0.1 permits this execution shape but does not yet prescribe graph edges or ordering fields.

## Example 3: Safety intervention

A Request contains suspected prompt injection. A detector emits a **Safety Signal** associated with the Request and Context. A policy mechanism blocks a sensitive Tool Invocation.

The signal is evidence, the block is an enforcement outcome, and neither is automatically an Incident. If the attempt exposes data or causes operational impact, responders may open an **Incident** referring to the Run and supporting signals.

## Example 4: Degraded but completed run

A Run completes and returns an answer, satisfying its runtime completion condition. A relevance Evaluation fails, while a fallback Reliability Event shows that the primary retrieval service was unavailable.

The Run can therefore be operationally completed, quality-failing, and degraded at the same time. These claims are not collapsed into one status.

## Example 5: Scheduled memory maintenance

A scheduled Request starts a Run without a human user. A Step reads stale records through Memory Operations, uses an LLM Interaction to summarize them, and writes a compact representation through another Memory Operation.

The local variables used during summarization are not Memory merely because they contain state. The persistence boundary makes the operations memory-related.

## Example 6: Ad hoc execution

A developer directly invokes a one-off model experiment. The occurrence is still a Run even when no registered Workflow definition exists. The Run contains a Request, one Step, a Prompt, an LLM Interaction, and an Evaluation.

This allows local experiments and framework-neutral traces without inventing a fake reusable Workflow.
