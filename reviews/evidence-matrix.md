# Acceptance Evidence Matrix

Use this matrix to show which acceptance gates are actually closed.

Status values:

- `open`
- `in progress`
- `ready for review`
- `closed`

## v0.1

| Gate | Status | Evidence | Notes |
|---|---|---|---|
| Review definitions against at least two independent frameworks | ready for review | `reviews/framework-mappings/agenticlens.md`, `reviews/framework-mappings/agentic-chaos.md` | Two implementation mappings now exist for the shared scenario pack |
| Record decisions and update all `v0.1` documents consistently | in progress | `specification/v0.1/decisions.md`, `reviews/decision-log.md` | Final close requires cross-doc consistency pass |
| Two independent implementers classify the same runtime objects consistently | ready for review | `reviews/scenarios/`, `reviews/framework-mappings/agenticlens.md`, `reviews/framework-mappings/agentic-chaos.md` | Two mappings exist; remaining work is reviewer sign-off and any concept refinements |

## v0.2

| Gate | Status | Evidence | Notes |
|---|---|---|---|
| Validate relationship vocabulary against at least two independent frameworks | ready for review | `reviews/framework-mappings/agenticlens.md`, `reviews/framework-mappings/agentic-chaos.md` | Two mappings now cover hierarchy, retries, and topology edges |
| Confirm ordering and retry semantics | closed | `reviews/framework-mappings/agenticlens.md`, `reviews/framework-mappings/agentic-chaos.md`, `reviews/decision-log.md` | Accepted in decision `D-002` |
| Record decisions and update affected documents | closed | `specification/v0.2/relationships.md`, `reviews/decision-log.md` | `D-002` wording folded into the Retry execution shape |

## v0.3

| Gate | Status | Evidence | Notes |
|---|---|---|---|
| Validate conventions against OpenTelemetry design principles | ready for review | `reviews/framework-mappings/agenticlens.md`, `reviews/framework-mappings/agentic-chaos.md` | Evidence supports transport neutrality; a short formal memo is still advisable |
| Validate event coverage against at least two reference implementations | ready for review | `reviews/framework-mappings/agenticlens.md`, `reviews/framework-mappings/agentic-chaos.md` | Two mappings recorded, though native canonical `aiops.*` adoption remains partial |
| Decide whether transport mappings belong in separate implementation profiles | closed | `reviews/framework-mappings/agenticlens.md`, `reviews/framework-mappings/agentic-chaos.md`, `reviews/decision-log.md` | Accepted in decision `D-003` |
| Record decisions and update affected documents | closed | `specification/v0.3/semantic-conventions.md`, `reviews/decision-log.md` | `D-003` wording folded into a new "Transport boundary" section |

## v0.4

| Gate | Status | Evidence | Notes |
|---|---|---|---|
| Resolve all open `v0.1` through `v0.3` gates | open | this matrix | Cannot close early |
| Validate artifacts produced by at least two independent implementations | open | `reviews/artifacts/agenticlens-support-run.aios.json`, `reviews/artifacts/agentic-chaos-customer-support.aios.json`, `reviews/artifacts/agenticlens-support-run.conformance.json`, `reviews/artifacts/agentic-chaos-customer-support.conformance.json` | Two implementation-derived AIOS draft artifacts now pass schema and semantic conformance, but both come from DeepAgentLabs-owned sibling repos. This evidence shows that two implementations produced valid artifacts; the gate stays open until a non-DeepAgentLabs producer artifact is recorded. |
| Review identifier, reference, extension, and unknown-value behavior | closed | `specification/v0.4/conformance.md`, `reviews/decision-log.md` (`D-004`), `specification/v0.4/examples/invalid/run-unknown-relationship-type.json`, `specification/v0.4/examples/invalid/run-unknown-object-type.json`, `specification/v0.4/examples/valid/run-namespaced-extensions.json` | Closed vocab vs. open-extension behavior is now normatively stated and fixture-tested. "Closed" here means the documentation/fixture work is done — `D-004` itself is still recorded as editor-proposed pending maintainer confirmation, not independent review; see `reviews/decision-log.md`'s own status note for that decision. |
| Replace the draft version marker when the milestone freezes | open | schema and fixture update | Only after earlier rows close |

## v0.5

| Gate | Status | Evidence | Notes |
|---|---|---|---|
| Resolve all open `v0.1` through `v0.4` gates | open | this matrix | Cannot close early |
| Decide additive vs. breaking change classification, including closed-vocabulary growth | closed | `specification/v0.5/versioning.md`, `specification/v0.5/examples.md`, `reviews/decision-log.md` (`D-005`) | "Closed" here means the documentation/example work is done; `D-005` is editor-proposed pending maintainer confirmation, not independent review |
| Validate the compatibility matrix against a real version transition from an independent implementation | open | none yet | No frozen version has ever been superseded, so no real transition exists to validate against |
| Decide the schema mechanism for `spec_version` once two frozen minors coexist | open | `specification/v0.5/versioning.md` ("Version markers in schemas") | Deferred until after the v0.4 freeze; this row records the obligation, not the implementation |

## v0.6

| Gate | Status | Evidence | Remaining work |
|---|---|---|---|
| Canonical examples and negative controls | drafted | `specification/v0.6/examples/manifest.json`, `tests/test_v06_examples.py` | Independent implementer review |
| Third-party extension guidance | drafted | `specification/v0.6/extension-model.md`, `examples.md` | Independent producer/consumer preservation evidence |
| Prerequisite layers and independent review | open | `specification/v0.6/acceptance-criteria.md`, decision D-001 | Close v0.1–v0.5 gates before freeze |

Repository validation is internal evidence and does not close these independent
review gates or establish stable conformance.

## v0.6.x (repository v0.6.1)

| Gate | Status | Evidence | Remaining work |
|---|---|---|---|
| Provenance and evidence-lineage concepts | drafted | `specification/v0.6/provenance.md`, `specification/v0.6/schemas/provenance.schema.json`, `specification/v0.6/provenance-rules.json`, `reviews/decision-log.md` (`D-006`) | Two independent producers emit records about the same subject |
| Portable conformance suite | drafted | `specification/v0.6/conformance-suite/suite.json`, `tests/test_v06_conformance_suite.py` | A non-DeepAgentLabs validator reports matching outcomes |
| Naming conventions | drafted | `specification/v0.6/naming-conventions.md`, `tests/test_naming_conventions.py` | Independent review of the rules before any freeze |
