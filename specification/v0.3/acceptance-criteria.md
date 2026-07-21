# v0.3 Acceptance Criteria

## Convention coverage

- [x] Canonical naming and extension namespace rules are defined.
- [x] Identity, time, correlation, privacy, and measurement rules are defined.
- [x] Lifecycle events cover all v0.1 runtime areas.
- [x] Detection, judgment, enforcement, failure, and incident semantics remain distinct.

## Review gates

- [ ] Validate conventions against OpenTelemetry design principles.
- [ ] Validate event coverage against at least two reference implementations.
- [ ] Decide whether transport mappings belong in separate implementation profiles.
- [ ] Record decisions and update affected documents.

## Exit condition

Independent producers attach the same meaning to equivalent events without sharing an SDK.
