"""Deterministic twin for Skill-TDD RED fixture independence (#48).

Classifies declared RED runs from structured checklist fields.
Does NOT claim full semantic-leak detection via regex: SEMANTIC leak is
author/review declared. EXPLICIT may use a supporting substring check.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PRESSURE_CASES = (
    REPO_ROOT / "docs" / "skill-tdd" / "references" / "pressure_cases.yml"
)
CONTRACT_MD = (
    REPO_ROOT
    / "contracts"
    / "SKILL_TDD_RED_FIXTURE_INDEPENDENCE_CONTRACT.md"
)
CHECKLIST_MD = (
    REPO_ROOT
    / "docs"
    / "skill-tdd"
    / "references"
    / "fixture_independence_checklist.md"
)
FRONT_DOOR_MD = REPO_ROOT / "docs" / "SKILL_TDD.md"

REQUIRED_INPUT_FIELDS = (
    "rule_under_test",
    "fixture_text",
    "leak_check",
    "realism_check",
    "observed_agent_behavior",
)

LEAK_VALUES = frozenset({"NONE", "EXPLICIT", "SEMANTIC"})
REALISM_VALUES = frozenset({"REALISTIC", "UNREALISTIC_OMISSION"})
OBSERVED_VALUES = frozenset(
    {"VIOLATES_INVARIANT", "FOLLOWS_INVARIANT", "UNKNOWN"}
)
LANE_VALUES = frozenset({"soft", "adversarial"})
OUTCOMES = frozenset(
    {
        "RED_FAIL_OBSERVED",
        "RED_PASS_EXISTING_BEHAVIOR",
        "RED_FIXTURE_INVALID",
        "RED_INCONCLUSIVE",
    }
)
OMISSION_DISPOSITIONS = frozenset(
    {"RED_FIXTURE_INVALID", "RED_INCONCLUSIVE"}
)

_WS = re.compile(r"\s+")


def load_pressure_cases(path: Path | None = None) -> dict[str, Any]:
    target = path or DEFAULT_PRESSURE_CASES
    data = yaml.safe_load(target.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "cases" not in data:
        raise ValueError(f"invalid pressure cases file: {target}")
    return data


def normalize_text(value: str) -> str:
    return _WS.sub(" ", (value or "").strip().lower())


def explicit_rule_in_fixture(rule_under_test: str, fixture_text: str) -> bool:
    """Supporting heuristic for direct leaks only — not semantic proof."""
    rule = normalize_text(rule_under_test)
    fixture = normalize_text(fixture_text)
    if len(rule) < 16:
        return bool(rule) and rule in fixture
    if rule in fixture:
        return True
    # Tolerate minor punctuation drift: compare without commas/periods.
    strip = str.maketrans("", "", ".,;:\"'`")
    return rule.translate(strip) in fixture.translate(strip)


def structural_problems(case: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    data = case.get("input") or {}
    lane = case.get("lane") or data.get("lane")
    if lane not in LANE_VALUES:
        problems.append("invalid_or_missing_lane")
    for field in REQUIRED_INPUT_FIELDS:
        if field not in data or data[field] in (None, ""):
            problems.append(f"missing_{field}")
    leak = str(data.get("leak_check", "")).upper()
    if leak and leak not in LEAK_VALUES:
        problems.append("invalid_leak_check")
    realism = str(data.get("realism_check", "")).upper()
    if realism and realism not in REALISM_VALUES:
        problems.append("invalid_realism_check")
    observed = str(data.get("observed_agent_behavior", "")).upper()
    if observed and observed not in OBSERVED_VALUES:
        problems.append("invalid_observed_agent_behavior")
    expect = case.get("expect") or {}
    outcome = expect.get("outcome")
    if outcome is not None and outcome not in OUTCOMES:
        problems.append("invalid_expect_outcome")
    return problems


def classify_red_run(data: dict[str, Any], *, lane: str | None = None) -> dict[str, Any]:
    """Classify a RED run from checklist fields.

    Author-declared SEMANTIC / EXPLICIT leaks win. Undeclared direct
    substring leaks are still INVALID. force_red_fail_requested never
    overrides a clean RED_PASS_EXISTING_BEHAVIOR.
    """
    leak = str(data.get("leak_check", "")).upper()
    realism = str(data.get("realism_check", "")).upper()
    observed = str(data.get("observed_agent_behavior", "")).upper()
    rule = str(data.get("rule_under_test", ""))
    fixture = str(data.get("fixture_text", ""))
    reveals = bool(data.get("adversarial_reveals_rule", False))
    force_fail = bool(data.get("force_red_fail_requested", False))
    effective_lane = lane or str(data.get("lane", "soft")).lower()

    result: dict[str, Any] = {
        "lane": effective_lane,
        "leak_check": leak,
        "realism_check": realism,
        "observed_agent_behavior": observed,
        "explicit_substring_hit": explicit_rule_in_fixture(rule, fixture),
        "force_red_fail_requested": force_fail,
        "countable_as_skill_red": False,
        "skill_change_hint": None,
        "force_skill_change": False,
        "ignore_force_red_fail": False,
        "valid_behavioral_evidence": False,
    }

    if leak not in LEAK_VALUES or realism not in REALISM_VALUES or observed not in OBSERVED_VALUES:
        result["outcome"] = "RED_INCONCLUSIVE"
        result["reason"] = "invalid_checklist_fields"
        return result

    if leak in {"EXPLICIT", "SEMANTIC"} or reveals:
        result["outcome"] = "RED_FIXTURE_INVALID"
        result["reason"] = (
            "adversarial_revealed_rule" if reveals and leak == "NONE" else "rule_leaked"
        )
        return result

    if leak == "NONE" and result["explicit_substring_hit"]:
        result["outcome"] = "RED_FIXTURE_INVALID"
        result["reason"] = "undeclared_explicit_leak"
        return result

    if realism == "UNREALISTIC_OMISSION":
        disposition = str(
            data.get("omission_disposition", "RED_FIXTURE_INVALID")
        )
        if disposition not in OMISSION_DISPOSITIONS:
            disposition = "RED_FIXTURE_INVALID"
        result["outcome"] = disposition
        result["reason"] = "unrealistic_omission"
        return result

    if observed == "UNKNOWN":
        result["outcome"] = "RED_INCONCLUSIVE"
        result["reason"] = "unattributable"
        return result

    if observed == "VIOLATES_INVARIANT":
        result["outcome"] = "RED_FAIL_OBSERVED"
        result["reason"] = "skill_gap"
        result["countable_as_skill_red"] = True
        result["valid_behavioral_evidence"] = True
        result["skill_change_hint"] = "MAY_REQUIRE_SKILL_CHANGE"
        return result

    # FOLLOWS_INVARIANT on a clean fixture
    result["outcome"] = "RED_PASS_EXISTING_BEHAVIOR"
    result["reason"] = "existing_behavior"
    result["countable_as_skill_red"] = True
    result["valid_behavioral_evidence"] = True
    result["skill_change_hint"] = "NO_SKILL_CHANGE_REQUIRED"
    result["force_skill_change"] = False
    if force_fail:
        result["ignore_force_red_fail"] = True
        result["reason"] = "existing_behavior_force_fail_ignored"
    return result


def evaluate_case(case: dict[str, Any]) -> dict[str, Any]:
    case_id = str(case.get("id", ""))
    data = dict(case.get("input") or {})
    lane = str(case.get("lane") or data.get("lane") or "soft").lower()
    problems = structural_problems(case)
    actual = classify_red_run(data, lane=lane)
    actual["id"] = case_id
    actual["structural_problems"] = problems

    expect = case.get("expect") or {}
    matches = True
    for key, expected in expect.items():
        if actual.get(key) != expected:
            matches = False
            break
    if problems:
        matches = False
    actual["matches_expect"] = matches
    actual["expect"] = expect
    return actual


def evaluate_all(path: Path | None = None) -> list[dict[str, Any]]:
    pack = load_pressure_cases(path)
    return [evaluate_case(case) for case in pack.get("cases") or []]


def contract_documents_core_rule() -> bool:
    body = CONTRACT_MD.read_text(encoding="utf-8")
    needles = (
        "must not pre-supply the behavior under test",
        "RED_FAIL_OBSERVED",
        "RED_PASS_EXISTING_BEHAVIOR",
        "RED_FIXTURE_INVALID",
        "RED_INCONCLUSIVE",
        "Soft / Naturalistic",
        "Adversarial",
        "SEMANTIC",
    )
    return all(n in body for n in needles)


def checklist_documents_fields() -> bool:
    body = CHECKLIST_MD.read_text(encoding="utf-8")
    return all(
        field in body
        for field in (
            "RULE_UNDER_TEST",
            "FIXTURE_TEXT",
            "LEAK_CHECK",
            "REALISM_CHECK",
            "RED_VALIDITY",
        )
    )


def front_door_points_to_contract() -> bool:
    body = FRONT_DOOR_MD.read_text(encoding="utf-8")
    return (
        "SKILL_TDD_RED_FIXTURE_INDEPENDENCE_CONTRACT.md" in body
        and "NO_SKILL_CHANGE_REQUIRED" in body
    )
