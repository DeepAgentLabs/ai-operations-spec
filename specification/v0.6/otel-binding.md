# OpenTelemetry companion binding

Status: non-normative, exploratory companion profile `aios.otel/1`, shipped
in repository v0.6.2. It neither changes canonical events nor establishes
AIOS or OpenTelemetry conformance. There is no exporter SDK in this repository.

## Upstream baseline

This profile deliberately targets the pinned OpenTelemetry semantic conventions
[v1.37.0 GenAI spans](https://github.com/open-telemetry/semantic-conventions/blob/v1.37.0/docs/gen-ai/gen-ai-spans.md)
and [v1.37.0 GenAI attributes](https://github.com/open-telemetry/semantic-conventions/blob/v1.37.0/docs/registry/attributes/gen-ai.md).
That GenAI baseline has Development status. It is a reproducible baseline,
not a claim to track the latest upstream release. Adapters should declare
both their upstream baseline and this profile revision, and explicitly opt
into any later upstream convention change. Existing instrumentation's
stability opt-in behavior remains under its owner's control.

## Mapping and identity

The [mapping catalog](otel/mapping.json) covers every canonical v0.3 event.
It proposes spans for observed operations and keeps the original `aiops.*`
transitions as span events. A span event's timestamp is `occurred_at`, its
name is `event_name`, and its flat attributes include `aios.event_id`,
`aios.object_id`, `aios.object_type` and, when known, `aios.run_id`.
These `aios.*` attributes are this companion profile's transport keys, not
new AIOS core fields or upstream semantic conventions. Keep the entire
original artifact separately when lossless reconstruction matters.

| AIOS observation | Suggested span | Upstream attributes, only when observed |
| --- | --- | --- |
| Run / Request / Step | Application-defined INTERNAL span | No invented GenAI operation |
| Agent lifecycle | Existing agent/application span | Agent identity only if known; waiting is an event, not completion |
| Model Interaction | One CLIENT inference span per attempt (INTERNAL for a local in-process model) | `gen_ai.operation.name`, `gen_ai.provider.name`, `gen_ai.request.model`, `gen_ai.response.model`, `gen_ai.response.id` |
| Tool Invocation | INTERNAL `execute_tool {tool name}` span | `gen_ai.operation.name=execute_tool`, `gen_ai.tool.name`, `gen_ai.tool.call.id` when known |
| Retrieval / memory | Existing instrumented operation or application-defined INTERNAL span | No universal GenAI operation asserted here |
| Evaluation / safety / reliability / incident | Event on an appropriate existing span; otherwise a separate log record with the same identity and timestamp | No upstream equivalent asserted here |
| Prompt / Context | Event, with references or redaction metadata | Content capture is opt-in |

Do not open or end a span without observed timing. Missing starts/ends,
sampling, asynchronous findings and late events may require separate logs;
do not attach a late result to a fabricated live span. Each retry gets a
separate span and occurrence identity. An AIOS Step is not synonymous with
every OTel span. An OTel trace ID is not a Run ID and a conversation ID is
not necessarily either. Keep correlation explicitly; do not coerce arbitrary
AIOS IDs into hexadecimal span/trace IDs.

Containment can map to span parentage only when it accurately represents
execution nesting. `caused`, `depends-on`, delegation, cross-Run and join
relationships may need span links with explicit AIOS source/target identities.
Do not turn every graph edge into a parent or infer a complete AIOS graph
from an OTel tree. Resource `service.name` and `service.version` describe the
emitting service, not the Agent or requested model. Do not copy arbitrary
resource metadata into an artifact without a documented mapping.

## Outcomes, measurements and content

Map observed operational failures to OTel ERROR status with a bounded
`error.type` when available. A failed evaluation, safety detection, denied
action or cancelled Run does not automatically mean a transport/operation
error. An `aiops.tool.authorized` event proves authorization only, not
execution, completion or containment. Successful HTTP transport does not
prove tool application success. Preserve AIOS outcome attributes on events.

AIOS duration measurements use milliseconds; OTel span timestamps/durations
use their transport's time representation. Convert units explicitly (the
example's 25 ms becomes 25,000,000 ns); never reinterpret milliseconds as
seconds. Observed token totals can populate `gen_ai.usage.input_tokens` and
`gen_ai.usage.output_tokens`. Keep measurement kind (`observed`, `estimated`,
`derived`), cost currency and score scale in companion attributes or retained
artifacts; do not pass derived/estimated values off as observed usage. A
missing metric is unknown, not zero.

Default to excluding prompts, context, tool arguments/results, secrets and
personal content from spans, events and resource attributes. References,
hashes and summaries can themselves be sensitive: redact/authorize them too.
Do not fetch referenced content during conversion. Record any redaction or
loss. Flat OTel attributes cannot represent every nested AIOS extension;
retain the original or record a documented encoding and loss report.

## Examples and validation boundary

The [paired example](otel/example.json) contains a schema-valid `0.4-draft`
Run and a readable transport projection. It is **not OTLP JSON** and is not
accepted by an OTLP collector. Two tool attempts preserve separate occurrence,
event and span identities; the first fails and the retry succeeds. Optional
transport status does not rewrite native outcomes.

```bash
uv run pytest tests/test_otel_binding.py
```

Tests check event coverage, graph/schema validity, preserved identities,
observed timestamps, retry distinction, units and outcome separation. They
do not certify an exporter, delivery completeness or runtime instrumentation.
To build an adapter, pin the catalog, validate its input, explicitly record
losses and unsupported fields, then test its real OTel output against the
chosen upstream SDK/collector. See the [migration guide](migration-guide.md).
