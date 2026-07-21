# v0.4 Acceptance Criteria

## Schema coverage

- [x] Workflow definitions and Run occurrences have separate schemas.
- [x] Requests, Steps, Agents, runtime occurrences, evidence, Incidents, relationships, and semantic events are representable.
- [x] Valid and invalid fixtures are automatically tested.
- [x] Sensitive content is optional and extensibility is namespaced.

## Review gates

- [ ] Resolve all open v0.1 through v0.3 review gates.
- [ ] Validate artifacts produced by at least two independent implementations.
- [ ] Review identifier, reference, extension, and unknown-value behavior.
- [ ] Replace the draft version marker when the milestone freezes.

## Exit condition

Independent producers can emit structurally equivalent artifacts that validate without importing a DeepAgentLabs package.
