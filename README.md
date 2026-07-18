# AI Operations Specification

The **AI Operations Specification** defines a language-neutral operational model for AI and agentic systems.

DeepAgentLabs stewards the standard. AgenticLens, Agentic Chaos, and DeepAgent MCP are reference implementations and consumers; none of them owns the contract.

## Current milestone

**v0.1 is a core-concepts draft.** It defines the vocabulary and boundaries of the runtime model. It intentionally does not standardize JSON fields, semantic event names, SDK classes, or transports yet.

Start here:

- [v0.1 overview](specification/v0.1/README.md)
- [Core concepts](specification/v0.1/core-concepts.md)
- [Terminology](specification/v0.1/terminology.md)
- [Conceptual examples](specification/v0.1/examples.md)
- [Acceptance criteria](specification/v0.1/acceptance-criteria.md)
- [Roadmap](ROADMAP.md)

The earlier workflow JSON Schema experiment is preserved as an [unreleased v0.4 draft](drafts/v0.4/README.md). It is not a conforming v0.1 contract.

## Specification-first rule

Normative concepts and relationships are defined here before package-specific models are changed. Implementations may experiment, but they must not redefine core terms independently.

## Scope boundaries

This repository defines meaning and interoperability. It does not contain:

- instrumentation SDK implementations
- dashboards or hosted services
- package-specific recommendation logic
- provider pricing catalogs
- transport-specific exporters

## Contributing

A proposal belongs here when it clarifies the runtime model, relationships, semantic conventions, schemas, compatibility, or extensions for all implementers. Package-only behavior belongs in its package repository.
