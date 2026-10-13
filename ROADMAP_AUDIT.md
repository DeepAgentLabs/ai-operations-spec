# AI Operations Specification roadmap implementation audit

Audit date: 2026-09-11. Baseline: commit `b7fe380` (`main`, clean working
tree, last commit 2026-08-16). Scope: [ROADMAP.md](ROADMAP.md),
[README.md](README.md), [SPECIFICATION.md](SPECIFICATION.md),
[MILESTONE_CLOSEOUT_PLAN.md](MILESTONE_CLOSEOUT_PLAN.md), the
`specification/` and `drafts/` trees, the `reviews/` evidence pack, and the
`tests/` suite. This is a specification repository, not a code package:
"evidence" below means normative text, schema files, fixtures, and recorded
review decisions that actually exist in the repo — not test pass counts,
though schema/fixture tests are spot-checked where present.

**The roadmap's top-level Release Status badges are not wrong, but they are
incomplete: substantial acceptance-gate work has been committed since the
badges and "Next Steps" prose were last written, and none of it is
mentioned in ROADMAP.md or README.md.** No milestone should be read as
frozen or externally validated merely because a decision was recorded or a
document section exists.

## Correctness note

This audit did not find any claim in ROADMAP.md that MILESTONE_CLOSEOUT_PLAN.md
or the repo contents contradict. The closeout plan (dated 2026-08-08, baseline
"20 passed") is itself a plan document, not a status report, and it explicitly
warns: "Do not mark v0.1 through v0.4 as done when only the prose looks
complete." The repo has since acted on much of that plan — a `reviews/`
evidence pack now exists with real content — but the one gate every milestone
depends on (independent, non-DeepAgentLabs review) remains open, and the
repo's own `reviews/EXTERNAL_REVIEW_INVITE.md` says explicitly: "Only then
reconsider the README.md/ROADMAP.md Release Status badges." This audit
therefore does not flip any badge. It corrects ROADMAP.md's "Next Steps" and
"Cross-Project Dependencies" text, which had gone stale relative to work
already committed, and documents the gap for the record.

## How to read this audit

- **Implemented (I):** normative text, a schema, or a fixture exists for the
  stated scope and is structurally sound. This does not assert the milestone
  is frozen, externally reviewed, or stable.
- **Partial (P):** a subset, an internal (DeepAgentLabs-only) version, or a
  narrower related artifact exists.
- **Missing (M):** no corresponding text, schema, fixture, or decision record
  was found in the inspected paths.
- **Unverified (U):** a claim requires evidence — typically from a sibling
  repo or an external party — that this audit could not establish from this
  repo alone.

## Milestone summary

| Milestone | Assessment | Main open work |
| --- | --- | --- |
| v0.1 Core concepts | Partial acceptance; vocabulary complete, external review open | Independent (non-DeepAgentLabs) framework review (`D-001`); final cross-document consistency pass |
| v0.2 Relationships | Partial acceptance; retry/ordering decision closed internally | Independent framework validation of the relationship vocabulary |
| v0.3 Semantic conventions | Partial acceptance; transport-boundary decision closed internally | OTel-alignment validation; independent event-coverage validation |
| v0.4 JSON Schemas | Partial acceptance; schemas/fixtures real and tested, unknown-value behavior decided | Non-DeepAgentLabs producer artifact; draft-marker freeze blocked on v0.1–v0.3 |
| v0.5 Versioning and compatibility | Missing | No `specification/v0.5/` directory exists; no version-marker or compatibility rule text found |
| v0.6 Examples and extension model | Missing as a dedicated layer | v0.4 already has a namespaced-extension model and canonical/invalid fixtures; a dedicated v0.6 conformance-suite layer does not exist |
| v0.6.x Provenance, evidence, operational artifacts | Missing as a spec layer; precursor exists | v0.4's `evidence` object family (`evaluation`/`safety_signal`/`reliability_event`) is a narrow precursor; no standalone provenance/evidence spec, naming-conventions doc, or migration guide exists |
| v1.0 Stable specification | Missing | Depends on all above; no stable-release layout decided |

## Evidence index

Paths are relative to this repository.

