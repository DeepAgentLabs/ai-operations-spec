# Review Pack

This directory contains the evidence scaffolding needed to move `v0.1` through `v0.4` from draft status toward reviewed acceptance.

These files do not by themselves close milestone gates. They provide a structured place to record:

- shared review scenarios
- framework mapping results
- acceptance-gate evidence
- reviewer decisions

## Contents

- `decision-log.md`
  Records review outcomes, unresolved questions, and accepted decisions.
- `evidence-matrix.md`
  Maps each milestone acceptance gate to concrete evidence.
- `framework-mappings/`
  Per-framework review notes showing how the same scenario is interpreted.
- `scenarios/`
  Shared scenarios used across `v0.1` through `v0.4`.
- `EXTERNAL_REVIEW_INVITE.md`
  Ready-to-send outreach packet for closing decision `D-001` — the
  independent, non-DeepAgentLabs review gate every milestone still needs.

## How to use this pack

1. Pick one scenario from `scenarios/`.
2. Review it through at least two independent frameworks or implementations.
3. Record concept classification results under `framework-mappings/`.
4. Compare graph, event, and artifact outputs across implementations.
5. Update `evidence-matrix.md` with links to committed evidence.
6. Record accepted decisions and ambiguities in `decision-log.md`.

## Review rule

Do not mark a milestone as reviewed only because the prose looks complete.
Mark it reviewed only when the corresponding acceptance gates have linked evidence in this directory.
