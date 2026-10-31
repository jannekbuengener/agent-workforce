"""Deterministic contract twin for evidence-backed-delivery pressure cases.

Layer A only: encodes Issue/PR/Evidence/Merge-order gates the skill mandates.
Does not prove a live agent obeyed SKILL.md — that is Layer B / dogfood evidence.

No jsonschema runtime dependency: structural envelope checks are plain Python.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PRESSURE_CASES = (
    REPO_ROOT
    / "docs"
    / "skills"
    / "evidence-backed-delivery"
    / "references"
    / "pressure_cases.yml"
)
SKILL_MD = (
    REPO_ROOT / "docs" / "skills" / "evidence-backed-delivery" / "SKILL.md"
)
CONSUMER_YML = (
    REPO_ROOT / "docs" / "skills" / "evidence-backed-delivery" / "consumer.yml"
)
CONTRACT_MD = REPO_ROOT / "contracts" / "EVIDENCE_BACKED_DELIVERY_CONTRACT.md"
SCHEMA_JSON = REPO_ROOT / "contracts" / "evidence_backed_delivery.v1.schema.json"
MODALITIES_YML = (
    REPO_ROOT
    / "docs"
    / "skills"
    / "evidence-backed-delivery"
    / "references"
    / "evidence_modalities.yml"
)

ISSUE_REQUIRED_FIELDS = (
    "intent",
    "goal",
    "authority",
    "scope",
    "constraints",
    "non_goals",
    "dependencies",
    "acceptance_criteria",
    "required_evidence",
    "exit",
)

LOCATOR_KINDS = frozenset(
    {
        "PR_EMBEDDED",
        "GITHUB_ATTACHMENT",
        "WORKFLOW_ARTIFACT",
        "STABLE_REVIEW_URL",
        "LOCAL_ONLY",
    }
)

HUMAN_OK_LOCATORS = frozenset(
    {
        "PR_EMBEDDED",
        "GITHUB_ATTACHMENT",
        "WORKFLOW_ARTIFACT",
        "STABLE_REVIEW_URL",
    }
)

PERCEPTION_MODALITIES = frozenset({"ui_visual", "animation", "audio"})

CLAIM_MATCHING_MODALITIES: dict[str, frozenset[str]] = {
    "ui_visual": frozenset({"ui_visual", "image"}),
    "animation": frozenset({"animation", "video", "gif"}),
    "audio": frozenset({"audio"}),
    "api_dataflow": frozenset({"api", "json", "contract", "request_response"}),
    "cli": frozenset({"cli", "command_log", "terminal"}),
    "performance": frozenset({"performance", "measurement", "measurement_report"}),
    "migration_persistence": frozenset(
        {"migration", "before_after_state", "roundtrip"}
    ),
    "bugfix": frozenset({"bugfix", "bugfix_before", "bugfix_after"}),
    "internal": frozenset({"internal", "test", "runtime_integration"}),
    "security_policy_governance": frozenset(
        {"security", "policy", "governance", "validator_output", "diff_state"}
    ),
}

_WINDOWS_ABS = re.compile(r"^[A-Za-z]:[\\/]")
_UNIX_ABS = re.compile(r"^/")
_FILE_URL = re.compile(r"^file:", re.I)


def load_pressure_cases(path: Path | None = None) -> dict[str, Any]:
    target = path or DEFAULT_PRESSURE_CASES
    data = yaml.safe_load(target.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "cases" not in data:
        raise ValueError(f"invalid pressure cases file: {target}")
    return data


def load_modalities(path: Path | None = None) -> dict[str, Any]:
    target = path or MODALITIES_YML
    data = yaml.safe_load(target.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"invalid modalities file: {target}")
    return data


def load_schema(path: Path | None = None) -> dict[str, Any]:
    target = path or SCHEMA_JSON
    data = json.loads(target.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"invalid schema file: {target}")
    return data


def classify_locator(artifact: dict[str, Any]) -> str:
    """Return locator_kind; infer LOCAL_ONLY from path-like locators when unset."""
    kind = artifact.get("locator_kind")
    if kind in LOCATOR_KINDS:
        return str(kind)
    locator = str(artifact.get("locator") or "")
    if (
        _WINDOWS_ABS.match(locator)
        or _UNIX_ABS.match(locator)
        or _FILE_URL.match(locator)
        or locator.startswith("\\\\")
    ):
        return "LOCAL_ONLY"
    if kind:
        raise ValueError(f"unknown locator_kind: {kind}")
    return "LOCAL_ONLY"


def evaluate_issue_contract(issue: dict[str, Any]) -> dict[str, Any]:
    missing = [
        field
        for field in ISSUE_REQUIRED_FIELDS
        if issue.get(field) is None
        or issue.get(field) == ""
        or (isinstance(issue.get(field), list) and field in ("acceptance_criteria",)
            and not issue.get(field))
    ]
    # Treat explicit null for core narrative fields as incomplete; empty lists
    # for constraints/non_goals/dependencies are allowed.
    core = ("intent", "goal", "authority", "scope", "acceptance_criteria",
            "required_evidence", "exit")
    incomplete = any(
        issue.get(field) is None or issue.get(field) == "" for field in core
    )
    if incomplete:
        return {
            "issue_status": "HOLD_ISSUE_CONTRACT_INCOMPLETE",
            "implementation_authorized": False,
            "missing_fields": missing,
        }
    return {
        "issue_status": "READY",
        "implementation_authorized": False,  # open issue ≠ implement auth
        "missing_fields": [],
    }


def _modality_satisfied(claim: str, artifacts: list[dict[str, Any]]) -> bool:
    allowed = CLAIM_MATCHING_MODALITIES.get(claim, frozenset({claim}))
    for art in artifacts:
        if classify_locator(art) == "LOCAL_ONLY":
            continue
        if str(art.get("modality", "")) in allowed:
            return True
    return False


def _has_local_only(artifacts: list[dict[str, Any]]) -> bool:
    return any(classify_locator(a) == "LOCAL_ONLY" for a in artifacts)


def _primary_locator(artifacts: list[dict[str, Any]]) -> str | None:
    if not artifacts:
        return None
    return classify_locator(artifacts[0])


def _stale(
    *,
    head_sha: str | None,
    evidence_head_sha: str | None,
    commits: list[dict[str, Any]],
    carry_forward_justified: bool,
) -> bool:
    if evidence_head_sha is None:
        return False
    if head_sha == evidence_head_sha:
        return False
    # Head mismatch is stale unless a justified carry-forward proves non-impact.
    if carry_forward_justified and not any(
        c.get("touches_claim_surface") for c in commits
    ):
        return False
    return True


def classify_evidence(data: dict[str, Any]) -> dict[str, Any]:
    claim = str(data.get("claim_modality") or "")
    artifacts = list(data.get("artifacts") or [])
    head = data.get("head_sha")
    evidence_head = data.get("evidence_head_sha")
    commits = list(data.get("commits_since_evidence") or [])
    carry = bool(data.get("carry_forward_justified"))
    perception = bool(data.get("human_perception_required"))
    owner_req = bool(data.get("owner_acceptance_required"))
    agent_pass = bool(data.get("agent_declares_owner_pass"))
    large_no_index = bool(data.get("large_pack_without_index")) or (
        len(artifacts) >= 5 and not bool(data.get("review_index_present"))
    )
    require_before = bool(data.get("require_before_fail"))
    require_after = bool(data.get("require_after_pass"))

    result: dict[str, Any] = {
        "locator_kind": _primary_locator(artifacts),
        "agent_may_self_pass_owner": False,
        "merge_candidate": False,
    }

    if owner_req and agent_pass:
        result.update(
            {
                "verdict": "AWAITING_OWNER",
                "evidence_status": "AWAITING_OWNER",
            }
        )
        return result

    if owner_req and not agent_pass:
        # Owner gate outstanding even if artifacts look fine.
        # Only force AWAITING_OWNER when evaluating acceptance path with owner flag.
        pass

    if large_no_index and len(artifacts) >= 5:
        result.update(
            {
                "verdict": "CURRENT_PR_REWORK_REQUIRED",
                "evidence_ux": "REWORK_REQUIRED",
                "evidence_status": "REWORK_REQUIRED",
            }
        )
        return result

    if claim == "bugfix" and (require_before or require_after):
        kinds = {str(a.get("modality")) for a in artifacts}
        has_before = "bugfix_before" in kinds or any(
            "before" in str(a.get("id", "")).lower() for a in artifacts
        )
        has_after = "bugfix_after" in kinds or any(
            "after" in str(a.get("id", "")).lower() for a in artifacts
        )
        if require_before and not has_before:
            result.update(
                {
                    "verdict": "BLOCKED_MISSING_EVIDENCE",
                    "evidence_incomplete": True,
                    "evidence_status": "INCOMPLETE",
                }
            )
            return result
        if require_after and not has_after:
            result.update(
                {
                    "verdict": "BLOCKED_MISSING_EVIDENCE",
                    "evidence_incomplete": True,
                    "evidence_status": "INCOMPLETE",
                }
            )
            return result

    if not artifacts:
        result.update(
            {
                "verdict": "BLOCKED_MISSING_EVIDENCE",
                "evidence_status": "MISSING",
            }
        )
        return result

    # LOCAL_ONLY never suffices for human-inspectable PR evidence.
    if _has_local_only(artifacts):
        non_local = [a for a in artifacts if classify_locator(a) != "LOCAL_ONLY"]
        if not non_local:
            result.update(
                {
                    "verdict": "BLOCKED_MISSING_EVIDENCE",
                    "locator_kind": "LOCAL_ONLY",
                    "evidence_status": "LOCAL_ONLY",
                }
            )
            return result

    if perception and not _modality_satisfied(claim, artifacts):
        result.update(
            {
                "verdict": "BLOCKED_MISSING_EVIDENCE",
                "evidence_status": "WRONG_MODALITY",
            }
        )
        return result

    if _stale(
        head_sha=str(head) if head else None,
        evidence_head_sha=str(evidence_head) if evidence_head else None,
        commits=commits,
        carry_forward_justified=carry,
    ):
        result.update(
            {
                "verdict": "BLOCKED_STALE_EVIDENCE",
                "evidence_status": "STALE",
            }
        )
        return result

    if carry and head != evidence_head and not any(
        c.get("touches_claim_surface") for c in commits
    ):
        result["evidence_status"] = "CARRY_FORWARD_OK"
    else:
        result["evidence_status"] = "ACCEPTABLE"

    if owner_req:
        result.update(
            {
                "verdict": "AWAITING_OWNER",
                "evidence_status": result.get("evidence_status", "ACCEPTABLE"),
            }
        )
        return result

    result["verdict"] = "EVIDENCE_OK"
    return result


def classify_dependency(prs: list[dict[str, Any]], **flags: Any) -> dict[str, Any]:
    if len(prs) < 2:
        return {
            "relation": "INDEPENDENT",
            "parallel_prep_allowed": True,
            "hold": None,
        }

    ids = {str(p["id"]) for p in prs}
    dep_edges = {
        str(p["id"]): [str(d) for d in (p.get("depends_on") or [])] for p in prs
    }

    # Cyclic deps → unclear
    for pid, deps in dep_edges.items():
        for dep in deps:
            if pid in dep_edges.get(dep, []):
                return {
                    "relation": "MERGE_ORDER_UNCLEAR",
                    "parallel_prep_allowed": False,
                    "hold": "HOLD_MERGE_ORDER_UNCLEAR",
                }

    # File overlap without declared dep
    file_owners: dict[str, str] = {}
    overlapping = False
    for p in prs:
        for f in p.get("files") or []:
            key = str(f)
            owner = file_owners.get(key)
            if owner and owner != str(p["id"]):
                overlapping = True
            else:
                file_owners[key] = str(p["id"])

    authorities = [str(p.get("authority") or "") for p in prs]
    same_authority = (
        len(set(a for a in authorities if a)) == 1 and len(authorities) > 1
    )

    has_deps = any(dep_edges[str(p["id"])] for p in prs)
    if has_deps:
        relation = "DOWNSTREAM_DEPENDENCY"
        if flags.get("upstream_merged") and flags.get("shared_authority_changed"):
            return {
                "relation": relation,
                "parallel_prep_allowed": False,
                "require_reconcile": True,
                "evidence_action": "REEVALUATE",
                "hold": None,
            }
        return {
            "relation": relation,
            "parallel_prep_allowed": False,
            "hold": None,
        }

    if same_authority and overlapping:
        return {
            "relation": "SAME_AUTHORITY_CONFLICT",
            "parallel_prep_allowed": False,
            "hold": "HOLD_MERGE_ORDER_UNCLEAR",
        }

    if overlapping:
        return {
            "relation": "OVERLAPPING_WRITER",
            "parallel_prep_allowed": False,
            "hold": None,
        }

    # Unknown external deps
    for deps in dep_edges.values():
        if any(d not in ids for d in deps):
            return {
                "relation": "MERGE_ORDER_UNCLEAR",
                "parallel_prep_allowed": False,
                "hold": "HOLD_MERGE_ORDER_UNCLEAR",
            }

    return {
        "relation": "INDEPENDENT",
        "parallel_prep_allowed": True,
        "hold": None,
    }


def evaluate_parent_close(data: dict[str, Any]) -> dict[str, Any]:
    exit_ok = bool(data.get("parent_meta_exit_evidenced"))
    return {
        "parent_may_close": exit_ok,
        "parent_issue_state": "CLOSED" if exit_ok else "OPEN",
        "residual_required": not exit_ok,
    }


def evaluate_acceptance(data: dict[str, Any]) -> dict[str, Any]:
    """Compose evidence + review + merge-order into a PR acceptance verdict."""
    if data.get("issue") is not None:
        issue_eval = evaluate_issue_contract(dict(data["issue"]))
        if issue_eval["issue_status"] == "HOLD_ISSUE_CONTRACT_INCOMPLETE":
            return {
                **issue_eval,
                "verdict": "HOLD_ISSUE_CONTRACT_INCOMPLETE",
                "merge_candidate": False,
            }

    if "prs" in data and data.get("claim_modality") is None:
        dep = classify_dependency(list(data["prs"]), **{
            k: data[k]
            for k in ("upstream_merged", "shared_authority_changed")
            if k in data
        })
        return {**dep, "merge_candidate": False}

    if "child_pr_merged" in data or "parent_meta_exit_evidenced" in data:
        return evaluate_parent_close(data)

    evidence = classify_evidence(data)
    unresolved = list(data.get("unresolved_must_fix") or [])
    merge_order = data.get("merge_order")
    issue_ok = data.get("issue_contract_complete", True)
    # Missing tests_green must not imply green — require explicit True.
    tests_green = data.get("tests_green") is True

    if not issue_ok:
        return {
            **evidence,
            "verdict": "HOLD_ISSUE_CONTRACT_INCOMPLETE",
            "merge_candidate": False,
        }

    # MUST_FIX findings take precedence over owner-wait for verdict clarity.
    if unresolved:
        return {
            **evidence,
            "verdict": "BLOCKED_REVIEW_FINDINGS",
            "merge_candidate": False,
        }

    if evidence.get("verdict") in {
        "BLOCKED_MISSING_EVIDENCE",
        "BLOCKED_STALE_EVIDENCE",
        "AWAITING_OWNER",
        "CURRENT_PR_REWORK_REQUIRED",
    }:
        evidence["merge_candidate"] = False
        return evidence

    if merge_order == "MERGE_ORDER_UNCLEAR":
        return {
            **evidence,
            "verdict": "BLOCKED_MERGE_ORDER",
            "merge_candidate": False,
        }

    if data.get("repo_gate_pass") is False:
        return {
            **evidence,
            "verdict": "BLOCKED_REPO_GATE",
            "merge_candidate": False,
        }

    # Evidence OK path — require explicit tests_green True.
    if evidence.get("evidence_status") in {"ACCEPTABLE", "CARRY_FORWARD_OK"}:
        if tests_green:
            return {
                **evidence,
                "verdict": "MERGE_CANDIDATE",
                "merge_candidate": True,
            }
        return {
            **evidence,
            "verdict": "CURRENT_PR_REWORK_REQUIRED",
            "merge_candidate": False,
            "reason": "tests_green_not_evidenced",
        }

    return {
        **evidence,
        "verdict": evidence.get("verdict", "CURRENT_PR_REWORK_REQUIRED"),
        "merge_candidate": False,
    }


def evaluate_case(case: dict[str, Any]) -> dict[str, Any]:
    case_id = str(case["id"])
    data = case.get("input") or {}
    expect = case.get("expect") or {}
    actual: dict[str, Any] = {"id": case_id}

    if case_id == "incomplete_issue_contract":
        actual.update(evaluate_issue_contract(dict(data["issue"])))
    elif case_id in {"independent_prs_parallel", "merge_order_unclear"}:
        actual.update(classify_dependency(list(data["prs"])))
    elif case_id == "upstream_merge_invalidates_downstream":
        actual.update(
            classify_dependency(
                list(data["prs"]),
                upstream_merged=bool(data.get("upstream_merged")),
                shared_authority_changed=bool(data.get("shared_authority_changed")),
            )
        )
    elif case_id == "child_merged_parent_exit_open":
        actual.update(evaluate_parent_close(data))
    else:
        actual.update(evaluate_acceptance(data))

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


def structural_schema_keys_present(schema: dict[str, Any] | None = None) -> bool:
    """Lightweight structural check — no jsonschema dependency."""
    data = schema if schema is not None else load_schema()
    required_top = {"$schema", "title", "type", "properties", "definitions"}
    if not required_top.issubset(data.keys()):
        return False
    props = data.get("properties") or {}
    needed = {
        "issue_contract",
        "pr_evidence",
        "locator_kind",
        "acceptance_verdict",
        "dependency_relation",
    }
    return needed.issubset(props.keys()) or needed.issubset(
        (data.get("definitions") or {}).keys()
    )


def skill_mandates_delivery_contract(text: str | None = None) -> bool:
    body = text if text is not None else SKILL_MD.read_text(encoding="utf-8")
    checks = [
        "evidence-backed-delivery" in body,
        "Evidence by Modality" in body or "evidence by modality" in body.lower(),
        "LOCAL_ONLY" in body,
        "PR_EMBEDDED" in body,
        "AWAITING_OWNER" in body,
        "BLOCKED_MISSING_EVIDENCE" in body,
        "BLOCKED_STALE_EVIDENCE" in body,
        "Final-Head" in body or "final head" in body.lower() or "Final Head" in body,
        "MERGE_CANDIDATE" in body,
        "HOLD_ISSUE_CONTRACT_INCOMPLETE" in body,
        "HOLD_MERGE_ORDER_UNCLEAR" in body,
    ]
    return all(checks)
