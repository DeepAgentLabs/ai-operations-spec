# AI Operations Specification

## Status

Draft `v0`

This document defines the first draft of the AI Operations Specification, a
shared operational data model for production AI systems.

## Purpose

The specification provides a common contract for representing AI execution in a
portable, inspectable form. It is intended to make interoperability possible
between:

- frameworks and orchestration runtimes
- observability and telemetry tooling
- resilience and chaos testing systems
- local analysis, audits, and CI workflows

## Primary Artifact

The primary reference JSON representation is `workflow.json`.

This JSON artifact is a serialization of the AI Operations Specification, not
the definition of the specification itself.

## Core Concepts

### Workflow

A workflow is one complete execution of an AI system or AI-assisted task.

Examples:

- a customer support run
- a RAG answer generation flow
- a multi-agent planning and execution cycle
- a degraded or chaos-tested execution

### Step

A step is a meaningful unit within a workflow.

Examples:

- planner step
- retriever step
- tool call
- LLM call
- memory step
- final response step

### Metrics

Metrics describe cost, token, latency, and related execution properties at the
workflow or step level.

### Evaluations

Evaluations describe quality, correctness, policy, or readiness judgments
associated with a workflow or step.

### Incidents

Incidents describe failures, degradations, anomalies, or noteworthy operational
events related to a workflow execution.

### Extensions

Extensions allow additional structured data to be attached without breaking core
interoperability, provided the base contract remains valid.

## Design Principles

- The specification must remain framework-agnostic.
- The specification must remain language-neutral.
- The specification should be additive by default.
- The specification should support local files and CI workflows.
- The specification should support interoperability without requiring a hosted
  control plane.

## Compatibility

Compatibility should follow these rules:

- additive fields are preferred over destructive renames
- unknown extension fields should not invalidate otherwise valid artifacts
- changes that break existing consumers should require a new major version

## Ownership

DeepAgentLabs stewards the specification.

Individual tools such as `agenticlens` may implement, extend, validate, and
export artifacts that conform to it, but no single tool owns the contract.

## Near-Term Follow-Up

This draft should eventually be expanded with:

- a machine-readable JSON Schema
- canonical example artifacts
- extension conventions
- field-level definitions and required/optional rules
- explicit version markers inside the artifact
