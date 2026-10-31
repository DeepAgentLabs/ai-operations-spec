## AI Operations Specification Development Reference

## Ecosystem Context

### Role in DeepAgentLabs

`ai-operations-spec` is the center of gravity for DeepAgentLabs. It defines the
shared operational contract that the implementation packages compose around:
runtime objects, semantic conventions, schemas, examples, and maturity rules.

### Owns

- Normative definitions of shared concepts, relationships, and event meaning
- Versioned specification documents, schema layers, examples, and evolution
  rules
- Ecosystem-wide clarity about what an artifact means independent of any one
  package implementation

### Does Not Own

- Standalone output scoring and release-gate computation — those belong in
  `agentic-evals`; Lens owns the observability and evaluation workflows

- Instrumentation, profiling, dashboards, or evaluation workflows — those
  belong in `agenticlens`
- Fault injection and resilience experiment execution — those belong in
  `agentic-chaos`
- Agent supervision, escalation, or pre-action governance runtime behavior —
  those belong in `agentic-sidecar`
- At the ecosystem-role level, `agentic-sidecar` is the **SUPERVISE** layer,
  while its concrete runtime functionality spans both supervision and
  governance.
- MCP transport, handler registration, or tool-serving logic — that belongs in
  `deep-agentic-core-mcp`

### Integrates With

- `agenticops-control-tower` for eventual explicit mappings between deployment
  identity and runtime evidence; its private link contract is not normative AIOS
- `agentic-evals` for evaluation evidence: Evals 0.10.0 exports v0.4-draft
  `evaluation` evidence from its native reports; native reports alone do not
  establish AIOS conformance

- `agenticlens` as a flagship implementation and exporter of spec-compatible
  operational artifacts
- `agentic-chaos` for resilience and degradation evidence extensions that still
  fit the shared model
- `agentic-sidecar` for future decision and intent-alignment artifacts that
  need common vocabulary
- `deep-agentic-core-mcp` as a delivery surface that exposes spec-aligned
  artifacts and workflows through MCP

### Current Roadmap Focus

Repository v0.6.1 delivered the first v0.6.x increment: `0.6-draft`
provenance records, a portable conformance suite and naming conventions. The
next focus is independent runs of the suite, migration guides, the
OpenTelemetry binding and verification-signal/audit-event shapes. Work here should make independent implementations more
interoperable and more precise, not encode package-specific behavior as if it
were normative.

### Before You Build Here

- Only add concepts that help multiple independent implementers share the same
  model; package-local behavior should stay in the implementation repo
- Resist the urge to standardize speculative abstractions before sibling repos
  have proven the pattern in practice
- When in doubt, clarify boundaries and vocabulary here, but keep execution
  logic, UX, and adapter details out of the spec repo

## Build and Run

- Install: `make install` (runs `uv sync --extra dev`)
- Test: `make test` or `make check`
- Validate schemas: `uv run pytest`

## Repository Purpose

This repository defines the **specification only**. It does not run agents,
collect telemetry, host dashboards, or provide an SDK.

Code changes here should make the shared runtime model clearer for independent
implementers. Package-specific behavior belongs in implementation repositories.

## Repo Map

| Path | Purpose |
|------|---------|
| `specification/v0.1/` | Core concepts — runtime objects and boundaries |
| `specification/v0.2/` | Relationships — execution graphs and structure |
| `specification/v0.3/` | Semantic conventions — event names and meanings |
| `specification/v0.4/` | JSON Schemas — machine-readable validation |
| `specification/v0.5/` | Versioning and compatibility — version markers, change classification, deprecation |
| `specification/v0.6/` | Canonical examples, extension model, provenance records, conformance suite and naming conventions (exploratory draft) |
| `specification/v0.6/schemas/provenance.schema.json` | `0.6-draft` provenance record schema (reuses v0.4 common definitions) |
| `specification/v0.6/provenance-rules.json` | `AIOS-0.6-*` rule catalog mirroring `provenance.md` |
| `specification/v0.6/conformance-suite/` | Portable fixtures with expected outcomes, rule citations and resolution reports |
| `drafts/` | Superseded or premature experiments (non-normative) |
| `drafts/v0.4/` | Early schema experiment (retained for history) |
| `tests/test_spec_docs.py` | Document structure validation |
| `tests/test_v04_schema.py` | Schema validation tests |
| `drafts/v0.4/tests/` | Legacy schema fixture tests |
| `reviews/` | Independent-review evidence: decision log, evidence matrix, framework mappings, and conformance artifacts |
| `reviews/decision-log.md` | Milestone-level review decisions (`D-001`-`D-006`) — a separate numbering series from `specification/v0.1/decisions.md`'s design decisions |
| `tests/test_review_artifacts.py` | Validates `reviews/artifacts/*.conformance.json` against v0.4 schema + semantic rules |
| `tests/test_v05_versioning.py` | Validates the v0.5 version-marker grammar against its own docs and the v0.4 schemas |
| `tests/aios_reference.py` | Repository reference checks: marker routing, provenance semantics, cross-artifact resolution (test code, not an SDK) |
| `tests/test_v06_provenance.py` | Provenance schema, catalog sync, semantic rules and resolution |
| `tests/test_v06_conformance_suite.py` | Runs every suite case and requires rule coverage |
| `tests/test_naming_conventions.py` | Enforces `naming-conventions.md` over every published schema |
| `MILESTONE_CLOSEOUT_PLAN.md` | Plan for closing remaining review gates before each milestone freezes |
| `SPECIFICATION.md` | Complete reading order and maturity rules |
| `CONTRIBUTING.md` | Contribution guidelines |
| `Makefile` | Local dev automation |

