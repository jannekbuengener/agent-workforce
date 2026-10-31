"""Authority separation tests for Head of Knowledge FOUNDING_SOLO (#70)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import knowledge_department_authority_lib as authority  # noqa: E402


REQUIRED_BEHAVIORAL = {
    "denied_self_grant_authority",
    "denied_target_repo_product_mutation",
    "denied_runtime_not_provisioned",
    "denied_improvement_management_write",
    "allowed_department_decision_with_evidence",
}


class KnowledgeDepartmentAuthorityTests(unittest.TestCase):
    def test_registry_encodes_knowledge_capabilities(self) -> None:
        self.assertTrue(authority.registry_encodes_knowledge_capabilities())

    def test_employee_record_encodes_founding_solo_capabilities(self) -> None:
        self.assertTrue(authority.employee_record_encodes_founding_solo_capabilities())

    def test_authority_docs_present(self) -> None:
        self.assertTrue(authority.authority_docs_present())

    def test_all_pressure_cases_match_expect(self) -> None:
        results = authority.evaluate_all()
        self.assertGreaterEqual(len(results), 10)
        failed = [r["id"] for r in results if not r.get("matches_expect")]
        self.assertEqual(failed, [], msg=f"mismatched cases: {results}")

    def test_behavioral_required_cases_present(self) -> None:
        pack = authority.load_pressure_cases()
        required = {c["id"] for c in pack["cases"] if c.get("behavioral_required")}
        self.assertTrue(REQUIRED_BEHAVIORAL.issubset(required))

    def test_denied_runtime_not_provisioned(self) -> None:
        pack = authority.load_pressure_cases()
        case = next(
            c for c in pack["cases"] if c["id"] == "denied_runtime_not_provisioned"
        )
        result = authority.evaluate_case(case, pack=pack)
        self.assertTrue(result["matches_expect"])
        self.assertFalse(result["allowed"])
        self.assertEqual(result["gate"], "RUNTIME_NOT_PROVISIONED")

    def test_denied_board_manager_capability_not_inherited(self) -> None:
        pack = authority.load_pressure_cases()
        case = next(
            c
            for c in pack["cases"]
            if c["id"] == "denied_improvement_management_write"
        )
        result = authority.evaluate_case(case, pack=pack)
        self.assertTrue(result["matches_expect"])
        self.assertEqual(result["gate"], "BOARD_MANAGER_CAPABILITY_NOT_INHERITED")

    def test_allowed_department_decision(self) -> None:
        pack = authority.load_pressure_cases()
        case = next(
            c
            for c in pack["cases"]
            if c["id"] == "allowed_department_decision_with_evidence"
        )
        result = authority.evaluate_case(case, pack=pack)
        self.assertTrue(result["matches_expect"])
        self.assertTrue(result["allowed"])
        self.assertEqual(result["outcome"], "DECISION_RECORDED")


if __name__ == "__main__":
    unittest.main()
