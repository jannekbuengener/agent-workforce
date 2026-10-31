"""Deterministic twin for PREFERRED capability decision observability (#57).

Layer A only: given an explicit preferred_match flag, require compact decision
evidence. Does not invent a runtime router, semantic trigger engine, telemetry
DB, or LLM classifier. CAPABILITY_ROUTING.md owns the semantics.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
ROUTING_MD = REPO_ROOT / "docs" / "CAPABILITY_ROUTING.md"
META_EPIC_SKILL_MD = (
    REPO_ROOT / "docs" / "skills" / "cursor-meta-epic-executor" / "SKILL.md"
)
EVIDENCE_SKILL_MD = (
    REPO_ROOT / "docs" / "skills" / "evidence-backed-delivery" / "SKILL.md"
)

DECISIONS = frozenset(
    {
        "USED_PREFERRED",
        "LOCAL_EQUIVALENT",
        "NOT_USED_WITH_REASON",
    }
)
REASON_REQUIRED = frozenset({"LOCAL_EQUIVALENT", "NOT_USED_WITH_REASON"})

def record_preferred_capability_decision(
    *,
    capability_id: str,
    matched: bool,
    decision: str | None = None,
    reason: str | None = None,
    resolved_provider: str | None = None,
) -> dict[str, Any]:
    """Record or validate a PREFERRED routing decision for one capability.

    Inputs are explicit (tests/orchestrators supply preferred_match). This
    helper never classifies free-text triggers.
    """
    cap = str(capability_id or "").strip()
    result: dict[str, Any] = {
        "capability_id": cap,
        "matched": bool(matched),
        "ok": True,
        "problems": [],
        "entry": None,
        "blocked_required": False,
        "receipt_required": False,
    }

    if not cap:
        result["ok"] = False
        result["problems"].append("MISSING_CAPABILITY_ID")
        return result

    if not matched:
        # NOT_MATCHED → silence. No receipt noise.
        if decision is not None:
            result["ok"] = False
            result["problems"].append("DECISION_WITHOUT_MATCH")
        return result

    result["receipt_required"] = True

    if decision is None:
        result["ok"] = False
        result["problems"].append("SILENT_OMISSION")
        return result

    decision_norm = str(decision).strip()
    if decision_norm not in DECISIONS:
        result["ok"] = False
        result["problems"].append("UNKNOWN_DECISION")
        return result

    reason_text = str(reason or "").strip()
    if decision_norm in REASON_REQUIRED and not reason_text:
        result["ok"] = False
        result["problems"].append("MISSING_REASON")
        return result

    entry: dict[str, Any] = {
        "capability_id": cap,
        "decision": decision_norm,
    }
    if reason_text:
        entry["reason"] = reason_text
    if resolved_provider:
        # Optional evidence only; identity remains the capability id.
        entry["resolved_provider"] = str(resolved_provider).strip()

    result["entry"] = entry
    return result


def render_capability_routing_decisions(
    records: list[dict[str, Any]],
) -> str | None:
    """Render receipt section text, or None when there is nothing to show."""
    lines: list[str] = []
    for record in records:
        entry = record.get("entry")
        if not entry:
            continue
        lines.append("PREFERRED_CAPABILITY_DECISION")
        lines.append(f"Capability: {entry['capability_id']}")
        lines.append(f"Decision: {entry['decision']}")
        if entry.get("reason"):
            lines.append(f"Reason: {entry['reason']}")
        if entry.get("resolved_provider"):
            lines.append(f"Resolved provider: {entry['resolved_provider']}")
        lines.append("")
    if not lines:
        return None
    return "\n".join(lines).rstrip() + "\n"


def preferred_unavailable_outcome(
    *,
    matched: bool,
    available: bool,
    local_equivalent_sufficient: bool,
    reason: str,
) -> dict[str, Any]:
    """PREFERRED must not become REQUIRED when unavailable."""
    if not matched:
        return {
            "ok": True,
            "outcome": "NO_MATCH",
            "blocked_required": False,
            "decision": None,
        }
    if available:
        return {
            "ok": True,
            "outcome": "AVAILABLE",
            "blocked_required": False,
            "decision": "USED_PREFERRED",
        }
    if local_equivalent_sufficient:
        recorded = record_preferred_capability_decision(
            capability_id="deterministic_validation",
            matched=True,
            decision="LOCAL_EQUIVALENT",
            reason=reason,
        )
        return {
            "ok": recorded["ok"],
            "outcome": "LOCAL_EQUIVALENT",
            "blocked_required": False,
            "decision": "LOCAL_EQUIVALENT",
            "problems": recorded["problems"],
        }
    recorded = record_preferred_capability_decision(
        capability_id="deterministic_validation",
        matched=True,
        decision="NOT_USED_WITH_REASON",
        reason=reason or "preferred capability unavailable or unauthorized",
    )
    return {
        "ok": recorded["ok"],
        "outcome": "NOT_USED_WITH_REASON",
        "blocked_required": False,
        "decision": "NOT_USED_WITH_REASON",
        "problems": recorded["problems"],
    }


def decision_identity_uses_capability_id(entry: dict[str, Any]) -> bool:
    return bool(entry.get("capability_id")) and "provider" not in entry


def routing_md_documents_preferred_decisions() -> bool:
    text = ROUTING_MD.read_text(encoding="utf-8")
    required = (
        "PREFERRED_CAPABILITY_DECISION",
        "USED_PREFERRED",
        "LOCAL_EQUIVALENT",
        "NOT_USED_WITH_REASON",
        "CAPABILITY ROUTING DECISIONS",
    )
    return all(token in text for token in required)


def meta_epic_receipt_includes_capability_routing_decisions() -> bool:
    text = META_EPIC_SKILL_MD.read_text(encoding="utf-8")
    return "CAPABILITY ROUTING DECISIONS" in text


def evidence_delivery_documents_preferred_decision_surface() -> bool:
    text = EVIDENCE_SKILL_MD.read_text(encoding="utf-8")
    return "CAPABILITY ROUTING DECISIONS" in text or "PREFERRED_CAPABILITY_DECISION" in text
