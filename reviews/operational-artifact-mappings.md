# Operational artifact implementation evidence

Source inspection on 2026-11-04 establishes a shared need across implementations.
These are internal design inputs, not independent acceptance evidence or claims
that the packages emit 0.8-draft today. Examples are explicit synthetic projections.

| Producer / pinned source | Observed fields | Draft mapping | Limits |
| --- | --- | --- | --- |
| [agenticlens](https://github.com/DeepAgentLabs/agenticlens/blob/23563ec8bb72e434fae2802528e565e10e87e0ad/src/agenticlens/evaluation/judging.py) | JudgeVerdict.verdict/confidence/unsupported_claims/evidence_missed; explicit judge-model metadata | verification_signal | No safety result exists in this native shape; safety is not_checked. partially_agree maps to partially_supports. A grounded claim needs separately supplied evidence references. |
| [agentic-evals](https://github.com/DeepAgentLabs/agentic-evals/blob/e0d7e02a62c4fd749b5446629e66d071fe9cf59b/src/agentic_evals/judging.py) | is_unavailable() and judge_status; JudgeResponse usage | verification_signal | An unavailable judgment has no verdict/confidence. Usage or a report score alone is insufficient to construct a completed verification signal. |
| [agentic-sidecar](https://github.com/DeepAgentLabs/agentic-sidecar/blob/34a37b3df97f48b3d6b593a9c6aab8c705ed53de/src/agentic_sidecar/core/provenance.py) | AuditRecord.decision_id/timestamp/outcome/trigger/causal_link | audit_event | Actor may be unknown; BLOCK denotes denial at the boundary. ALLOW is no execution receipt. Omit raw arguments and execution_context. Native Sidecar audit records are not provenance records. |
| [mcp-server](https://github.com/DeepAgentLabs/mcp-server/blob/61db7e8942a9fddaed85905a55fa8ac98fd1f0a7/src/deep_agentic_core_mcp/services/access_evidence.py) | mcp.access-decision.v1: event, subject, tool, recorded_at, correlation_id | audit_event | dispatch maps to started; denial/revocation_acknowledged map to denied for one dispatch. recorded_at is the emitter observation time. Completion needs a native outcome before mapping success. Actor attribution is a logical service subject, not proof of authentication. |
| [agenticops-control-tower](https://github.com/DeepAgentLabs/agenticops-control-tower/blob/0089c84d581f931b164e6d777114ac4a17d53748/src/agenticops_control_tower/incidents/models.py) | Investigation.finding/certainty/citations/missing/timeline; Incident.state/events | investigation_report | observed_failure maps to observed, hypothesis remains hypothesis. Native evidence ids become report-local references; missing maps to missing_evidence_items. Do not infer recovery from incident closure. Projecting native state requires an explicit mapping. |
| [agentic-chaos](https://github.com/DeepAgentLabs/agentic-chaos/blob/e4ebf1b98e5a1b66dbbba38bc655f7bee9023b17/src/agentic_chaos/models/report.py) | Native chaos reports and producer-owned resilience evidence | investigation_report evidence input | Fault injection and recovery observations remain native evidence, not authorization or judge verdicts. No generic Chaos report replacement is defined. |

The common report requirement is evidence-cited operator interpretation: Tower
Investigations consume native timelines while Lens supplies findings and Chaos
supplies resilience observations. investigation_report is the bounded shared
shape. A universal report or native report-schema replacement remains out of
scope because source inspection does not establish that need.

## Mapping requirements

Projectors supply producer/version, recording time and stable projected ids.
Preserve source artifact identity and format in references and native outcomes
in the projected record. If an input does not contain enough observations,
record explicit unknown/unavailable state or decline the projection. Never
copy private payloads into attributes or extensions to avoid the closed wrapper.
No automatic adapter is introduced and no independent review gate closes.
