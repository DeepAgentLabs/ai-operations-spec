# Access evidence v1 — exploratory interoperability profile

This profile defines a namespaced extension, not a new AIOS artifact family or
normative event catalog. Existing Run artifacts retain `spec_version: 0.4-draft`.
Independent layer review is still required before promotion to the specification.

Producer observations use `io.deepagentlabs.access` with `format: access/1`,
`event_id`, `producer`, `subject`, `task_id` (nullable), `correlation_id`,
`occurred_at`, `kind`, `tool`, and optional `reason` and `outcome`.
Kinds are `dispatched`, `completed`, `denied`, and `revocation_acknowledged`.
A revocation acknowledgement here means a particular attempted dispatch was
rejected after reauthentication, not that all credentials or running calls stopped.
Sidecar's native stop acknowledgement remains separate and preserves running
invocations, revoker outcomes and audit failures. A request is never an effective
acknowledgement. A dispatch reservation is the start of in-flight work; its side
effects or completion can occur after acknowledgement and must be reported.

The extension retains producer attribution and source correlation IDs. Tool
arguments, credentials and credential hashes must be omitted. This profile does
not establish authorization, integrity, exhaustive capture or a containment score.
Authenticate the full ordered observation snapshot with Lens, and require verified
coverage for the expected stream. Missing, failed, unknown or incomplete evidence
cannot establish containment. Policy and configuration versions belong in the
scenario metadata. A negative control with bypassed enforcement must fail.

Example: MCP `dispatch` maps to `dispatched`, `completion` to `completed`,
`denial` to `denied`; the original `mcp.access-decision.v1` record stays intact.
A Run event uses the producer-namespaced event name and includes this object in
`extensions`; the Run's object references still follow the v0.4 semantic rules.
