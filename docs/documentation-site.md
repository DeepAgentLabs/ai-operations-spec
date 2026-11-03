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
paths and the historical `v0.4/*.schema.json` / `v0.6/*.schema.json` URL paths.
The JSON `$id` values and relative `$ref` behavior remain unchanged.

A repository release snapshots sources, not a stable specification. `main`
is the current draft site; use Git tags for reproducible historical inputs.
Independent-review gates remain open even when the site builds and deploys.
