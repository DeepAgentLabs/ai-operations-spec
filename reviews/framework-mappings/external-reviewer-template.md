# External Review Mapping Template

Use this template if you are reviewing AIOS from outside DeepAgentLabs —
as an independent framework maintainer, a consultant, or an unaffiliated
practitioner. It mirrors the internal mapping template but does not assume
you are mapping onto a specific DeepAgentLabs product.

Save your completed copy as `reviews/framework-mappings/<your-project-or-name>.md`.

- Framework or context: (name of your framework, product, or "N/A — reviewing as an unaffiliated practitioner")
- Reviewer:
- Affiliation: (confirm you have no DeepAgentLabs authorship, funding, or editorial role — see `reviews/decision-log.md` decision `D-001`)
- Date:
- Version or commit reviewed:

## Scenario coverage

- [ ] `scenario-01-customer-support.md`
- [ ] `scenario-02-retry-and-recovery.md`
- [ ] `scenario-03-safety-and-incident.md`

For each scenario you cover, work from the narrative only — don't read the
other framework mappings in this directory first. The value of this exercise
is in seeing where your independent interpretation agrees or disagrees with
ours, not in converging on a pre-agreed answer.

## v0.1 concept classification

For each scenario, state how you would classify the runtime objects
described in `specification/v0.1/core-concepts.md`:

- Run
- Request
- Step
- Agent
- Model Interaction
- Prompt
- Context
- Tool Invocation
- RAG Retrieval
- Memory Operation
- Evaluation
- Safety Signal
- Reliability Event
- Incident

Flag anything that doesn't map cleanly, anything you'd split further, and
anything you'd merge.

## v0.2 relationship notes

Using `specification/v0.2/relationships.md`, record how you would represent:

- containment
- dependency / causal order
- retry linkage (does the failed attempt and the retry need an explicit
  edge, or is adjacency/timestamp enough in your model?)
- delegation or handoff
- parent-child runs, if applicable

## v0.3 semantic event notes

Using `specification/v0.3/semantic-conventions.md`, record:

- which canonical `aiops.*` events clearly fit
- which scenario moments have no canonical event and would need an
  extension (`<your-reverse-domain>.*`)
- any naming, cardinality, or lifecycle assumptions you disagree with
- whether the transport-neutrality stance (events are not OTel spans; OTel
  bindings are a separate profile) matches how you'd actually instrument this

## v0.4 artifact notes

Using `specification/v0.4/schemas/` and `specification/v0.4/examples/`:

- did you attempt to produce or hand-construct an artifact for one of the
  scenarios? What broke or felt unnatural?
- schema validation result, if you ran one
- reference/identifier integrity issues
- reaction to the unknown-value policy in `specification/v0.4/conformance.md`
  ("Unknown-value behavior") — closed enums reject unknown values, growth
  happens via `attributes`/`extensions`. Does that match how you'd want a
  consumer to behave?

## Reviewer summary

- Equivalent meaning achieved: (full / partial / minimal — and why)
- Ambiguities:
- Disagreements or changes requested:
- Would you be willing to be named as an external reviewer in
  `reviews/decision-log.md`? (yes/no — either is fine, this is optional)
