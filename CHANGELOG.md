# Changelog

Repository releases of the AI Operations Specification. A repository tag
snapshots the documents, schemas, catalogs, and fixtures; it does not by
itself change any milestone's review status (see [ROADMAP.md](ROADMAP.md)).

## [Unreleased]

## [0.6.1] - 2026-10-31

### Added

- `specification/v0.6/provenance.md`: exploratory `0.6-draft` provenance
  records — subjects (with optional `sha-256`/`sha-384`/`sha-512` digests of
  exact bytes), source references (`aios_object`, `artifact`, `document`,
  `dataset`, `log`, `tool_output`, `human_input`), derived findings and
  evidence lineage (`derived-from`, `supports`, `contradicts`, `supersedes`).
- `specification/v0.6/schemas/provenance.schema.json`, reusing the
  `0.4-draft` common definitions, and the canonical
  `examples/provenance/support-finding.provenance.json`.
- `specification/v0.6/provenance-rules.json`: `AIOS-0.6-R01`–`R07` producer
  rules, `C01`–`C08` consumer rules (including a new `cross_artifact` check
  kind), `D01`, `K01` and `S01`.
- `specification/v0.6/conformance-suite/`: 41 outcome cases with expected
  rule citations and 5 cross-artifact resolution cases, plus the expected
  validator behavior.
- `specification/v0.6/naming-conventions.md` and
  `tests/test_naming_conventions.py`.
- Decision `D-006`: provenance is a companion artifact under its own marker.
- `.gitattributes` keeps JSON fixtures LF-only so digests are reproducible.

### Changed

- `specification/v0.5/compatibility.json`: every published schema set lists
  its `artifact_types`; a new `0.6-draft` set validates provenance records and
  declares `depends_on: ["0.4-draft"]`. The `0.4-draft` set is otherwise
  unchanged.
- Repository reference checks cite rule IDs. Step end-before-start timestamps
  are now checked under `AIOS-0.4-P04`, and missing endpoints and unmarked
  Workflow references cite `AIOS-0.4-X01`, matching deep-agentic-core-mcp.

### Notes

- Run and Workflow artifacts stay `0.4-draft`; no v0.4 schema, catalog or
  closed vocabulary changed, and no milestone's review status changed.
- Consumers that do not check `0.6-draft` must keep rejecting provenance
  records under `AIOS-0.5-V03`. See `docs/v0.6.1-ecosystem.md`.

## [0.6.0] - 2026-10-19

### Added

- Exploratory v0.6 canonical examples and extension model: minimal Workflow and
  Run, advanced support graph, retries and schema/semantic negative controls.
- Machine-readable fixture manifest and offline validation tests.
- Third-party extension placement, naming, preservation, versioning, publication
  and interpretation guidance, with sibling compatibility documentation.

### Changed

- Included from the prior `[Unreleased]` section: `reviews/framework-mappings/agentic-chaos.md`: Agentic Chaos 0.6.0 addendum.
  Covers the additive native call log and `unhandled_error`, the two new members
  of the `io.deepagentlabs.agentic-chaos` extension, and why chaos contract
  verdicts are producer-native rather than AIOS `evaluation` objects. No schema,
  catalog or core object change.

### Notes

- Artifacts remain `0.4-draft`. No schemas, catalogs, closed vocabularies or
  prerequisite review status change. Portable conformance and provenance objects
  remain v0.6.x work. Sibling runtime dependencies and releases are not required.


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