| Key | Source | Notes |
| --- | --- | --- |
| V01-CORE | [core-concepts.md](specification/v0.1/core-concepts.md), [terminology.md](specification/v0.1/terminology.md), [examples.md](specification/v0.1/examples.md), [decisions.md](specification/v0.1/decisions.md) | 192-line concept catalog; each of the 15 core concepts has Purpose/Identity/Owns/References/Must-not-represent sections, enforced by `tests/test_spec_docs.py` |
| V01-ACCEPT | [acceptance-criteria.md](specification/v0.1/acceptance-criteria.md) | Vocabulary/coherence/scope-discipline boxes checked; the two external-review boxes are unchecked |
| V02-REL | [relationships.md](specification/v0.2/relationships.md), [acceptance-criteria.md](specification/v0.2/acceptance-criteria.md) | Retry recoverability-edge rule present (line 77), citing decision `D-002` |
| V03-SEM | [semantic-conventions.md](specification/v0.3/semantic-conventions.md), [acceptance-criteria.md](specification/v0.3/acceptance-criteria.md) | "Transport boundary" section (line 58) citing decision `D-003`; canonical `aiops.*` catalog is enum-matched against v0.4 schema by `tests/test_v04_schema.py::test_v03_event_catalog_matches_v04_schema` |
| V04-SCHEMA | [common.schema.json](specification/v0.4/schemas/common.schema.json), [run.schema.json](specification/v0.4/schemas/run.schema.json), [workflow.schema.json](specification/v0.4/schemas/workflow.schema.json) | Draft 2020-12 schemas with real `$defs`, closed enums, and cross-file `$ref`s — confirmed structurally valid (see Verification) |
| V04-FIXTURES | [examples/valid](specification/v0.4/examples/valid/), [examples/invalid](specification/v0.4/examples/invalid/), [examples/semantic-invalid](specification/v0.4/examples/semantic-invalid/) | 10 fixtures covering valid artifacts, schema-invalid artifacts, and semantically-invalid-but-schema-valid artifacts (dangling references, merged retry attempts) |
| V04-CONFORM | [conformance.md](specification/v0.4/conformance.md) | Producer/consumer MUST-list plus a dedicated "Unknown-value behavior" section citing decision `D-004` |
| REVIEWS | [reviews/README.md](reviews/README.md), [decision-log.md](reviews/decision-log.md), [evidence-matrix.md](reviews/evidence-matrix.md) | Evidence scaffolding recommended by `MILESTONE_CLOSEOUT_PLAN.md` and actually built; tracks gate-by-gate status as open/in progress/ready for review/closed |
| MAPPINGS | [framework-mappings/agenticlens.md](reviews/framework-mappings/agenticlens.md), [framework-mappings/agentic-chaos.md](reviews/framework-mappings/agentic-chaos.md) | Two internal (DeepAgentLabs-owned) framework mappings, each with executed commands, generated artifacts, and per-concept classification results |
| SCENARIOS | [scenarios/scenario-01-customer-support.md](reviews/scenarios/scenario-01-customer-support.md), [scenario-02-retry-and-recovery.md](reviews/scenarios/scenario-02-retry-and-recovery.md), [scenario-03-safety-and-incident.md](reviews/scenarios/scenario-03-safety-and-incident.md) | Shared narrative scenarios used to drive the two framework mappings and intended for external reviewers |
| REVIEW-ARTIFACTS | [agenticlens-support-run.aios.json](reviews/artifacts/agenticlens-support-run.aios.json) + [.conformance.json](reviews/artifacts/agenticlens-support-run.conformance.json), [agentic-chaos-customer-support.aios.json](reviews/artifacts/agentic-chaos-customer-support.aios.json) + [.conformance.json](reviews/artifacts/agentic-chaos-customer-support.conformance.json) | Two sibling-repo-derived run artifacts, both recorded as `schema_valid: true`, `semantic_valid: true`, `aligned: true`; validated by `tests/test_review_artifacts.py` |
| INVITE | [EXTERNAL_REVIEW_INVITE.md](reviews/EXTERNAL_REVIEW_INVITE.md) | Ready-to-send outreach packet for closing `D-001`, the shared external-review gate; explicitly instructs not to touch the Release Status badges until it closes |
| TESTS | [test_spec_docs.py](tests/test_spec_docs.py), [test_v04_schema.py](tests/test_v04_schema.py), [test_review_artifacts.py](tests/test_review_artifacts.py) | Document-structure checks, schema/fixture validation, and review-artifact conformance checks |
| DRAFT-LEGACY | [drafts/v0.4/README.md](drafts/v0.4/README.md), [drafts/v0.4/schemas/workflow.schema.json](drafts/v0.4/schemas/workflow.schema.json) | Retained early schema experiment, clearly labeled non-normative; `tests/test_spec_docs.py::test_v04_draft_does_not_claim_v01_schema_identity` guards against re-conflating it with the current design |

