"""Deterministic twin for Improvement GitHub Issue Create routing (#51).

Layer A only: encodes fail-closed preconditions, ownership, idempotency, and
lineage gates from docs/IMPROVEMENT_GITHUB_ISSUE_CREATE.md.

Does not invent a mutable workforce runtime DB. Known work items are supplied
as GitHub/blackboard live-state projections in fixtures or caller input.
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
    / "improvement-github-issue-create"
    / "pressure_cases.yml"
)
CONTRACT_MD = REPO_ROOT / "docs" / "IMPROVEMENT_GITHUB_ISSUE_CREATE.md"
POLICY_MD = REPO_ROOT / "docs" / "WORKFORCE_POLICY.md"
ROLE_MD = REPO_ROOT / "agents" / "improvement-board-manager.md"
QUALITY_SCOUT = REPO_ROOT / "agents" / "quality-scout.md"
PROCESS_SCOUT = REPO_ROOT / "agents" / "process-scout.md"
REGISTRY_PATH = REPO_ROOT / "capabilities" / "REGISTRY.yml"

AUTHORIZED_ROLE = "improvement_board_manager"
SCOUT_LIKE_ROLES = frozenset({"quality_scout", "process_scout", "supervisor"})
CAPABILITY_ID = "improvement_github_issue_create"

LIFECYCLE_ALLOWED_FOR_CREATE = frozenset({"VALIDATED", "PLANNED", "IMPLEMENTED"})
LIFECYCLE_DENIED_UNVALIDATED = frozenset({"NEW", "RECURRING", "CLOSED"})

REQUIRED_LINEAGE_FIELDS = (
    "improvement_id",
    "root_cause_or_problem",
    "evidence_summary",
    "recommended_change",
    "expected_benefit",
    "scope_owner",
    "acceptance_or_verification",
    "improvement_record_ref",
    "closed_not_verified_notice",
)

LINEAGE_FIELD_LABELS = {
    "improvement_id": "Improvement ID",
    "root_cause_or_problem": "Root Cause / Problem",
    "evidence_summary": "Evidence Summary",
    "recommended_change": "Recommended Change",
    "expected_benefit": "Expected Benefit",
    "scope_owner": "Scope / Owner",
    "acceptance_or_verification": "Acceptance / Verification",
    "improvement_record_ref": "Improvement Record Ref",
    "closed_not_verified_notice": "Closed ≠ Verified notice",
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


def required_lineage_missing(body_fields: dict[str, Any] | None) -> list[str]:
    fields = body_fields or {}
    missing: list[str] = []
    for key in REQUIRED_LINEAGE_FIELDS:
        value = fields.get(key)
        if value is None or (isinstance(value, str) and not value.strip()):
            missing.append(key)
    return missing


def build_issue_body(body_fields: dict[str, Any]) -> str:
    """Render a deterministic issue body from lineage fields."""
    missing = required_lineage_missing(body_fields)
    if missing:
        raise ValueError(f"missing lineage fields: {missing}")
    lines = ["## Improvement Implementation Hand-off", ""]
    for key in REQUIRED_LINEAGE_FIELDS:
        label = LINEAGE_FIELD_LABELS[key]
        lines.append(f"### {label}")
        lines.append(str(body_fields[key]).strip())
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def closed_issue_implies_verified(closed: bool, verified_evidence: bool) -> bool:
    """closed != verified: a closed issue alone never yields VERIFIED."""
    if not closed:
        return False
    return bool(verified_evidence)


def _active_work_items(
    known: list[dict[str, Any]], *, improvement_id: str, owning_repo: str
) -> list[dict[str, Any]]:
    active: list[dict[str, Any]] = []
    for item in known:
        if str(item.get("improvement_id") or "") != improvement_id:
            continue
        if owning_repo and str(item.get("owning_repo") or "") not in {"", owning_repo}:
            continue
        state = str(item.get("state") or "").lower()
        if state in {"open", "active"}:
            active.append(item)
    return active


def _matching_operation(
    known: list[dict[str, Any]], *, create_operation_id: str
) -> dict[str, Any] | None:
    if not create_operation_id:
        return None
    for item in known:
        if str(item.get("create_operation_id") or "") == create_operation_id:
            return item
    return None


def evaluate_create_request(data: dict[str, Any]) -> dict[str, Any]:
    """Evaluate one create request. Fail closed on missing gates."""
    role = str(data.get("role") or "")
    capability_id = str(data.get("capability_id") or CAPABILITY_ID)
    lifecycle = str(data.get("lifecycle_state") or "")
    improvement_id = str(data.get("improvement_id") or "")
    owning_repo = str(data.get("owning_repo") or "")
    owning_clear = bool(data.get("owning_repo_clear"))
    identity_clear = bool(data.get("improvement_identity_clear"))
    work_concrete = bool(data.get("work_concrete", True))
    target_allows = bool(data.get("target_authority_allows_issue_create"))
    title_ok = bool(data.get("title_follows_german_policy", True))
    claims_global = bool(data.get("claims_global_routing"))
    create_operation_id = str(data.get("create_operation_id") or "")
    known = list(data.get("known_work_items") or [])
    body_fields = data.get("body_fields") or {}
    if improvement_id and "improvement_id" not in body_fields:
        body_fields = {**body_fields, "improvement_id": improvement_id}

    result: dict[str, Any] = {
        "allowed": False,
        "created": False,
        "reused": False,
        "issue_ref": None,
        "closed_implies_verified": False,
    }

    if claims_global:
        result.update(
            outcome="DENIED_SPECIALIST_OVERREACH",
            gate="SPECIALIST_OVERREACH",
        )
        return result

    if capability_id != CAPABILITY_ID:
        result.update(
            outcome="DENIED_WRONG_CAPABILITY",
            gate=(
                "SHARED_CONTEXT_INSUFFICIENT"
                if capability_id == "shared_context_evidence"
                else "WRONG_CAPABILITY"
            ),
        )
        return result

    if role in SCOUT_LIKE_ROLES or role != AUTHORIZED_ROLE:
        result.update(
            outcome="DENIED_ROLE_LACKS_CAPABILITY",
            gate="SCOUT_WRITE_DENIED" if role in SCOUT_LIKE_ROLES else "ROLE_WRITE_DENIED",
        )
        return result

    if lifecycle in LIFECYCLE_DENIED_UNVALIDATED or (
        lifecycle and lifecycle not in LIFECYCLE_ALLOWED_FOR_CREATE
    ):
        result.update(
            outcome="DENIED_UNVALIDATED_IMPROVEMENT",
            gate="LIFECYCLE_BELOW_VALIDATED",
        )
        return result

    if not identity_clear or not improvement_id:
        result.update(
            outcome="HOLD",
            gate="HOLD_IDENTITY_AMBIGUOUS",
        )
        return result

    if not owning_clear or not owning_repo:
        result.update(
            outcome="HOLD",
            gate="HOLD_OWNER_AMBIGUOUS",
        )
        return result

    if not work_concrete:
        result.update(
            outcome="DENIED_WORK_NOT_CONCRETE",
            gate="WORK_NOT_IMPLEMENTABLE",
        )
        return result

    if not target_allows:
        result.update(
            outcome="DENIED_TARGET_AUTHORITY",
            gate="TARGET_ISSUE_CREATE_FORBIDDEN",
        )
        return result

    if not title_ok:
        result.update(
            outcome="DENIED_TITLE_POLICY",
            gate="GERMAN_TITLE_REQUIRED",
        )
        return result

    missing = required_lineage_missing(body_fields)
    if missing:
        result.update(
            outcome="DENIED_LINEAGE_INCOMPLETE",
            gate="LINEAGE_FIELDS_MISSING",
            missing_lineage_fields=missing,
        )
        return result

    prior_op = _matching_operation(known, create_operation_id=create_operation_id)
    if prior_op is not None:
        result.update(
            allowed=False,
            created=False,
            reused=True,
            outcome="IDEMPOTENT_RETRY_NO_DUPLICATE",
            gate="CREATE_OPERATION_ALREADY_APPLIED",
            issue_ref=prior_op.get("issue_ref") or prior_op.get("issue_url"),
        )
        return result

    active = _active_work_items(
        known, improvement_id=improvement_id, owning_repo=owning_repo
    )
    if active:
        first = active[0]
        result.update(
            allowed=False,
            created=False,
            reused=True,
            outcome="REUSED_EXISTING_WORK_ITEM",
            gate="ACTIVE_WORK_ITEM_EXISTS",
            issue_ref=first.get("issue_ref") or first.get("issue_url"),
        )
        return result

    issue_ref = (
        data.get("would_create_issue_ref")
        or f"github.com/example/{owning_repo}/issues/new#{improvement_id}"
    )
    result.update(
        allowed=True,
        created=True,
        reused=False,
        outcome="GITHUB_ISSUE_CREATED",
        gate="BOARD_MANAGER_GITHUB_ALLOWED",
        issue_ref=issue_ref,
        body=build_issue_body(body_fields),
    )
    return result


def evaluate_case(
    case: dict[str, Any], *, pack: dict[str, Any] | None = None
) -> dict[str, Any]:
    _ = pack  # pack reserved for shared role tables; cases are self-contained
    case_id = str(case["id"])
    data = dict(case.get("input") or {})
    expect = case.get("expect") or {}
    actual = evaluate_create_request(data)
    actual["id"] = case_id

    if "closed_issue" in data or "verified_evidence" in data:
        actual["closed_implies_verified"] = closed_issue_implies_verified(
            bool(data.get("closed_issue")),
            bool(data.get("verified_evidence")),
        )

    compare_keys = [
        k
        for k in expect
        if k
        not in {
            # optional soft fields ignored unless present on both sides
        }
    ]
    actual["matches_expect"] = all(actual.get(k) == expect.get(k) for k in compare_keys)
    actual["expect"] = expect
    return actual


def evaluate_all(path: Path | None = None) -> list[dict[str, Any]]:
    pack = load_pressure_cases(path)
    return [evaluate_case(case, pack=pack) for case in pack["cases"]]


def contract_is_active() -> bool:
    text = CONTRACT_MD.read_text(encoding="utf-8")
    return all(
        [
            "ACTIVE" in text,
            "Preconditions for `GITHUB_ISSUE_CREATE`" in text
            or "Preconditions for GITHUB_ISSUE_CREATE" in text,
            "Closed ≠ Verified" in text or "closed ≠ verified" in text.lower(),
            "IDEMPOTENT_RETRY_NO_DUPLICATE" in text or "Idempotenz" in text,
            "HOLD_OWNER_AMBIGUOUS" in text or "Owning repository" in text,
            "STUB" not in text.split("Status", 1)[-1][:200],
        ]
    )


def registry_points_at_active_contract(
    registry: dict[str, Any] | None = None,
) -> bool:
    caps = (registry or load_registry()).get("capabilities") or {}
    github = caps.get(CAPABILITY_ID) or {}
    description = str(github.get("description") or "")
    return all(
        [
            str(github.get("contract") or "").endswith("IMPROVEMENT_GITHUB_ISSUE_CREATE.md"),
            github.get("requirement") == "REQUIRED",
            (github.get("availability") or {}).get("silent_substitution") is False,
            "stub" not in description.lower(),
            "until #51" not in description.lower(),
        ]
    )


def scouts_remain_denied() -> bool:
    quality = QUALITY_SCOUT.read_text(encoding="utf-8")
    process = PROCESS_SCOUT.read_text(encoding="utf-8")
    role = ROLE_MD.read_text(encoding="utf-8")
    policy = POLICY_MD.read_text(encoding="utf-8")
    return all(
        [
            "authority_level: advisory-v1" in quality,
            "authority_level: advisory-v1" in process,
            "recommend, but never create" in quality,
            "recommend, but never create" in process,
            CAPABILITY_ID not in quality,
            CAPABILITY_ID not in process,
            "claims_global_routing: false" in role,
            CAPABILITY_ID in role,
            CAPABILITY_ID in policy,
        ]
    )
