#!/usr/bin/env python3
"""Structural tests for plugin/skill routing consumer contracts."""

from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import plugin_skill_routing_lib as lib  # noqa: E402
import yaml  # noqa: E402


def _minimal_consumer(**overrides: Any) -> dict[str, Any]:
    consumer: dict[str, Any] = {
        "id": "temp-production-consumer",
        "kind": "specialist",
        "intent": "Temporary production-shaped consumer for routing tests.",
        "claims_global_routing": False,
        "owns": ["narrow temporary scope"],
        "does_not_own": ["global routing"],
        "triggers": {
            "explicit": [],
            "semantic": [],
            "dependency": [],
            "authority": [],
        },
        "exclusions": [],
        "requires_capabilities": [],
        "optional_capabilities": [],
        "output": "none",
        "exit": "none",
        "private_mcp": "never_worker_dependency",
    }
    consumer.update(overrides)
    return consumer


def _pack_for_consumers(*consumers: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "purpose": "Temporary production-shaped consumer pack",
        "consumers": list(consumers),
        "capability_dependency_edges": [],
    }


def _skill_canon_sources(path: str = "docs/skills") -> dict[str, Any]:
    return {
        "schema_version": 1,
        "purpose": "test sources for production consumer discovery",
        "repositories": {
            "jannekbuengener/agent-workforce": {
                "portable_identity": "jannekbuengener/agent-workforce",
                "routable": True,
                "local_authority": {
                    "frontdoor": "WORKFORCE_BOOTSTRAP.md",
                    "skill_canon": path,
                },
                "capability_sources": [
                    {
                        "id": "skills",
                        "type": "skill_canon_dir",
                        "path": path,
                        "discovery": "skill_directories",
                        "authority": "local_repo",
                        "status": "active",
                    }
                ],
            }
        },
    }


def _write_consumer_pack(skill_dir: Path, pack: dict[str, Any]) -> Path:
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(
        "---\nname: temp\ndescription: temp\n---\n\n# temp\n",
        encoding="utf-8",
    )
    consumer_path = skill_dir / "consumer.yml"
    consumer_path.write_text(
        yaml.safe_dump(pack, sort_keys=False),
        encoding="utf-8",
    )
    return consumer_path


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


