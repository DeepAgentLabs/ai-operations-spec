# AIOS external reviewer task list

Thank you for reviewing AIOS. We need to know whether people outside
DeepAgentLabs can understand the same execution the same way and build tools
that exchange its data without adopting our runtime packages.

Choose the tasks that fit your experience. You do not need to review every
layer or implement a complete validator. Partial findings and disagreements are
useful; say what you did and did not test.

**New here? [Start on the single reviewer page](https://github.com/DeepAgentLabs/.github/blob/main/profile/EXTERNAL_REVIEW_CHECKLIST.md)**
and choose one area. If you chose specification or data compatibility and need
full AIOS requirements, continue below. Use the one report template linked
from the start page; formal scenario mappings can be attached as evidence.

## 1. Record your review scope

- [ ] Record your name/contact, affiliation, date, framework and the full AIOS
  commit reviewed. Ask maintainers which revision to use if unsure.
- [ ] Disclose AIOS authorship, DeepAgentLabs funding and editorial involvement.
  Feedback from affiliated people is welcome; independent gates need the
  [D-001 independence conditions](decision-log.md).
- [ ] Pick a task: scenario mapping, telemetry, independent validation,
  producer/consumer exchange, or operational companion review.

## 2. Review the shared scenarios (ecosystem R1)

Begin with one scenario for a small review. For complete mapping evidence, use
the same agreed scenario set as the other independent reviewer; covering all
three avoids gaps:

- [ ] [Customer support](scenarios/scenario-01-customer-support.md).
- [ ] [Retry and recovery](scenarios/scenario-02-retry-and-recovery.md).
- [ ] [Safety and incident](scenarios/scenario-03-safety-and-incident.md).

Read the narratives before reading other mappings. Copy the
[external mapping template](framework-mappings/external-reviewer-template.md).
For each scenario, explain:

- [ ] Which objects are a Run, Request, Step, model/tool call, retrieval, memory
  operation, evaluation, safety signal or incident?
- [ ] Which relationships express containment, dependency, retry and delegation?
- [ ] Which events express an observation, judgment, enforcement or failure?
- [ ] Can you produce a Workflow/Run JSON artifact with equivalent meaning?
- [ ] What is missing, ambiguous, unnecessarily complex or specific to our SDKs?

**Return:** your filled template and any sample artifacts. The existing closure
rule requires at least two independent mappings for the same shared scenario
set, followed by maintainer reconciliation; one review does not close every layer.

## 3. Check the specification in reading order (ecosystem R2/R6)

Use [SPECIFICATION.md](../SPECIFICATION.md) for the reading order. For each layer
you review, link any finding to a section and a small example.

| Layer | Question to answer | Acceptance details |
| --- | --- | --- |
| v0.1 concepts | Are definition objects, occurrences and evidence clearly different? | [Criteria](../specification/v0.1/acceptance-criteria.md) |
| v0.2 relationships | Can you represent parallel work, retries, nesting and handoffs accurately? | [Criteria](../specification/v0.2/acceptance-criteria.md) |
| v0.3 conventions | Are event meaning, time, identity, units and privacy coherent with OTel design principles? | [Criteria](../specification/v0.3/acceptance-criteria.md) |
| v0.4 schemas | Can two independent producers emit equivalent valid artifacts? | [Criteria](../specification/v0.4/acceptance-criteria.md) |
| v0.5 versioning | Can a consumer distinguish supported versions and reject incompatible marker/type pairs? | [Criteria](../specification/v0.5/acceptance-criteria.md) |
| v0.6 interoperability | Do extensions survive exchange, and does provenance resolve from exact held bytes? | [Criteria](../specification/v0.6/acceptance-criteria.md) |
| v0.8 companions | Do verification, audit and investigation records preserve source meaning? | [Criteria](../specification/v0.8/acceptance-criteria.md) |

For telemetry review, inspect the [pinned OTel binding](../specification/v0.6/otel-binding.md)
and record the upstream revision compared. For provenance and companion design,
give an explicit assessment of decisions D-006 and D-007 in the
[decision log](decision-log.md). Later-layer feedback does not bypass earlier
layers' outstanding acceptance criteria.

For versioning review, propose a real change from your own implementation and
check its additive/breaking classification and old-consumer behavior. Include
the before/after artifacts and expected acceptance or rejection.

## 4. Test an independent validator (ecosystem R3)

- [ ] Read the [portable suite instructions](../specification/v0.6/conformance-suite/README.md)
  and the cases/expected results in its [manifest](../specification/v0.6/conformance-suite/suite.json).
- [ ] Run your own or another non-DeepAgentLabs implementation against every
  covered case: currently 66 artifact cases and five resolution cases.
- [ ] Report expected vs actual outcomes and rule IDs, including unsupported
  markers, invalid references/cycles, unknown extensions and changed subject bytes.
- [ ] Clearly label schema-only results and semantic/resolution rules you have
  not implemented. Do not silently count unsupported checks as passed.

**Return:** implementation source/revision, exact commands and case-by-case
results. AIOS `make check`, Lens and MCP are our own reference checks; running
them helps reproduction but does not constitute independent implementation.

## 5. Exchange independently produced data (ecosystem R4)

- [ ] Arrange two independent producer implementations for an agreed scenario,
  with a consumer that reads the artifacts without our runtime packages.
- [ ] Include two provenance records about the same subject bytes. Resolve
  both, then test missing bytes, modified bytes and incorrect subject identity.
- [ ] Pass an unfamiliar namespaced extension with nested values through the
  consumer and re-export it without changing the values.
- [ ] Try the [migration guidance](../specification/v0.6/migration-guide.md)
  and report any information lost during exchange.

**Return:** sanitized source artifacts, hashes, producer/consumer revisions,
validation output and before/after extension values.

## 6. Review the operational companions (ecosystem R5)

Read the [operational family](../specification/v0.8/README.md) and
[source mappings](operational-artifact-mappings.md). Review each family against
native observations, and contribute independently produced examples:

- [ ] `verification_signal`: unavailable is not a successful judgment; confidence,
  method, source and evidence states are explicit.
- [ ] `audit_event`: permission to proceed is not proof of execution success;
  unknown actors and actual causal/correlation identity remain explicit.
- [ ] `investigation_report`: hypotheses are distinct from observations;
  citations are meaningful; closure alone does not prove recovery.
- [ ] Unknown extensions survive a consumer round trip, and private payloads
  are omitted from public projections. Use synthetic secret markers for tests.

**Return:** source-to-artifact examples and consumer output for the families
tested, including an unavailable or invalid case. List any family not tested.

## 7. Submit the evidence

Open an AIOS issue or PR. Save completed scenario mappings under
`reviews/framework-mappings/<your-name-or-project>.md`; include test artifacts
and reproduction commands or links to them. The ecosystem
[report template](https://github.com/DeepAgentLabs/.github/blob/main/profile/EXTERNAL_REVIEW_REPORT_TEMPLATE.md)
works for all other reviews. Request a private reporting path from maintainers
before sending confidential data; send no credentials or customer data publicly.

Maintainers preserve attribution, reconcile disagreements, update only the
covered rows in the [evidence matrix](evidence-matrix.md), record decisions and
link fixes. They handle machine-readable acceptance receipts and final freezes.
The [existing invitation](EXTERNAL_REVIEW_INVITE.md) remains available for outreach.
No external acceptance is recorded by the existence of this checklist.
