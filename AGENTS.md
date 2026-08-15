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

- `agenticlens` as a flagship implementation and exporter of spec-compatible
  operational artifacts
- `agentic-chaos` for resilience and degradation evidence extensions that still
  fit the shared model
- `agentic-sidecar` for future decision and intent-alignment artifacts that
  need common vocabulary
- `deep-agentic-core-mcp` as a delivery surface that exposes spec-aligned
  artifacts and workflows through MCP

### Current Roadmap Focus

The current focus is provenance/evidence concepts, a conformance test suite,
and naming conventions. Work here should make independent implementations more
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
| `drafts/` | Superseded or premature experiments (non-normative) |
| `drafts/v0.4/` | Early schema experiment (retained for history) |
| `tests/test_spec_docs.py` | Document structure validation |
| `tests/test_v04_schema.py` | Schema validation tests |
| `drafts/v0.4/tests/` | Legacy schema fixture tests |
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
4. Add schema (v0.4) if the concept is schema-representable
5. Add validation test in `tests/`
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

1. Bump versioned package or document metadata if the release process requires it
2. Update `CHANGELOG.md` with the release section
3. Tag: create an annotated `vX.Y.Z` tag and use the latest `CHANGELOG.md`
   release section as the tag description
4. Push: `git push origin main --tags`

## Pre-push Checklist

Run `make check` before every push. It runs the schema validation tests.
