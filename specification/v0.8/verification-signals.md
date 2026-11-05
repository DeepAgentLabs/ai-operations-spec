# Verification signals

Exploratory draft. A verification signal records one second-opinion assessment
of a named subject. It is separate from an Evals score, a Sidecar decision,
authority to execute, and a recovery receipt.

[Schema](schemas/verification_signal.schema.json) ·
[Completed example](examples/verification_signal.json) ·
[Unavailable example](examples/verification_unavailable.json)

Required fields include the envelope (id, marker, artifact type, created_at,
producer), native source reference, subject reference, versioned method, status, verdict, confidence,
rationale, evidence, grounding, safety and native_outcome. Confidence is an
optional measurement represented by a number in [0,1] or null when absent; it
is not a score multiplier or calibrated probability.

| Field | Vocabulary / meaning |
| --- | --- |
| status | completed, unavailable, error, skipped |
| verdict | supports, partially_supports, contradicts, inconclusive; null without a completed assessment |
| grounding.status | grounded, partial, ungrounded, not_checked |
| safety.status | concerns, no_concerns, not_checked |
| method.kind | rule, model, human, statistical, heuristic |

Non-completed results have null verdict and confidence, not_checked grounding
and safety, and empty assessment-detail arrays. A completed inconclusive result
is an assessment, unlike an unavailable judge. Safety concerns require a
nonempty concerns array; no_concerns means an assessment found none, whereas
not_checked makes no safety statement. Grounded results have no unsupported
claims or missed evidence; partial and grounded states need evidence references.

Lens partially_agree maps to partially_supports while retaining its original
value in native_outcome. Lens unsupported_claims and evidence_missed map to
grounding.unsupported_claims and grounding.missed_evidence_items to preserve
grounding detail, but their absence alone does not prove grounding or safety.
Sidecar ALLOW/BLOCK remain governance outcomes: a projector needs the separate
underlying assessment and an explicit mapping before emitting a verdict.
An Evals unavailable judge becomes unavailable, never supports.

See [conformance](conformance.md) for identity, grounding and process rules.
