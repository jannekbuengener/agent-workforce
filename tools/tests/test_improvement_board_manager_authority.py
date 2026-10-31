"""Authority separation tests for Improvement Board Manager (#50)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import plugin_skill_routing_lib as lib  # noqa: E402


class ImprovementBoardManagerAuthorityTests(unittest.TestCase):
    def test_valid_pack_includes_board_manager_specialist(self) -> None:
        problems = lib.validate_fixture_valid_pack()
        self.assertEqual(problems, [])
        pack = lib.load_yaml(
            ROOT / "tests" / "fixtures" / "plugin-skill-routing" / "valid_consumers.yml"
        )
        consumer = next(
            item for item in pack["consumers"] if item["id"] == "fixture-improvement-board-manager"
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
        # Observation and management must not collapse into shared_context_evidence alone.
        self.assertNotEqual(
            caps["improvement_management_write"].get("requirement"),
            caps["shared_context_evidence"].get("requirement"),
        )


if __name__ == "__main__":
    unittest.main()