## v0.1 — Core runtime concepts

| Roadmap/closeout deliverable | Status | Evidence / remaining boundary |
| --- | --- | --- |
| Workflow/Run/Request/Step boundaries defined | I | V01-CORE; distinct sections with exclusions ("Must not represent") |
| Agent, Model Interaction, Prompt, Context, Tool Invocation, RAG Retrieval, Memory Operation defined | I | V01-CORE covers all 15 concepts required by `tests/test_spec_docs.py` |
| Evaluation, Safety Signal, Reliability Event, Incident defined | I | V01-CORE |
| Internal naming/boundary decisions recorded | I | `specification/v0.1/decisions.md` (D-001–D-003: Run vs. WorkflowRun, MCP as integration protocol not core concept, Model Interaction as general name) |
| Review definitions against at least two independent frameworks | P | MAPPINGS gives two frameworks reviewed, but both are DeepAgentLabs-owned (`agenticlens`, `agentic-chaos`); `reviews/decision-log.md` `D-001` explicitly states this does not satisfy the "independent" bar it defines (no DeepAgentLabs authorship/funding/editorial control) |
| Record decisions and update all v0.1 documents consistently | P | Acceptance-criteria checkbox is unticked; `tests/test_spec_docs.py` enforces cross-document concept coverage between the overview and acceptance criteria, but a full consistency pass is still an open acceptance-criteria item |
| Two independent implementers classify the same runtime objects consistently | U | Two DeepAgentLabs-internal mappings agree closely; no non-DeepAgentLabs classification exists yet to test this |

Acceptance: v0.1's own [acceptance-criteria.md](specification/v0.1/acceptance-criteria.md) has every vocabulary/coherence/scope-discipline box checked and both review-gate boxes unchecked. ROADMAP.md's "In review" badge for v0.1 is accurate to this state. What is missing from ROADMAP.md is that a concrete, reusable review packet (SCENARIOS, MAPPINGS, INVITE) now exists and is waiting on an external respondent — not on further internal drafting.

## v0.2 — Relationships and execution structure

| Roadmap deliverable | Status | Evidence / remaining boundary |
| --- | --- | --- |
| Structural/causal/participation/evidence relationship types distinguished | I | V02-REL |
| Execution shapes (sequential, parallel, branch, join, retry, loop) and graph-integrity rules stated | I | V02-REL; `tests/test_v04_schema.py` enforces acyclicity for `parent-of` and for the `{caused, follows, depends-on}` group at the v0.4 fixture level |
| Retry/ordering semantics confirmed | I | Decision `D-002` (accepted): retries keep distinct identities linked by an explicit recoverability edge; folded into `relationships.md` line 77 |
| Validate relationship vocabulary against ≥2 independent frameworks | P | MAPPINGS covers hierarchy, retries, delegation, and topology edges for two DeepAgentLabs-owned frameworks; `evidence-matrix.md` marks this row "ready for review," not closed, pending an independent party |

Acceptance: the internal decision that was v0.2's main open design question (how retries and ordering are represented) is closed and reflected in normative text. The remaining v0.2 gate is the same external-review dependency as v0.1, not new v0.2-specific drafting work — this distinction is not visible from ROADMAP.md alone today.

## v0.3 — Semantic conventions

| Roadmap deliverable | Status | Evidence / remaining boundary |
| --- | --- | --- |
| Canonical event names, naming rules, minimum attributes | I | V03-SEM; canonical `aiops.*` catalog is cross-checked byte-for-byte against the v0.4 schema enum by `tests/test_v04_schema.py::test_v03_event_catalog_matches_v04_schema` |
| Transport-mapping boundary decided | I | Decision `D-003` (accepted): transport bindings (e.g. OTel) MUST stay out of core semantics and belong in separate non-normative profiles; folded into `semantic-conventions.md`'s "Transport boundary" section |
| Validate conventions against OpenTelemetry design principles | M | `evidence-matrix.md` marks this "ready for review" on the strength of the two framework mappings' general transport-neutrality discussion; no dedicated OTel-alignment memo exists yet, and `reviews/EXTERNAL_REVIEW_INVITE.md` names an OTel GenAI semantic-conventions contributor as the ideal reviewer for exactly this gate |
| Validate event coverage against ≥2 reference implementations | P | MAPPINGS discuss event/lifecycle coverage per framework, but note neither framework natively emits the canonical `aiops.*` names yet — coverage is by concept mapping, not literal event-name adoption |

