# Changelog

Repository releases of the AI Operations Specification. A repository tag
snapshots the documents, schemas, catalogs, and fixtures; it does not by
itself change any milestone's review status (see [ROADMAP.md](ROADMAP.md)).

## [Unreleased]

### Changed

- `reviews/framework-mappings/agentic-chaos.md`: Agentic Chaos 0.6.0 addendum.
  Covers the additive native call log and `unhandled_error`, the two new members
  of the `io.deepagentlabs.agentic-chaos` extension, and why chaos contract
  verdicts are producer-native rather than AIOS `evaluation` objects. No schema,
  catalog or core object change.

## [0.5.1] - 2026-10-13

### Added

- `specification/v0.4/conformance-rules.json`: machine-readable catalog that
  assigns a stable identifier to every MUST/MUST NOT/SHOULD obligation in the
  v0.4 conformance document: producer rules `AIOS-0.4-P01`–`P12`,
  external-reference rules `X01`–`X02`, consumer rules `C01`–`C04`, D-004
  closed-vocabulary rules `U01`–`U02`, extension naming `E01`, draft
  self-description `D01`, and claim format `K01`. Each rule quotes its
  normative sentence and says whether schema validation, semantic checks, or
  only a process obligation can decide it.
- `specification/v0.5/compatibility.json`: the `spec_version` marker grammar,
  the schema set published behind each marker (`0.4-draft` today), and
  identifiers `AIOS-0.5-V01`–`V06` for each row of the consumer compatibility
  table.
- `tests/test_conformance_catalogs.py`: fails if either catalog drifts from
  the normative Markdown it mirrors.

### Notes

- The Markdown documents remain normative; the catalogs only label what they
  already require. No schema, vocabulary, or milestone status changed.
- Released as a patch on the v0.5 line (`v0.5.1`) because it labels existing
  rules rather than adding normative content.
