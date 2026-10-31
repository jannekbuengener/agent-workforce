"""Deterministic twin for Head of Knowledge weekly Owner report (#73).

Validates report schema, fail-closed data-quality rules, and example generation
from fixture evidence. Does not send email or invent KPIs.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_MD = REPO_ROOT / "docs" / "HEAD_OF_KNOWLEDGE_OWNER_REPORT.md"
EMPLOYEE_MD = REPO_ROOT / "agents" / "dieter-datenbank.md"
REGISTRY_PATH = REPO_ROOT / "capabilities" / "REGISTRY.yml"
DEFAULT_FIXTURE = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "knowledge-owner-report"
    / "example_report.yml"
)

REQUIRED_SECTION_IDS = (
    "what_happened",
    "what_is_critical",
    "what_was_decided",
    "current_data_quality_situation",
    "relevant_uncertainties",
    "concrete_action_recommendations",
)

CAPABILITY_ID = "knowledge_owner_report"
ACTOR_ID = "workforce.employee.dieter-datenbank.v1"
UNQUANTIFIABLE = "Datenqualität: nicht belastbar quantifizierbar"


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_registry(path: Path | None = None) -> dict[str, Any]:
    data = load_yaml(path or REGISTRY_PATH)
    if not isinstance(data, dict):
        raise ValueError("registry must be a mapping")
    return data


def contract_is_complete() -> bool:
    text = CONTRACT_MD.read_text(encoding="utf-8")
    return all(
        [
            "CONTRACT_COMPLETE" in text,
            "HEAD_OF_KNOWLEDGE_OWNER_REPORT_DEFINED" in text,
            "what_happened" in text,
            "nicht belastbar quantifizierbar" in text,
            "immediate_escalation_included: false" in text,
            "INVENTED_QUALITY_KPI" in text,
        ]
    )


def employee_binds_report_contract() -> bool:
    text = EMPLOYEE_MD.read_text(encoding="utf-8")
    return all(
        [
            "knowledge_owner_report" in text,
            "docs/HEAD_OF_KNOWLEDGE_OWNER_REPORT.md" in text,
            "what_happened" in text,
            "capability_id: knowledge_owner_report" in text,
        ]
    )


def registry_points_at_contract(registry: dict[str, Any] | None = None) -> bool:
    caps = (registry or load_registry()).get("capabilities") or {}
    entry = caps.get(CAPABILITY_ID) or {}
    return str(entry.get("contract") or "").endswith(
        "HEAD_OF_KNOWLEDGE_OWNER_REPORT.md"
    ) and entry.get("requirement") == "REQUIRED"


def _nonempty_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_report(
    report: dict[str, Any],
    *,
    employment_state: str = "ACTIVE",
    runtime_exists: bool = True,
    capability_authorized: bool = True,
) -> dict[str, Any]:
    """Return validation result for a candidate Owner report."""
    result: dict[str, Any] = {
        "allowed": False,
        "outcome": "DENIED",
        "gate": "UNKNOWN",
        "problems": [],
    }

    if not capability_authorized:
        result.update(
            outcome="BLOCKED_REQUIRED_CAPABILITY_UNAVAILABLE",
            gate="CAPABILITY_UNAUTHORIZED",
            problems=["knowledge_owner_report not authorized"],
        )
        return result

    if employment_state != "ACTIVE" or not runtime_exists:
        result.update(
            outcome="DENIED_RUNTIME_NOT_PROVISIONED",
            gate="RUNTIME_NOT_PROVISIONED",
            problems=["employee not ACTIVE with runtime_exists true"],
        )
        return result

    if not isinstance(report, dict):
        result.update(
            outcome="DENIED_INVALID_REPORT",
            gate="SCHEMA_INVALID",
            problems=["report must be a mapping"],
        )
        return result

    problems: list[str] = []
    if report.get("report_kind") != "head_of_knowledge_weekly_owner_report":
        problems.append("report_kind mismatch")
    if report.get("capability_id") != CAPABILITY_ID:
        problems.append("capability_id mismatch")
    if report.get("actor_employee_id") != ACTOR_ID:
        problems.append("actor_employee_id mismatch")
    if report.get("immediate_escalation_included") is not False:
        problems.append("immediate escalation must stay out of weekly report")

    sections = report.get("sections") or {}
    if not isinstance(sections, dict):
        problems.append("sections must be a mapping")
        sections = {}

    for section_id in REQUIRED_SECTION_IDS:
        if section_id not in sections:
            problems.append(f"missing section: {section_id}")

    for key in (
        "what_happened",
        "what_is_critical",
        "what_was_decided",
    ):
        if key in sections and not _nonempty_text(sections.get(key)):
            problems.append(f"empty section: {key}")

    dq = sections.get("current_data_quality_situation")
    if isinstance(dq, dict):
        quantifiable = bool(dq.get("quantifiable"))
        percentage = dq.get("percentage")
        method_id = dq.get("method_id")
        summary = dq.get("summary")
        if quantifiable:
            if percentage is None or not _nonempty_text(str(method_id or "")):
                problems.append("INVENTED_QUALITY_KPI")
        else:
            if percentage is not None:
                problems.append("INVENTED_QUALITY_KPI")
            if not _nonempty_text(summary) or UNQUANTIFIABLE not in str(summary):
                problems.append("unquantifiable summary required")
    elif "current_data_quality_situation" in sections:
        problems.append("current_data_quality_situation must be a mapping")

    uncertainties = sections.get("relevant_uncertainties")
    if "relevant_uncertainties" in sections and not isinstance(
        uncertainties, list
    ):
        problems.append("relevant_uncertainties must be a list")
    elif isinstance(uncertainties, list) and not uncertainties:
        problems.append("relevant_uncertainties must not be empty")

    recommendations = sections.get("concrete_action_recommendations")
    if "concrete_action_recommendations" in sections and not isinstance(
        recommendations, list
    ):
        problems.append("concrete_action_recommendations must be a list")
    elif isinstance(recommendations, list):
        if not recommendations:
            problems.append("concrete_action_recommendations must not be empty")
        for item in recommendations:
            if not isinstance(item, dict) or not _nonempty_text(item.get("text")):
                problems.append("recommendation entries need non-empty text")
                break

    if problems:
        gate = (
            "INVENTED_QUALITY_KPI"
            if "INVENTED_QUALITY_KPI" in problems
            else "SCHEMA_INVALID"
        )
        result.update(
            allowed=False,
            outcome="DENIED_INVALID_REPORT",
            gate=gate,
            problems=problems,
        )
        return result

    result.update(
        allowed=True,
        outcome="REPORT_VALID",
        gate="OWNER_REPORT_ALLOWED",
        problems=[],
    )
    return result


def build_example_report_from_fixture(
    path: Path | None = None,
) -> dict[str, Any]:
    fixture = load_yaml(path or DEFAULT_FIXTURE)
    if not isinstance(fixture, dict):
        raise ValueError("fixture must be a mapping")
    evidence = fixture.get("evidence") or {}
    period = fixture.get("period") or {
        "start": "2026-10-24",
        "end": "2026-10-31",
    }
    return {
        "schema_version": 1,
        "report_kind": "head_of_knowledge_weekly_owner_report",
        "capability_id": CAPABILITY_ID,
        "actor_employee_id": ACTOR_ID,
        "period": period,
        "channel": "email",
        "sections": {
            "what_happened": str(evidence.get("what_happened") or "").strip(),
            "what_is_critical": str(evidence.get("what_is_critical") or "").strip(),
            "what_was_decided": str(evidence.get("what_was_decided") or "").strip(),
            "current_data_quality_situation": {
                "summary": UNQUANTIFIABLE,
                "quantifiable": False,
                "percentage": None,
                "method_id": None,
                "band": None,
            },
            "relevant_uncertainties": list(
                evidence.get("relevant_uncertainties") or ["unspecified"]
            ),
            "concrete_action_recommendations": list(
                evidence.get("concrete_action_recommendations")
                or [{"type": "other", "text": "none recorded"}]
            ),
        },
        "evidence_refs": list(evidence.get("evidence_refs") or []),
        "immediate_escalation_included": False,
    }


def render_human_report(report: dict[str, Any]) -> str:
    sections = report.get("sections") or {}
    dq = sections.get("current_data_quality_situation") or {}
    dq_line = dq.get("summary") if isinstance(dq, dict) else str(dq)
    uncertainties = sections.get("relevant_uncertainties") or []
    recs = sections.get("concrete_action_recommendations") or []
    lines = [
        "# Head of Knowledge — Weekly Owner Report",
        "",
        f"Period: {report.get('period')}",
        f"Channel: {report.get('channel')}",
        "",
        "## Was ist passiert?",
        str(sections.get("what_happened") or ""),
        "",
        "## Was ist kritisch?",
        str(sections.get("what_is_critical") or ""),
        "",
        "## Was wurde entschieden?",
        str(sections.get("what_was_decided") or ""),
        "",
        "## Aktuelle Datenqualität",
        str(dq_line or ""),
        "",
        "## Relevante Unsicherheiten",
    ]
    for item in uncertainties:
        lines.append(f"- {item}")
    lines.extend(["", "## Konkrete Handlungsempfehlungen"])
    for item in recs:
        if isinstance(item, dict):
            lines.append(f"- ({item.get('type')}) {item.get('text')}")
        else:
            lines.append(f"- {item}")
    return "\n".join(lines) + "\n"