Acceptance: the transport-boundary decision that most affects how v0.3 interacts with implementation repos (should OTel bindings live here?) is closed. Literal `aiops.*` adoption by producers remains **P**, and formal OTel-principles validation remains **M**.

## v0.4 — JSON Schemas

| Roadmap deliverable | Status | Evidence / remaining boundary |
| --- | --- | --- |
| Machine-readable schemas for Workflow/Run and their nested objects | I | V04-SCHEMA; all three schema files are valid Draft 2020-12 documents (`$schema` set, cross-file `$ref`s resolve, closed enums for object/relationship/event types) |
| Valid and invalid fixtures, semantic (graph-level) invalid fixtures | I | V04-FIXTURES; `tests/test_v04_schema.py` parametrizes all three fixture directories and additionally implements identity-uniqueness, dangling-reference, retry-recoverability, and cycle checks that JSON Schema itself cannot express |
| Sensitive content optional; extension namespace rules | I | `common.schema.json`'s `extension_name`/`extensions` `$defs` require a reverse-domain name outside the `aiops` namespace; enforced by `run-namespace-collision.json` (invalid) and `run-namespaced-extensions.json` (valid) fixtures |
| Identifier/reference/extension/unknown-value review | I | Decision `D-004` (accepted, editor-proposed — flagged in the decision log itself as needing maintainer confirmation, not external review): closed vocabularies reject unknown enum values; `attributes`/`extensions` are the only forward-compatible growth points; folded into `conformance.md` |
| Success = "artifacts can be validated without a DeepAgentLabs package" | P | The schemas are plain JSON Schema (no DeepAgentLabs package needed to validate structurally), and `agenticlens`'s validator (`src/agenticlens/validation/aios.py` in the sibling repo) independently re-implements Draft202012 + semantic checks against this same schema layout rather than importing this repo as a package — consistent with, though not full proof of, that goal |
| Validate artifacts from ≥2 independent implementations | P | REVIEW-ARTIFACTS: two sibling-repo-derived artifacts both pass schema and semantic conformance (`aligned: true`), automatically re-checked by `tests/test_review_artifacts.py`. `evidence-matrix.md` is explicit that this stays open until a non-DeepAgentLabs producer artifact exists — both current producers are DeepAgentLabs-owned |
| Replace draft version marker when milestone freezes | M | `spec_version` is still hard-pinned to the `"0.4-draft"` constant in `run.schema.json`; freezing is correctly gated on v0.1–v0.3 closing first |

Acceptance: v0.4 is the most concretely evidenced layer — real schemas, real fixtures (including deliberately tricky semantic-invalid cases like merged retry attempts and dangling references), and two passing conformance runs from sibling repos. The "exploratory draft" badge is still correct because the freeze itself is explicitly blocked on earlier-layer review, but the underlying artifact work is materially further along than "exploratory" alone suggests.

## v0.5 — Versioning and compatibility

All listed deliverables are **M**: no `specification/v0.5/` directory exists, and no version-marker, additive/breaking-change, deprecation, or compatibility-behavior rule text was found anywhere in the repo. `spec_version` today is a single hardcoded constant (`"0.4-draft"`) with no migration or coexistence rule defined. ROADMAP.md's "Planned" badge is accurate.

## v0.6 / v0.6.x — Examples, extension model, provenance and evidence

