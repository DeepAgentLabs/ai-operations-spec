# Evals 0.10.0 evaluation evidence export

[Agentic Evals 0.10.0](https://github.com/DeepAgentLabs/agentic-evals/releases/tag/v0.10.0)
exports its native evaluation reports as v0.4-draft `evaluation` evidence and
attaches them to an existing `run` artifact:

- `to_aios_evidence(report, run_id=..., targets=..., gate=...)` produces one
  `evaluation` per score, one per case verdict and, optionally, one
  `release_gate` evaluation of the Run. `attributes` carry `criterion`,
  `method` (evaluator, version and type), `result` and `score`.
- Every evaluation gets an `evaluates` relationship to each target the caller
  maps its case to. The export raises rather than emit an evaluation with no
  target (rule `AIOS-0.4-P08`).
- `attach_aios_evidence(run, export)` resolves every non-external target with
  its declared type (`AIOS-0.4-P05`) and rejects reused IDs (`P02`, `P03`).
- Events are `aiops.evaluation.completed`, or `aiops.evaluation.failed` when the
  judge could not deliver a verdict. Their `attributes` identify method,
  criterion, targets and result, as the v0.3 semantic conventions require.

This follows the handling proposed in the
[Evals 0.9.0 note](evals-0.9-judge-reliability.md):

- an unavailable judgment is exported with result `unavailable` and no score,
  never as a pass. A skipped score is `skipped`, with no score and no event
- a case with no observed output (no sample, or a live target that timed out
  or errored) is not exported. Its `target_call` score describes the harness,
  not the Run, and the case is reported in `unobserved_cases`
- judge cost stays in the evaluation's attributes and is never added to the
  Run's own `measurements`

## Example evaluation (from the Evals example)

```json
{
  "id": "support-run-042:evals:support-refunds:refund-tool:score:2",
  "type": "evaluation",
  "name": "tool_args:refund on Refund issued with an order ID",
  "status": "failed",
  "attributes": {
    "criterion": "tool_args",
    "method": {"evaluator": "agentic_evals.builtin", "evaluator_version": "0.10.0", "evaluator_type": "deterministic"},
    "result": "failed",
    "score": 0.0
  },
  "extensions": {"io.deepagentlabs.agentic-evals": {"producer": "agentic-evals", "producer_version": "0.10.0", "report_schema_version": "1.0"}}
}
```

The merged run is checked in as
[a review artifact](../reviews/artifacts/agentic-evals-support-run.aios.json).
It passes this repository's schema and semantic checks and MCP's
`spec.validate_artifact` (`conformance.aligned = true`).

## Status

- Producer-side alignment with the v0.4 draft only. It is not stable
  conformance and makes no claim about the scored behavior.
- No specification, schema or conformance-rule change. The mapping (criterion,
  method, result and score under `attributes`) is producer-defined, which
  `attributes` allows. A normative evaluation attribute vocabulary remains a
  future specification decision.
- Evals vendors the v0.4 run schemas in its tests and compares them with this
  repository when a checkout is present. A schema change here should be
  copied there.

See the [Evals guide](https://github.com/DeepAgentLabs/agentic-evals/blob/v0.10.0/docs/aios-evidence.md).
