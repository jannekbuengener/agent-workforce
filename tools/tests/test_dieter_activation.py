"""Activation gate tests for Dieter FOUNDING_SOLO provisioning (#71)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import dieter_activation_lib as activation  # noqa: E402
import knowledge_owner_report_lib as owner_report  # noqa: E402


class DieterActivationTests(unittest.TestCase):
    def test_activation_gate_passes(self) -> None:
        gate = activation.evaluate_activation_gate()
        self.assertTrue(
            gate["passed"],
            msg=f"gate failed: {gate['problems']} checks={gate['checks']}",
        )
        self.assertEqual(gate["outcome"], "GATE_PASS")
        self.assertTrue(gate["may_set_runtime_exists"])

    def test_employee_record_active_founding_solo(self) -> None:
        self.assertTrue(activation.employee_record_is_active_founding_solo())
        self.assertTrue(activation.activation_consistent_with_gate())

    def test_surface_and_consumer_present(self) -> None:
        self.assertTrue(activation.surface_exists())
        ok, problems = activation.consumer_pack_valid()
        self.assertTrue(ok, msg=problems)

    def test_owner_report_still_denied_without_claiming_invented_kpi(self) -> None:
        example = owner_report.build_example_report_from_fixture()
        result = owner_report.validate_report(example)
        self.assertTrue(result["allowed"])


if __name__ == "__main__":
    unittest.main()
