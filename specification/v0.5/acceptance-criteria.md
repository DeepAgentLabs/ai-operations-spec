# v0.5 Acceptance Criteria

## Versioning coverage

- [x] Version marker grammar (`MAJOR.MINOR` with an optional `-draft` suffix) is defined.
- [x] Editorial, additive, and breaking change classification is defined.
- [x] Closed-vocabulary growth is explicitly classified as breaking, not additive (decision `D-005`).
- [x] Consumer compatibility behavior is defined for same-version, draft, and cross-version artifacts.
- [x] Deprecation policy (grace period, migration-note obligation) is defined for releases after v1.0.
- [x] Extension-point stability (`attributes`, `extensions`) is reconfirmed as always-safe growth, independent of `spec_version`.

## Review gates

- [ ] Resolve all open `v0.1` through `v0.4` review gates (v0.5 cannot freeze before them).
- [ ] Validate the change-classification rules against a real version transition proposed by an independent implementation.
- [x] Record the closed-vocabulary-growth classification as a reviewable decision (`D-005`; see `reviews/decision-log.md`).
- [ ] Decide the concrete schema mechanism (`enum` vs. pattern) for `spec_version` once two frozen minors must coexist; deferred until after the v0.4 freeze.

## Exit condition

Implementers can determine whether they may safely consume an artifact. For a frozen `spec_version`, the marker alone is sufficient. For a `-draft` marker, the marker must be combined with the observation date or snapshot tag identifying the exact draft content, per the draft volatility rule in `versioning.md` — the marker alone does not disambiguate two incompatible snapshots that happen to share the same `-draft` string.
