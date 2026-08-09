# Scenario 02: Retry and Recovery

## Narrative

A user asks for a product comparison. The system starts a run and begins a model-backed analysis step. The first model attempt times out. A reliability signal records the timeout. The system retries once, the second attempt succeeds, and the run completes with an answer.

## Minimum expected objects

- one `Run`
- one `Request`
- one logical analysis `Step`
- two distinct `Model Interaction` attempts
- at least one `Reliability Event`
- optional `Evaluation`

## v0.1 review questions

- Are the two attempts treated as separate model interaction occurrences?
- Is the timeout a `Reliability Event` rather than automatically an `Incident`?
- Can the run be completed even though it experienced degradation?

## v0.2 review questions

- How is the retry chain represented?
- What ordering relation proves the second attempt follows the first?
- Does the logical step stay one step while attempts remain separate occurrences?

## v0.3 expected event areas

- run lifecycle
- step lifecycle
- model requested
- model failed or timed out
- retry or recovery semantics
- model responded
- run completed

## v0.4 artifact expectations

- both attempts have stable identities
- the reliability event references the failed attempt
- graph references remain valid after retry
