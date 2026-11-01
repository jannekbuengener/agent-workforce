"""Structural invariants for the XERJ reference-coding gate in reuse-before-build."""

from __future__ import annotations

import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "capabilities" / "REGISTRY.yml"


class ReuseBeforeBuildXerjContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        registry = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
        cls.route = registry["capabilities"]["reuse_before_build"]

    def test_new_feature_planning_and_implementation_trigger_discovery(self) -> None:
        triggers = self.route["triggers"]
        self.assertIn("planning a new feature", triggers)
        self.assertIn("implementing a new feature", triggers)

    def test_xerj_reference_coding_is_mandatory_and_fail_closed(self) -> None:
        gate = self.route["discovery"]["reference_coding"]
        self.assertEqual(gate["provider"], "XERJ")
        self.assertTrue(gate["required"])
        self.assertEqual(gate["unavailable_outcome"], "BLOCKED_TOOL_UNAVAILABLE")
        self.assertFalse(gate["automatic_adoption_authority"])

    def test_xerj_runs_after_local_checks_before_external_or_custom_choice(self) -> None:
        order = self.route["discovery"]["order"]
        xerj_step = "XERJ reference-code search across authorized indexed peer or Hub corpora"
        self.assertLess(order.index("dependencies already used by the target repository"), order.index(xerj_step))
        self.assertLess(order.index(xerj_step), order.index("established language/runtime libraries or packages"))
        self.assertLess(order.index(xerj_step), order.index("custom implementation when prior options are insufficient"))

    def test_reference_coding_receipt_has_bounded_outcomes_and_evidence(self) -> None:
        gate = self.route["discovery"]["reference_coding"]
        self.assertEqual(gate["outcomes"], ["REFERENCE_FOUND", "NO_RELEVANT_REFERENCE"])
        self.assertEqual(
            gate["evidence"],
            [
                "query_or_problem_intent",
                "corpus_or_prefix",
                "pin_or_revision_when_available",
                "license_when_available",
                "file_line_when_reference_found",
                "decision_impact",
            ],
        )

    def test_human_canon_wires_same_gate(self) -> None:
        reuse = (ROOT / "docs" / "REUSE_BEFORE_BUILD.md").read_text(encoding="utf-8")
        routing = (ROOT / "docs" / "CAPABILITY_ROUTING.md").read_text(encoding="utf-8")
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        bootstrap = (ROOT / "WORKFORCE_BOOTSTRAP.md").read_text(encoding="utf-8")
        for text in (reuse, routing, agents, bootstrap):
            self.assertIn("XERJ", text)
        self.assertIn("REFERENCE_FOUND", reuse)
        self.assertIn("NO_RELEVANT_REFERENCE", reuse)
        self.assertIn("BLOCKED_TOOL_UNAVAILABLE", reuse)

    def test_cursor_and_claude_surfaces_wire_the_gate_portably(self) -> None:
        cursor = (ROOT / ".cursor" / "rules" / "xerj-reference-coding.mdc").read_text(
            encoding="utf-8"
        )
        claude = (
            ROOT / ".claude" / "skills" / "xerj-reference-coding" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("alwaysApply: true", cursor)
        for text in (cursor, claude):
            self.assertIn("reuse_before_build", text)
            self.assertIn("BLOCKED_TOOL_UNAVAILABLE", text)
            self.assertNotIn("C:\\Users\\janne", text)


if __name__ == "__main__":
    unittest.main()
