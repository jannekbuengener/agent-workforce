"""Authority separation tests for Improvement Board Manager (#50)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import improvement_board_authority_lib as authority  # noqa: E402
import plugin_skill_routing_lib as lib  # noqa: E402


REQUIRED_BEHAVIORAL = {
    "denied_scout_management_write",
    "denied_ambiguous_routing",
    "denied_specialist_overreach",
    "allowed_board_manager_management",
    "denied_imaginary_dieter_approval_while_planned_only",
}


class ImprovementBoardManagerAuthorityTests(unittest.TestCase):
    def test_valid_pack_includes_board_manager_specialist(self) -> None:
        problems = lib.validate_fixture_valid_pack()
        self.assertEqual(problems, [])
        pack = lib.load_yaml(
            ROOT / "tests" / "fixtures" / "plugin-skill-routing" / "valid_consumers.yml"
        )
        consumer = next(
            item
            for item in pack["consumers"]
            if item["id"] == "fixture-improvement-board-manager"
        )
        self.assertEqual(consumer["kind"], "specialist")
        self.assertFalse(consumer["claims_global_routing"])
        required = {item["id"] for item in consumer["requires_capabilities"]}
        self.assertEqual(
            required,
            {"improvement_management_write", "improvement_github_issue_create"},
        )
        self.assertNotIn("shared_context_evidence", required)

    def test_denied_scout_write_overreach_is_structural(self) -> None:
        packs = lib.load_yaml(
            ROOT / "tests" / "fixtures" / "plugin-skill-routing" / "invalid_cases.yml"
        )
        pack = packs["packs"]["scout_management_overreach"]
        problems = lib.collect_consumer_pack_problems(
            {"consumers": pack["consumers"], "capability_dependency_edges": []},
            registry=lib.load_registry(),
            sources=lib.load_sources(),
            routing=lib.load_routing(),
        )
        self.assertIn("SPECIALIST_OVERREACH", lib.problem_codes(problems))

    def test_board_manager_overreach_fixture_emits_code(self) -> None:
        packs = lib.load_yaml(
            ROOT / "tests" / "fixtures" / "plugin-skill-routing" / "invalid_cases.yml"
        )
        pack = packs["packs"]["board_manager_specialist_overreach"]
        problems = lib.collect_consumer_pack_problems(
            {"consumers": pack["consumers"], "capability_dependency_edges": []},
            registry=lib.load_registry(),
            sources=lib.load_sources(),
            routing=lib.load_routing(),
        )
        self.assertIn("SPECIALIST_OVERREACH", lib.problem_codes(problems))

    def test_registry_separates_observation_management_and_github_create(self) -> None:
        registry = lib.load_registry()
        caps = registry["capabilities"]
        for capability_id in (
            "improvement_read",
            "improvement_observation_write",
            "improvement_management_write",
            "improvement_github_issue_create",
        ):
            self.assertIn(capability_id, caps)
        self.assertEqual(
            caps["improvement_github_issue_create"].get("contract"),
            "docs/IMPROVEMENT_GITHUB_ISSUE_CREATE.md",
        )
        self.assertNotEqual(
            caps["improvement_management_write"].get("requirement"),
            caps["shared_context_evidence"].get("requirement"),
        )
        self.assertFalse(
            (caps["improvement_management_write"].get("availability") or {}).get(
                "silent_substitution"
            )
        )


class ImprovementBoardPressureCaseTests(unittest.TestCase):
    def test_all_pressure_cases_match_expect(self) -> None:
        results = authority.evaluate_all()
        self.assertGreaterEqual(len(results), 8)
        failed = [r["id"] for r in results if not r.get("matches_expect")]
        self.assertEqual(failed, [], msg=f"mismatched cases: {results}")

    def test_behavioral_required_cases_present(self) -> None:
        pack = authority.load_pressure_cases()
        required = {c["id"] for c in pack["cases"] if c.get("behavioral_required")}
        self.assertTrue(REQUIRED_BEHAVIORAL.issubset(required))

    def test_denied_scout_write(self) -> None:
        pack = authority.load_pressure_cases()
        case = next(
            c for c in pack["cases"] if c["id"] == "denied_scout_management_write"
        )
        result = authority.evaluate_case(case, pack=pack)
        self.assertTrue(result["matches_expect"])
        self.assertFalse(result["allowed"])
        self.assertEqual(result["gate"], "SCOUT_WRITE_DENIED")

    def test_denied_ambiguous_routing(self) -> None:
        pack = authority.load_pressure_cases()
        case = next(c for c in pack["cases"] if c["id"] == "denied_ambiguous_routing")
        result = authority.evaluate_case(case, pack=pack)
        self.assertTrue(result["matches_expect"])
        self.assertFalse(result["allowed"])
        self.assertEqual(result["outcome"], "HOLD")
        self.assertEqual(result["gate"], "HOLD_OWNER_AMBIGUOUS")

    def test_denied_specialist_overreach(self) -> None:
        pack = authority.load_pressure_cases()
        case = next(
            c for c in pack["cases"] if c["id"] == "denied_specialist_overreach"
        )
        result = authority.evaluate_case(case, pack=pack)
        self.assertTrue(result["matches_expect"])
        self.assertEqual(result["gate"], "SPECIALIST_OVERREACH")

    def test_allowed_board_manager_management(self) -> None:
        pack = authority.load_pressure_cases()
        case = next(
            c for c in pack["cases"] if c["id"] == "allowed_board_manager_management"
        )
        result = authority.evaluate_case(case, pack=pack)
        self.assertTrue(result["matches_expect"])
        self.assertTrue(result["allowed"])
        self.assertEqual(result["outcome"], "MANAGEMENT_APPLIED")

    def test_github_issue_create_deferred_without_contract(self) -> None:
        pack = authority.load_pressure_cases()
        case = next(
            c
            for c in pack["cases"]
            if c["id"] == "github_issue_create_requires_separate_contract"
        )
        result = authority.evaluate_case(case, pack=pack)
        self.assertTrue(result["matches_expect"])
        self.assertEqual(result["gate"], "GITHUB_ISSUE_CREATE_DEFERRED")

    def test_canon_and_scouts_unchanged(self) -> None:
        self.assertTrue(authority.registry_encodes_improvement_capabilities())
        self.assertTrue(authority.policy_encodes_board_manager())
        self.assertTrue(authority.scouts_remain_advisory_unchanged())

    def test_denied_imaginary_dieter_approval_while_planned_only(self) -> None:
        pack = authority.load_pressure_cases()
        case = next(
            c
            for c in pack["cases"]
            if c["id"] == "denied_imaginary_dieter_approval_while_planned_only"
        )
        result = authority.evaluate_case(case, pack=pack)
        self.assertTrue(result["matches_expect"])
        self.assertFalse(result["allowed"])
        self.assertEqual(result["gate"], "IMAGINARY_MANAGER_APPROVAL")

    def test_board_manager_operable_without_dieter_while_planned(self) -> None:
        pack = authority.load_pressure_cases()
        case = next(
            c
            for c in pack["cases"]
            if c["id"] == "allowed_board_manager_without_dieter_approval_while_planned"
        )
        result = authority.evaluate_case(case, pack=pack)
        self.assertTrue(result["matches_expect"])
        self.assertTrue(result["allowed"])


if __name__ == "__main__":
    unittest.main()
