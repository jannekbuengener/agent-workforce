"""Verification twin for Dieter FOUNDING_SOLO pilot (#74)."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
TOOLS = REPO_ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import dieter_activation_lib as activation  # noqa: E402
import knowledge_department_authority_lib as knowledge_auth  # noqa: E402
import knowledge_owner_report_lib as owner_report  # noqa: E402

PILOT_DIR = (
    REPO_ROOT
    / "docs"
    / "knowledge"
    / "pilots"
    / "2026-10-31-founding-solo"
)
DECISION_PATH = PILOT_DIR / "DECISION_RECEIPT.yml"
OWNER_REPORT_PATH = PILOT_DIR / "OWNER_REPORT.yml"
EMPLOYEE_MD = REPO_ROOT / "agents" / "dieter-datenbank.md"


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"expected mapping: {path}")
    return data


def evaluate_pilot() -> dict[str, Any]:
    problems: list[str] = []
    checks: dict[str, bool] = {}

    checks["activation_gate"] = activation.evaluate_activation_gate()["passed"]
    checks["employee_active"] = activation.employee_record_is_active_founding_solo()
    if not checks["activation_gate"]:
        problems.append("activation gate not passing on live tree")
    if not checks["employee_active"]:
        problems.append("employee record not ACTIVE FOUNDING_SOLO")

    checks["decision_present"] = DECISION_PATH.is_file()
    checks["owner_report_present"] = OWNER_REPORT_PATH.is_file()
    if not checks["decision_present"]:
        problems.append("missing decision receipt")
    if not checks["owner_report_present"]:
        problems.append("missing owner report")

    decision = load_yaml(DECISION_PATH) if checks["decision_present"] else {}
    report = load_yaml(OWNER_REPORT_PATH) if checks["owner_report_present"] else {}

    checks["decision_actor"] = (
        decision.get("actor_employee_id")
        == "workforce.employee.dieter-datenbank.v1"
    )
    checks["decision_runtime"] = (
        decision.get("employment_state_at_run") == "ACTIVE"
        and decision.get("runtime_exists_at_run") is True
    )
    checks["decision_capability"] = (
        decision.get("capability_id") == "knowledge_department_decision"
    )
    checks["uncertainty_named"] = bool(
        str(decision.get("uncertainty_statement") or "").strip()
    )
    checks["target_repo_preserved"] = (
        decision.get("target_repo_authority_preserved") is True
    )
    forbidden = set(decision.get("forbidden_actions_confirmed_not_taken") or [])
    required_forbidden = {
        "improvement_management_write",
        "raw_database_admin",
        "target_repository_product_mutation",
        "self_grant_authority",
    }
    checks["forbidden_acked"] = required_forbidden.issubset(forbidden)
    checks["live_evidence"] = any(
        "agent-brain#" in str(item.get("ref") if isinstance(item, dict) else item)
        or "agent-workforce#" in str(item.get("ref") if isinstance(item, dict) else item)
        or "https://github.com/" in str(item.get("ref") if isinstance(item, dict) else item)
        for item in (decision.get("evidence_refs") or [])
    )

    for key, ok in list(checks.items()):
        if key.startswith("decision_") or key in {
            "uncertainty_named",
            "target_repo_preserved",
            "forbidden_acked",
            "live_evidence",
        }:
            if not ok:
                problems.append(f"decision check failed: {key}")

    # Authority twin: ACTIVE decision with evidence should be allowed.
    case = {
        "id": "pilot_decision",
        "input": {
            "role": "head_of_knowledge",
            "action": "department_decision",
            "capability_id": "knowledge_department_decision",
            "employment_state": "ACTIVE",
            "runtime_exists": True,
            "evidence_sufficient": True,
            "uncertainty_stated": True,
            "half_certain_as_fact": False,
            "target_repo_mutation": False,
        },
        "expect": {
            "allowed": True,
            "outcome": "DECISION_RECORDED",
            "gate": "KNOWLEDGE_DECISION_ALLOWED",
        },
    }
    auth_result = knowledge_auth.evaluate_case(case)
    checks["authority_allows_decision"] = bool(auth_result.get("matches_expect"))
    if not checks["authority_allows_decision"]:
        problems.append(f"authority twin rejected pilot decision: {auth_result}")

    report_result = owner_report.validate_report(
        report,
        employment_state="ACTIVE",
        runtime_exists=True,
        capability_authorized=True,
    )
    checks["owner_report_valid"] = bool(report_result.get("allowed"))
    if not checks["owner_report_valid"]:
        problems.append(f"owner report invalid: {report_result}")

    employee_text = EMPLOYEE_MD.read_text(encoding="utf-8")
    checks["record_matches_live"] = all(
        [
            "employment_state: ACTIVE" in employee_text,
            "runtime_exists: true" in employee_text,
            "current_operating_phase: FOUNDING_SOLO" in employee_text,
            "docs/skills/head-of-knowledge" in employee_text,
        ]
    )
    if not checks["record_matches_live"]:
        problems.append("employee record does not match expected live ACTIVE state")

    passed = all(checks.values()) and not problems
    return {
        "passed": passed,
        "outcome": (
            "DIETER_FOUNDING_SOLO_PILOT_PROVEN" if passed else "PILOT_HOLD"
        ),
        "checks": checks,
        "problems": problems,
        "decision_path": str(DECISION_PATH.relative_to(REPO_ROOT).as_posix()),
        "owner_report_path": str(
            OWNER_REPORT_PATH.relative_to(REPO_ROOT).as_posix()
        ),
    }
