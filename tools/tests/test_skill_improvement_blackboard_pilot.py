"""Layer-A tests for Skill Improvement Blackboard V1 pilot (#52)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import skill_improvement_blackboard_pilot_lib as pilot  # noqa: E402


class SkillImprovementBlackboardPilotTests(unittest.TestCase):
    def test_layer_a_pilot_pass(self) -> None:
        report = pilot.run_layer_a_pilot()
        self.assertEqual(report["exit_id"], pilot.EXIT_ID)
        self.assertFalse(report["mutable_workforce_db"])
        self.assertEqual(report["reuse_before_build"], "REUSE_EXISTING + BUILD_THIN")
        self.assertEqual(report["board_authority_failed"], [])
        self.assertEqual(report["github_create_failed"], [])
        self.assertTrue(report["authority_separation"]["ok"])
        self.assertTrue(report["layer_a_pass"])
        self.assertTrue(report["contract_active"])
        self.assertTrue(report["registry_active"])
        self.assertTrue(report["scouts_remain_denied"])


if __name__ == "__main__":
    unittest.main()
