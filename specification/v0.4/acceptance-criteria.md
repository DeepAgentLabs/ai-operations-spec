# v0.4 Acceptance Criteria

## Schema coverage

- [x] Workflow definitions and Run occurrences have separate schemas.
- [x] Requests, Steps, Agents, runtime occurrences, evidence, Incidents, relationships, and semantic events are representable.
- [x] Valid and invalid fixtures are automatically tested.
- [x] Sensitive content is optional and extensibility is namespaced.
- [x] `event_name` accepts both the canonical `aiops.*` catalog and reverse-domain
  namespaced extension events; extension names MUST NOT collide with the
  `aiops` namespace.

## Review gates

- [ ] Resolve all open v0.1 through v0.3 review gates.
- [ ] Validate artifacts produced by at least two independent implementations.
- [x] Review identifier, reference, extension, and unknown-value behavior
  (decision `D-004`; see `specification/v0.4/conformance.md` and the
  `run-unknown-relationship-type.json`, `run-unknown-object-type.json`, and
  `run-namespaced-extensions.json` fixtures).
- [ ] Replace the draft version marker when the milestone freezes.

## Exit condition

Independent producers can emit structurally equivalent artifacts that validate without importing a DeepAgentLabs package.
