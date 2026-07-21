# Contributing

AI Operations Specification contributions should improve interoperability for independent producers and consumers.

## Where a change belongs

- Core meaning and object boundaries belong in v0.1.
- Execution graph semantics belong in v0.2.
- Transport-neutral event and attribute meaning belongs in v0.3.
- Machine-readable artifact structure belongs in v0.4.
- Premature experiments belong in `drafts/` and MUST identify themselves as non-conforming.
- SDK behavior, dashboards, storage, pricing, and package-specific recommendations belong in implementation repositories.

## Proposal expectations

A proposal SHOULD state the interoperability problem, affected concepts, compatibility impact, privacy implications, and at least one realistic example. Changes that affect an earlier layer MUST update dependent documents, schemas, fixtures, and tests in the same proposal.

Do not mark an acceptance gate complete without recorded evidence. External review gates require evidence from an independent implementation or standard, not only internal agreement.

## Validation

```bash
uv sync --extra dev
uv run pytest
```
