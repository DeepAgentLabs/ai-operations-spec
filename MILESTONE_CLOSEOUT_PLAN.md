# AIOS Milestone Close-Out Plan

This document turns the current `v0.1` through `v0.4` draft milestones into a concrete path to reviewed completion.

It does not change milestone status by itself. A milestone is complete only when its acceptance criteria, dependency gates, repo updates, and validation evidence are all closed.

## Current baseline

- Documented milestone chain:
  - `v0.1` core concepts
  - `v0.2` relationships
  - `v0.3` semantic conventions
  - `v0.4` JSON Schemas
- Local validation baseline as of `2026-08-09`:
  - `UV_CACHE_DIR=/tmp/uv-cache uv run pytest`
  - `20 passed`
- Immediate blocker pattern:
  - most remaining work is review evidence, cross-document consistency, and independent implementation validation
  - later milestones cannot freeze before earlier review gates close

## Done criteria by milestone

### v0.1

Must close:

- review definitions against at least two independent frameworks
- record decisions and update all `v0.1` documents consistently
- show that two independent implementers can classify the same runtime objects without package-specific knowledge

Evidence package:

- framework mapping notes for two independent frameworks
- classification worksheet using shared runtime examples
- maintainer decision log
- consistency pass across `README.md`, `core-concepts.md`, `terminology.md`, `examples.md`, and `acceptance-criteria.md`

### v0.2

Must close:

- validate the relationship vocabulary against at least two independent agent frameworks
- confirm ordering and retry semantics
- record decisions and update affected documents

Evidence package:

- graph reconstruction examples from the same scenario across two frameworks
- explicit decisions for parent-child, causal order, retry attempt, branch, join, and loop semantics
- updated examples and any test coverage needed for graph/document invariants

### v0.3

Must close:

- validate conventions against OpenTelemetry design principles
- validate event coverage against at least two reference implementations
- decide whether transport mappings belong in separate implementation profiles
- record decisions and update affected documents

Evidence package:

- event catalog review against OTel naming, cardinality, lifecycle, and extension principles
- coverage matrix showing each runtime area is representable by canonical or extension events
- written decision separating normative semantics from transport bindings

### v0.4

Must close:

- resolve all open `v0.1` through `v0.3` review gates
- validate artifacts produced by at least two independent implementations
- review identifier, reference, extension, and unknown-value behavior
- replace the draft version marker when the milestone freezes

Evidence package:

- artifact samples from at least two independent producers
- validation outputs against current schemas
- issue log for identifier/reference/extension edge cases
- final schema/version marker update and fixture refresh

## Workstreams

## 1. Repo-internal work

These items can be completed directly in `ai-operations-spec`.

- normalize milestone language across `README.md`, `ROADMAP.md`, `SPECIFICATION.md`, and milestone READMEs
- create or expand decision logs for unresolved reviewer questions
- add scenario-based review worksheets for object classification, graph reconstruction, and semantic event coverage
- add tests for any newly clarified document invariants or schema edge cases
- add a review ledger documenting which acceptance gates are closed, by whom, and with what evidence

## 2. Cross-project coordination

These items need evidence from sibling repos in this workspace.

- `agenticlens`
  - export draft-conforming artifacts
  - prove consumer and producer use of relationships, events, and schemas
  - supply examples for findings, traces, and conformance-oriented validation
- `agentic-chaos`
  - exercise degraded, failed, retried, and recovered execution paths
  - validate whether reliability and incident concepts are sufficient
  - produce artifacts that stress event semantics and edge-case relationships
- `mcp-server`
  - validate consumer-side reading, transformation, and interoperability expectations
  - verify artifact references and unknown-value handling in a control-plane style consumer

## 3. Independent review work

These items cannot honestly be self-certified inside this repo alone.

- choose two non-DeepAgentLabs frameworks or implementers for external review
- run the same scenario pack through both
- compare concept classification results for `v0.1`
- compare execution graph reconstruction results for `v0.2`
- compare event semantics interpretation results for `v0.3`
- compare schema artifact output and validation results for `v0.4`

## Review sequence

The fastest safe path is:

1. Close `v0.1` first.
2. Use the finalized `v0.1` vocabulary to tighten `v0.2`.
3. Freeze `v0.3` only after `v0.2` ordering and retry semantics are explicit.
4. Freeze `v0.4` last after artifact validation from independent producers.

Doing `v0.2` through `v0.4` first would create churn because each later layer inherits names and boundaries from `v0.1`.

## Proposed close-out checklist

### Phase A: close the `v0.1` foundation

- create a single review packet with:
  - concept glossary
  - boundary decisions
  - three to five shared runtime scenarios
- run the packet against two independent frameworks
- capture disagreements and resolve naming or boundary ambiguity
- update all `v0.1` docs together
- mark `v0.1` review gates complete only after evidence is recorded

### Phase B: lock `v0.2` execution semantics

- derive graph examples from the same shared scenarios
- write explicit rules for:
  - ordering
  - retries
  - branches
  - joins
  - loops
  - parent-child runs
- validate equivalent graph reconstruction across two implementations
- update relationship docs, examples, and any tests together

### Phase C: lock `v0.3` semantics

- produce a catalog review worksheet covering every runtime area
- align event naming and extension guidance with OTel design principles
- decide and document that transport mappings stay outside the core spec unless added as separate non-normative profiles
- validate event coverage using artifacts from at least two implementations

### Phase D: freeze `v0.4` schemas

- generate artifacts from at least two independent producers
- validate all artifacts against the schemas
- add missing edge-case fixtures for identifiers, references, extensions, and unknown values
- replace draft version markers only after `v0.1` through `v0.3` are closed

## Recommended repo additions

The repo would benefit from a small review infrastructure layer:

- `reviews/decision-log.md`
- `reviews/evidence-matrix.md`
- `reviews/scenarios/`
- `reviews/framework-mappings/`

These would let the project prove why a milestone is reviewed instead of only claiming it.

## Exit standard

Do not mark `v0.1` through `v0.4` as done when only the prose looks complete.

Mark them done only when:

- the acceptance criteria are checked off
- dependencies are closed in order
- tests and fixtures pass
- review evidence is committed in the repo
- at least the required independent implementation validation is recorded
