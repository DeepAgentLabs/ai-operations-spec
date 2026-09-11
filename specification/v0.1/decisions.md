# v0.1 Design Decisions

> **Note:** `D-00x` IDs in this file are a separate numbering series from
> [`reviews/decision-log.md`](../../reviews/decision-log.md)'s milestone
> review decisions — the two files both start at `D-001` but track different
> kinds of decisions (core-model design here vs. review-gate outcomes there).
> Cite the file alongside the ID to avoid ambiguity.

## D-001: Use `Run`

**Decision:** Use **Run**, not `WorkflowRun`.

**Reason:** A Run may execute an ad hoc process without a registered Workflow. `WorkflowRun` would incorrectly imply that every execution has a Workflow definition.

## D-002: Treat MCP as an integration protocol

**Decision:** MCP is not a v0.1 core runtime concept.

**Reason:** A Tool Invocation describes the occurrence regardless of whether MCP, a direct function call, HTTP, or another integration carries it.

## D-003: Use `Model Interaction`

**Decision:** Use **Model Interaction** as the general occurrence. Model family and modality are attributes; an LLM call is one kind of Model Interaction.

**Reason:** The same operational boundary applies to language, multimodal, embedding, reranking, and future model endpoints.
