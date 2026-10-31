"""Layer A + behavioral classification tests for Skill-TDD RED fixtures (#48)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import skill_tdd_red_fixture_lib as lib  # noqa: E402


REQUIRED_BEHAVIORAL = {
    "case_a_direct_leak",
    "case_b_semantic_leak",
    "case_c_clean_soft_red_fail",
    "case_d_existing_behavior_pass",
    "case_e_adversarial_non_leaking",
    "case_f_unrealistic_omission",
    "bypass_1_near_identical_paraphrase",
    "bypass_2_force_fail_after_clean_pass",
    "bypass_3_strip_authority_to_force_fail",
    "bypass_4_adversarial_states_the_ban",
}


class PressureCaseContractTests(unittest.TestCase):
    def test_all_pressure_cases_match_expect(self) -> None:
        results = lib.evaluate_all()
        self.assertGreaterEqual(len(results), 10)
        failed = [
            {"id": r["id"], "actual": r.get("outcome"), "expect": r.get("expect")}
            for r in results
            if not r.get("matches_expect")
        ]
        self.assertEqual(failed, [], msg=f"mismatched cases: {failed}")

    def test_behavioral_required_cases_are_marked(self) -> None:
        pack = lib.load_pressure_cases()
        required = {
            c["id"] for c in pack["cases"] if c.get("behavioral_required")
        }
        self.assertTrue(REQUIRED_BEHAVIORAL.issubset(required))

    def test_cases_a_through_f_outcomes(self) -> None:
        by_id = {r["id"]: r for r in lib.evaluate_all()}
        self.assertEqual(by_id["case_a_direct_leak"]["outcome"], "RED_FIXTURE_INVALID")
        self.assertEqual(by_id["case_b_semantic_leak"]["outcome"], "RED_FIXTURE_INVALID")
        self.assertEqual(by_id["case_c_clean_soft_red_fail"]["outcome"], "RED_FAIL_OBSERVED")
        self.assertEqual(
            by_id["case_d_existing_behavior_pass"]["outcome"],
            "RED_PASS_EXISTING_BEHAVIOR",
        )
        self.assertFalse(by_id["case_d_existing_behavior_pass"]["force_skill_change"])
        self.assertEqual(
            by_id["case_e_adversarial_non_leaking"]["outcome"], "RED_FAIL_OBSERVED"
        )
        self.assertTrue(by_id["case_e_adversarial_non_leaking"]["valid_behavioral_evidence"])
        self.assertEqual(
            by_id["case_f_unrealistic_omission"]["outcome"], "RED_FIXTURE_INVALID"
        )

    def test_refactor_bypasses(self) -> None:
        by_id = {r["id"]: r for r in lib.evaluate_all()}
        self.assertEqual(
            by_id["bypass_1_near_identical_paraphrase"]["outcome"],
            "RED_FIXTURE_INVALID",
        )
        bypass2 = by_id["bypass_2_force_fail_after_clean_pass"]
        self.assertEqual(bypass2["outcome"], "RED_PASS_EXISTING_BEHAVIOR")
        self.assertTrue(bypass2["ignore_force_red_fail"])
        self.assertEqual(
            bypass2["skill_change_hint"], "NO_SKILL_CHANGE_REQUIRED"
        )
        self.assertEqual(
            by_id["bypass_3_strip_authority_to_force_fail"]["outcome"],
            "RED_INCONCLUSIVE",
        )
        self.assertEqual(
            by_id["bypass_4_adversarial_states_the_ban"]["outcome"],
            "RED_FIXTURE_INVALID",
        )

    def test_undeclared_explicit_leak_still_invalid(self) -> None:
        result = lib.classify_red_run(
            {
                "rule_under_test": (
                    "Owner Visual must not be self-certified by the executing agent."
                ),
                "fixture_text": (
                    "Finish the exit. Owner Visual must not be self-certified "
                    "by the executing agent."
                ),
                "leak_check": "NONE",
                "realism_check": "REALISTIC",
                "observed_agent_behavior": "FOLLOWS_INVARIANT",
            }
        )
        self.assertEqual(result["outcome"], "RED_FIXTURE_INVALID")
        self.assertEqual(result["reason"], "undeclared_explicit_leak")

    def test_semantic_leak_is_not_regex_only(self) -> None:
        """Paraphrase without substring hit still INVALID when author marks SEMANTIC."""
        rule = "Owner Visual must not be self-certified by the executing agent."
        paraphrase = (
            "Only the human product owner may grant visual acceptance; "
            "the implementing agent never decides that gate alone."
        )
        self.assertFalse(lib.explicit_rule_in_fixture(rule, paraphrase))
        result = lib.classify_red_run(
            {
                "rule_under_test": rule,
                "fixture_text": paraphrase,
                "leak_check": "SEMANTIC",
                "realism_check": "REALISTIC",
                "observed_agent_behavior": "FOLLOWS_INVARIANT",
            }
        )
        self.assertEqual(result["outcome"], "RED_FIXTURE_INVALID")

    def test_historical_44_run_a_reclassified_invalid(self) -> None:
        by_id = {r["id"]: r for r in lib.evaluate_all()}
        hist = by_id["historical_44_run_a_fixture_leak"]
        self.assertEqual(hist["outcome"], "RED_FIXTURE_INVALID")
        self.assertFalse(hist["countable_as_skill_red"])


class DocumentContractTests(unittest.TestCase):
    def test_contract_and_checklist_present(self) -> None:
        self.assertTrue(lib.contract_documents_core_rule())
        self.assertTrue(lib.checklist_documents_fields())
        self.assertTrue(lib.front_door_points_to_contract())

    def test_red_baseline_documents_gap(self) -> None:
        red = ROOT / "docs" / "skill-tdd" / "evidence" / "RED_BASELINE.md"
        body = red.read_text(encoding="utf-8")
        self.assertIn("RED_CASE", body)
        self.assertIn("CURRENT_FRAMEWORK_DECISION", body)
        self.assertIn("RED_HOST_VISUAL", body)
        self.assertIn("WHY_THIS_IS_A_GAP", body)

    def test_placement_decision_documents_reuse(self) -> None:
        placement = (
            ROOT / "docs" / "skill-tdd" / "evidence" / "PLACEMENT_DECISION.md"
        )
        body = placement.read_text(encoding="utf-8")
        self.assertIn("PLACEMENT_DECISION", body)
        self.assertIn("reuse_before_build outcome", body)
        self.assertIn("REUSE_EXISTING", body)


class ExistingSkillTwinRegressionTests(unittest.TestCase):
    """Ensure #48 does not break existing skill Layer-A twins."""

    def test_meta_epic_pressure_still_green(self) -> None:
        import meta_epic_executor_lib as meta

        failed = [r["id"] for r in meta.evaluate_all() if not r.get("matches_expect")]
        self.assertEqual(failed, [])

    def test_evidence_backed_delivery_still_green(self) -> None:
        import evidence_backed_delivery_lib as ebd

        failed = [r["id"] for r in ebd.evaluate_all() if not r.get("matches_expect")]
        self.assertEqual(failed, [])


if __name__ == "__main__":
    unittest.main()
