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

Feature completion expectations:

- Every spec or schema behavior change must include tests or fixtures.
- Normative or user-guiding changes should include or update realistic
  examples in the same proposal.
- If a roadmap or milestone item is completed or its status changes, update
  `README.md` and `ROADMAP.md` in the same pull request.

Do not mark an acceptance gate complete without recorded evidence. External review gates require evidence from an independent implementation or standard, not only internal agreement.

## Validation

```bash
uv sync --extra dev
uv run pytest
```

## Tagging draft snapshots and releases

Snapshot repo state with **git tags**, not zip archives. GitHub already
generates a downloadable source zip/tarball for every tag or release, so
committing archives into the repo only adds undiffable bloat.

- `specification/v0.4/conformance.md` asks implementers to cite claims like
  *"aligned with v0.4-draft as observed on 2026-07-21"*. That citation is
  only checkable if the repo state on that date is retrievable — that's
  what a tag is for.
- Use `vX.Y-draft-YYYY-MM-DD` for an informal, citable snapshot of an
  in-progress milestone (draft content keeps moving, so date-stamp it).
- Reserve the bare `vX.Y` tag for when a milestone's acceptance criteria
  (see each milestone's `acceptance-criteria.md`) are fully checked and the
  layer actually freezes — that tag then means something stable, not a
  moving draft.
- Attach a GitHub Release on top of a tag once it's worth announcing
  externally (e.g. summarizing which acceptance gates closed); not required
  for every draft snapshot.
