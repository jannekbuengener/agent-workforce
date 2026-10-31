"""Layer-A orchestrator for Skill Improvement Blackboard V1 pilot (#52).

Reuses board-authority and github-issue-create twins. No workforce runtime DB.
Live GitHub / Brain verification remain outside this unit surface.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import improvement_board_authority_lib as board_authority
import improvement_github_issue_create_lib as github_create

REPO_ROOT = Path(__file__).resolve().parents[1]
EXIT_ID = "SKILL_IMPROVEMENT_BLACKBOARD_V1_PILOT_PROVEN"


def _all_match(results: list[dict[str, Any]]) -> list[str]:
    return [item["id"] for item in results if not item.get("matches_expect")]


def run_layer_a_pilot() -> dict[str, Any]:
    """Evaluate workforce Layer-A pressure packs required by the pilot."""
    board_results = board_authority.evaluate_all()
    github_results = github_create.evaluate_all()

    board_failed = _all_match(board_results)
    github_failed = _all_match(github_results)

    scout_cases = [
        item
        for item in github_results
        if item["id"] in {"scout_denied", "supervisor_denied"}
    ]
    ambiguous = next(item for item in github_results if item["id"] == "ambiguous_owner_hold")
    unvalidated = next(
        item for item in github_results if item["id"] == "unvalidated_improvement_denied"
    )
    allowed = next(item for item in github_results if item["id"] == "allowed_create")
    closed = next(item for item in github_results if item["id"] == "closed_issue_not_verified")

    layer_a_pass = not board_failed and not github_failed
    report: dict[str, Any] = {
        "exit_id": EXIT_ID,
        "layer": "A",
        "reuse_before_build": "REUSE_EXISTING + BUILD_THIN",
        "mutable_workforce_db": False,
        "board_authority_cases": len(board_results),
        "github_create_cases": len(github_results),
        "board_authority_failed": board_failed,
        "github_create_failed": github_failed,
        "authority_separation": {
            "scouts_and_supervisor_denied": all(
                item.get("outcome") == "DENIED_ROLE_LACKS_CAPABILITY" for item in scout_cases
            ),
            "board_manager_create_allowed": allowed.get("outcome") == "GITHUB_ISSUE_CREATED",
            "ambiguous_owner_hold": ambiguous.get("gate") == "HOLD_OWNER_AMBIGUOUS",
            "unvalidated_denied": unvalidated.get("outcome")
            == "DENIED_UNVALIDATED_IMPROVEMENT",
            "closed_implies_verified": bool(closed.get("closed_implies_verified")),
        },
        "contract_active": github_create.contract_is_active(),
        "registry_active": github_create.registry_points_at_active_contract(),
        "scouts_remain_denied": github_create.scouts_remain_denied(),
        "layer_a_pass": layer_a_pass
        and github_create.contract_is_active()
        and github_create.registry_points_at_active_contract()
        and github_create.scouts_remain_denied()
        and closed.get("closed_implies_verified") is False,
    }
    report["authority_separation"]["ok"] = all(
        [
            report["authority_separation"]["scouts_and_supervisor_denied"],
            report["authority_separation"]["board_manager_create_allowed"],
            report["authority_separation"]["ambiguous_owner_hold"],
            report["authority_separation"]["unvalidated_denied"],
            report["authority_separation"]["closed_implies_verified"] is False,
        ]
    )
    return report
