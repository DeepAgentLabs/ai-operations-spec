# CI Readiness — Pre-push Checklist

Run these checks locally before every push or PR.

## Docs-only shortcut

If your diff only touches prose **outside** `specification/` and `drafts/`
(e.g., `README.md`, `CONTRIBUTING.md`), skip code checks. Verify with:

```bash
git status --short
```

Changes inside `specification/` or `drafts/` must still run `make check`
because tests validate document structure, required files, and links.

## Required checks (all schema or test changes)

```bash
make check
```

This runs the schema validation test suite.

Or run directly:

1. **Clean tree** — no accidental untracked files

   ```bash
   git status --short
   ```

2. **Test**

   ```bash
   make test
   ```

## What the tests validate

- Document structure in `specification/` (`tests/test_spec_docs.py`)
- JSON Schema validity in `specification/v0.4/` (`tests/test_v04_schema.py`)
- Legacy schema fixtures in `drafts/v0.4/tests/`

## When tests must pass

- Any change to schema files (`*.schema.json`)
- Any change to test fixtures (`examples/valid/`, `examples/invalid/`)
- Any structural change to specification documents

## CI parity

The GitHub Actions CI workflow runs `uv run pytest` across Python 3.10–3.13.
If `make check` passes locally, CI should pass too.
