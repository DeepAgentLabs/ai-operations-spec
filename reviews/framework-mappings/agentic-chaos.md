# Agentic Chaos Review Mapping

- Framework: `agentic-chaos`
- Reviewer: Codex
- Date: 2026-08-09
- Version or commit: local workspace checkout

## Scenario coverage

- [x] `scenario-01-customer-support.md`
- [x] `scenario-02-retry-and-recovery.md`
- [~] `scenario-03-safety-and-incident.md`

`agentic-chaos` strongly covers failure, retry, degradation, tool failure, memory corruption, and handoff corruption. It is weaker as direct evidence for first-class safety-signal and incident semantics because those remain closer to planned or adjacent resilience behavior than to a dedicated current object model.

## Evidence reviewed

- `README.md`
- `src/agentic_chaos/models/chaos_event.py`
- `src/agentic_chaos/models/report.py`
- `src/agentic_chaos/integrations/agenticlens.py`
- `examples/chaos_customer_support_demo.py`
- `examples/chaos_with_agenticlens_demo.py`
- `tests/test_report.py`
- `tests/test_agent_topology.py`
- `tests/test_integrations_agenticlens.py`

## Executable evidence

Generated a local standalone chaos report:

- command:
  `UV_CACHE_DIR=/tmp/uv-cache uv run agentic-chaos chaos run examples/chaos_customer_support_demo.py --inject rate_limit_storm,token_timeout,silent_degradation --save /tmp/agentic-chaos-review-report.json`
- output artifact:
  `/tmp/agentic-chaos-review-report.json`

Observed result:

- planner recorded three `rate_limit_storm` events and recovered after retries
- retriever recorded one `token_timeout` event and degraded to zero chunks
- final response recorded one `silent_degradation` event and returned corrupted content

This is strong direct evidence for retry, degraded completion, and reliability-event semantics.

## v0.1 concept classification

### Scenario 01: Customer support

Strong alignment:

- `Run`
  Maps cleanly to `ChaosReport`, a standalone report for one chaos execution.
- `Step`
  Represented indirectly through `step_id` and `step_name` correlation on each `ChaosEvent`.
- `Tool Invocation`
  Strongly represented by tool-targeted faults such as `tool_failure`.
- `RAG Retrieval`
  Strongly represented in the customer-support demo where the retriever is an explicit fault target.
- `Reliability Event`
  Very strong alignment. `ChaosEvent` is effectively a resilience/fault occurrence model with timestamp, outcome, message, and detail payload.

Partial alignment:

- `Request`
  Present narratively in examples but not a first-class native report object.
- `Model Interaction`
  Strong for fault injection against model-like calls, but not a generic first-class object separate from step correlation.
- `Prompt`
  Present as call input in examples, but not a first-class native report object.
- `Context`
  Present as payload or result of retrieval, but not modeled separately.
- `Memory Operation`
  Strongly implied by `memory_corruption` and memory-decay behavior, though the current report centers on the fault event more than on an independent memory-occurrence object.
- `Incident`
  Not yet a first-class report object; events can show impact or degradation without opening a separate incident object.

Weak alignment:

- `Evaluation`
  Present only indirectly through fidelity judges and optional scoring, not as a central standalone object in the base report.
- `Safety Signal`
  Adjacent in spirit to resilience validation, but not strongly evidenced as a dedicated current object in the reviewed files.
- `Agent`
  Topology tracking captures agents and edges well when enabled, but the base `ChaosReport` does not require agent objects.

Conclusion for `v0.1`:

- `agentic-chaos` strongly validates that AIOS needs distinct concepts for degraded completion, retries, tool failures, memory corruption, and reliability evidence.
- It is weaker as evidence for first-class request, evaluation, safety-signal, and incident objects.

## v0.2 relationship notes

Strong alignment:

- retry chains
  Explicitly demonstrated by repeated planner failures that later recover
- ordering
  Event timestamps and attempt counters provide clear sequence semantics
- step correlation
  `step_id` and `step_name` correlate each event to a runtime step
- topology edges
  `TopologyTracker` records agent, tool, and handoff edges
- handoff relationships
  edge-scoped corruption and `from_node` / `to_node` fields support non-node relationships

Partial alignment:

- generalized execution graph
  `agentic-chaos` can describe significant relationships and topology, but its native report is event-centric and resilience-centric rather than a full neutral graph of all runtime objects

Conclusion for `v0.2`:

- `agentic-chaos` is strong evidence that AIOS must represent retries, causal order, topology edges, and handoff corruption distinctly.
- It meaningfully strengthens the case for non-tree relationships beyond what a pure span tree provides.

## v0.3 semantic event notes

Strong alignment:

