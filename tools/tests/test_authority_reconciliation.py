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
    # Issue #69 — structural precedent + intent (A–D, F; E = ordinary_implementation_child)
    "existing_owner_stops_without_precedents",
    "candidate_belongs_to_existing_owner",
    "genuine_structural_gap_after_precedents",
    "intent_collapsed_to_owner_cleanup",
    "no_local_same_class_precedent",
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

    def test_existing_owner_does_not_skip_precedent_evaluation(self) -> None:
        pack = lib.load_pressure_cases()
        case = next(
            c
            for c in pack["cases"]
            if c["id"] == "existing_owner_stops_without_precedents"
        )
        result = lib.evaluate_case(case)
        self.assertTrue(result["matches_expect"])
        self.assertFalse(result["create_new_allowed"])
        self.assertEqual(result["decision"], "HOLD_PRECEDENT_EVALUATION_REQUIRED")
        self.assertEqual(result["gate"], "AUTHORITY_RECONCILIATION_HOLD")

    def test_candidate_reconciles_to_existing_owner(self) -> None:
        pack = lib.load_pressure_cases()
        case = next(
            c
            for c in pack["cases"]
            if c["id"] == "candidate_belongs_to_existing_owner"
        )
        result = lib.evaluate_case(case)
        self.assertTrue(result["matches_expect"])
        self.assertFalse(result["create_new_allowed"])
        self.assertIn(
            result["decision"],
            {"UPDATE_EXISTING", "RECONCILE_EXISTING", "NO_STRUCTURAL_CHANGE"},
        )

    def test_genuine_gap_after_precedents_allows_create_new(self) -> None:
        pack = lib.load_pressure_cases()
        case = next(
            c
            for c in pack["cases"]
            if c["id"] == "genuine_structural_gap_after_precedents"
        )
        result = lib.evaluate_case(case)
        self.assertTrue(result["matches_expect"])
        self.assertTrue(result["create_new_allowed"])
        self.assertEqual(result["decision"], "CREATE_NEW_AUTHORITY")

    def test_intent_collapse_fails_closed(self) -> None:
        pack = lib.load_pressure_cases()
        case = next(
            c
            for c in pack["cases"]
            if c["id"] == "intent_collapsed_to_owner_cleanup"
        )
        result = lib.evaluate_case(case)
        self.assertTrue(result["matches_expect"])
        self.assertFalse(result["create_new_allowed"])
        self.assertEqual(result["decision"], "INTENT_COLLAPSED_FAIL")
        self.assertEqual(result["gate"], "AUTHORITY_RECONCILIATION_FAIL")

    def test_ordinary_child_skips_precedent_ceremony(self) -> None:
        """Case E — ordinary child must not trigger precedent ceremony."""
        pack = lib.load_pressure_cases()
        case = next(
            c for c in pack["cases"] if c["id"] == "ordinary_implementation_child"
        )
        result = lib.evaluate_case(case)
        self.assertTrue(result["matches_expect"])
        self.assertFalse(result["gate_applicable"])
        self.assertEqual(result["gate"], "GATE_NOT_APPLICABLE")

    def test_none_found_precedents_continue_without_block(self) -> None:
        pack = lib.load_pressure_cases()
        case = next(
            c for c in pack["cases"] if c["id"] == "no_local_same_class_precedent"
        )
        result = lib.evaluate_case(case)
        self.assertTrue(result["matches_expect"])
        self.assertNotEqual(result["decision"], "HOLD_PRECEDENT_EVALUATION_REQUIRED")
        self.assertNotEqual(result["gate"], "AUTHORITY_RECONCILIATION_HOLD")
        self.assertTrue(result["create_new_allowed"])
        self.assertEqual(result["decision"], "CREATE_NEW_AUTHORITY")


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

    def test_missing_intent_flag_holds_when_candidate_analysis(self) -> None:
        case = {
            "id": "ad_hoc_missing_intent_preservation",
            "input": {
                "proposing": "meta_epic",
                "candidate_analysis_requested": True,
                # original_intent_preserved intentionally omitted
                "local_precedent_status": "EVALUATED",
                "candidate_reconciliation_completed": True,
                "existing_authorities": [
                    {
                        "id": "product_owner",
                        "kind": "product_authority",
                        "owns_outcome": True,
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
                "decision": "HOLD_INTENT_PRESERVATION_REQUIRED",
                "gate": "AUTHORITY_RECONCILIATION_HOLD",
            },
        }
        result = lib.evaluate_case(case)
        self.assertTrue(result["matches_expect"])


if __name__ == "__main__":
    unittest.main()
