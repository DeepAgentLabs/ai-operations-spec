# v0.1 Core Concepts

This document defines the normative conceptual vocabulary for v0.1. “Owns” means the information naturally belongs to the concept; it does not prescribe JSON nesting.

## Workflow

**Purpose.** A Workflow is a reusable definition of an AI-assisted process, capability, or orchestration pattern.

**Identity and lifecycle.** A Workflow has identity independent of any execution and may be versioned, activated, revised, or retired. Exact version fields are deferred.

**Owns.** Intended purpose, configuration identity, and declared process structure.

**References.** Implementations may associate a Workflow with its Runs and with definitions of agents, tools, prompts, and policies.

**Must not represent.** A Workflow MUST NOT mean one execution, its observed timestamps, or its measured outcome. Those belong to a Run.

## Run

**Purpose.** A Run is one execution instance of a Workflow or of an ad hoc AI process.

**Identity and lifecycle.** Every Run has its own identity and an execution lifecycle. Multiple Runs may refer to the same Workflow. A Run may exist without a registered Workflow definition.

**Owns.** Execution timing, completion condition, runtime status, aggregate operational evidence, and the boundary within which Requests and Steps occur.

**References.** A Run may refer to a Workflow, initiating Request, Steps, participating Agents, Evaluations, Safety Signals, Reliability Events, and Incidents.

**Must not represent.** A Run MUST NOT be used as the reusable definition of the process it executes.

## Request

**Purpose.** A Request is a unit of work or intent entering or advancing a Run.

**Identity and lifecycle.** A Request has identity within its operational context and a lifecycle from receipt through disposition. A Run may process one or many Requests; a Request may initiate a new Run or continue an existing one.

**Owns.** The submitted intent or input reference, source category, receipt context, and request-level outcome.

**References.** A Request may refer to its actor, Run, parent Request, response, and Steps caused by it.

**Must not represent.** A Request MUST NOT automatically mean the entire execution. It MUST NOT require raw sensitive content to be embedded.

## Step

**Purpose.** A Step is a bounded unit of execution within a Run.

**Identity and lifecycle.** A Step has identity within the Run and an execution lifecycle. Steps may be sequential, parallel, nested, retried, repeated, or graph-shaped.

**Owns.** Its activity category, execution timing, outcome, and step-local evidence.

**References.** A Step may refer to a responsible Agent and to one primary runtime occurrence such as a Model Interaction, Tool Invocation, RAG Retrieval, or Memory Operation. Formal graph edges are deferred to v0.2.

**Must not represent.** A Step MUST NOT be assumed to be an Agent, an LLM call, or a strictly sequential list item. A Step is the execution boundary; the associated occurrence explains what happened within it.

## Agent

**Purpose.** An Agent is an autonomous or semi-autonomous runtime participant that pursues a goal by selecting or coordinating actions.

**Identity and lifecycle.** An Agent has participant identity. A runtime Agent occurrence may be instantiated, act, wait, delegate, hand off, complete, or fail. A reusable agent definition and a runtime Agent occurrence are distinct.

**Owns.** Runtime role, goal or delegated objective, decision evidence, and participation outcome.

**References.** An Agent may participate in Runs and Steps and may invoke models and tools, use memory, delegate to other Agents, or produce Requests.

**Must not represent.** A deterministic function or isolated model call MUST NOT be labeled an Agent solely because it runs inside an AI system. Agency requires some bounded action selection or coordination responsibility.

## Model Interaction

**Purpose.** A Model Interaction is one invocation of a model endpoint, including language, multimodal, embedding, reranking, and other model operations.

**Identity and lifecycle.** Each attempted invocation is an occurrence. Retries are distinct attempts even when they serve the same Step.

**Owns.** Provider and model identity as observed, invocation parameters, usage, latency, response status, and references to sent and received content.

**References.** It may refer to a Prompt, Context, responsible Step or Agent, provider request identifier, and Reliability Events.

**Must not represent.** A model definition and a Model Interaction MUST NOT share one conceptual identity. A Model Interaction MUST NOT own retrieval, memory, or tool semantics merely because their output appeared in model input.

## Prompt

**Purpose.** A Prompt describes the instructions and content intentionally prepared for a model interaction.

**Identity and lifecycle.** A reusable prompt template may have identity and revision. A rendered Prompt is an occurrence derived from a template and variables. These identities must remain distinguishable.

**Owns.** Template reference, revision, rendering inputs, message roles or sections, and rendered-content evidence subject to privacy controls.

**References.** A Prompt may refer to Context and to the Model Interaction that consumed it.

**Must not represent.** A Prompt MUST NOT automatically include every piece of model input as prompt-authored content; injected Context remains distinguishable. Raw prompt content MUST NOT be required when a redacted reference is safer.

## Context

**Purpose.** Context is the assembled information made available to an AI participant for an action or decision beyond the immediate instruction.

**Identity and lifecycle.** A Context assembly is an occurrence. Its components may originate from conversation history, retrieval, memory, tools, policies, or application state.

**Owns.** Composition evidence, source categories, ordering or selection evidence, size, truncation, compression, and redaction information.

**References.** Context may refer to source Requests, RAG Retrievals, Memory Operations, Tool Invocations, Prompts, and consuming Steps.

