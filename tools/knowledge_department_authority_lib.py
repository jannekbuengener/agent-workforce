"""Deterministic twin for Head of Knowledge FOUNDING_SOLO authority (#70).

Layer A only: encodes role/capability gates from
docs/KNOWLEDGE_DEPARTMENT_AUTHORITY.md and agents/dieter-datenbank.md.
Does not invent a mutable workforce runtime DB or activate Dieter.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PRESSURE_CASES = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "knowledge-department-authority"
    / "pressure_cases.yml"
)
EMPLOYEE_MD = REPO_ROOT / "agents" / "dieter-datenbank.md"
AUTHORITY_MD = REPO_ROOT / "docs" / "KNOWLEDGE_DEPARTMENT_AUTHORITY.md"
OWNER_REPORT_MD = REPO_ROOT / "docs" / "HEAD_OF_KNOWLEDGE_OWNER_REPORT.md"
REGISTRY_PATH = REPO_ROOT / "capabilities" / "REGISTRY.yml"
ROUTING_MD = REPO_ROOT / "docs" / "CAPABILITY_ROUTING.md"
POLICY_MD = REPO_ROOT / "docs" / "WORKFORCE_POLICY.md"

REQUIRED_CAPABILITY_IDS = {
    "knowledge_department_decision",
    "knowledge_owner_report",
}
PREFERRED_CAPABILITY_IDS = {
    "shared_context_evidence",
    "improvement_read",
}

FORBIDDEN_ACTION_GATES = {
    "self_grant_authority": ("DENIED_FORBIDDEN_ACTION", "SELF_GRANT_DENIED"),
    "mutate_target_repo_product": (
        "DENIED_FORBIDDEN_ACTION",
        "TARGET_REPO_AUTHORITY_PRESERVED",
    ),
    "raw_database_admin": ("DENIED_FORBIDDEN_ACTION", "RAW_DB_ADMIN_DENIED"),
    "generic_memory_write": (
        "DENIED_FORBIDDEN_ACTION",
        "MEMORY_WRITE_OUT_OF_SCOPE",
    ),
}

BOARD_MANAGER_ONLY = {
    "improvement_management_write",
    "improvement_github_issue_create",
}


def load_pressure_cases(path: Path | None = None) -> dict[str, Any]:
    target = path or DEFAULT_PRESSURE_CASES
    data = yaml.safe_load(target.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "cases" not in data:
        raise ValueError(f"invalid pressure cases file: {target}")
    return data


def load_registry(path: Path | None = None) -> dict[str, Any]:
    data = yaml.safe_load((path or REGISTRY_PATH).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("registry must be a mapping")
    return data


def role_allows_capability(
    role: str, capability_id: str, pack: dict[str, Any] | None = None
) -> bool:
    roles = (pack or load_pressure_cases()).get("roles") or {}
    entry = roles.get(role) or {}
    allowed = set(entry.get("allowed_capabilities") or [])
    denied = set(entry.get("denied_capabilities") or [])
    if capability_id in denied:
        return False
    return capability_id in allowed


def evaluate_case(
    case: dict[str, Any], *, pack: dict[str, Any] | None = None
) -> dict[str, Any]:
    case_id = str(case["id"])
    data = case.get("input") or {}
    expect = case.get("expect") or {}
    pack = pack or load_pressure_cases()
    actual: dict[str, Any] = {"id": case_id}

    role = str(data.get("role") or "")
    action = str(data.get("action") or "")
    capability_id = str(data.get("capability_id") or "")
    employment_state = str(data.get("employment_state") or "")
    runtime_exists = bool(data.get("runtime_exists"))
    evidence_sufficient = bool(data.get("evidence_sufficient"))
    half_certain = bool(data.get("half_certain_as_fact"))
    target_mutation = bool(data.get("target_repo_mutation"))

    if target_mutation or action == "mutate_target_repo_product":
        outcome, gate = FORBIDDEN_ACTION_GATES["mutate_target_repo_product"]
        actual.update(allowed=False, outcome=outcome, gate=gate)
    elif action in FORBIDDEN_ACTION_GATES:
        outcome, gate = FORBIDDEN_ACTION_GATES[action]
        actual.update(allowed=False, outcome=outcome, gate=gate)
    elif action in BOARD_MANAGER_ONLY or capability_id in BOARD_MANAGER_ONLY:
        actual.update(
            allowed=False,
            outcome="DENIED_ROLE_LACKS_CAPABILITY",
            gate="BOARD_MANAGER_CAPABILITY_NOT_INHERITED",
        )
    elif employment_state != "ACTIVE" or not runtime_exists:
        actual.update(
            allowed=False,
            outcome="DENIED_RUNTIME_NOT_PROVISIONED",
            gate="RUNTIME_NOT_PROVISIONED",
        )
    elif action == "department_decision" and capability_id != (
        "knowledge_department_decision"
    ):
        actual.update(
            allowed=False,
            outcome="BLOCKED_REQUIRED_CAPABILITY_UNAVAILABLE",
            gate="WRONG_OR_MISSING_CAPABILITY",
        )
    elif not role_allows_capability(role, capability_id, pack):
        actual.update(
            allowed=False,
            outcome="DENIED_ROLE_LACKS_CAPABILITY",
            gate="ROLE_CAPABILITY_DENIED",
        )
    elif half_certain:
        actual.update(
            allowed=False,
            outcome="DENIED_HALF_CERTAIN_AS_FACT",
            gate="HALF_CERTAIN_AS_FACT",
        )
    elif action in {"department_decision", "founding_solo_self_work"} and (
        not evidence_sufficient
    ):
        actual.update(
            allowed=False,
            outcome="DENIED_INSUFFICIENT_EVIDENCE",
            gate="EVIDENCE_INSUFFICIENT",
        )
    elif action == "department_decision":
        actual.update(
            allowed=True,
            outcome="DECISION_RECORDED",
            gate="KNOWLEDGE_DECISION_ALLOWED",
        )
    elif action == "improvement_read":
        actual.update(
            allowed=True,
            outcome="READ_OK",
            gate="IMPROVEMENT_READ_ALLOWED",
        )
    elif action == "founding_solo_self_work":
        actual.update(
            allowed=True,
            outcome="FOUNDING_SOLO_SELF_WORK_OK",
            gate="FOUNDING_SOLO_SELF_WORK_ALLOWED",
        )
    else:
        actual.update(
            allowed=False,
            outcome="DENIED_ROLE_LACKS_CAPABILITY",
            gate="ROLE_CAPABILITY_DENIED",
        )

    actual["matches_expect"] = all(actual.get(k) == expect.get(k) for k in expect)
    actual["expect"] = expect
    return actual


def evaluate_all(path: Path | None = None) -> list[dict[str, Any]]:
    pack = load_pressure_cases(path)
    return [evaluate_case(case, pack=pack) for case in pack["cases"]]


def registry_encodes_knowledge_capabilities(
    registry: dict[str, Any] | None = None,
) -> bool:
    caps = (registry or load_registry()).get("capabilities") or {}
    if not REQUIRED_CAPABILITY_IDS.issubset(caps.keys()):
        return False
    if not PREFERRED_CAPABILITY_IDS.issubset(caps.keys()):
        return False
    decision = caps["knowledge_department_decision"]
    report = caps["knowledge_owner_report"]
    return all(
        [
            decision.get("requirement") == "REQUIRED",
            report.get("requirement") == "REQUIRED",
            (decision.get("availability") or {}).get("silent_substitution")
            is False,
            (report.get("availability") or {}).get("silent_substitution")
            is False,
            str(decision.get("contract") or "").endswith(
                "KNOWLEDGE_DEPARTMENT_AUTHORITY.md"
            ),
            str(report.get("contract") or "").endswith(
                "HEAD_OF_KNOWLEDGE_OWNER_REPORT.md"
            ),
        ]
    )


def employee_record_authority_defined_not_activated() -> bool:
    text = EMPLOYEE_MD.read_text(encoding="utf-8")
    return all(
        [
            "employment_state: PLANNED_ONLY" in text,
            "runtime_exists: false" in text,
            "AUTHORITY_DEFINED_NOT_ACTIVATED" in text,
            "knowledge_department_decision" in text,
            "knowledge_owner_report" in text,
            "improvement_management_write" in text,
            "active: false" in text,
        ]
    )


def authority_docs_present() -> bool:
    authority = AUTHORITY_MD.read_text(encoding="utf-8")
    report = OWNER_REPORT_MD.read_text(encoding="utf-8")
    routing = ROUTING_MD.read_text(encoding="utf-8")
    policy = POLICY_MD.read_text(encoding="utf-8")
    return all(
        [
            "DIETER_FOUNDING_SOLO_AUTHORITY_DEFINED" in authority,
            "knowledge_department_decision" in authority,
            "FOUNDING_SOLO" in authority,
            "HEAD_OF_KNOWLEDGE_OWNER_REPORT_DEFINED" in report,
            "knowledge_owner_report" in report,
            "knowledge_department_decision" in routing,
            "Head of Knowledge" in policy,
            "knowledge_department_decision" in policy,
        ]
    )
