# v0.1 Terminology

## Definition and occurrence

A **definition** describes reusable configuration or intended behavior. An **occurrence** is evidence of something that happened during a Run. Implementations must not silently substitute one for the other.

Examples: a Workflow is a definition; a Run is an occurrence. A tool definition describes an available capability; a Tool Invocation records its use.

## Identity

**Identity** distinguishes an object from peers and allows evidence to refer to it. v0.1 requires the concept of identity but does not prescribe identifier syntax.

A reusable definition and its runtime occurrence have separate identities. Many Runs may refer to one Workflow.

## Lifecycle

A **lifecycle** is the meaningful progression of an occurrence, such as created, active, completed, failed, or cancelled. v0.1 describes which concepts have lifecycles but does not standardize state values or events.

## Evidence

**Evidence** is recorded information supporting an operational claim. Model responses, tool results, scores, safety detections, retry records, and timestamps can be evidence. Evidence may be redacted or referenced rather than embedded.

## Actor and participant

An **actor** initiates or influences work. A **participant** performs work inside a Run. Users, services, agents, and schedulers may be actors. An Agent is a particular kind of runtime participant.

## Input, output, and content

**Input** enters an occurrence; **output** is produced by it. **Content** is the payload carried by either. The specification must permit secure references, hashes, summaries, or redactions instead of requiring sensitive raw content.

## Correlation and causation

**Correlation** associates objects that belong to the same operational context. **Causation** asserts that one occurrence led to another. They are not interchangeable. Relationship encoding is deferred to v0.2.

## Parent and child

A **parent-child relationship** expresses structural or causal nesting between occurrences. It does not by itself imply sequential execution. Formal graph rules are deferred to v0.2.

## Sequential, parallel, and graph-shaped execution

- **Sequential** activities have an intended order.
- **Parallel** activities may overlap.
- **Graph-shaped** execution may branch, join, retry, loop, or delegate.

v0.1 acknowledges these shapes without defining their serialization.

## Success, failure, and degradation

- **Success** means an occurrence satisfied its operational completion condition.
- **Failure** means it did not complete as intended.
- **Degradation** means it completed with reduced quality, performance, safety, or capability.

Business quality and runtime completion are separate: a Run may complete successfully while failing an Evaluation.

## Telemetry and transport

**Telemetry** is an observation representation. A **transport** moves or exports it. OpenTelemetry, OTLP, JSON, logs, and message systems are representations or transports—not core runtime objects.

## Runtime object

A **runtime object** is a conceptual entity used to describe execution or operational evidence. It does not imply an object-oriented programming class.

## Normative versus conceptual example

A normative statement defines required meaning. A conceptual example tests that meaning without committing to a wire format. JSON Schema begins at v0.4.
