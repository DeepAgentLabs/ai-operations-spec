# v0.6 — Canonical Examples, Extension Model and Provenance

## Status

Exploratory draft. This layer cannot freeze before v0.1–v0.5 and independent
review. Repository releases v0.6.0 and v0.6.1 do not close decision D-001 or
establish stable conformance.

Run and Workflow artifacts continue to declare `spec_version: "0.4-draft"`.
The only artifact this layer adds is the provenance record, which declares
`spec_version: "0.6-draft"` and `artifact_type: "provenance"`; see
[compatibility.json](../v0.5/compatibility.json) for the schema set behind
each marker.

## Documents

Repository v0.6.0:

- [Extension model](extension-model.md): placement, namespaces, preservation,
  evolution and third-party publication requirements.
- [Canonical examples](examples.md): minimal and advanced artifacts, negative
  controls and expected validation behavior.
- [Example manifest](examples/manifest.json): offline fixture paths and outcomes.

Repository v0.6.1 (the first v0.6.x increment):

- [Provenance records](provenance.md): subjects, source references, derived
  findings and evidence lineage as a companion artifact, with its
  [schema](schemas/provenance.schema.json) and
  [rule catalog](provenance-rules.json) (`AIOS-0.6-*`).
- [Portable conformance suite](conformance-suite/README.md): fixtures with
  expected outcomes and rule citations for the v0.4 rules, v0.5 routing and
  v0.6 provenance rules, plus cross-artifact resolution cases.
- [Naming conventions](naming-conventions.md): field, vocabulary,
  abbreviation and rule-identifier rules for specification-defined names.

- [Acceptance criteria](acceptance-criteria.md): remaining review gates.

The v0.4 schemas and semantic conformance rules remain authoritative for Run
and Workflow validation. This layer adds no runtime objects to Runs, no event
names and no dependency requirements. Migration guides, an OpenTelemetry
binding, verification-signal and audit-event shapes remain later v0.6.x work.
