# MCP 0.4.0 unified workflows

[MCP 0.4.0](https://github.com/DeepAgentLabs/mcp-server/releases/tag/v0.4.0) completes Phase 4 with its unified workflows: `core.compare_runs`, a fail-closed `core.release_check`, `core.incident_summary` and `core.export_report`. MCP judges nothing itself; it composes Lens comparisons, the Evals release gate and Chaos run reports. Malformed or failed-call evidence always blocks readiness, and so does missing evidence of a required kind; all three kinds are required by default and `required_evidence` narrows that.

## Export envelope

- `schema_version: "mcp.unified-report.v1"`, with `generator`, `session_id`, and
  the session's workflow, analysis, comparison, chaos, release-check, incident and
  history sections in their producers' shapes.
- It is not an AIOS artifact and carries no AIOS conformance claim.

## Example

A not-ready export where chaos evidence was required but never supplied
(producer sections abbreviated; `comparison` is a Lens `ComparisonReport` plus
MCP's `ok` flag, `chaos` would be a `chaos.run_experiment` report):

```json
{
  "schema_version": "mcp.unified-report.v1",
  "generator": {"name": "io.github.DeepAgentLabs/deep-agentic-core-mcp", "version": "0.4.0"},
  "session_id": "release-42",
  "workflow": null,
  "analysis": null,
  "comparison": {"ok": true, "schema_version": "1.0", "regressions": [], "regression_threshold": 0.05},
  "chaos": null,
  "release_check": {
    "ok": true,
    "ready": false,
    "required_evidence": ["comparison", "evaluation", "chaos"],
    "missing_evidence": ["chaos"],
    "gates": [
      {"name": "comparison", "status": "passed", "passed": true, "reasons": [], "observed": {"regression_count": 0}},
      {"name": "evaluation", "status": "passed", "passed": true, "reasons": [], "observed": {"pass_rate": 1.0}},
      {"name": "chaos", "status": "missing", "passed": false, "reasons": ["No chaos evidence supplied or stored"], "observed": {}}
    ]
  },
  "incident_summary": null,
  "history": [{"tool": "core.compare_runs", "ok": true, "at": "2026-10-19T22:00:00+00:00"}]
}
```

None of this is AIOS data: `release_check` and the envelope are MCP-defined,
and the embedded sections are Lens, Evals and Chaos native shapes.

## Future specification work

If release evidence needs to travel between packages, define it here first (gate
statuses, evidence references and provenance), then have MCP export it.

## Compatibility

No specification change or release. AIOS validation and conformance in MCP are
unchanged.

See the [MCP unified workflows guide](https://github.com/DeepAgentLabs/mcp-server/blob/v0.4.0/docs/unified-workflows.md).
