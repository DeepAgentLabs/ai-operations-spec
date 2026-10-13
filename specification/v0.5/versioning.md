# v0.5 Versioning and Compatibility Rules

Because v0.5 is pre-release, this document's own rules apply to itself only informally until v0.1–v0.4 freeze. It describes the rules implementations SHOULD start following now so that the eventual freeze does not require rewriting existing producers and consumers.

## Version marker grammar

A `spec_version` string MUST match:

```text
^(0\.[1-9][0-9]*|[1-9][0-9]*\.[0-9]+)(-draft)?$
```

In words: a `0.` prefix followed by a nonzero minor number (matching the milestone numbering used throughout this repository, e.g. `0.4`), or any `MAJOR.MINOR` pair where `MAJOR` is one or greater (e.g. `1.0`, `1.1`, `2.3`). Either form MAY carry a literal `-draft` suffix.

- `0.4-draft` — the current v0.4 marker, matches the `0.4` branch of the grammar.
- `1.0` — the eventual frozen stable release, matches the `MAJOR.MINOR` branch with `MAJOR = 1`.
- `1.1-draft` — a draft of a future additive minor release after v1.0.

A patch segment (`MAJOR.MINOR.PATCH`) is intentionally absent. AIOS does not define a patch level: every normative change belongs to a MINOR (additive) or MAJOR (breaking) release, per the classification below. Editorial changes carry no version marker change at all.

## Draft volatility rule

A `-draft` suffix means the content behind that marker MAY still change incompatibly. This is not new: `specification/v0.4/conformance.md` already states that no compatibility is promised across different draft snapshots and asks implementers to cite an observation date. v0.5 generalizes that rule to every milestone:

1. Two artifacts carrying the same `-draft` `spec_version` string are NOT guaranteed compatible with each other.
2. A claim of draft alignment MUST cite an observation date (see `specification/v0.4/conformance.md`'s claim format), or, for a reproducible snapshot, the `vX.Y-draft-YYYY-MM-DD` git tag described in `CONTRIBUTING.md`.
3. Once a milestone freezes, its `-draft` suffix is dropped and that exact `spec_version` string becomes immutable: the rules it names MUST NOT change again. Any further change — however small — requires a new version marker (an editorial fix excepted, see below).

## Change classification

Every change to a normative document, schema, or canonical vocabulary falls into exactly one of three categories.

### Editorial

A wording clarification, a non-normative example fix, a typo correction, or a `description` string update that does not change what a producer may emit or a consumer must accept. Editorial changes do not require any `spec_version` change, before or after freeze.

### Additive (MINOR)

A backward-compatible change that an unmodified consumer built against the prior MINOR can safely ignore without misinterpreting the artifact. Additive changes include:

- a new optional field whose absence has always been valid
- relaxing a constraint (making a required field optional, widening a numeric range or string pattern)
- a new object, relationship, or event exposed only through an existing open extension point (the freeform `attributes` object or a reverse-domain-namespaced `extensions` object, per `specification/v0.4/conformance.md`'s unknown-value behavior)

Additive changes bump the MINOR component of `spec_version`.

### Breaking (MAJOR)

A change an old consumer could silently mishandle, or that invalidates artifacts that previously validated. Breaking changes include:

- removing or renaming a required field
- changing the meaning of an existing field or event without renaming it
- narrowing a constraint (making an optional field required, shrinking an enum, tightening a pattern)
- **adding a member to any closed vocabulary** — `object_type`, reference/relationship/occurrence/evidence `type`, or the canonical `event_name` catalog

Breaking changes bump the MAJOR component of `spec_version`.

## Closed-vocabulary growth is breaking, not additive

Decision `D-004` (`reviews/decision-log.md`) fixed `object_type`, reference/relationship/occurrence/evidence `type`, and the canonical `event_name` catalog as closed vocabularies: a value outside the enum is a schema violation, and a consumer MUST reject it rather than tolerate it as unknown.

That decision has a direct consequence for versioning: adding a new member to one of these enums looks additive (existing values still mean the same thing) but is not safe for an unmodified old consumer, because that consumer's schema still rejects the new value. An artifact using the new member would fail validation against the old consumer's pinned schema even though nothing about the artifact's use of old members changed.

v0.5 therefore classifies closed-vocabulary growth as a **MAJOR** change. This is recorded as decision `D-005` (`reviews/decision-log.md`) so the classification itself goes through the same review process as every other milestone decision, rather than being asserted only in prose here.

Producers that need forward-compatible growth without a MAJOR release MUST use the two existing open extension points — freeform `attributes` and namespaced `extensions` — exactly as `specification/v0.4/conformance.md` already requires. Those two points remain additive-safe at any version, per "Extension-point stability" below.
