"""Fail-closed activation gate for Dieter Datenbank (#71).

Verifies identity, #70 authority, #73 report contract, #72 org wiring, and the
head-of-knowledge execution surface before allowing ACTIVE / runtime_exists.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
TOOLS = REPO_ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import knowledge_department_authority_lib as knowledge_auth  # noqa: E402
import knowledge_owner_report_lib as owner_report  # noqa: E402
import plugin_skill_routing_lib as routing  # noqa: E402

EMPLOYEE_MD = REPO_ROOT / "agents" / "dieter-datenbank.md"
BOARD_MANAGER_MD = REPO_ROOT / "agents" / "improvement-board-manager.md"
SKILL_MD = REPO_ROOT / "docs" / "skills" / "head-of-knowledge" / "SKILL.md"
CONSUMER_YML = (
    REPO_ROOT / "docs" / "skills" / "head-of-knowledge" / "consumer.yml"
)
GATE_MD = REPO_ROOT / "docs" / "DIETER_ACTIVATION_GATE.md"
EMPLOYEE_ID = "workforce.employee.dieter-datenbank.v1"


def _load_employee_machine_record() -> dict[str, Any]:
    text = EMPLOYEE_MD.read_text(encoding="utf-8")
    marker = "## MACHINE RECORD"
    if marker not in text:
        raise ValueError("employee record missing MACHINE RECORD section")
    after = text.split(marker, 1)[1]
    if "```yaml" not in after:
        raise ValueError("employee record missing yaml fence")
    body = after.split("```yaml", 1)[1].split("```", 1)[0]
    data = yaml.safe_load(body)
    if not isinstance(data, dict):
        raise ValueError("employee machine record must be a mapping")
    return data


def surface_exists() -> bool:
    return SKILL_MD.is_file() and CONSUMER_YML.is_file()


def consumer_pack_valid() -> tuple[bool, list[str]]:
    if not CONSUMER_YML.is_file():
        return False, ["missing consumer.yml"]
    problems = routing.validate_production_consumer_packs()
    # Only fail on problems that mention head-of-knowledge path, or any problem
    # if the pack is the only new consumer — keep strict: any production pack
    # problem blocks activation because the host must stay valid.
    return (len(problems) == 0), problems


def board_manager_reports_to_dieter() -> bool:
    text = BOARD_MANAGER_MD.read_text(encoding="utf-8")
    return f"reports_to: {EMPLOYEE_ID}" in text


def evaluate_activation_gate() -> dict[str, Any]:
    problems: list[str] = []
    checks: dict[str, bool] = {}

    record = _load_employee_machine_record()
    employee = record.get("employee") or {}
    checks["identity"] = employee.get("id") == EMPLOYEE_ID
    if not checks["identity"]:
        problems.append("employee identity mismatch")

    checks["authority_registry"] = (
        knowledge_auth.registry_encodes_knowledge_capabilities()
    )
    if not checks["authority_registry"]:
        problems.append("knowledge capabilities missing from registry")

    checks["authority_docs"] = knowledge_auth.authority_docs_present()
    if not checks["authority_docs"]:
        problems.append("authority docs incomplete")

    checks["authority_pressure"] = all(
        r.get("matches_expect") for r in knowledge_auth.evaluate_all()
    )
    if not checks["authority_pressure"]:
        problems.append("knowledge authority pressure cases failing")

    checks["owner_report_contract"] = owner_report.contract_is_complete()
    if not checks["owner_report_contract"]:
        problems.append("owner report contract incomplete")

    checks["board_manager_reports_to"] = board_manager_reports_to_dieter()
    if not checks["board_manager_reports_to"]:
        problems.append("board manager reports_to missing")

    checks["surface_exists"] = surface_exists()
    if not checks["surface_exists"]:
        problems.append("head-of-knowledge skill surface missing")

    ok_consumer, consumer_problems = consumer_pack_valid()
    checks["consumer_valid"] = ok_consumer
    if not ok_consumer:
        problems.extend(consumer_problems[:5] or ["consumer pack invalid"])

    checks["gate_doc"] = GATE_MD.is_file() and (
        "DIETER_FOUNDING_SOLO_PROVISIONED" in GATE_MD.read_text(encoding="utf-8")
    )
    if not checks["gate_doc"]:
        problems.append("activation gate doc missing")

    passed = all(checks.values()) and not problems
    return {
        "passed": passed,
        "outcome": "GATE_PASS" if passed else "GATE_HOLD",
        "checks": checks,
        "problems": problems,
        "may_set_runtime_exists": passed,
    }


def employee_record_is_active_founding_solo() -> bool:
    text = EMPLOYEE_MD.read_text(encoding="utf-8")
    return all(
        [
            "employment_state: ACTIVE" in text,
            "runtime_exists: true" in text,
            "active: true" in text,
            "FOUNDING_SOLO" in text,
            "head-of-knowledge" in text,
            EMPLOYEE_ID in text,
            "AUTHORITY_DEFINED_NOT_ACTIVATED" not in text
            or "ACTIVE_FOUNDING_SOLO" in text,
        ]
    )


def activation_consistent_with_gate() -> bool:
    gate = evaluate_activation_gate()
    record = _load_employee_machine_record()
    employee = record.get("employee") or {}
    runtime = bool(employee.get("runtime_exists"))
    state = str(employee.get("employment_state") or "")
    if runtime or state == "ACTIVE":
        return gate["passed"] and employee_record_is_active_founding_solo()
    return not gate["passed"] or state == "PLANNED_ONLY"
