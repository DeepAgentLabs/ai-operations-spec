# Review Artifacts

These artifacts are AIOS `v0.4-draft` review examples derived from real sibling-project outputs in this workspace.

They are intended as producer-evidence fixtures for review and conformance work.

## Included artifacts

- `agenticlens-support-run.aios.json`
  Derived from `agenticlens/examples/artifacts/support-run.json`
- `agentic-chaos-customer-support.aios.json`
  Derived from `/tmp/agentic-chaos-review-report.json`
- `*.conformance.json`
  Saved AIOS conformance results for the derived review artifacts

## Important note

These are reviewed mapping artifacts, not proof that the native producer formats are already identical to AIOS.

They demonstrate that:

- meaningful AIOS-aligned `run` artifacts can be derived from real producer output
- the current AIOS draft can express runtime structure, retries, degradation, tools, and reliability evidence from both sibling implementations
- both derived artifacts passed schema and semantic conformance checks on 2026-08-09
