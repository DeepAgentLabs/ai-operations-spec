# Specification Guide

The AI Operations Specification is one cumulative standard developed in milestone layers. A milestone number identifies the layer introduced; it is not a separate competing edition of the entire standard.

## Reading order

1. [v0.1 core concepts](specification/v0.1/core-concepts.md) and [terminology](specification/v0.1/terminology.md)
2. [v0.2 relationships and execution structure](specification/v0.2/relationships.md)
3. [v0.3 semantic conventions](specification/v0.3/semantic-conventions.md)
4. [v0.4 JSON Schemas](specification/v0.4/README.md)

Examples explain intended meaning; acceptance criteria track readiness and unresolved review gates. Acceptance checklists are contributor material, not part of the runtime contract.

## Maturity

All current documents are pre-release drafts. Normative keywords describe requirements **within the named draft**, but do not imply a stable release or compatibility promise.

An implementation may say it is "aligned with the AIOS v0.4 draft dated YYYY-MM-DD." It MUST NOT claim stable AIOS conformance until the applicable review gates and versioning rules are complete.

Later exploratory milestones may be developed to test earlier decisions. Their existence does not mean their dependencies have been accepted.

## Normative language

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are interpreted as described by RFC 2119 and RFC 8174 when, and only when, they appear in uppercase.

## Conformance boundary

For the v0.4 draft, structural alignment requires both:

1. JSON Schema validation against the declared artifact schema.
2. Semantic validation of identity, references, relationships, and graph invariants that JSON Schema cannot express.

Validation does not establish factual accuracy, runtime success, evaluation quality, safety, or reliability.

See the [roadmap](ROADMAP.md) for planned compatibility and stable-release work.
