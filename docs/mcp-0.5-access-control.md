# MCP 0.5.0 hosted access control

[MCP 0.5.0](https://github.com/DeepAgentLabs/mcp-server/releases/tag/v0.5.0) completes MCP Phase 5 with hosted access control. Each hosted key can carry allow and deny tool globs, an expiry and a task scope. The server enforces them at dispatch, outside the model: before each hosted handler runs, it re-authenticates the key and reloads its policy. Revocation, a narrower policy or expiry therefore stops queued calls, retries and calls on existing connections. Calls already running finish. Denied calls return an MCP-local `mcp.access-decision.v1` record, and every hosted call logs `dispatch`/`completion` records that share a `correlation_id`. These records are not AIOS artifacts. `core.access_status` reports a key's effective policy, and operators use `deep-agentic-core-mcp-admin` to narrow or revoke a key by user ID.

## What changes for the specification

- Nothing normative. MCP 0.5.0 adds no AIOS object or schema, and the
  `0.4-draft` and `0.6-draft` conformance results are unchanged.
- MCP emits access decisions as an MCP-local `mcp.access-decision.v1` record with
  `event` (`dispatch`, `completion`, `denial` or `revocation_acknowledged`),
  `decision`, `correlation_id`, `subject`, `tool`, `task_id`, `reason` and
  `outcome`. It is a candidate input for a future AIOS authority and
  access-evidence proposal, which MCP Phase 6 would then emit or map to. Until
  that proposal is accepted, the record is not an AIOS artifact.

## Compatibility

No spec change or release.

See the [MCP hosted access control guide](https://github.com/DeepAgentLabs/mcp-server/blob/v0.5.0/docs/access-control.md).
