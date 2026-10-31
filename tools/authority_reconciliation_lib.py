"""Deterministic twin for AUTHORITY_RECONCILIATION_REQUIRED pressure cases.

Layer A only: encodes gate rules from docs/WORKFORCE_POLICY.md. Does not prove
a live planning agent obeyed the policy — that is Layer B / producer evidence.
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
    / "authority-reconciliation"
    / "pressure_cases.yml"
)
POLICY_MD = REPO_ROOT / "docs" / "WORKFORCE_POLICY.md"
OPERATING_MODEL_MD = (
    REPO_ROOT / "backoffice" / "chatgpt-workflows" / "02_OPERATING_MODEL.md"
)
AGENTS_MD = REPO_ROOT / "AGENTS.md"
BOOTSTRAP_MD = REPO_ROOT / "WORKFORCE_BOOTSTRAP.md"

STRUCTURING_PROPOSALS = {
    "goal",
    "epic",
    "meta_epic",
    "coordinator",
    "foundation_owner",
    "program_owner",
    "manager",
    "durable_owner_structure",
}

ORDINARY_TASK_KINDS = {
    "small_bugfix",
    "implementation_child",
    "docs_only",
}


def load_pressure_cases(path: Path | None = None) -> dict[str, Any]:
    target = path or DEFAULT_PRESSURE_CASES
    data = yaml.safe_load(target.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "cases" not in data:
        raise ValueError(f"invalid pressure cases file: {target}")
    return data


def gate_applicable(*, proposing: str, task_kind: str | None) -> bool:
    kind = (task_kind or "").strip().lower()
    if kind in ORDINARY_TASK_KINDS:
        return False
    return proposing.strip().lower() in STRUCTURING_PROPOSALS


def _truthy_proof(proof: Any) -> bool:
    if proof is None:
        return False
    text = str(proof).strip()
    return bool(text) and text.lower() not in {"null", "none", "false", ""}


def evaluate_case(case: dict[str, Any]) -> dict[str, Any]:
    case_id = str(case["id"])
    data = case.get("input") or {}
    expect = case.get("expect") or {}
    actual: dict[str, Any] = {"id": case_id}

    proposing = str(data.get("proposing") or "")
    task_kind = data.get("task_kind")
    if task_kind is None and proposing == "implementation_child":
        task_kind = "implementation_child"

    applicable = gate_applicable(
        proposing=proposing,
        task_kind=str(task_kind) if task_kind is not None else None,
    )
    actual["gate_applicable"] = applicable

    authorities = list(data.get("existing_authorities") or [])
    bodies_fully_read = bool(data.get("bodies_fully_read"))
    if authorities:
        bodies_fully_read = bodies_fully_read and all(
            bool(a.get("body_fully_read")) for a in authorities
        )
    newer_delta = bool(data.get("newer_relevant_delta"))
    alternatives_scored = bool(data.get("alternatives_scored"))
    proof = data.get("missing_authority_proof")
    inventory_entire = bool(data.get("inventory_entire_portfolio"))
    actual["overreach"] = inventory_entire
    actual["requires_freshness_reconciliation"] = bool(applicable and newer_delta)

    if not applicable:
        actual["create_new_allowed"] = False
        actual["preferred_decision"] = "NO_STRUCTURAL_CHANGE"
        actual["decision"] = "NO_STRUCTURAL_CHANGE"
        actual["gate"] = "GATE_NOT_APPLICABLE"
        actual["matches_expect"] = _subset_match(actual, expect)
        return actual

    if authorities and not bodies_fully_read:
        actual["create_new_allowed"] = False
        actual["preferred_decision"] = "HOLD_FULL_BODY_READ_REQUIRED"
        actual["decision"] = "HOLD_FULL_BODY_READ_REQUIRED"
        actual["gate"] = "AUTHORITY_RECONCILIATION_HOLD"
        actual["matches_expect"] = _subset_match(actual, expect)
        return actual

    owns_full = any(bool(a.get("owns_outcome") is True) for a in authorities)
    owns_partial = any(
        str(a.get("owns_outcome", "")).lower() == "partial" for a in authorities
    )
    has_proof = _truthy_proof(proof)

    if owns_full:
        decision = "UPDATE_EXISTING"
        create_new = False
    elif newer_delta:
        decision = "RECONCILE_EXISTING"
        create_new = False
    elif owns_partial and has_proof and alternatives_scored:
        decision = "CREATE_NEW_AUTHORITY"
        create_new = True
    elif owns_partial and not has_proof:
        decision = "LINK_EXISTING" if alternatives_scored else "RECONCILE_EXISTING"
        create_new = False
    elif has_proof and alternatives_scored and bodies_fully_read:
        decision = "CREATE_NEW_AUTHORITY"
        create_new = True
    else:
        decision = "NO_STRUCTURAL_CHANGE"
        create_new = False

    # Default remains do-not-create without missing-authority proof.
    if create_new and not has_proof:
        create_new = False
        decision = "RECONCILE_EXISTING" if newer_delta else "UPDATE_EXISTING"

    actual["create_new_allowed"] = create_new
    actual["preferred_decision"] = decision
    actual["decision"] = decision
    actual["gate"] = "AUTHORITY_RECONCILIATION_PASS"
    actual["matches_expect"] = _subset_match(actual, expect)
    return actual


def _subset_match(actual: dict[str, Any], expect: dict[str, Any]) -> bool:
    for key, expected in expect.items():
        if key not in actual:
            return False
        if actual[key] != expected:
            return False
    return True


def evaluate_all(path: Path | None = None) -> list[dict[str, Any]]:
    pack = load_pressure_cases(path)
    return [evaluate_case(case) for case in pack["cases"]]


def policy_encodes_authority_reconciliation(text: str | None = None) -> bool:
    body = text if text is not None else POLICY_MD.read_text(encoding="utf-8")
    checks = [
        "AUTHORITY_RECONCILIATION_REQUIRED" in body,
        "## Authority reconciliation" in body,
        "Existing owner discovery" in body,
        "Scope overlap check" in body,
        "Freshness / delta reconciliation" in body,
        "Missing-authority proof" in body,
        "DO NOT CREATE NEW AUTHORITY" in body,
        "UPDATE_EXISTING" in body,
        "RECONCILE_EXISTING" in body,
        "LINK_EXISTING" in body,
        "NO_STRUCTURAL_CHANGE" in body,
        "CREATE_NEW_AUTHORITY" in body,
        "title or search snippets alone are insufficient" in body.lower()
        or "Title or search snippets alone are insufficient" in body,
        "Ordinary implementation children" in body
        or "ordinary implementation children" in body.lower(),
    ]
    return all(checks)


def operating_model_places_reconciliation_gate(text: str | None = None) -> bool:
    body = (
        text
        if text is not None
        else OPERATING_MODEL_MD.read_text(encoding="utf-8")
    )
    route = body.upper().find("ROUTE")
    reconcile = body.upper().find("AUTHORITY RECONCILIATION")
    decide = body.upper().find("DECIDE")
    if min(route, reconcile, decide) < 0:
        return False
    if not (route < reconcile < decide):
        return False
    return "WORKFORCE_POLICY.md" in body


def frontdoors_reference_policy_gate() -> bool:
    agents = AGENTS_MD.read_text(encoding="utf-8")
    bootstrap = BOOTSTRAP_MD.read_text(encoding="utf-8")
    return (
        "AUTHORITY_RECONCILIATION_REQUIRED" in agents
        and "authority-reconciliation" in agents
        and "AUTHORITY_RECONCILIATION_REQUIRED" in bootstrap
        and "WORKFORCE_POLICY.md" in bootstrap
    )
