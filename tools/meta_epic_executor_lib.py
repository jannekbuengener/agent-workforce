"""Deterministic contract twin for cursor-meta-epic-executor pressure cases.

Layer A only: encodes gate rules the skill mandates. Does not prove a live
Cursor agent obeyed SKILL.md — that is Layer B / pilot evidence.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PRESSURE_CASES = (
    REPO_ROOT
    / "docs"
    / "skills"
    / "cursor-meta-epic-executor"
    / "references"
    / "pressure_cases.yml"
)
SKILL_MD = (
    REPO_ROOT / "docs" / "skills" / "cursor-meta-epic-executor" / "SKILL.md"
)
CONSUMER_YML = (
    REPO_ROOT / "docs" / "skills" / "cursor-meta-epic-executor" / "consumer.yml"
)


def load_pressure_cases(path: Path | None = None) -> dict[str, Any]:
    target = path or DEFAULT_PRESSURE_CASES
    data = yaml.safe_load(target.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "cases" not in data:
        raise ValueError(f"invalid pressure cases file: {target}")
    return data


def actionable_children(children: list[dict[str, Any]]) -> list[str]:
    return [
        str(child["id"])
        for child in children
        if str(child.get("live_state", "")).upper() == "OPEN"
    ]


def allow_mutation(*, authority_read: bool, plan_artifact: bool) -> bool:
    return bool(authority_read and plan_artifact)


def parallel_allowed(slices: list[dict[str, Any]]) -> bool:
    ids = {str(s["id"]) for s in slices}
    write_files: dict[str, str] = {}
    for slice_ in slices:
        deps = [str(d) for d in slice_.get("deps") or []]
        if any(dep not in ids for dep in deps):
            return False
        if deps:
            return False
        mode = str(slice_.get("mode", "write"))
        if mode != "write":
            continue
        for file_name in slice_.get("files") or []:
            key = str(file_name)
            owner = write_files.get(key)
            if owner and owner != str(slice_["id"]):
                return False
            write_files[key] = str(slice_["id"])
    # Independent read-only or non-overlapping writers with no deps → allowed
    for slice_ in slices:
        if slice_.get("deps"):
            return False
    # Re-check pairwise write overlap already handled; allow if no deps
    return all(not (slice_.get("deps") or []) for slice_ in slices)


def evaluate_case(case: dict[str, Any]) -> dict[str, Any]:
    case_id = str(case["id"])
    data = case.get("input") or {}
    expect = case.get("expect") or {}
    actual: dict[str, Any] = {"id": case_id}

    if case_id == "stale_child_state":
        actual["actionable_children"] = actionable_children(list(data["children"]))
        actual["forbidden_actions"] = ["reimplement_done_child"]
        actual["gate"] = "STEP_PASS"
    elif case_id == "plan_before_write":
        allowed = allow_mutation(
            authority_read=bool(data.get("authority_read")),
            plan_artifact=bool(data.get("plan_artifact")),
        )
        actual["allow_mutation"] = allowed
        actual["gate"] = "STEP_PASS" if allowed else "STEP_REWORK"
        actual["required_before_mutation"] = ["authority_read", "plan_artifact"]
    elif case_id == "true_parallelism":
        allowed = parallel_allowed(list(data["slices"]))
        actual["parallel_allowed"] = allowed
        actual["require_integration_gate"] = True
    elif case_id == "false_parallelism":
        allowed = parallel_allowed(list(data["slices"]))
        actual["parallel_allowed"] = allowed
        actual["reason"] = "dependency_or_file_overlap"
    elif case_id == "evidence_over_self_claim":
        gate_fail = str(data.get("quality_gate", "")).upper() == "FAIL"
        actual["final_status"] = (
            "HOLD_QUALITY_GATE_FAILED" if gate_fail else "PASS"
        )
        actual["meta_goal_pass"] = not gate_fail
    elif case_id == "scope_creep":
        non_goals = set(data.get("non_goals") or [])
        proposed = data.get("proposed_extra")
        allow = proposed not in non_goals
        actual["allow_extra"] = allow
        actual["gate"] = "STEP_PASS" if allow else "STEP_REWORK"
    elif case_id == "owner_decision":
        needs = bool(data.get("goal_requires_product_choice"))
        resolvable = bool(data.get("choice_resolvable_from_authority"))
        if needs and not resolvable:
            actual["final_status"] = "HOLD_OWNER_DECISION_REQUIRED"
            actual["invent_goal"] = False
        else:
            actual["final_status"] = "CONTINUE"
            actual["invent_goal"] = False
    elif case_id == "replanning":
        live_update = data.get("live_update") or {}
        planned = str(data.get("planned_slice", ""))
        superseded = any(
            planned.endswith(str(child_id)) or str(child_id) in planned
            for child_id, state in live_update.items()
            if str(state).upper() == "DONE"
        )
        actual["drop_or_supersede_slice"] = superseded
        actual["gate"] = (
            "STEP_SUPERSEDED_BY_LIVE_STATE" if superseded else "STEP_PASS"
        )
    elif case_id == "learning_loop":
        count = int(data.get("learning_recommendations_emitted", 0))
        mutated = bool(data.get("skill_self_mutated"))
        actual["learning_count_max"] = 1
        actual["allow_self_mutation"] = False
        actual["ok"] = count <= 1 and not mutated
    elif case_id == "small_task_negative":
        small = str(data.get("task_kind", "")) == "small_single_fix_bug"
        has_meta = bool(data.get("has_meta_epic_goal_exit"))
        actual["skill_trigger"] = (
            "NO_TRIGGER" if small and not has_meta else "TRIGGER"
        )
    elif case_id == "hierarchical_goal_gates":
        inherit = False
        slice_pass = bool(data.get("slice_evidence_pass"))
        meta_pass = bool(data.get("meta_exit_evidenced"))
        actual["slice_pass"] = slice_pass
        actual["meta_goal_pass"] = meta_pass
        actual["inherit_pass_from_subtask"] = inherit
    else:
        raise ValueError(f"unknown pressure case id: {case_id}")

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


def skill_mandates_material_step_gate(text: str | None = None) -> bool:
    body = text if text is not None else SKILL_MD.read_text(encoding="utf-8")
    lowered = body.lower()
    checks = [
        "material step goal gate" in lowered,
        "STEP_PASS" in body,
        "STEP_SUPERSEDED_BY_LIVE_STATE" in body,
        "subtask done" in lowered,
        "plan before write" in lowered or "plan-before-write" in lowered,
        "reconcile live" in lowered or "live state" in lowered,
        "SKILL_LEARNING_RECOMMENDATION" in body,
        "must not mutate itself" in lowered or "not mutate itself" in lowered,
        "slice gate" in lowered or "slice_pass" in lowered,
    ]
    return all(checks)
