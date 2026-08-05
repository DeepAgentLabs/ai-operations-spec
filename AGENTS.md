## AI Operations Specification Development Reference

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

## Pre-push Checklist

Run `make check` before every push. It runs the schema validation tests.
