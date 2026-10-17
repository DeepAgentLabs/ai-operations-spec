# Sidecar 0.8 integration boundary

## Sidecar 0.8 interoperability

The native sidecar.correlation/1 convention is recorded in
[drafts/sidecar-correlation-v1](../drafts/sidecar-correlation-v1/README.md), with a
validated producer/consumer fixture. This is non-normative and does not promote
AIOS maturity or add a runtime dependency.

Sidecar 0.8 provides Shared/Exclusive context-only, guardrails-only or combined
configuration, explicit host context delivery and mandatory guardrail composition.
Exclusive rules cannot weaken shared restrictions. Cross-framework privacy,
revocation and delegated authority remain v0.9 validation; stable schemas remain
v1.0. Native correlated Lens readback requires Lens 0.7.1. All sibling packages
stay optional; no dependency floor is increased without a runtime requirement.
See the [Sidecar integration contract](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/docs/integrations.md).
