"""End-to-end pilot verification for Dieter FOUNDING_SOLO (#74)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import dieter_founding_solo_pilot_lib as pilot  # noqa: E402
import knowledge_owner_report_lib as owner_report  # noqa: E402


class DieterFoundingSoloPilotTests(unittest.TestCase):
    def test_pilot_proven(self) -> None:
        result = pilot.evaluate_pilot()
        self.assertTrue(result["passed"], msg=result)
        self.assertEqual(result["outcome"], "DIETER_FOUNDING_SOLO_PILOT_PROVEN")

    def test_owner_report_human_renderable(self) -> None:
        report = pilot.load_yaml(pilot.OWNER_REPORT_PATH)
        human = owner_report.render_human_report(report)
        self.assertIn("Was ist passiert?", human)
        self.assertIn(owner_report.UNQUANTIFIABLE, human)
        self.assertIn("Unsicherheiten", human)


if __name__ == "__main__":
    unittest.main()