| Roadmap deliverable | Status | Evidence / remaining boundary |
| --- | --- | --- |
| Canonical minimal/advanced example artifacts | P | V04-FIXTURES already serves this purpose informally at the v0.4 layer (`run.json`, `workflow.json`, extension examples); no dedicated v0.6 canonical-examples document exists |
| Namespace rules for third-party extensions | I (at v0.4) | Already implemented and fixture-tested in v0.4 (see above); a dedicated v0.6 layer would formalize rather than originate this |
| Conformance test suite producers can run independently | P | `tests/test_v04_schema.py` + `tests/test_review_artifacts.py` are exactly this in embryonic form, but they live under this repo's own `tests/`, not yet packaged as an independently distributable conformance suite |
| Provenance/evidence concepts as first-class spec objects | P | v0.4's `evidence` array (`evaluation`/`safety_signal`/`reliability_event` types, linked via `evaluates`/`signals-on`/`evidence-for` relationships) is a real precursor, but there is no source-reference/evidence-lineage model beyond that — the roadmap's own "Implement now" item is not yet started as a dedicated concept |
| Naming conventions document | M | No dedicated naming-conventions document found |
| Migration guides, hosted docs site, verification-signal schema, audit-event schema | M | None found |

ROADMAP.md's "Planned" badge for both v0.6 and v0.6.x is accurate — no dedicated v0.6 directory or document exists — but the roadmap doesn't currently note that v0.4's `evidence` object family already anticipates part of v0.6.x's stated scope.

## v1.0 — Stable specification

All listed deliverables are **M**: no stable-release layout has been decided (README.md and AGENTS.md both say this explicitly), no version freeze has occurred, and the milestone depends on every earlier layer. "Planned" is accurate.

## Cross-project dependency verification

| Claim in ROADMAP.md | Status | Evidence / boundary |
| --- | --- | --- |
| `agenticlens` provides producer/consumer evidence for traces, findings, conformance tooling, schema usage | I (repo-verifiable portion) | MAPPINGS + REVIEW-ARTIFACTS give concrete, executed evidence (commands run, artifacts generated, conformance reports produced). Independently, `agenticlens/src/agenticlens/validation/aios.py` (sibling repo) implements its own Draft202012 + semantic validator keyed to `DEFAULT_SPEC_VERSION = "0.4"` and the same relationship-type vocabulary as this repo's `common.schema.json` — this is genuine cross-repo alignment, not just a roadmap assertion. Whether `agenticlens`'s own roadmap/tests currently pass is out of scope here (see the sibling `agenticlens/ROADMAP_AUDIT.md`) |
| `agentic-chaos` provides resilience/fault evidence | I (repo-verifiable portion) | MAPPINGS's `agentic-chaos.md` documents an executed chaos run (rate-limit storm, token timeout, silent degradation) and a resulting artifact validated against v0.4 schemas |
| `deep-agentic-core-mcp` provides a consumer/control-plane view | U | No evidence of this repo was inspected; ROADMAP.md's phrasing ("Provides") is presently aspirational for this dependency as far as this repo's own files show |
| `agentic-sidecar`, `agenticops-control-tower` provide future decision/governance/inventory artifacts | U | Explicitly framed as future work in ROADMAP.md itself ("Provides future..."); no artifacts from either repo were found here, consistent with that framing |

## Verification

- JSON validity: every `*.json` file under `specification/` and `drafts/` (19 files, excluding the untracked/gitignored `drafts/v0.4/.venv` and `.pytest_cache`) was parsed successfully via `ConvertFrom-Json`. None are stub/empty files — the smallest schema (`workflow.schema.json`, 20 lines) still declares required fields, a closed `spec_version`/`artifact_type` pair, and `$ref`s into `common.schema.json`.
- Schema structure: `specification/v0.4/schemas/{common,run,workflow}.schema.json` all declare `"$schema": "https://json-schema.org/draft/2020-12/schema"`, use `$defs`/`$ref` correctly, and encode real constraints (closed enums for object/relationship/event/occurrence/evidence types, a reverse-domain pattern for extension names, `additionalProperties: false` throughout). This is consistent with `tests/test_v04_schema.py::test_v04_schemas_are_valid`, which calls `Draft202012Validator.check_schema` on each.
- Test execution: this audit could not execute `uv run pytest` — no working Python interpreter was available in the environment used for the audit (the repo's committed `.venv` contains broken `uv` trampolines pointing at a since-removed interpreter, and no system Python/`uv`/Node was reachable). Test *files* were read in full instead (`test_spec_docs.py`, `test_v04_schema.py`, `test_review_artifacts.py`) to confirm what they actually check, and their assertions were spot-verified by hand for the specific fixtures/decisions cited in this audit (e.g. the retry-recoverability rule, the `aiops.*` catalog match, the two review-artifact conformance reports' recorded `aligned: true`). `MILESTONE_CLOSEOUT_PLAN.md` records a prior local run of `20 passed` on 2026-08-09; the test suite has grown since (a third test file, `test_review_artifacts.py`, did not exist at that baseline), so that count is now stale but this audit cannot supply a fresh one.
- CI: `.github/workflows/ci.yml` runs `uv run pytest` across Python 3.10–3.13 on push/PR to `main`; this audit did not re-trigger or inspect a live CI run.
- No external model, non-DeepAgentLabs reviewer, or hosted documentation site was contacted or verified — those remain the explicitly open gates (`D-001`) that this audit also could not close.

