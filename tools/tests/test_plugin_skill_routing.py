#!/usr/bin/env python3
"""Structural tests for plugin/skill routing consumer contracts."""

from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import plugin_skill_routing_lib as lib  # noqa: E402


class PluginSkillRoutingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = lib.load_registry()
        cls.sources = lib.load_sources()
        cls.routing = lib.load_routing()
        cls.valid = lib.load_yaml(lib.FIXTURE_VALID)
        cls.invalid = lib.load_yaml(lib.FIXTURE_INVALID)

    def test_valid_fixture_pack_passes(self) -> None:
        problems = lib.collect_consumer_pack_problems(
            self.valid,
            registry=self.registry,
            sources=self.sources,
            routing=self.routing,
        )
        self.assertEqual(problems, [])

    def test_valid_pack_has_all_regression_case_types(self) -> None:
        cases = self.valid.get("routing_regression_cases") or []
        types = {case["type"] for case in cases}
        self.assertEqual(types, set(lib.ALLOWED_CASE_TYPES))

    def test_production_required_capabilities_have_canonical_providers(self) -> None:
        problems = lib.validate_required_canonical_providers(
            consumers=[], registry=self.registry
        )
        self.assertEqual(problems, [])
        reverse = self.registry["capabilities"]["reverse_engineering"]
        self.assertEqual(reverse["requirement"], "REQUIRED")
        self.assertTrue(lib.has_canonical_provider(reverse))

    def test_invalid_packs_emit_expected_codes(self) -> None:
        packs = self.invalid["packs"]
        for name, pack in packs.items():
            with self.subTest(pack=name):
                registry = pack.get("registry_override") or self.registry
                problems = lib.collect_consumer_pack_problems(
                    pack,
                    registry=registry,
                    sources=self.sources,
                    routing=self.routing,
                )
                codes = lib.problem_codes(problems)
                for expected in pack["expect"]:
                    self.assertIn(expected, codes, problems)

    def test_direct_plugin_coupling_is_structural_not_text_search(self) -> None:
        pack = copy.deepcopy(self.invalid["packs"]["direct_plugin_coupling"])
        problems = lib.collect_consumer_pack_problems(
            pack,
            registry=self.registry,
            sources=self.sources,
            routing=self.routing,
        )
        self.assertIn("DIRECT_PLUGIN_COUPLING", lib.problem_codes(problems))
        # Freitext in intent must not create coupling findings.
        self.assertTrue(
            all("Reverse Engineering Orchestrator" not in p or "id" in p for p in problems)
        )

    def test_cycle_detection_requires_structured_edges(self) -> None:
        pack = copy.deepcopy(self.valid)
        pack["capability_dependency_edges"] = []
        problems = lib.collect_consumer_pack_problems(
            pack,
            registry=self.registry,
            sources=self.sources,
            routing=self.routing,
        )
        self.assertNotIn("CYCLIC_DEPENDENCY", lib.problem_codes(problems))

        pack["capability_dependency_edges"] = [
            {"from": "reverse_engineering", "to": "shared_context_evidence"},
            {"from": "shared_context_evidence", "to": "reverse_engineering"},
        ]
        problems = lib.collect_consumer_pack_problems(
            pack,
            registry=self.registry,
            sources=self.sources,
            routing=self.routing,
        )
        self.assertIn("CYCLIC_DEPENDENCY", lib.problem_codes(problems))

    def test_competing_global_ownership_uses_exact_owns_overlap(self) -> None:
        pack = copy.deepcopy(self.invalid["packs"]["competing_global_ownership"])
        pack["consumers"][1]["owns"] = ["different-exclusive-scope"]
        problems = lib.collect_consumer_pack_problems(
            pack,
            registry=self.registry,
            sources=self.sources,
            routing=self.routing,
        )
        self.assertNotIn("COMPETING_GLOBAL_OWNERSHIP", lib.problem_codes(problems))

    def test_specialist_overreach_uses_claims_global_routing_field(self) -> None:
        pack = copy.deepcopy(self.invalid["packs"]["specialist_overreach"])
        pack["consumers"][0]["claims_global_routing"] = False
        problems = lib.collect_consumer_pack_problems(
            pack,
            registry=self.registry,
            sources=self.sources,
            routing=self.routing,
        )
        self.assertNotIn("SPECIALIST_OVERREACH", lib.problem_codes(problems))

    def test_repo_duplication_is_forbidden_field_only(self) -> None:
        pack = copy.deepcopy(self.valid)
        pack["consumers"][0]["notes"] = (
            "Mentions sample-brain-control-orchestrator only in prose"
        )
        problems = lib.collect_consumer_pack_problems(
            pack,
            registry=self.registry,
            sources=self.sources,
            routing=self.routing,
        )
        self.assertNotIn("REPO_CAPABILITY_DUPLICATION", lib.problem_codes(problems))

    def test_missing_source_pointer_with_known_source_passes(self) -> None:
        pack = copy.deepcopy(self.valid)
        pack["consumers"][2]["repository_provider"] = "jannekbuengener/sample-brain"
        problems = lib.collect_consumer_pack_problems(
            pack,
            registry=self.registry,
            sources=self.sources,
            routing=self.routing,
        )
        self.assertNotIn("MISSING_SOURCE_POINTER", lib.problem_codes(problems))

    def test_cli_check_passes_on_production_and_valid_fixture(self) -> None:
        import check_plugin_skill_routing as cli

        self.assertEqual(cli.main([]), 0)


if __name__ == "__main__":
    unittest.main()
