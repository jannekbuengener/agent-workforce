"""Layer-A tests for Improvement GitHub Issue Create routing (#51)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import improvement_github_issue_create_lib as github_create  # noqa: E402

REQUIRED_BEHAVIORAL = {
    "allowed_create",
    "duplicate_retry",
    "existing_issue_reuse",
    "ambiguous_owner_hold",
    "unvalidated_improvement_denied",
    "denied_target_authority",
    "scout_denied",
}


COMPLETE_BODY = {
    "improvement_id": "imp-unit",
    "root_cause_or_problem": "problem",
    "evidence_summary": "evidence",
    "recommended_change": "change",
    "expected_benefit": "benefit",
    "scope_owner": "agent-workforce",
    "acceptance_or_verification": "tests green",
    "improvement_record_ref": "blackboard://improvements/imp-unit",
    "closed_not_verified_notice": "Closed issue != VERIFIED",
}


class ImprovementGithubIssueCreateTests(unittest.TestCase):
    def test_all_pressure_cases_match_expect(self) -> None:
        results = github_create.evaluate_all()
        self.assertGreaterEqual(len(results), 7)
        failed = [r["id"] for r in results if not r.get("matches_expect")]
        self.assertEqual(failed, [], msg=f"mismatched cases: {failed}")

    def test_behavioral_required_cases_present(self) -> None:
        pack = github_create.load_pressure_cases()
        required = {c["id"] for c in pack["cases"] if c.get("behavioral_required")}
        self.assertTrue(REQUIRED_BEHAVIORAL.issubset(required))

    def test_allowed_create(self) -> None:
        pack = github_create.load_pressure_cases()
        case = next(c for c in pack["cases"] if c["id"] == "allowed_create")
        result = github_create.evaluate_case(case, pack=pack)
        self.assertTrue(result["matches_expect"])
        self.assertTrue(result["allowed"])
        self.assertTrue(result["created"])
        self.assertEqual(result["outcome"], "GITHUB_ISSUE_CREATED")
        self.assertIn("Improvement ID", result["body"])
        self.assertIn("Closed ≠ Verified notice", result["body"])

    def test_duplicate_retry(self) -> None:
        pack = github_create.load_pressure_cases()
        case = next(c for c in pack["cases"] if c["id"] == "duplicate_retry")
        result = github_create.evaluate_case(case, pack=pack)
        self.assertTrue(result["matches_expect"])
        self.assertFalse(result["created"])
        self.assertTrue(result["reused"])
        self.assertEqual(result["outcome"], "IDEMPOTENT_RETRY_NO_DUPLICATE")

    def test_existing_issue_reuse(self) -> None:
        pack = github_create.load_pressure_cases()
        case = next(c for c in pack["cases"] if c["id"] == "existing_issue_reuse")
        result = github_create.evaluate_case(case, pack=pack)
        self.assertTrue(result["matches_expect"])
        self.assertEqual(result["outcome"], "REUSED_EXISTING_WORK_ITEM")
        self.assertEqual(
            result["issue_ref"],
            "github.com/jannekbuengener/agent-workforce/issues/88",
        )

    def test_ambiguous_owner_hold(self) -> None:
        pack = github_create.load_pressure_cases()
        case = next(c for c in pack["cases"] if c["id"] == "ambiguous_owner_hold")
        result = github_create.evaluate_case(case, pack=pack)
        self.assertTrue(result["matches_expect"])
        self.assertEqual(result["gate"], "HOLD_OWNER_AMBIGUOUS")

    def test_unvalidated_improvement_denied(self) -> None:
        pack = github_create.load_pressure_cases()
        case = next(
            c for c in pack["cases"] if c["id"] == "unvalidated_improvement_denied"
        )
        result = github_create.evaluate_case(case, pack=pack)
        self.assertTrue(result["matches_expect"])
        self.assertEqual(result["outcome"], "DENIED_UNVALIDATED_IMPROVEMENT")

    def test_denied_target_authority(self) -> None:
        pack = github_create.load_pressure_cases()
        case = next(c for c in pack["cases"] if c["id"] == "denied_target_authority")
        result = github_create.evaluate_case(case, pack=pack)
        self.assertTrue(result["matches_expect"])
        self.assertEqual(result["outcome"], "DENIED_TARGET_AUTHORITY")

    def test_scout_denied(self) -> None:
        pack = github_create.load_pressure_cases()
        case = next(c for c in pack["cases"] if c["id"] == "scout_denied")
        result = github_create.evaluate_case(case, pack=pack)
        self.assertTrue(result["matches_expect"])
        self.assertEqual(result["gate"], "SCOUT_WRITE_DENIED")

    def test_closed_not_verified(self) -> None:
        self.assertFalse(
            github_create.closed_issue_implies_verified(
                closed=True, verified_evidence=False
            )
        )
        self.assertTrue(
            github_create.closed_issue_implies_verified(
                closed=True, verified_evidence=True
            )
        )
        pack = github_create.load_pressure_cases()
        case = next(c for c in pack["cases"] if c["id"] == "closed_issue_not_verified")
        result = github_create.evaluate_case(case, pack=pack)
        self.assertTrue(result["matches_expect"])
        self.assertFalse(result["closed_implies_verified"])

    def test_build_issue_body_requires_lineage(self) -> None:
        body = github_create.build_issue_body(COMPLETE_BODY)
        self.assertIn("### Improvement ID", body)
        with self.assertRaises(ValueError):
            github_create.build_issue_body({"improvement_id": "x"})

    def test_contract_and_scouts(self) -> None:
        self.assertTrue(github_create.contract_is_active())
        self.assertTrue(github_create.registry_points_at_active_contract())
        self.assertTrue(github_create.scouts_remain_denied())


if __name__ == "__main__":
    unittest.main()
