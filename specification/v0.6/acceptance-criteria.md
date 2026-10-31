# v0.6 Acceptance Criteria

## Status

Exploratory draft; implementation of this layer does not freeze it.

- [x] Minimal Workflow and Run artifacts validate offline.
- [x] Advanced examples show relationships, evaluation, retries and extensions.
- [x] Negative controls distinguish schema and semantic failures.
- [x] Namespace, placement, preservation and extension evolution are documented.
- [x] Sibling ownership and dependency boundaries are recorded.
- [ ] v0.1–v0.5 prerequisite review gates close.
- [ ] Independent implementers review the examples and extension model.
- [ ] A non-DeepAgentLabs producer/consumer demonstrates preservation of unknown
      extension values and agrees on interpretation of the canonical examples.

Evidence and decisions belong in [the evidence matrix](../../reviews/evidence-matrix.md)
and [decision log](../../reviews/decision-log.md). Tests alone cannot close
independent review or prove artifact truth, safety or runtime success.

## v0.6.x provenance, conformance suite and naming (repository v0.6.1)

- [x] Provenance records define subjects, source references, derived findings
      and evidence lineage without changing any `0.4-draft` schema.
- [x] The provenance schema, rule catalog and normative text are kept in sync
      by tests, and every semantic rule has a targeted negative fixture.
- [x] A portable conformance suite lists expected outcomes and rule citations
      for every schema and semantic producer rule, marker routing and
      cross-artifact resolution.
- [x] Naming conventions are documented and enforced across published schemas.
- [ ] A non-DeepAgentLabs validator runs the conformance suite and reports
      matching outcomes.
- [ ] Two independent producers emit provenance records about the same
      subject artifact and a consumer resolves both.
- [ ] Review confirms that a companion artifact under its own marker
      (decision `D-006`) is preferable to a future Run field.
