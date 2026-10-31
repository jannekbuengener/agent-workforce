"""Deterministic AUTHORITY_RECONCILIATION_REQUIRED contract tests."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import authority_reconciliation_lib as lib  # noqa: E402


REQUIRED_BEHAVIORAL = {
    "existing_authority_owns_outcome",
    "newer_delta_requires_freshness_reconciliation",
    "genuine_missing_authority",
    "ordinary_implementation_child",
    "search_snippet_insufficient",
}


class PressureCaseContractTests(unittest.TestCase):
    def test_all_pressure_cases_match_expect(self) -> None:
        results = lib.evaluate_all()
        self.assertGreaterEqual(len(results), 5)
        failed = [r["id"] for r in results if not r.get("matches_expect")]
        self.assertEqual(failed, [], msg=f"mismatched cases: {results}")

    def test_behavioral_required_cases_are_marked(self) -> None:
        pack = lib.load_pressure_cases()
        required = {
            c["id"] for c in pack["cases"] if c.get("behavioral_required")
        }
        self.assertTrue(REQUIRED_BEHAVIORAL.issubset(required))

    def test_existing_authority_forbids_create_new(self) -> None:
        pack = lib.load_pressure_cases()
        case = next(
            c for c in pack["cases"] if c["id"] == "existing_authority_owns_outcome"
        )
        result = lib.evaluate_case(case)
        self.assertTrue(result["matches_expect"])
        self.assertFalse(result["create_new_allowed"])
        self.assertEqual(result["decision"], "UPDATE_EXISTING")

    def test_newer_delta_requires_freshness_not_new_meta(self) -> None:
        pack = lib.load_pressure_cases()
        case = next(
            c
            for c in pack["cases"]
            if c["id"] == "newer_delta_requires_freshness_reconciliation"
        )
        result = lib.evaluate_case(case)
        self.assertTrue(result["matches_expect"])
        self.assertTrue(result["requires_freshness_reconciliation"])
        self.assertFalse(result["create_new_allowed"])
        self.assertEqual(result["decision"], "RECONCILE_EXISTING")

    def test_genuine_missing_authority_allows_create_new(self) -> None:
        pack = lib.load_pressure_cases()
        case = next(
            c for c in pack["cases"] if c["id"] == "genuine_missing_authority"
        )
        result = lib.evaluate_case(case)
        self.assertTrue(result["matches_expect"])
        self.assertTrue(result["create_new_allowed"])
        self.assertEqual(result["decision"], "CREATE_NEW_AUTHORITY")

    def test_ordinary_child_skips_gate(self) -> None:
        pack = lib.load_pressure_cases()
        case = next(
            c for c in pack["cases"] if c["id"] == "ordinary_implementation_child"
        )
        result = lib.evaluate_case(case)
        self.assertTrue(result["matches_expect"])
        self.assertFalse(result["gate_applicable"])
        self.assertEqual(result["gate"], "GATE_NOT_APPLICABLE")

    def test_search_snippet_blocks_create_new(self) -> None:
        pack = lib.load_pressure_cases()
        case = next(
            c for c in pack["cases"] if c["id"] == "search_snippet_insufficient"
        )
        result = lib.evaluate_case(case)
        self.assertTrue(result["matches_expect"])
        self.assertFalse(result["create_new_allowed"])
        self.assertEqual(result["decision"], "HOLD_FULL_BODY_READ_REQUIRED")

    def test_portfolio_inventory_flagged_as_overreach(self) -> None:
        pack = lib.load_pressure_cases()
        case = next(
            c for c in pack["cases"] if c["id"] == "portfolio_inventory_overreach"
        )
        result = lib.evaluate_case(case)
        self.assertTrue(result["matches_expect"])
        self.assertTrue(result["overreach"])
        self.assertFalse(result["create_new_allowed"])


class CanonPlacementTests(unittest.TestCase):
    def test_policy_encodes_full_gate(self) -> None:
        self.assertTrue(lib.policy_encodes_authority_reconciliation())

    def test_operating_model_pipeline_order(self) -> None:
        self.assertTrue(lib.operating_model_places_reconciliation_gate())

    def test_frontdoors_reference_policy(self) -> None:
        self.assertTrue(lib.frontdoors_reference_policy_gate())

    def test_create_new_default_denied_without_proof(self) -> None:
        case = {
            "id": "ad_hoc_partial_no_proof",
            "input": {
                "proposing": "meta_epic",
                "existing_authorities": [
                    {
                        "id": "a",
                        "kind": "epic",
                        "owns_outcome": "partial",
                        "body_fully_read": True,
                    }
                ],
                "bodies_fully_read": True,
                "newer_relevant_delta": False,
                "alternatives_scored": True,
                "missing_authority_proof": None,
                "inventory_entire_portfolio": False,
            },
            "expect": {
                "create_new_allowed": False,
                "decision": "LINK_EXISTING",
            },
        }
        result = lib.evaluate_case(case)
        self.assertTrue(result["matches_expect"])


if __name__ == "__main__":
    unittest.main()
