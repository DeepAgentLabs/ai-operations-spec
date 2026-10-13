# v0.5 Versioning Examples

These fragments demonstrate meaning, not a new artifact schema. The version marker grammar is normative in [versioning.md](versioning.md); these lists are illustrative and are checked for consistency by `tests/test_v05_versioning.py`.

## Valid version markers

```text
0.1-draft
0.4-draft
0.5-draft
1.0
1.1-draft
2.3
```

- `0.4-draft` is the marker actually used by `specification/v0.4/schemas/*.schema.json` today.
- `1.0` is the eventual frozen stable release with no suffix.
- `2.3` illustrates a later MAJOR.MINOR pair; AIOS does not define a patch segment.

## Invalid version markers

```text
v0.4-draft
0.4.0-draft
0.04-draft
0.4_draft
draft
0.0-draft
```

- `v0.4-draft` — a leading `v` belongs in a git tag, not in `spec_version` itself.
- `0.4.0-draft` — a patch segment is not part of the grammar.
- `0.04-draft` — a leading zero on the minor number is not permitted.
- `0.4_draft` — the suffix separator must be a hyphen, not an underscore.
- `draft` — the suffix cannot stand alone without a `MAJOR.MINOR` pair.
- `0.0-draft` — the grammar requires a nonzero minor number when `MAJOR` is `0`, matching the fact that milestone numbering starts at `v0.1`.

## Change classification walkthrough

A hypothetical change to the v0.4 `run.schema.json`, classified under the v0.5 rules:

| Change | Classification | Reason |
| --- | --- | --- |
| Add an optional `cost_usd` number under an occurrence's `attributes` | Additive (MINOR) | Uses the existing open extension point; an old consumer ignores an unrecognized `attributes` key. |
| Add `"superseded-by"` as a new member of the relationship `type` enum | Breaking (MAJOR) | Grows a closed vocabulary fixed by decision `D-004`; an old consumer's schema rejects the new enum member (decision `D-005`). |
| Fix a typo in the `status` enum's description string | Editorial | Changes no accepted or rejected value. |
| Make `ended_at` acceptable before `started_at` is set (currently required together) | Breaking (MAJOR) | Narrows nothing, but changes the meaning of an existing invariant that consumers rely on for semantic validation. |
| Mark the `declared_structure` field deprecated, still schema-valid | Additive (MINOR), only valid starting at v1.0 | Deprecation does not remove anything yet; see the deprecation policy's one-MINOR grace period. |

## Draft citation example

```text
Aligned with AI Operations Specification v0.4-draft as observed on 2026-07-21.
```

This citation format is defined in `specification/v0.4/conformance.md` and generalized to every milestone by v0.5's draft volatility rule.
