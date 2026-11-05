# Investigation reports and incident context

Exploratory draft. One investigation report is a point-in-time operator summary
of an incident, its affected targets and available evidence. It standardizes the
shared investigation/report need without defining a generic report container,
runbook engine or replacement for producer reports.

[Schema](schemas/investigation_report.schema.json) ·
[Example](examples/investigation_report.json)

Required content comprises the envelope, incident context, summary, evidence,
timeline_entries, findings, missing_evidence_items and recovery. Arrays may be empty when
observations are missing; an affected target is always required.

| Section | Meaning |
| --- | --- |
| incident | Native incident id/status, projected status, detected_at and affected targets |
| summary | Statement, certainty and evidence_ids for the operator |
| evidence | Source-attributed references with report-local citation ids |
| findings | Distinct statements with certainty and evidence_ids |
| timeline_entries | Observed instants and evidence_ids; array order alone does not establish causality |
| missing_evidence_items | Explicit missing inputs; an empty array is no completeness guarantee |
| recovery | not_attempted, pending, verified, failed or unknown, with evidence_ids |

Incident status is open, investigating, resolved, escalated or unknown.
Summary/finding certainty is observed, hypothesis, contradictory or inconclusive.
Observed and contradictory claims require citations; hypotheses may have none.
Verified recovery also requires citations, but citation existence alone cannot
establish successful recovery. Incident closure and recovery verification are
separate: resolved may mean an operator dismissed an incident, while verified
recovery needs native recovery observations. Preserve native_state and explain
any projection in the implementation mapping.

Tower observed_failure maps to observed with its evidence citations;
hypothesis and contradictory retain their meaning. Tower missing becomes
missing_evidence_items. A Tower state awaiting_verification maps to investigating,
with recovery pending. Lens diagnosis findings can supply report evidence; the
projector retains native categories, confidence and evidence meaning rather
than reclassifying a suspicion into a confirmed cause. Chaos recovery evidence
and Evals gates remain separate inputs; neither becomes fleet health.

See [conformance](conformance.md) for reference scopes and validation limits.
