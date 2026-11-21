# Building and publishing the specification documentation

The MkDocs site is built from tracked Markdown and JSON sources, preserving
repository-relative links. No generated document copies are maintained in Git.
The staging script excludes untracked files, symlinks and runtime/source trees.

```bash
make docs        # strict build into site/
make docs-serve  # local preview
```

Run `git add` for new documentation before building: staging intentionally
reads only tracked paths. MkDocs is a development dependency group; it adds
no runtime dependency to any sibling package. A strict build runs for pull
requests. Only `main` or a manual run on `main` can deploy through GitHub Pages.
Configure the repository's Pages source as GitHub Actions. Deployment uses the
`github-pages` environment with short-lived OIDC credentials. Pull requests
cannot deploy. The hosted URL is
<https://deepagentlabs.github.io/ai-operations-spec/> (the organization custom
domain may redirect it). Raw schemas are copied unchanged at both their source
paths and the versioned `v0.4/*.schema.json`, `v0.6/*.schema.json` and
`v0.8/*.schema.json` URL paths. Each schema directory is discovered automatically.
The JSON `$id` values and relative `$ref` behavior remain unchanged.

A repository release snapshots sources, not a stable specification. `main`
is the current draft site; use Git tags for reproducible historical inputs.
Independent-review gates remain open even when the site builds and deploys.

## Developer and AI reference guides

The [Developer Guide (simple)](developer-guide.md) and
[AI Reference capability index](ai-reference-index.md) list the same capabilities.
The generated [robust reference](https://deepagentlabs.io/ai-operations-spec/docs/llms-full.md)
includes the full maintained specification, non-normative profiles, review and
compatibility prose, JSON Schemas, catalogs, mappings, examples and portable cases.
`ai-docs.json` selects inputs; `ai-docs-manifest.json` records normalized source
hashes and the generated output checksum. Original fixture bytes remain the
source of truth for provenance digests. The structural-validation tutorial is
an example, not a supported runtime API.

With Python 3.11 or newer and the website repository checked out alongside this one:

```bash
python3 ../deepagentlabs.github.io/scripts/build_ai_docs.py --sources .. --project ai-operations-spec
python3 ../deepagentlabs.github.io/scripts/build_ai_docs.py --sources .. --project ai-operations-spec --check
```

Regenerate after changing selected inputs; add new Markdown sources explicitly to
`docs/ai-docs.json`. JSON globs include new schemas/catalogs/fixtures automatically.
Keep both indexes and `docs/navigation.json` current. Negative and historical
fixtures must retain their labels. The shared site publishes at
`https://deepagentlabs.io/ai-operations-spec/docs/`, preserving the repository
layout and serving `llms-full.md` verbatim. The standalone build excludes that
large file from HTML/search and copies it verbatim to `docs/llms-full.md` after
MkDocs completes. Neither site publication changes specification maturity.
