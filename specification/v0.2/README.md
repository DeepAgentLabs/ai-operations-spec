# v0.2 — Relationships and Execution Structure

## Status

Exploratory draft. This milestone tests and extends the v0.1 core concepts; it cannot freeze before v0.1.

## Goal

v0.2 defines how runtime objects are connected without requiring a particular telemetry transport or programming language. It enables independent implementations to describe the same execution graph consistently.

## Documents

- [Relationships](relationships.md) defines normative relationship types and graph rules.
- [Examples](examples.md) applies those rules to common execution shapes.
- [Acceptance criteria](acceptance-criteria.md) records the review gates for this milestone.

## Scope

v0.2 standardizes structural and causal meaning. It does not yet standardize serialized property names, event names, span mappings, or JSON Schema.
