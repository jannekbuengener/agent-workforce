"""Layer A contract tests + structural skill/consumer checks for #41."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import meta_epic_executor_lib as lib  # noqa: E402
import plugin_skill_routing_lib as routing  # noqa: E402
import yaml  # noqa: E402


class PressureCaseContractTests(unittest.TestCase):
    def test_all_pressure_cases_match_expect(self) -> None:
        results = lib.evaluate_all()
        self.assertGreaterEqual(len(results), 10)
        failed = [r["id"] for r in results if not r.get("matches_expect")]
        self.assertEqual(failed, [], msg=f"mismatched cases: {results}")

    def test_behavioral_required_cases_are_marked(self) -> None:
        pack = lib.load_pressure_cases()
        required = {
            c["id"] for c in pack["cases"] if c.get("behavioral_required")
        }
        self.assertTrue(
            {
                "plan_before_write",
                "false_parallelism",
                "evidence_over_self_claim",
                "replanning",
                "hierarchical_goal_gates",
                "learning_loop",
            }.issubset(required)
        )

    def test_stale_child_actionable_only_open(self) -> None:
        pack = lib.load_pressure_cases()
        case = next(c for c in pack["cases"] if c["id"] == "stale_child_state")
        result = lib.evaluate_case(case)
        self.assertEqual(result["actionable_children"], ["c5", "c7"])

    def test_plan_before_write_blocks_mutation(self) -> None:
        case = {
            "id": "plan_before_write",
            "input": {
                "authority_read": False,
                "plan_artifact": False,
                "mutation_attempted": True,
            },
            "expect": {
                "allow_mutation": False,
                "gate": "STEP_REWORK",
                "required_before_mutation": ["authority_read", "plan_artifact"],
            },
        }
        result = lib.evaluate_case(case)
        self.assertTrue(result["matches_expect"])
        self.assertFalse(result["allow_mutation"])


class SkillDocumentTests(unittest.TestCase):
    def test_skill_md_encodes_material_step_gate(self) -> None:
        self.assertTrue(lib.skill_mandates_material_step_gate())

    def test_skill_description_excludes_small_tasks(self) -> None:
        text = lib.SKILL_MD.read_text(encoding="utf-8")
        self.assertIn("Do not use for a small single-change bug/fix", text)
        self.assertIn("name: cursor-meta-epic-executor", text)

    def test_red_baseline_documents_observed_fail(self) -> None:
        red = (
            ROOT
            / "docs"
            / "skills"
            / "cursor-meta-epic-executor"
            / "evidence"
            / "RED_BASELINE.md"
        )
        body = red.read_text(encoding="utf-8")
        self.assertIn("RED_FAIL_OBSERVED", body)
        self.assertIn("CONTRACT.md", body)
        self.assertIn("LIVE_BOARD", body)


class ConsumerPackTests(unittest.TestCase):
    def test_skill_colocated_consumer_validates(self) -> None:
        pack = yaml.safe_load(lib.CONSUMER_YML.read_text(encoding="utf-8"))
        problems = routing.collect_consumer_pack_problems(
            pack,
            registry=routing.load_registry(),
            sources=routing.load_sources(),
            routing=routing.load_routing(),
        )
        self.assertEqual(problems, [])


if __name__ == "__main__":
    unittest.main()