## Contribution Rules

- A contribution belongs here when it makes the shared model clearer for
  **independent implementers**
- Package-specific behavior belongs in implementation repos (agenticlens,
  agentic-chaos, mcp-server)
- Later spec layers depend on earlier ones — don't bypass review gates
- Schemas are non-normative until the corresponding spec layer is reviewed

## Maturity Levels

| Status | Meaning |
|--------|---------|
| Draft | Open for design feedback, not stable |
| Exploratory draft | Blocked by earlier layer review |
| Reviewed | Accepted after independent review |
| Stable | Frozen, breaking changes require new version |

## Spec Layer Dependencies

```
v0.1 (core concepts)
  └── v0.2 (relationships) — blocked by v0.1 review
       └── v0.3 (semantics) — blocked by v0.1 + v0.2
            └── v0.4 (schemas) — blocked by v0.1–v0.3
                 └── v0.5 (versioning) — blocked by v0.1–v0.4
                      └── v0.6 (examples, extensions, provenance) — blocked by v0.1–v0.5
```

## Package Roles

- `ai-operations-spec` — defines the standard
- `agenticlens` — instruments and exports the standard
- `agentic-chaos` — extends the standard with resilience evidence
- `deep-agentic-core-mcp` — exposes the standard through MCP

## Adding a New Concept

1. Determine which spec layer it belongs to
2. Check that prerequisite layers are reviewed
3. Write prose definition with boundaries and examples
4. Add schema (v0.4) if the concept is schema-representable; a new artifact
   family gets its own marker and schema set (see decision `D-006`)
5. Follow `specification/v0.6/naming-conventions.md`, add a rule catalog entry,
   a conformance-suite case, and a validation test in `tests/`
6. State maturity clearly in the document

## Feature Completion Expectations

- Every spec or schema behavior change must include tests or fixtures.
- Normative or user-guiding changes must include or update realistic examples.
- When a milestone item is completed or its status changes, update `README.md`
  and `ROADMAP.md` in the same change.
- If that milestone or release changes the public ecosystem story, also update
  the shared org-profile docs in the `.github` repository:
  `profile/README.md` and, when relevant, `profile/ROADMAP.md`.
- When a change affects an earlier layer, also update dependent milestone
  documents, schemas, fixtures, and tests before considering the work done.

## Release

Two phases, split by the merge to `main` — bumping happens before, tagging
happens after:

**1. Pre-release (on the feature branch, before merge):** Bump versioned
package or document metadata if the release process requires it, and
update `CHANGELOG.md` with the release section. Commit as part of the
branch's normal history; goes in with the rest of the PR.

**2. Release (on `main`, once that branch has merged):**

1. Pull the merge commit on `main`.
2. Tag: create an annotated `vX.Y.Z` tag pointing at the merge commit,
   using the CHANGELOG's release section as the tag message:
   `git tag -a vX.Y.Z -F <file-with-that-section> --cleanup=verbatim`.
   `--cleanup=verbatim` is required — git's default cleanup silently strips
   lines starting with `#`, which would eat the CHANGELOG's `###` headers.
3. Push the tag: `git push origin vX.Y.Z`.

No `release-pypi.yml` exists for this repo — it isn't a published Python
package, so the tag itself is the release; nothing to trigger.

## Pre-push Checklist

Run `make check` before every push. It runs the schema validation tests.
