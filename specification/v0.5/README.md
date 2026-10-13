# v0.5 — Versioning and Compatibility Rules

## Status

Exploratory draft. These rules test the v0.1 concepts, v0.2 relationships, v0.3 semantic conventions, and v0.4 schemas and cannot freeze before them.

## Goal

v0.5 defines how `spec_version` markers are formed, how a change to the specification is classified, what a consumer must do when it encounters an artifact from a different version, and how deprecation works once a version freezes. For a frozen `spec_version`, that marker alone is enough to decide safe consumption. For a `-draft` marker, the marker is necessary but not sufficient: per the draft volatility rule in [versioning.md](versioning.md), two artifacts can share the same `-draft` `spec_version` and still be incompatible, so a consumer also needs the observation date or snapshot tag that identifies the exact draft content.

## Central distinction

v0.5 separates two different questions that earlier milestones left implicit:

```text
Is this artifact structurally valid?      -> v0.4 schemas + conformance
May I safely consume this artifact given  -> v0.5 versioning and
its declared spec_version?                   compatibility rules
```

An artifact can be schema-valid under the schema it names and still be unsafe for an older consumer to treat as equivalent to what it already supports. v0.5 exists to make that distinction explicit instead of leaving it to each implementation to guess.

## What v0.5 defines

- the grammar for `spec_version` strings, including the `-draft` suffix
- how a change is classified as editorial, additive, or breaking
- why growing a closed vocabulary (decision `D-004`) is a breaking change, not an additive one
- the compatibility behavior a consumer MUST follow for same-version, draft, and cross-version artifacts
- the deprecation grace period and migration-note obligation that begin once a version freezes

## What v0.5 does not define

- the content of a specific migration guide between two frozen versions — that is a v0.6.x deliverable, produced once such a transition actually exists
- changes to the v0.4 schemas themselves (for example, turning the `spec_version` `const` into a multi-value pattern) — that remains blocked on the v0.4 freeze, which is blocked on the v0.1–v0.3 review gates
- a stable-release layout or packaging format — that is v1.0 scope

## Documents

- [Versioning and compatibility rules](versioning.md) is the normative text.
- [Compatibility catalog](compatibility.json) mirrors it for tooling: the `spec_version` grammar, the schema set published for each marker, and stable identifiers (`AIOS-0.5-V01` … `V06`) for each row of the consumer compatibility table.
- [Examples](examples.md) walks through valid/invalid version markers and change-classification scenarios.
- [Acceptance criteria](acceptance-criteria.md) defines when v0.5 is ready to freeze.

See decision `D-005` in [reviews/decision-log.md](../../reviews/decision-log.md) for the closed-vocabulary-growth classification this milestone depends on.
