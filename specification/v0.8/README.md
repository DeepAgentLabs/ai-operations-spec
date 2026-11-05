# Operational artifacts — 0.8-draft

Exploratory draft, delivered in repository v0.8.0 as the remaining operational
artifact increment of roadmap Phase 6.x. Prerequisite v0.1–v0.6 reviews remain
open; this directory is a companion schema family, not a replacement edition.

- [Verification signals](verification-signals.md): second-opinion results,
  confidence, grounding and explicit safety assessment state.
- [Audit events](audit-events.md): attributed actions, target references,
  occurrence/recording times and native outcomes.
- [Investigation reports](investigation-reports.md): incident context,
  operator summaries, evidence-cited findings, timelines and recovery state.
- [Conformance](conformance.md), [rule catalog](operational-rules.json),
  [acceptance criteria](acceptance-criteria.md) and
  [implementation evidence](../../reviews/operational-artifact-mappings.md).
- [Ecosystem adoption and migration](../../docs/v0.8.0-ecosystem.md).

The new families declare `spec_version: "0.8-draft"`; Run and Workflow remain
`0.4-draft` and provenance remains `0.6-draft`. No new v0.4 object type, event
name or field is added. Every artifact type has its own schema; common
operational definitions live in [common.schema.json](schemas/common.schema.json).
The family reuses the v0.4 reverse-domain extension definition. Register both
schema sets by `$id` for offline validation.

The [portable suite](../v0.6/conformance-suite/README.md) includes positive,
schema-negative, semantic-negative and unsupported-marker examples. Repository
reference checks are test code; no runtime SDK or automatic exporter ships here.

Every operational envelope includes a required source reference identifying the
native record being projected. This is distinct from a verification subject or
audit target. Retain the original native record under that identity; the
projected artifact id identifies the companion, not its native source.
