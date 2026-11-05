"""Repository checks for the 0.8-draft operational artifacts; not an SDK."""
from datetime import datetime


def instant(value: str) -> datetime:
    return datetime.fromisoformat(value.upper().replace("Z", "+00:00"))


def operational_issues(document: dict) -> list[tuple[str, str]]:
    """Check a schema-valid artifact without fetching or executing any reference."""
    issues: list[tuple[str, str]] = []
    kind = document["artifact_type"]
    created = instant(document["created_at"])

    def problem(rule: str, message: str) -> None:
        issues.append((f"AIOS-0.8-{rule}", message))

    if kind == "audit_event":
        if instant(document["occurred_at"]) > created:
            problem("R04", "An audit event occurred after it was recorded")
        if document["id"] in document.get("causal_event_ids", []):
            problem("R07", "An audit event cannot cause itself")
        return issues

    groups = [document["evidence"]]
    if kind == "investigation_report":
        groups.extend([document["findings"], document["timeline_entries"]])
    identities = [item["id"] for group in groups for item in group]
    if len(identities) != len(set(identities)):
        problem("R02", "Evidence, finding and timeline identities must be unique")

    if kind == "verification_signal":
        if document["grounding"]["status"] in {"grounded", "partial"} and not document["evidence"]:
            problem("R05", "Assessed grounding needs at least one evidence reference")
        return issues

    evidence = {item["id"] for item in document["evidence"]}
    cited = [document["summary"], document["recovery"], *document["findings"], *document["timeline_entries"]]
    for item in cited:
        if not set(item["evidence_ids"]) <= evidence:
            problem("R03", "A citation names undeclared evidence")
    for item in [document["incident"], *document["timeline_entries"]]:
        value = item.get("occurred_at", item.get("detected_at"))
        if instant(value) > created:
            problem("R04", "An incident or timeline observation follows report creation")
    for item in [document["summary"], *document["findings"]]:
        if item["certainty"] in {"observed", "contradictory"} and not evidence.intersection(item["evidence_ids"]):
            problem("R06", "Observed or contradictory claims need citations")
    if document["recovery"]["status"] == "verified" and not evidence.intersection(document["recovery"]["evidence_ids"]):
        problem("R06", "Verified recovery needs citations")
    return issues
