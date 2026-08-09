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
| Validate artifacts produced by at least two independent implementations | closed, but see caveat | `reviews/artifacts/agenticlens-support-run.aios.json`, `reviews/artifacts/agentic-chaos-customer-support.aios.json`, `reviews/artifacts/agenticlens-support-run.conformance.json`, `reviews/artifacts/agentic-chaos-customer-support.conformance.json` | Two implementation-derived AIOS draft artifacts now pass schema and semantic conformance. Caveat: `agenticlens` and `agentic-chaos` are both DeepAgentLabs-owned sibling repos, not the non-DeepAgentLabs implementer that `README.md` and `D-001` call for. Treat this row as satisfying "two implementations produced valid artifacts," not as satisfying the separate "independent/unrelated producer" bar. |
| Review identifier, reference, extension, and unknown-value behavior | closed | `specification/v0.4/conformance.md`, `reviews/decision-log.md` (`D-004`), `specification/v0.4/examples/invalid/run-unknown-relationship-type.json`, `specification/v0.4/examples/invalid/run-unknown-object-type.json`, `specification/v0.4/examples/valid/run-namespaced-extensions.json` | Closed vocab vs. open-extension behavior is now normatively stated and fixture-tested |
| Replace the draft version marker when the milestone freezes | open | schema and fixture update | Only after earlier rows close |
