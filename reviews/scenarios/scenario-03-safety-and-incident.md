# Scenario 03: Safety Signal and Incident Escalation

## Narrative

A request appears to contain prompt injection aimed at exfiltrating sensitive data through a privileged tool. A detector emits a safety signal. Policy blocks the tool request. Later review determines no data left the system, so the event remains a blocked attempt and does not automatically become an incident. In a variant of the same scenario, if sensitive data is exposed or operational impact occurs, responders open an incident linked to the run and prior safety evidence.

## Minimum expected objects

- one `Run`
- one `Request`
- one or more `Step` occurrences
- one `Safety Signal`
- one blocked `Tool Invocation`
- optional `Incident` depending on outcome

## v0.1 review questions

- Is the safety signal distinct from the enforcement result?
- Is a blocked tool invocation distinct from an incident?
- Under what condition does an actual `Incident` begin?

## v0.2 review questions

- How do the safety signal and tool block relate to the request or step?
- If an incident is opened later, what relationship links it to prior evidence?

## v0.3 expected event areas

- safety detected
- tool requested
- authorization or denial
- mitigation or block
- incident opened if impact occurs

## v0.4 artifact expectations

- incident remains optional
- references can link signals, blocked tool attempts, and later incident evidence
- extension events can be namespaced if a producer needs provider-specific safety detail