**Must not represent.** Context MUST NOT erase provenance by treating all injected information as one authored prompt. It MUST NOT imply that included information was correct or used effectively.

## Tool Invocation

**Purpose.** A Tool Invocation is one attempt to call an external or application-provided capability.

**Identity and lifecycle.** Each attempt has occurrence identity and may be requested, authorized, started, completed, failed, timed out, or cancelled.

**Owns.** Tool definition reference, operation name, input and output evidence, authorization outcome, duration, and invocation result.

**References.** It may refer to the requesting Agent or Step, an MCP interaction, Reliability Events, and affected resources.

**Must not represent.** A tool definition and its invocation MUST NOT share one conceptual identity. A Tool Invocation MUST NOT be classified as successful merely because a transport call returned; application-level outcome remains distinct.

## RAG Retrieval

**Purpose.** A RAG Retrieval is an occurrence that searches, selects, or reranks external knowledge for grounding or context construction.

**Identity and lifecycle.** Each retrieval attempt has occurrence identity. Query generation, search, reranking, and selection may be separate Steps while belonging to one retrieval activity.

**Owns.** Query evidence, corpus or index reference, retrieval strategy, candidate and selected item evidence, ranks, scores, and retrieval outcome.

**References.** It may contribute items to Context and may be judged by Evaluations for relevance, recall, or groundedness.

**Must not represent.** Retrieval MUST NOT imply that results were placed into Context, cited, correct, or used by the model. Those are separate claims requiring evidence.

## Memory Operation

**Purpose.** A Memory Operation is one read, search, write, update, or deletion against state intended to persist beyond an immediate computation.

**Identity and lifecycle.** Each operation is an occurrence. The memory store or namespace may have separate identity.

**Owns.** Operation category, store reference, key or query evidence, value reference, consistency or freshness evidence, and outcome.

**References.** A Memory Operation may be performed by an Agent or Step and may contribute to Context.

**Must not represent.** Ordinary local variables or transient prompt assembly MUST NOT automatically be called Memory. A memory read MUST NOT imply its content was accurate, current, or used.

## Evaluation

**Purpose.** An Evaluation is a judgment about quality, correctness, groundedness, policy compliance, performance, or readiness.

**Identity and lifecycle.** An Evaluation occurrence has evaluator identity or method, target identity, criterion, and outcome. Human, model-based, rule-based, and programmatic evaluations are all valid when disclosed.

**Owns.** Criterion, method, score or categorical result, threshold where applicable, explanation, and evaluator evidence.

**References.** It must identify or correlate to its target, such as a Run, Step, response, retrieval result, or Prompt.

**Must not represent.** An Evaluation MUST NOT be treated as objective truth without its method and target. Runtime success MUST NOT imply evaluation success.

## Safety Signal

**Purpose.** A Safety Signal is evidence that content or behavior may match a safety, security, privacy, or policy concern.

**Identity and lifecycle.** A signal is detected at a point in a Run and may be reviewed, confirmed, dismissed, mitigated, or escalated.

**Owns.** Signal category, detector or policy reference, confidence or severity when available, affected target, and mitigation evidence.

**References.** It may refer to Requests, Prompts, Context, outputs, Tool Invocations, Steps, or Incidents.

**Must not represent.** A Safety Signal MUST NOT automatically mean a confirmed violation. Detection, policy decision, enforcement action, and Incident are distinct concepts.

## Reliability Event

**Purpose.** A Reliability Event records evidence about runtime continuity or resilience, including errors, retries, timeouts, fallbacks, circuit breaking, degradation, and recovery.

**Identity and lifecycle.** A Reliability Event occurs at a known or correlated point in a Run. Related events may form an attempt and recovery sequence in v0.2.

**Owns.** Event category, observed condition, affected target, operational effect, and recovery evidence.

**References.** It may refer to Runs, Steps, Model Interactions, Tool Invocations, Agents, or Incidents.

**Must not represent.** A Reliability Event MUST NOT automatically be an Incident. Routine retries may be operational evidence without requiring incident management.

## Incident

**Purpose.** An Incident is a managed record of a notable operational occurrence requiring awareness, investigation, mitigation, or follow-up.

**Identity and lifecycle.** An Incident has identity beyond a single event and may be opened, updated, mitigated, resolved, and reviewed. One Incident may aggregate evidence from multiple Runs.

**Owns.** Operational summary, severity, impact, detection and resolution timing, status, response evidence, and retained findings.

**References.** It may refer to Runs, Requests, Steps, Safety Signals, Reliability Events, Evaluations, and external incident systems.

**Must not represent.** Every error, failed Evaluation, or Safety Signal MUST NOT automatically become an Incident. Incident declaration is an operational decision.

## Model boundary summary

- Workflow defines; Run executes.
- Request introduces work; Step bounds activity.
- Agent participates and selects actions; Step records execution.
- Prompt instructs; Context supplies surrounding information.
- Model Interaction, Tool Invocation, RAG Retrieval, and Memory Operation record distinct runtime occurrences.
- Evaluation judges; Safety Signal detects concern; Reliability Event records stability behavior; Incident manages notable impact.
