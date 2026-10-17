# Sidecar correlation convention v1

**Non-normative implementation draft, 2026-10-17.** This records the native
`sidecar.correlation/1` convention tested by Sidecar 0.8.0 and Lens 0.7.1. It does
not promote any AIOS layer or establish stable schema conformance. Formal scope,
intent and decision/audit schemas remain Sidecar v1.0 coordination work.

`schema.json` is generated from Sidecar's DecisionEvidence model; `example.json`
is the same fixture used by both producers and consumers. It preserves the
original decision ID/status/rationale/causal link, boundary, tool name, timestamp,
policy fingerprint and journal source event; host-supplied run/trace/span IDs
identify the exact Lens target. Logical system/task/agent IDs are additive scope
identity, not granted authority or proof of task access.

Shared context applies to all agents within a declared system/task; Exclusive
context is assigned to designated agents. Shared and applicable exclusive
guardrails must all pass; local rules cannot weaken shared restrictions. Context
transport and enforced restrictions are separate. Private-context lifecycle and
delegation validation remain v0.9 work. The harness authenticates identities.

A decision projection is not an execution receipt. Actual dispatch/completion,
approval actors and stop acknowledgements remain in the complete Sidecar journal.
Sidecar and Lens verify native sequence/task/hash links before correlation;
without an external anchor, a hash chain cannot prevent a producer rewriting its
whole history. Reasons may contain sensitive data; readers need authorization.
Tower retains separate deployment health; Evals owns scoring; Chaos owns faults;
MCP owns tool transport. No implementation dependency is added to this spec.
