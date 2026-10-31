"""Owner report contract tests for Head of Knowledge (#73)."""

from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import knowledge_owner_report_lib as report  # noqa: E402


class KnowledgeOwnerReportTests(unittest.TestCase):
    def test_contract_complete_and_wired(self) -> None:
        self.assertTrue(report.contract_is_complete())
        self.assertTrue(report.employee_binds_report_contract())
        self.assertTrue(report.registry_points_at_contract())

    def test_example_report_from_fixture_is_valid(self) -> None:
        example = report.build_example_report_from_fixture()
        result = report.validate_report(example)
        self.assertTrue(result["allowed"], msg=result)
        self.assertEqual(result["outcome"], "REPORT_VALID")
        human = report.render_human_report(example)
        self.assertIn("Was ist passiert?", human)
        self.assertIn(report.UNQUANTIFIABLE, human)

    def test_invented_percentage_denied(self) -> None:
        example = report.build_example_report_from_fixture()
        bad = copy.deepcopy(example)
        bad["sections"]["current_data_quality_situation"] = {
            "summary": "92 % – gut",
            "quantifiable": True,
            "percentage": 92,
            "method_id": None,
            "band": "gut",
        }
        result = report.validate_report(bad)
        self.assertFalse(result["allowed"])
        self.assertEqual(result["gate"], "INVENTED_QUALITY_KPI")

    def test_runtime_not_provisioned_denied(self) -> None:
        example = report.build_example_report_from_fixture()
        result = report.validate_report(
            example,
            employment_state="PLANNED_ONLY",
            runtime_exists=False,
        )
        self.assertFalse(result["allowed"])
        self.assertEqual(result["gate"], "RUNTIME_NOT_PROVISIONED")

    def test_immediate_escalation_flag_denied(self) -> None:
        example = report.build_example_report_from_fixture()
        bad = copy.deepcopy(example)
        bad["immediate_escalation_included"] = True
        result = report.validate_report(bad)
        self.assertFalse(result["allowed"])
        self.assertIn(
            "immediate escalation must stay out of weekly report",
            result["problems"],
        )

    def test_missing_section_denied(self) -> None:
        example = report.build_example_report_from_fixture()
        bad = copy.deepcopy(example)
        del bad["sections"]["what_was_decided"]
        result = report.validate_report(bad)
        self.assertFalse(result["allowed"])
        self.assertEqual(result["gate"], "SCHEMA_INVALID")


if __name__ == "__main__":
    unittest.main()
