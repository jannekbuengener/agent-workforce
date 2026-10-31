"""Deterministic twin for Improvement Board Manager capability separation (#50).

Layer A only: encodes role/tier gates from agents/improvement-board-manager.md
and docs/WORKFORCE_POLICY.md. Does not invent a mutable workforce runtime DB.
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
    / "improvement-board-authority"
    / "pressure_cases.yml"
)
ROLE_MD = REPO_ROOT / "agents" / "improvement-board-manager.md"
POLICY_MD = REPO_ROOT / "docs" / "WORKFORCE_POLICY.md"
TOPOLOGY_MD = REPO_ROOT / "docs" / "META_TOPOLOGY.md"
REGISTRY_PATH = REPO_ROOT / "capabilities" / "REGISTRY.yml"
ROUTING_MD = REPO_ROOT / "docs" / "CAPABILITY_ROUTING.md"
QUALITY_SCOUT = REPO_ROOT / "agents" / "quality-scout.md"
PROCESS_SCOUT = REPO_ROOT / "agents" / "process-scout.md"

WRITE_TIERS = {
    "OBSERVATION_WRITE",
    "MANAGEMENT_WRITE",
    "GITHUB_ISSUE_CREATE",
}
SCOUT_LIKE_ROLES = {"quality_scout", "process_scout", "supervisor"}
TIER_TO_CAPABILITY = {
    "READ": "improvement_read",
    "OBSERVATION_WRITE": "improvement_observation_write",
    "MANAGEMENT_WRITE": "improvement_management_write",
    "GITHUB_ISSUE_CREATE": "improvement_github_issue_create",
}
REQUIRED_CAPABILITY_IDS = set(TIER_TO_CAPABILITY.values())


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


def role_allows_tier(role: str, tier: str, pack: dict[str, Any] | None = None) -> bool:
    roles = (pack or load_pressure_cases()).get("roles") or {}
    entry = roles.get(role) or {}
    allowed = set(entry.get("allowed_tiers") or [])
    if tier == "GITHUB_ISSUE_CREATE":
        return entry.get("github_issue_create") == "via_separate_contract_only"
    return tier in allowed


def evaluate_case(
    case: dict[str, Any], *, pack: dict[str, Any] | None = None
) -> dict[str, Any]:
    case_id = str(case["id"])
    data = case.get("input") or {}
    expect = case.get("expect") or {}
    pack = pack or load_pressure_cases()
    actual: dict[str, Any] = {"id": case_id}

    role = str(data.get("role") or "")
    tier = str(data.get("requested_tier") or "")
    capability_id = str(data.get("capability_id") or "")
    owning_clear = bool(data.get("owning_repo_clear"))
    identity_clear = bool(data.get("improvement_identity_clear"))
    claims_global = bool(data.get("claims_global_routing"))
    general_memory = bool(data.get("general_memory_write"))
    github_ready = bool(data.get("github_issue_contract_ready"))
    expected_cap = TIER_TO_CAPABILITY.get(tier)

    if claims_global:
        actual.update(
            allowed=False,
            outcome="DENIED_SPECIALIST_OVERREACH",
            gate="SPECIALIST_OVERREACH",
        )
    elif general_memory:
        actual.update(
            allowed=False,
            outcome="DENIED_GENERAL_MEMORY_WRITE",
            gate="MEMORY_WRITE_OUT_OF_SCOPE",
        )
    elif expected_cap and capability_id != expected_cap:
        actual.update(
            allowed=False,
            outcome="DENIED_WRONG_CAPABILITY",
            gate=(
                "SHARED_CONTEXT_INSUFFICIENT"
                if capability_id == "shared_context_evidence"
                else "WRONG_CAPABILITY"
            ),
        )
    elif role in SCOUT_LIKE_ROLES and tier in WRITE_TIERS:
        actual.update(
            allowed=False,
            outcome="DENIED_ROLE_LACKS_CAPABILITY",
            gate="SCOUT_WRITE_DENIED",
        )
    elif not role_allows_tier(role, tier, pack) and tier in WRITE_TIERS:
        actual.update(
            allowed=False,
            outcome="DENIED_ROLE_LACKS_CAPABILITY",
            gate="ROLE_WRITE_DENIED",
        )
    elif tier == "GITHUB_ISSUE_CREATE":
        if role != "improvement_board_manager":
            actual.update(
                allowed=False,
                outcome="DENIED_ROLE_LACKS_CAPABILITY",
                gate="SCOUT_WRITE_DENIED",
            )
        elif not github_ready:
            actual.update(
                allowed=False,
                outcome="HOLD",
                gate="GITHUB_ISSUE_CREATE_DEFERRED",
            )
        elif not owning_clear:
            actual.update(
                allowed=False,
                outcome="HOLD",
                gate="HOLD_OWNER_AMBIGUOUS",
            )
        else:
            actual.update(
                allowed=True,
                outcome="GITHUB_ISSUE_CREATED",
                gate="BOARD_MANAGER_GITHUB_ALLOWED",
            )
    elif tier == "MANAGEMENT_WRITE" and not identity_clear:
        actual.update(
            allowed=False,
            outcome="HOLD",
            gate="HOLD_IDENTITY_AMBIGUOUS",
        )
    elif (
        tier == "MANAGEMENT_WRITE"
        and str(data.get("lifecycle_transition") or "") == "VALIDATED_TO_PLANNED"
        and not owning_clear
    ):
        actual.update(
            allowed=False,
            outcome="HOLD",
            gate="HOLD_OWNER_AMBIGUOUS",
        )
    elif not owning_clear and tier in {"MANAGEMENT_WRITE", "GITHUB_ISSUE_CREATE"}:
        actual.update(
            allowed=False,
            outcome="HOLD",
            gate="HOLD_OWNER_AMBIGUOUS",
        )
    elif role == "improvement_board_manager" and tier == "MANAGEMENT_WRITE":
        actual.update(
            allowed=True,
            outcome="MANAGEMENT_APPLIED",
            gate="BOARD_MANAGER_MANAGEMENT_ALLOWED",
        )
    elif role == "improvement_board_manager" and tier == "OBSERVATION_WRITE":
        actual.update(
            allowed=True,
            outcome="OBSERVATION_RECORDED",
            gate="BOARD_MANAGER_OBSERVATION_ALLOWED",
        )
    elif role == "improvement_board_manager" and tier == "READ":
        actual.update(
            allowed=True,
            outcome="READ_OK",
            gate="BOARD_MANAGER_READ_ALLOWED",
        )
    else:
        actual.update(
            allowed=False,
            outcome="DENIED_ROLE_LACKS_CAPABILITY",
            gate="ROLE_WRITE_DENIED",
        )

    actual["matches_expect"] = all(actual.get(k) == expect.get(k) for k in expect)
    actual["expect"] = expect
    return actual


def evaluate_all(path: Path | None = None) -> list[dict[str, Any]]:
    pack = load_pressure_cases(path)
    return [evaluate_case(case, pack=pack) for case in pack["cases"]]


def registry_encodes_improvement_capabilities(
    registry: dict[str, Any] | None = None,
) -> bool:
    caps = (registry or load_registry()).get("capabilities") or {}
    if not REQUIRED_CAPABILITY_IDS.issubset(caps.keys()):
        return False
    obs = caps["improvement_observation_write"]
    mgmt = caps["improvement_management_write"]
    github = caps["improvement_github_issue_create"]
    return all(
        [
            obs.get("requirement") == "REQUIRED",
            mgmt.get("requirement") == "REQUIRED",
            github.get("requirement") == "REQUIRED",
            (obs.get("availability") or {}).get("silent_substitution") is False,
            (mgmt.get("availability") or {}).get("silent_substitution") is False,
            (github.get("availability") or {}).get("silent_substitution") is False,
            str((obs.get("tool") or {}).get("identity") or "")
            == "jannekbuengener/agent-brain",
            str((mgmt.get("tool") or {}).get("identity") or "")
            == "jannekbuengener/agent-brain",
            str(github.get("contract") or "").endswith(
                "IMPROVEMENT_GITHUB_ISSUE_CREATE.md"
            ),
        ]
    )


def policy_encodes_board_manager() -> bool:
    policy = POLICY_MD.read_text(encoding="utf-8")
    role = ROLE_MD.read_text(encoding="utf-8")
    topology = TOPOLOGY_MD.read_text(encoding="utf-8")
    routing = ROUTING_MD.read_text(encoding="utf-8")
    return all(
        [
            "Improvement Board Manager" in policy,
            "improvement_management_write" in policy,
            "improvement_github_issue_create" in policy,
            "claims_global_routing: false" in role,
            "HOLD" in role,
            "Memory" in role or "memory" in role.lower(),
            "Improvement Board Manager" in topology,
            "improvement_management_write" in routing
            or "Improvement Blackboard" in routing,
        ]
    )


def scouts_remain_advisory_unchanged() -> bool:
    quality = QUALITY_SCOUT.read_text(encoding="utf-8")
    process = PROCESS_SCOUT.read_text(encoding="utf-8")
    return all(
        [
            "authority_level: advisory-v1" in quality,
            "authority_level: advisory-v1" in process,
            "recommend, but never create" in quality,
            "recommend, but never create" in process,
            "improvement_management_write" not in quality,
            "improvement_management_write" not in process,
            "improvement_observation_write" not in quality,
            "improvement_observation_write" not in process,
        ]
    )
