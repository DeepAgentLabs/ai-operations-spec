# MCP 0.4.0 unified workflows

[MCP 0.4.0](https://github.com/DeepAgentLabs/mcp-server/releases/tag/v0.4.0) ships the first Phase 4 unified workflows: `core.compare_runs`, a fail-closed `core.release_check`, `core.incident_summary` and `core.export_report`. MCP judges nothing itself; it composes Lens comparisons, the Evals release gate and Chaos run reports, and missing, malformed or failed-call evidence blocks readiness.

## Export envelope

- `schema_version: "mcp.unified-report.v1"`, with `generator`, `session_id`, and
  the session's workflow, analysis, comparison, chaos, release-check, incident and
  history sections in their producers' shapes.
- It is not an AIOS artifact and carries no AIOS conformance claim.

## Future specification work

If release evidence needs to travel between packages, define it here first (gate
statuses, evidence references and provenance), then have MCP export it.

## Compatibility

No specification change or release. AIOS validation and conformance in MCP are
unchanged.

See the [MCP unified workflows guide](https://github.com/DeepAgentLabs/mcp-server/blob/v0.4.0/docs/unified-workflows.md).
