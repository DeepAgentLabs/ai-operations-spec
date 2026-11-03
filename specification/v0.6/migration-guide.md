# Adopting the cumulative AIOS draft layers

Status: non-normative implementation guide, repository v0.7.0. All layers
remain drafts; this guide does not close independent-review gates.

## Layers are not wire-format upgrades

v0.1, v0.2 and v0.3 introduce concepts, relationships and events. They do
not define three historical JSON formats. There is no supported automatic
`0.1` → `0.2` → `0.3` JSON rewrite. The first published Run/Workflow schema
set is `0.4-draft`. Repository v0.7.0 is a snapshot tag, never an artifact's
`spec_version`. Pin both producer and validator snapshot when using drafts.

| Adoption step | Preserve | Add or verify | Stop when |
| --- | --- | --- | --- |
| v0.1 → v0.2 | Identity of each Run, Request, Step and occurrence | Explicit containment, causal order, handoff and retry relationships | A parent, endpoint or identity is unknown; report incomplete evidence rather than inventing it |
| v0.2 → v0.3 | Graph and distinct occurrence identities | Observed lifecycle events, timestamps, outcome and measurement kind | Only a state snapshot exists; do not invent a transition |
| v0.3 → v0.4 | Meaning of events and graph | `artifact_type`, `spec_version: "0.4-draft"`, schema field layout, structural and semantic checks | Schema or semantic checks fail; a JSON parse is insufficient |
| v0.4 → v0.5 policy | Original artifact marker | Declared-marker routing, consumer compatibility decision and snapshot identity | No matching schema is available; do not retry against another marker |
| v0.4 + v0.6 provenance | Original Run/Workflow bytes and marker | Separate `0.6-draft` provenance record, resolvable subjects and evidence lineage | A source is unavailable; report unresolved, never claim verified |

## Worked example: a retried lookup

Start with two observed calls to the same logical tool activity: first failed,
second completed. In v0.1 terms these are two Tool Invocations within one
Step, not a single invocation overwritten with its final outcome. In v0.2,
link each invocation to that Step using `observed-in` and order the attempts
with `follows`; the Run contains the Step. In v0.3, emit `aiops.tool.failed`
only if the failure was observed, and `aiops.tool.completed` with an outcome
only if completion was observed. Do not infer timestamps from array order.

The [retry Run](examples/retry-run.json) is the schema-valid v0.4 packaging of
that graph. It deliberately has no events because no event observations were
provided. The [telemetry example](otel/example.json) separately demonstrates
observed events with timestamps and an optional transport projection.

To check this repository's examples and the portable suite offline after
installing development dependencies:

```bash
uv sync --extra dev
uv run pytest tests/test_v06_examples.py tests/test_v06_conformance_suite.py
```

An external implementation should use its own validator with the
[portable suite manifest](conformance-suite/README.md), comparing expected
outcomes and rule citations. The repository checks are reference test code,
not a supported SDK or end-user conformance CLI.

## Legacy experiment migration

`drafts/v0.4/` is a superseded experiment, not an earlier compatible version
of `specification/v0.4/`. Inventory source identities and meaning first; map
them to the [v0.1 concepts](../v0.1/core-concepts.md), reconstruct observed
relationships using [v0.2](../v0.2/relationships.md), and validate the resulting
artifact against the current [v0.4 schemas](../v0.4/README.md) and semantic
rules. Keep the original artifact and a mapping/loss report. Do not merely
change its version marker or copy unknown fields into the closed core.
Producer-specific data can use reverse-domain `extensions` as described in
the [extension model](extension-model.md); preserve unknown extensions.

## Provenance is additive, not a Run upgrade

The [provenance example](examples/provenance/support-finding.provenance.json)
uses its own `0.6-draft` marker. Keep the subject Run `0.4-draft` and dispatch
each artifact using the [compatibility catalog](../v0.5/compatibility.json).
When a digest is present, hash the exact original bytes, not reserialized
JSON. Resolution, digest verification and the truth of a finding are separate
claims. Unknown schemas, unavailable subjects and digest mismatches must be
reported separately; none establishes a successful verification.

## Rollout and rollback

1. Pin schemas, catalogs and the suite to one repository tag; record current
   producer and consumer support by artifact family.
2. Validate archived samples before enabling a new exporter. Record unmapped
   fields and missing observations, and retain originals under local policy.
3. Dual-write only with explicit correlation and deduplication; never count
   native evidence and its projection twice.
4. Route by declared marker. Keep the old reader while comparing outputs.
5. Roll back the adapter/configuration if needed; do not rewrite stored
   markers or describe retained older artifacts as a newer version.

See [ecosystem compatibility](../../docs/v0.7.0-ecosystem.md) for sibling
ownership, dependencies and the absence of automatic adapters in this release.
