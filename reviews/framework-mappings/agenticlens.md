# AgenticLens Review Mapping

- Framework: `agenticlens`
- Reviewer: Codex
- Date: 2026-08-09
- Version or commit: local workspace checkout

## Scenario coverage

- [x] `scenario-01-customer-support.md`
- [x] `scenario-02-retry-and-recovery.md`
- [~] `scenario-03-safety-and-incident.md`

`agenticlens` has direct evidence for customer-support, retrieval, tools, hierarchical traces, retry analysis, and AIOS draft conformance tooling. Safety and incident semantics are named in high-level docs, but this review pass did not find a first-class native trace example that exercises them end to end.

## Evidence reviewed

- `README.md`
- `docs/aios-validation-and-otel.md`
- `schemas/trace.schema.json`
- `src/agenticlens/models/trace.py`
- `examples/rag_customer_support_demo.py`
- `examples/multiagent_support_demo.py`
- `examples/operational_intelligence_demo.py`
- `tests/test_trace.py`

## Executable evidence

Generated a local AgenticLens trace artifact:

- command: `UV_CACHE_DIR=/tmp/uv-cache uv run python examples/operational_intelligence_demo.py`
- output artifact: `agenticlens/examples/artifacts/support-run.json`

Attempted AIOS conformance:

- command: `UV_CACHE_DIR=/tmp/uv-cache uv run agenticlens conformance examples/artifacts/support-run.json --version 0.4 --spec-root ../ai-operations-spec`
- result:
  `artifact_type` is missing, so the native AgenticLens trace artifact is not directly an AIOS `run` or `workflow` artifact

This is an important review finding:

- `agenticlens` is a strong implementation evidence source for runtime meaning
- `agenticlens` already contains AIOS validation tooling
- but its native trace JSON is not yet equivalent to a frozen AIOS artifact format

## v0.1 concept classification

### Scenario 01: Customer support

Strong alignment:

- `Run`
  Maps well to AgenticLens trace `Run` and to the profiler-level workflow execution record.
- `Request`
  Present conceptually in the examples as the user question, but not yet a first-class native trace object in the `trace` schema.
- `Step`
  Maps strongly to `step()` profiler steps and approximately to trace spans for execution occurrences.
- `Model Interaction`
  Maps strongly to `SpanType.MODEL_CALL` and LLM profiler steps.
- `Prompt`
  Present in profiler examples and can be captured or referenced, but is not required by the native trace schema.
- `Context`
  Present conceptually through retrieved chunks and duplicated-context analysis, but not a first-class standalone trace object.
- `Tool Invocation`
  Maps strongly to `SpanType.TOOL_CALL` and tool-oriented step metadata.
- `RAG Retrieval`
  Maps strongly to `SpanType.RETRIEVAL` and retriever examples.
- `Evaluation`
  Present strongly at the product level through evaluation suites and findings, though not a dedicated span type in the trace schema.

Partial alignment:

- `Agent`
  Supported through `agent_name` metadata and multi-agent examples, but not as a top-level native object.
- `Memory Operation`
  Maps strongly to `SpanType.MEMORY_READ` and `SpanType.MEMORY_WRITE`.
- `Safety Signal`
  Mentioned in the README as a runtime area, but not evidenced here as a dedicated native trace object.
- `Reliability Event`
  Represented operationally through retry analysis, failures, span status, and error metadata rather than a dedicated first-class object.
- `Incident`
  Not evidenced as a first-class native trace object in the reviewed files.

Conclusion for `v0.1`:

- AgenticLens supports most runtime occurrences AIOS cares about.
- It is strongest on execution evidence, retrieval, memory, tools, retries, and evaluations.
- It is weaker on first-class native objects for `Request`, `Safety Signal`, `Reliability Event`, and `Incident`.

## v0.2 relationship notes

Strong alignment:

- containment
  Native trace spans support parent-child hierarchy through `parent_span_id`
- graph integrity
  native validation rejects unknown parents and cycles
- delegation
  supported by `SpanType.DELEGATION` and multi-agent examples
- retry linkage
  supported by `SpanType.RETRY`, `retry_number`, and retry attribution analysis

Partial alignment:

- causal dependency between sibling steps
  hierarchy is strong, but generalized causal relationships beyond parentage are not expressed as a separate native relation model
- joins, branches, and equivalent execution graphs
  examples imply them, but the native trace structure is closer to a tree plus span metadata than to the full AIOS relationship vocabulary

Conclusion for `v0.2`:

- AgenticLens is good evidence that hierarchy, retries, and delegation matter.
- It is not yet full proof that two independent implementations will reconstruct the same execution graph semantics, especially for non-tree relationships.

## v0.3 semantic event notes

Strong alignment:

- lifecycle meaning
  runs and spans have explicit statuses and times
- transport boundary awareness
  docs clearly separate AIOS semantics from OTLP export
- extension awareness
  the project can export OTLP while also validating AIOS draft artifacts

Partial alignment:

- canonical AIOS event names
  AgenticLens trace artifacts are span-oriented and status-oriented, not expressed natively as the AIOS `aiops.*` event catalog
- event coverage for safety and incident semantics
  not directly demonstrated in reviewed examples

Conclusion for `v0.3`:

- AgenticLens provides strong evidence for the need for transport-neutral semantics.
- It also supports the AIOS position that transport bindings should remain separate from core meaning.
- It does not yet prove native adoption of the AIOS canonical event namespace.

## v0.4 artifact notes

Strong alignment:

- structured, validated local JSON artifacts exist
- native trace schema enforces identity and parent-reference integrity
- AIOS `validate` and `conformance` tooling is implemented in AgenticLens

Key finding:

- the native `trace.schema.json` artifact is not itself an AIOS `run` artifact
- conformance failed on the generated demo trace because `artifact_type` was missing and the payload was not in AIOS artifact shape

Implication:

- AgenticLens is currently best treated as:
  - a source of execution evidence for AIOS design review
  - a validator/consumer of AIOS artifacts
  - a partial producer candidate if an explicit AIOS export layer is added

## Reviewer summary

- Equivalent meaning achieved:
  partial but meaningful
- Ambiguities:
  `Request`, `Safety Signal`, `Reliability Event`, and `Incident` are not yet strongly represented as first-class native trace objects in the reviewed evidence
- Changes requested:
  add or document an explicit AIOS export path from AgenticLens traces to AIOS `run` artifacts, and add at least one safety/incident example if AgenticLens is going to be used as a formal AIOS review implementation
