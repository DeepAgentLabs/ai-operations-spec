# v0.3 Semantic Event Examples

These fragments demonstrate meaning, not the v0.4 artifact format.

## Successful model step

```text
aiops.step.started
aiops.prompt.rendered
aiops.context.assembled
aiops.model.requested
aiops.model.responded
aiops.step.completed
```

Prompt and Context remain separately identifiable even when a provider combines them.

## Tool denied by policy

```text
aiops.tool.requested
aiops.safety.detected
aiops.tool.authorized   outcome=denied
aiops.safety.mitigated mitigation=blocked
```

No Incident is implied.

## Model retry

Two model attempts have distinct interaction identities. A Reliability Event targets the failed first attempt; the successful second attempt follows it under the v0.2 retry model.