- event meaning is explicit
  `fault_type`, `outcome`, `message`, `timestamp`, and `detail` convey stable semantics
- degraded-versus-errored distinction
  outcomes such as `errored` and `degraded` stay distinct
- retry semantics
  rate-limit events include `retry_after`, attempt number, and recovery context
- edge semantics
  `edge_id`, `from_node`, and `to_node` support handoff-specific meaning

Partial alignment:

- canonical AIOS event namespace
  `agentic-chaos` uses its own fault/event vocabulary rather than native `aiops.*` names
- transport neutrality
  event meaning is portable, but not yet expressed as AIOS canonical event names

Conclusion for `v0.3`:

- `agentic-chaos` strongly supports the need for AI-native semantic events that are independent of transport.
- It also supports keeping transport mappings separate from the core semantic layer.
- It does not, by itself, prove adoption of the final AIOS canonical event catalog.

## v0.4 artifact notes

Strong alignment:

- standalone JSON artifacts exist with stable identifiers and timestamps
- event references to step identity are explicit
- optional topology can capture agent and handoff structure
- optional AgenticLens integration can merge `chaos_events` into a shared workflow artifact

Key findings:

- the native `ChaosReport` is not itself an AIOS `run` artifact
- it intentionally shares JSON shape with AgenticLens workflow artifacts for interoperability
- optional integration shows a practical path from resilience evidence into a broader shared artifact

Implication:

- `agentic-chaos` is a strong evidence producer for AIOS design review
- it is not yet a direct AIOS artifact producer in its standalone report format

## Agentic Chaos 0.6.0 addendum

Reviewed against `agentic-chaos` 0.6.0 (pytest plugin and chaos contracts).
Nothing below changes a core AIOS object, schema or catalog.

- The native `ChaosReport` gains three additive fields: `calls` (a bounded
  per-session log of instrumented calls with `step_name`, `status`,
  `started_at`, `duration_s` and the `fault_type`/`event_id` that hit them),
  `calls_dropped`, and `unhandled_error` (the exception that escaped the code
  under test). Older reports still load; the event shape and IDs are
  unchanged.
- `to_aios_run()` carries only `calls: {recorded, dropped}` and
  `unhandled_error` inside the existing `io.deepagentlabs.agentic-chaos`
  extension. Per-call records are not mapped to AIOS steps or occurrences, so
  the export still claims no retry chain or recovery the events cannot show.
  Exports validate against this repository's pre-release v0.4-draft run schema
  and semantic checker in agentic-chaos's sibling-integration CI job; this is
  draft alignment, not a stable conformance claim.
- Chaos contracts (`MaxRetries`, `NoRetryStorm`, `RecoveredAfterFailure` and
  others) are producer-native verdicts (`passed`, `failed` or `inconclusive`) over
  one chaos run. `MaxCostImpact` and `FullTopologyTraversal` also compare that run
  with an optional baseline report. Verdicts are serialized as the package's own
  JSON. They are **not** AIOS `evaluation` objects and make no
  conformance claim. They fail closed: a check that cannot be evaluated is
  `inconclusive` and does not pass.
- The call log is new direct evidence for retry and recovery semantics
  (a retry is a call to a step whose previous call raised). If AIOS later
  standardizes retry chains or evaluation verdicts, this is the producer data
  to review first.

## Reviewer summary

- Equivalent meaning achieved:
  strong for reliability, retries, degradation, topology edges, and resilience evidence
- Ambiguities:
  request, safety-signal, evaluation, and incident concepts are not yet first-class in the native standalone report
- Changes requested:
  add or document an explicit AIOS export path from `ChaosReport` to AIOS `run` artifacts, and add a safety/policy-oriented example if `agentic-chaos` will be used as formal evidence for those concepts

## Chaos 0.7.0 interoperability

Chaos 0.7.0 adds sequential fault cascades, deterministic monotonic breaking-point
search, synthetic response poisoning (including prompt/tool-response instruction
and policy-bypass payloads), and explicit-price retry cost estimates. Native
child event IDs and fault types remain intact; cascade IDs/stages and poisoning
strategy/payload/seed are additive event detail. Existing report readers and
AIOS exports remain compatible.

See the [v0.7 guide and offline synthetic example](https://github.com/DeepAgentLabs/agentic-chaos/blob/v0.7.0/docs/v0.7.md).
The example includes observed synthetic dispatches and a bypassed negative
control. Injection or recovery alone does not prove containment. No new shared
schema, automatic adapter, hosted execution capability or containment guarantee
is introduced.

These are producer-local extensions, not normative concepts or schema changes. Existing AIOS Run mappings preserve native evidence; specification maturity and conformance claims remain unchanged. No spec release is needed.
