# Shared Review Scenarios

These scenarios are the common acceptance test pack for `v0.1` through `v0.4`.

Use the same scenarios across all compared frameworks so differences in interpretation are visible.

## Included scenarios

- `scenario-01-customer-support.md`
  Normal request, retrieval, answer, and evaluation.
- `scenario-02-retry-and-recovery.md`
  Failed first attempt, retry, and successful completion.
- `scenario-03-safety-and-incident.md`
  Safety detection, policy block, and possible incident escalation.

## What reviewers should extract

- `v0.1`
  Object classification and boundaries.
- `v0.2`
  Relationship graph and ordering semantics.
- `v0.3`
  Canonical event interpretation and extension needs.
- `v0.4`
  Structurally valid artifacts and edge-case behavior.