## Issues worth addressing (not fixed by this audit)

1. Two unrelated `D-00x` numbering sequences exist in the repo:
   `specification/v0.1/decisions.md` (D-001–D-003, about `Run`/MCP/`Model
   Interaction`) and `reviews/decision-log.md` (D-001–D-004, about external
   review/retry semantics/transport boundary/unknown-value behavior). Both
   are legitimately scoped decision logs, but the shared prefix invites
   miscitation across documents.
2. `reviews/artifacts/*.conformance.json` embed an absolute local filesystem
   path (`/home/pramodbn27/PyPi Projects/ai-operations-spec/...`) in
   `artifact_path`. It's not a normative AIOS field and doesn't affect
   validation, but it leaks a contributor's local directory layout into
   committed fixtures.
3. `MILESTONE_CLOSEOUT_PLAN.md`'s "Local validation baseline" (`20 passed`,
   2026-08-09) predates `tests/test_review_artifacts.py` and is now stale as
   a specific count, though the document is explicitly a plan rather than a
   live status report.
4. ROADMAP.md's "Repository organization" tree and AGENTS.md's "Repo Map"
   both omit `reviews/` entirely, even though it now holds the evidence this
   audit relies on most and is the operative home for closing every
   milestone's remaining review gate.
5. Decision `D-004` (v0.4 unknown-value behavior) is recorded as "accepted"
   in `evidence-matrix.md`/`decisions-log.md`, but the decision log itself
   flags it as an editor-proposed decision needing maintainer confirmation,
   not independent review — the "closed" status in `evidence-matrix.md` for
   that row is about the documentation/fixture work being done, not about
   independent sign-off, and a reader skimming only the matrix's status
   column could conflate the two.

No product, specification, schema, or fixture content was changed by this
audit. All relative links in this document were checked against files that
exist in the repository at the audited commit.

## Addendum (2026-10-12): v0.5 draft added

This section is appended after the original audit above; it does not alter
that audit's findings about the commit it examined. As of 2026-10-12, the
"v0.5 — Versioning and compatibility" gap this audit documented (**Missing**:
no `specification/v0.5/` directory, no version-marker or compatibility rule
text) has been addressed:

- `specification/v0.5/{README.md,versioning.md,examples.md,acceptance-criteria.md}`
  define the `spec_version` grammar, editorial/additive/breaking change
  classification, the consumer compatibility matrix, the deprecation policy,
  and extension-point stability.
- `reviews/decision-log.md` records decision `D-005` (closed-vocabulary
  growth is a breaking change), following the same editor-proposed,
  pending-maintainer-confirmation pattern as `D-004`.
- `reviews/evidence-matrix.md` adds a `v0.5` gate section.
- `tests/test_v05_versioning.py` cross-checks the version-marker grammar
  against the v0.5 docs and the existing v0.4 schema `spec_version` constants.

This is repo-internal drafting, consistent with every other milestone's
status in this audit: it does **not** close the shared independent-review
gate (`D-001`), and the Release Status badge change (Missing → Exploratory
draft) mirrors the same "Planned → Exploratory draft" transition v0.2–v0.4
already went through once a milestone directory and normative text exist.
Exactly one `v0.5` acceptance-criteria review-gate checkbox is marked
complete by this addendum — "record the closed-vocabulary-growth
classification as a reviewable decision (`D-005`)," which is a documentation
task this addendum itself finishes. The remaining `v0.5` review-gate
checkboxes (resolving the shared `v0.1`–`v0.4` dependency, validating the
rules against a real independent version transition, and deciding the
`spec_version` schema-routing mechanism) stay open; see
`specification/v0.5/acceptance-criteria.md` for the full list.


