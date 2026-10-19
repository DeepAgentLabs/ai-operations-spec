# Evals 0.9.0 judge reliability and live resilience

[Agentic Evals 0.9.0](https://github.com/DeepAgentLabs/agentic-evals/releases/tag/v0.9.0) adds optional judge and live-target fields to
its package-local native report contract (schema `1.0`): `summary.judge`
(judge cost, unavailable judgments, agreement), `summary.live` (retried,
timed-out and errored cases) and `cases[].target_status`.

These are not AIOS evaluation evidence and make no conformance claim. They
inform the planned Evals v0.10 export to v0.4 `evaluation` evidence objects:

- an unavailable judgment (`judge_status: "unavailable"`) records that no
  verdict was made. Exporting it as a passing evaluation would violate the
  export's "state only what the report records" rule;
- a `timed_out` or `error` live case has no observed output to evaluate. Its
  outcome describes the evaluation harness, not the run under evaluation;
- judge cost is the cost of evaluating, kept apart from the run's own cost.

No specification, schema or conformance-rule change is required now. Any
normative mapping will be proposed with the v0.10 export. See the
[Evals guide](https://github.com/DeepAgentLabs/agentic-evals/blob/v0.9.0/docs/judge-reliability.md).