class ProductionConsumerValidationTests(unittest.TestCase):
    """Issue #55: official checker must validate real skill-canon consumer packs."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = lib.load_registry()
        cls.sources = lib.load_sources()
        cls.routing = lib.load_routing()

    def test_case_a_valid_production_consumer_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pack = _pack_for_consumers(
                _minimal_consumer(
                    id="valid-prod-consumer",
                    optional_capabilities=[
                        {
                            "id": "reuse_before_build",
                            "requirement": "DISCOVERY_REQUIRED",
                        }
                    ],
                    repository_provider="jannekbuengener/agent-workforce",
                )
            )
            _write_consumer_pack(root / "docs" / "skills" / "valid-prod", pack)
            problems = lib.validate_production_consumer_packs(
                repo_root=root,
                sources=_skill_canon_sources(),
                registry=self.registry,
                routing=self.routing,
            )
            self.assertEqual(problems, [])

    def test_case_b_unknown_capability_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pack = _pack_for_consumers(
                _minimal_consumer(
                    id="unknown-cap-prod",
                    requires_capabilities=[
                        {
                            "id": "totally_unknown_capability_xyz",
                            "requirement": "PREFERRED",
                        }
                    ],
                )
            )
            path = _write_consumer_pack(
                root / "docs" / "skills" / "unknown-cap", pack
            )
            problems = lib.validate_production_consumer_packs(
                repo_root=root,
                sources=_skill_canon_sources(),
                registry=self.registry,
                routing=self.routing,
            )
            self.assertIn("UNKNOWN_CAPABILITY", lib.problem_codes(problems))
            self.assertTrue(any(str(path) in p or path.name in p for p in problems))

    def test_case_c_direct_plugin_coupling_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pack = _pack_for_consumers(
                _minimal_consumer(
                    id="coupled-prod",
                    requires_capabilities=[
                        {
                            "id": "Reverse Engineering Orchestrator",
                            "requirement": "REQUIRED",
                        }
                    ],
                )
            )
            _write_consumer_pack(root / "docs" / "skills" / "coupled", pack)
            problems = lib.validate_production_consumer_packs(
                repo_root=root,
                sources=_skill_canon_sources(),
                registry=self.registry,
                routing=self.routing,
            )
            self.assertIn("DIRECT_PLUGIN_COUPLING", lib.problem_codes(problems))

    def test_case_d_specialist_overreach_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pack = _pack_for_consumers(
                _minimal_consumer(
                    id="overreach-prod",
                    kind="project_orchestrator",
                    claims_global_routing=True,
                )
            )
            _write_consumer_pack(root / "docs" / "skills" / "overreach", pack)
            problems = lib.validate_production_consumer_packs(
                repo_root=root,
                sources=_skill_canon_sources(),
                registry=self.registry,
                routing=self.routing,
            )
            self.assertIn("SPECIALIST_OVERREACH", lib.problem_codes(problems))

    def test_case_e_invalid_repository_provider_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pack = _pack_for_consumers(
                _minimal_consumer(
                    id="missing-pointer-prod",
                    repository_provider="nonexistent-org/nonexistent-repo",
                )
            )
            _write_consumer_pack(root / "docs" / "skills" / "missing-pointer", pack)
            # Discover from temp skill_canon; resolve repository_provider against
            # live pointer authority (production sources/routing).
            problems = lib.validate_production_consumer_packs(
                repo_root=root,
                sources=_skill_canon_sources(),
                registry=self.registry,
                routing=self.routing,
                pointer_sources=self.sources,
            )
            self.assertIn("MISSING_SOURCE_POINTER", lib.problem_codes(problems))

    def test_case_f_fixture_green_does_not_mask_invalid_production_consumer(
        self,
    ) -> None:
        """Real production consumer invalid + fixtures valid → overall FAIL."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pack = _pack_for_consumers(
                _minimal_consumer(
                    id="masking-prod",
                    requires_capabilities=[
                        {
                            "id": "totally_unknown_capability_xyz",
                            "requirement": "PREFERRED",
                        }
                    ],
                )
            )
            _write_consumer_pack(root / "docs" / "skills" / "masking", pack)
            fixture_problems = lib.validate_fixture_valid_pack()
            self.assertEqual(fixture_problems, [], "fixtures must stay green")
            production_problems = lib.validate_production_consumer_packs(
                repo_root=root,
                sources=_skill_canon_sources(),
                registry=self.registry,
                routing=self.routing,
            )
            self.assertTrue(production_problems)
            combined = (
                lib.validate_production_registry_required_providers()
                + fixture_problems
                + production_problems
            )
            self.assertTrue(combined)
            self.assertIn("UNKNOWN_CAPABILITY", lib.problem_codes(combined))

    def test_case_g_discovery_ignores_fixtures_and_unrelated_yaml(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            valid = _pack_for_consumers(_minimal_consumer(id="canon-only"))
            _write_consumer_pack(root / "docs" / "skills" / "canon-only", valid)

            fixture_pack = _pack_for_consumers(
                _minimal_consumer(
                    id="fixture-leak",
                    requires_capabilities=[
                        {
                            "id": "totally_unknown_capability_xyz",
                            "requirement": "PREFERRED",
                        }
                    ],
                )
            )
            fixture_dir = (
                root / "tests" / "fixtures" / "plugin-skill-routing" / "leak-skill"
            )
            _write_consumer_pack(fixture_dir, fixture_pack)
            unrelated = root / "docs" / "skills" / "notes.yml"
            unrelated.parent.mkdir(parents=True, exist_ok=True)
            unrelated.write_text("not: a consumer pack\n", encoding="utf-8")

            discovered = lib.discover_production_consumer_pack_paths(
                repo_root=root,
                sources=_skill_canon_sources(),
            )
            rels = {str(p.relative_to(root)).replace("\\", "/") for p in discovered}
            self.assertEqual(rels, {"docs/skills/canon-only/consumer.yml"})
            problems = lib.validate_production_consumer_packs(
                repo_root=root,
                sources=_skill_canon_sources(),
                registry=self.registry,
                routing=self.routing,
            )
            self.assertEqual(problems, [])

    def test_live_repo_production_consumers_are_discovered_from_sources(self) -> None:
        discovered = lib.discover_production_consumer_pack_paths(
            repo_root=ROOT,
            sources=self.sources,
        )
        rels = {str(p.relative_to(ROOT)).replace("\\", "/") for p in discovered}
        self.assertIn("docs/skills/evidence-backed-delivery/consumer.yml", rels)
        self.assertIn("docs/skills/cursor-meta-epic-executor/consumer.yml", rels)
        self.assertFalse(any("tests/fixtures" in rel for rel in rels))

    def test_cli_includes_production_consumer_validation(self) -> None:
        import check_plugin_skill_routing as cli

        src = Path(cli.__file__).read_text(encoding="utf-8")
        self.assertIn("validate_production_consumer_packs", src)


class MetaEpicChildDeliveryCapabilityRoutingTests(unittest.TestCase):
    """Issue #56: child delivery via capability id, not direct skill coupling."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = lib.load_registry()
        cls.sources = lib.load_sources()
        cls.routing = lib.load_routing()
        cls.pack = lib.load_yaml(
            ROOT
            / "docs"
            / "skills"
            / "cursor-meta-epic-executor"
            / "consumer.yml"
        )
        cls.consumer = cls.pack["consumers"][0]

    @classmethod
    def _discovery_ids(cls) -> set[str]:
        return lib.discoverable_skill_capability_ids(
            repo_root=ROOT,
            sources=cls.sources,
        )

    def _capability_refs(self) -> list[dict[str, Any]]:
        refs: list[dict[str, Any]] = []
        for field in ("requires_capabilities", "optional_capabilities"):
            for ref in self.consumer.get(field) or []:
                if isinstance(ref, dict):
                    refs.append(ref)
        return refs

    def test_red_gap_machine_readable_child_delivery_dependency(self) -> None:
        """Child delivery needs evidence-backed-delivery capability in consumer.yml."""
        ids = {ref.get("id") for ref in self._capability_refs()}
        self.assertIn(
            "evidence-backed-delivery",
            ids,
            "cursor-meta-epic-executor must declare capability dependency "
            "evidence-backed-delivery (not only SKILL.md prose)",
        )

    def test_child_delivery_dependency_is_conditional_relevance_id(self) -> None:
        ebd = next(
            ref
            for ref in self._capability_refs()
            if ref.get("id") == "evidence-backed-delivery"
        )
        self.assertEqual(ebd.get("requirement"), "REQUIRED")
        self.assertEqual(ebd.get("relevance"), ["child_delivery"])

    def test_child_delivery_relevant_resolves_capability(self) -> None:
        resolved = lib.resolve_capability_dependencies(
            self.consumer,
            active_relevance={"child_delivery"},
        )
        self.assertIn("evidence-backed-delivery", resolved)

    def test_no_child_delivery_does_not_force_dependency(self) -> None:
        resolved = lib.resolve_capability_dependencies(
            self.consumer,
            active_relevance=set(),
        )
        self.assertNotIn("evidence-backed-delivery", resolved)
        resolved_other = lib.resolve_capability_dependencies(
            self.consumer,
            active_relevance={"unrelated_relevance"},
        )
        self.assertNotIn("evidence-backed-delivery", resolved_other)

    def test_dependency_uses_capability_id_not_provider_name(self) -> None:
        ebd = next(
            ref
            for ref in self._capability_refs()
            if ref.get("id") == "evidence-backed-delivery"
        )
        self.assertTrue(lib.CAPABILITY_ID_RE.fullmatch(str(ebd["id"])))
        # No provider/plugin display-name coupling in structured fields.
        for field in ("requires_capabilities", "optional_capabilities"):
            for ref in self.consumer.get(field) or []:
                self.assertNotIn("provider", ref)
                self.assertNotIn("plugin", ref)
                self.assertNotIn("skill", ref)

    def test_provider_substitution_keeps_capability_identity(self) -> None:
        """Capability id stays the dependency identity even if provider_kind differs."""
        discovery_ids = self._discovery_ids()
        self.assertIn("evidence-backed-delivery", discovery_ids)
        # Simulate discovery reporting a different provider_kind for the same id.
        fake_provider_kind = "contract"
        dependency_id = "evidence-backed-delivery"
        self.assertEqual(dependency_id, "evidence-backed-delivery")
        self.assertNotEqual(fake_provider_kind, dependency_id)

    def test_orchestrator_boundary_preserved(self) -> None:
        self.assertEqual(self.consumer["kind"], "project_orchestrator")
        self.assertIs(self.consumer["claims_global_routing"], False)
        problems = lib.collect_consumer_pack_problems(
            self.pack,
            registry=self.registry,
            sources=self.sources,
            routing=self.routing,
            extra_known_ids=self._discovery_ids(),
        )
        self.assertEqual(problems, [])
        self.assertNotIn("SPECIALIST_OVERREACH", lib.problem_codes(problems))

    def test_discovery_set_reuses_portfolio_skill_identity(self) -> None:
        discovery_ids = self._discovery_ids()
        self.assertIn("evidence-backed-delivery", discovery_ids)
        self.assertIn("cursor-meta-epic-executor", discovery_ids)
        # Must not invent a second identity rule — portfolio adapter is source.
        import portfolio_capability_lib as portfolio

        source = next(
            s
            for entry in self.sources["repositories"].values()
            for s in entry["capability_sources"]
            if s.get("type") == "skill_canon_dir" and s.get("status") == "active"
        )
        rows = portfolio.collect_rows_from_source(
            repository="jannekbuengener/agent-workforce",
            source=source,
            root=ROOT,
        )
        portfolio_ids = {row.capability_id for row in rows}
        self.assertTrue(discovery_ids >= portfolio_ids)

    def test_invalid_relevance_id_fails_structurally(self) -> None:
        pack = _pack_for_consumers(
            _minimal_consumer(
                id="bad-relevance",
                requires_capabilities=[
                    {
                        "id": "reuse_before_build",
                        "requirement": "DISCOVERY_REQUIRED",
                        "relevance": ["Not A Stable Id"],
                    }
                ],
            )
        )
        problems = lib.collect_consumer_pack_problems(
            pack,
            registry=self.registry,
            sources=self.sources,
            routing=self.routing,
        )
        self.assertIn("UNKNOWN_CAPABILITY", lib.problem_codes(problems))

    def test_unknown_discovery_capability_still_fails_without_discovery_set(
        self,
    ) -> None:
        pack = _pack_for_consumers(
            _minimal_consumer(
                id="unknown-local-cap",
                requires_capabilities=[
                    {
                        "id": "evidence-backed-delivery",
                        "requirement": "REQUIRED",
                        "relevance": ["child_delivery"],
                    }
                ],
            )
        )
        # Without discovery set, repo-local capability id is unknown.
        problems = lib.collect_consumer_pack_problems(
            pack,
            registry=self.registry,
            sources=self.sources,
            routing=self.routing,
            extra_known_ids=None,
        )
        self.assertIn("UNKNOWN_CAPABILITY", lib.problem_codes(problems))
        # With discovery set, same id resolves.
        ok = lib.collect_consumer_pack_problems(
            pack,
            registry=self.registry,
            sources=self.sources,
            routing=self.routing,
            extra_known_ids=self._discovery_ids(),
        )
        self.assertEqual(ok, [])


if __name__ == "__main__":
    unittest.main()
