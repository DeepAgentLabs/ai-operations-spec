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

## Example native report fragment (Evals 0.9.0)

```json
{
  "summary": {
    "judge": {"judge_scores": 2, "unavailable_scores": 1, "unavailable_cases": ["refund-policy"]},
    "live": {"total_cases": 3, "ok_cases": 2, "timed_out_cases": 1, "error_cases": 0,
             "timed_out_case_ids": ["slow-lookup"]}
  },
  "cases": [
    {"case_id": "refund-policy", "passed": false, "target_status": "ok",
     "scores": [{"name": "faithfulness", "value": 0.0, "passed": false,
                 "evaluator_type": "llm_rubric",
                 "metadata": {"judge_status": "unavailable", "judge_attempts": 3,
                              "judge_error": "TimeoutError: judge provider timed out"}}]},
    {"case_id": "slow-lookup", "passed": false, "target_status": "timed_out",
     "target_attempts": 2, "target_error": "TimeoutError: Python target timed out after 20 s",
     "scores": [{"name": "target_call", "value": 0.0, "passed": false}]}
  ]
}
```

The intended (non-normative) handling for the v0.10 export:

- `refund-policy`: the `faithfulness` judgment was never made. It must not
  become an `evaluation` object with a passing result. Either omit it and report
  it as unexported, or export it with a result stating that no verdict was
  available. Exporting it as a pass is never allowed.
- `slow-lookup`: the target produced no output, so there is nothing to evaluate
  and no run step for an `evaluates` relationship to target. The `target_call`
  score is a harness outcome, reported rather than exported as an evaluation
  of the run.

No specification, schema or conformance-rule change is required now. Any
normative mapping will be proposed with the v0.10 export. See the
[Evals guide](https://github.com/DeepAgentLabs/agentic-evals/blob/v0.9.0/docs/judge-reliability.md).
