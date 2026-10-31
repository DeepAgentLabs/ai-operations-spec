# v0.6 Canonical Examples

## Status

Exploratory draft. These synthetic examples demonstrate the cumulative model;
they are not independent implementation evidence or stable conformance claims.
They use the existing v0.4 schemas and `0.4-draft` marker.

## Reading and running

From the repository root, run `uv sync --extra dev` then `make check`.
`tests/test_v06_examples.py` checks every entry in the
[manifest](examples/manifest.json) using local schemas with format checking and
the repository's semantic checks. No network service or sibling package is
needed. This is repository validation, not the planned v0.6.x portable suite.

| Artifact | Purpose | Expected result |
|---|---|---|
| [Minimal Workflow](examples/minimal-workflow.json) | Reusable workflow definition | Accept |
| [Minimal Run](examples/minimal-run.json) | A completed Run with no observed steps | Accept |
| [Advanced support Run](examples/advanced-support-run.json) | Retrieval, model, evaluation, external Workflow reference and custom event | Accept |
| [Retry Run](examples/retry-run.json) | Distinct failed and successful attempts with an explicit ordering edge | Accept |
| [Reserved namespace](examples/invalid-reserved-namespace.json) | Producer extension under `aiops` | Schema rejection |
| [Invented core type](examples/invalid-core-type.json) | Custom occurrence type despite valid extension | Schema rejection |
| [Missing Step](examples/invalid-missing-step.json) | Core endpoint unresolved despite valid extension | Semantic rejection |

The minimal Run intentionally makes no execution or evaluation claim. The
advanced Run's evaluation score is synthetic; its completed status does not
prove safety. The external Workflow is not resolved by validation and MUST NOT
be reported as verified. The retry example's `attempt` and
`logical_activity_id` attributes describe producer metadata, not new core fields.

## Example extension contract

`org.example.support` is an illustrative namespace controlled by no real producer
in this example. Its Run payload has `version: "1.0"`, a synthetic
`case_id` string and a `labels` array containing JSON values. A reader supporting
1.x accepts unknown members and preserves them; an unsupported major version
means it cannot interpret this payload for support-specific operations. Breaking
changes require a new major version and a migration note. No remote schema fetch
is needed. `org.example.support.reviewed` is an extension event targeting the
Run, with producer-defined attributes; it is not a canonical safety review.

The advanced example includes nested unknown values and nulls to exercise
lossless JSON preservation. Removing its extension entries and custom event
leaves the core graph valid. Changing the extension version to `99.0` also
leaves core validation unchanged: support-specific validation is separate.
See [extension requirements](extension-model.md) before publishing a contract.

## Provenance example (repository v0.6.1)

[support-finding.provenance.json](examples/provenance/support-finding.provenance.json)
is a `0.6-draft` provenance record about the advanced support Run. It is not
listed in the v0.6.0 manifest above because it is validated by the 0.6-draft
schema set, not the v0.4 schemas; `tests/test_v06_provenance.py` checks it,
resolves its references against the Run and verifies the subject's `sha-256`
digest. Its findings are synthetic and their `confirmed` or `open` status
proves nothing about the Run. More valid and invalid records, each citing the
rule it breaks, are in the [conformance suite](conformance-suite/README.md).
