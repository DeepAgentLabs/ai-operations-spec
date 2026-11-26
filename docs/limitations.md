# Limitations

This page lists what the AI Operations Specification defines and what it leaves to the products and tools that implement it, so you can plan around it. Planned work is tracked in the [Roadmap](../ROADMAP.md). Topic guides list further boundaries for their own areas.

## Scope of the contract

- **A contract, not a runtime.** AIOS defines artifacts, vocabularies and rules. Running agents, collecting telemetry, storing artifacts and hosting dashboards are done by the products that implement it.
- **No SDK or exporter in this repository.** Producers build artifacts in their own language. The DeepAgentLabs products provide exporters and validators; for example, Agentic Chaos exports a Run and AgenticLens validates artifacts and summarizes conformance.
- **Language-neutral.** The Python tooling in this repository validates the specification itself: schemas, catalogs, examples and the conformance suite.

## Validation

- **Schemas check structure only.** Identity, reference, timestamp and graph rules are semantic checks. The [portable conformance suite](../specification/v0.6/conformance-suite/README.md) lists the expected rule IDs for each case.
- **Process rules cannot be decided from one artifact.** Consumer and implementation obligations, such as preserving unknown extensions, are checked against the implementation's behavior. The [API reference](api-reference.md#conformance-rules) marks every rule's check kind.
- **Cross-artifact rules need the subject artifact.** Provenance resolution and digest checks run against the artifact bytes a consumer actually holds.
- **Structural validity is not factual accuracy.** A valid artifact describes what a producer recorded; it does not prove that the recorded outcome was correct.

## Versioning

- **One marker per family.** Run and Workflow use `0.4-draft`, provenance uses `0.6-draft` and the operational artifacts use `0.8-draft`. Consumers route by the marker an artifact declares.
- **No patch levels.** Version markers are `MAJOR.MINOR` only; every normative change is additive (minor) or breaking (major). See [Versioning and compatibility](../specification/v0.5/versioning.md).
- **Repository versions are separate.** A repository release (such as 1.0.2) packages documents, schemas and fixtures; it does not change any artifact marker.

## Vocabularies and extensions

- **Closed vocabularies are fixed by the schemas.** Object types, reference types, relationship types and canonical event names are closed. A value outside them is a schema violation, so new meaning goes in an extension.
- **Extensions use reverse-domain names.** The `aiops` namespace is reserved. Consumers preserve extensions they do not recognize but do not interpret them.
- **`attributes` is open.** Its keys are not standardized; consumers preserve them without assigning shared meaning.

## OpenTelemetry companion

- **A projection, not a replacement.** The [OpenTelemetry companion](../specification/v0.6/otel-binding.md) maps every canonical event to spans and span events. Flat OTel attributes cannot represent every nested extension, so keep the original artifact when lossless reconstruction matters.
- **The companion is non-normative.** Its `aios.*` attributes are transport keys for the mapping, not core AIOS fields or upstream semantic conventions.

## Companion profiles

- **Non-normative profiles.** Access evidence, Sidecar correlation and Sidecar contracts have their own schemas and guides. They add no conformance rules and do not change the core families.

## Privacy

- **Redaction is the producer's job.** The operational rules forbid credentials, credential hashes, raw tool arguments and privileged context in artifacts. Provenance records reference sensitive content by URI or digest rather than copying it. A schema cannot detect a secret inside free text, so producers apply redaction before emitting.
- **References are not fetched automatically.** Consumers do not fetch a URI or execute content merely because an artifact contains it.
