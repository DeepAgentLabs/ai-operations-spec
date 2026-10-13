# Changelog

Repository releases of the AI Operations Specification. A repository tag
snapshots the documents, schemas, catalogs, and fixtures; it does not by
itself change any milestone's review status (see [ROADMAP.md](ROADMAP.md)).

## [Unreleased]

## [0.6.0] - 2026-10-13

### Added

- `specification/v0.4/conformance-rules.json`: machine-readable catalog that
  assigns stable identifiers to every v0.4 conformance requirement — producer
  rules `AIOS-0.4-P01`–`P12`, external-reference rules `X01`–`X02`, consumer
  rules `C01`–`C03`, and the D-004 unknown-value rule `U01` — each tagged with
  whether it is decidable by schema validation, semantic checks, or only as a
  process obligation.
- `specification/v0.5/compatibility.json`: the `spec_version` marker grammar,
  the schema set published behind each marker (`0.4-draft` today), and
  identifiers `AIOS-0.5-V01`–`V06` for each row of the consumer compatibility
  table.
- `tests/test_conformance_catalogs.py`: fails if either catalog drifts from
  the normative Markdown it mirrors.

### Notes

- The Markdown documents remain normative; the catalogs only label what they
  already require. No schema, vocabulary, or milestone status changed.
- The `v0.6.0` tag is a repository release number. The v0.6 *milestone*
  (canonical examples and extension model) is still planned.
