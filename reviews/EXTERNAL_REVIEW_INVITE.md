# External Review Invite

This is a ready-to-send packet for closing `reviews/decision-log.md` decision
`D-001` — the one gate every `v0.1`–`v0.4` acceptance criteria still needs:
review from someone with no DeepAgentLabs authorship, funding, or editorial
role over AIOS.

It exists so outreach doesn't stall on "who do we even ask" or "what do we
send them." Copy the message below, fill the brackets, and send it.

## Who to send it to

Anyone who fits the independence definition in `D-001` and has real exposure
to agent/LLM runtime instrumentation. Good candidate categories, roughly in
order of how directly comparable their domain is:

- Maintainers or core contributors of **other agent/LLM observability or
  tracing projects** (open-source tracing/eval tools, OpenTelemetry
  GenAI semantic-conventions contributors, agent-framework tracing
  maintainers). They will have the strongest opinions on `v0.2`/`v0.3`.
- **OpenTelemetry** contributors specifically, for the `v0.3` OTel-alignment
  gate (`specification/v0.3/acceptance-criteria.md`) — someone active in
  the OTel GenAI/AI semantic-conventions working group is close to ideal.
- Independent **AI reliability/safety practitioners** (incident response,
  red-teaming, eval-tooling authors) for the `v0.1`/`v0.3` safety-and-incident
  scenario.
- A **second, structurally different** agent framework or platform than the
  first reviewer's — pick for maximum disagreement surface, not agreement.

Two completed reviews close `D-001` (the closure rule in
`reviews/framework-mappings/README.md` requires at least two independent
mapping files against the same scenario set). They don't need to be from the
same category above — variety is more useful than volume.

## Copy-paste message

```text
Subject: 30–90 min external review request: AI Operations Specification (AIOS)

Hi [name],

I'm working on the AI Operations Specification (AIOS) — a vendor-neutral
draft contract for describing what happens when an AI/agentic system runs
(Runs, Steps, model interactions, tool calls, retrieval, memory,
evaluations, safety signals, incidents). Repo:
https://github.com/DeepAgentLabs/ai-operations-spec

It's specification-first, not tied to one SDK, and it's explicitly not
"vendor-neutral" yet in fact — that label is only earned once independent
implementers outside DeepAgentLabs have reviewed it. Right now the only
reviewers have been DeepAgentLabs' own sibling projects, which we've been
upfront isn't enough (see reviews/decision-log.md, decision D-001).

I'd like to ask for your independent read, with no obligation beyond what
you have time for:

1. Pick 1–3 scenarios from reviews/scenarios/ (each is a short narrative,
   ~5 min read):
   - scenario-01-customer-support.md
   - scenario-02-retry-and-recovery.md
   - scenario-03-safety-and-incident.md
2. Work through how you'd classify the objects, relationships, and events
   using specification/v0.1–v0.4, from your own framework's or your own
   independent judgment — not ours.
3. Record it using reviews/framework-mappings/external-reviewer-template.md
   (copy it to reviews/framework-mappings/<your-name-or-project>.md).

Rough time: 30–90 minutes depending on how many scenarios and how deep you
go. Partial answers or "this doesn't map, here's why" are exactly as useful
as full agreement — disagreement is the point of an independent review.

To send it back: open a PR against the repo with your file under
reviews/framework-mappings/, or just reply with the filled template and
I'll commit it with attribution. Public credit in the decision log is
optional — happy to keep you anonymous if you'd rather.

No pressure if this isn't a fit right now — thanks either way for
considering it.

[your name]
```

## Short version (for a DM / issue comment / forum post)

```text
Reviewing an early-draft spec for AI agent runtime telemetry (Runs, Steps,
model calls, tool calls, retrieval, safety signals, incidents —
https://github.com/DeepAgentLabs/ai-operations-spec) and looking for an
independent (non-DeepAgentLabs) read on whether the concepts hold up
against a real framework. ~30–90 min: pick a scenario from reviews/scenarios/,
fill reviews/framework-mappings/external-reviewer-template.md. Interested?
```

## After you get a response back

1. Save their filled template as `reviews/framework-mappings/<name>.md`.
2. Update `reviews/decision-log.md` `D-001`: move it toward `accepted` once
   two such files exist, and summarize where the independent reviewers
   agreed or disagreed with the DeepAgentLabs-internal mappings.
3. Update `reviews/evidence-matrix.md` rows that cite "at least two
   independent frameworks" for `v0.1`, `v0.2`, and `v0.3` — flip to `closed`
   only for rows their review actually covered, not the whole matrix at
   once.
4. Only then reconsider the `README.md`/`ROADMAP.md` Release Status badges.
