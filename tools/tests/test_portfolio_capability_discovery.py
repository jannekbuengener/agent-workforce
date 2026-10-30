#!/usr/bin/env python3
"""Deterministic tests for repository capability source discovery."""

from __future__ import annotations

import copy
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import portfolio_capability_lib as lib  # noqa: E402


FIXTURES = ROOT / "tests" / "fixtures"


class PortfolioCapabilityDiscoveryTests(unittest.TestCase):
    def test_production_sources_schema_and_no_fixture_topology(self) -> None:
        sources = lib.load_sources()
        problems = lib.validate_sources_schema(sources)
        self.assertEqual(problems, [])
        for key in sources["repositories"]:
            self.assertFalse(str(key).startswith("fixtures/"))
            self.assertNotIn("tests/fixtures", str(key))

    def test_generate_separates_global_and_repository_capabilities(self) -> None:
        index = lib.build_index()
        self.assertTrue(index["generated"])
        self.assertGreaterEqual(len(index["global_capabilities"]), 1)
        self.assertEqual(index["repository_capabilities"], [])
        for row in index["global_capabilities"]:
            self.assertEqual(row["source_type"], "workforce_capability_registry")
            self.assertNotIn("repository", row)
            self.assertEqual(row["authority"], "workforce_routing")
            self.assertIn("requirement", row)

    def test_sample_brain_style_fixture_adapter(self) -> None:
        source = {
            "id": "primary",
            "type": "capability_registry_json",
            "path": "docs/operations/CAPABILITY_REGISTRY.json",
            "discovery": "registry_entries",
            "authority": "local_repo",
            "status": "active",
        }
        rows = lib.collect_rows_from_source(
            repository="fixture/sample-brain-style",
            source=source,
            root=FIXTURES / "sample-brain-style",
        )
        ids = {row.capability_id for row in rows}
        self.assertEqual(
            ids,
            {"fixture-root-cause", "fixture-session-plan", "fixture-external-helper"},
        )
        for row in rows:
            self.assertEqual(row.section, "repository_capabilities")
            self.assertEqual(row.authority, "local_repo")
            self.assertEqual(row.repository, "fixture/sample-brain-style")

    def test_cdb_style_fixture_adapter(self) -> None:
        source = {
            "id": "skills",
            "type": "skill_canon_dir",
            "path": "docs/skills",
            "discovery": "skill_directories",
            "authority": "local_repo",
            "status": "active",
        }
        rows = lib.collect_rows_from_source(
            repository="fixture/cdb-style",
            source=source,
            root=FIXTURES / "cdb-style",
        )
        ids = {row.capability_id for row in rows}
        self.assertEqual(ids, {"fixture-diagnose", "fixture-ship-check"})
        for row in rows:
            self.assertEqual(row.provider_kind, "skill")
            self.assertEqual(row.authority, "local_repo")

    def test_authority_must_be_copied_exactly(self) -> None:
        source = {
            "id": "primary",
            "type": "capability_registry_json",
            "path": "docs/operations/CAPABILITY_REGISTRY.json",
            "discovery": "registry_entries",
            "authority": "local_repo",
            "status": "active",
        }
        rows = lib.collect_rows_from_source(
            repository="fixture/sample-brain-style",
            source=source,
            root=FIXTURES / "sample-brain-style",
        )
        self.assertTrue(rows)
        for row in rows:
            self.assertEqual(row.authority, "local_repo")

        # Entry-level authority from the JSON fixture must not replace source authority.
        registry = json.loads(
            (FIXTURES / "sample-brain-style" / source["path"]).read_text(encoding="utf-8")
        )
        fixture_authorities = {entry["authority"] for entry in registry["capabilities"]}
        self.assertIn("external-example", fixture_authorities)
        self.assertTrue(all(row.authority == source["authority"] for row in rows))

    def test_missing_active_source_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sources = {
                "schema_version": 1,
                "purpose": "test",
                "repositories": {
                    "example/missing": {
                        "portable_identity": "example/missing",
                        "routable": True,
                        "local_authority": {"frontdoor": "README.md"},
                        "capability_sources": [
                            {
                                "id": "primary",
                                "type": "capability_registry_json",
                                "path": "docs/operations/CAPABILITY_REGISTRY.json",
                                "discovery": "registry_entries",
                                "authority": "local_repo",
                                "status": "active",
                            }
                        ],
                    }
                },
            }
            with self.assertRaises(ValueError) as ctx:
                lib.build_index(
                    sources=sources,
                    repo_roots={"example/missing": root},
                )
            self.assertIn("Failed to load", str(ctx.exception))

    def test_unresolvable_root_fails_closed(self) -> None:
        sources = {
            "schema_version": 1,
            "purpose": "test",
            "repositories": {
                "example/other": {
                    "portable_identity": "example/other",
                    "routable": True,
                    "local_authority": {"frontdoor": "README.md"},
                    "capability_sources": [
                        {
                            "id": "primary",
                            "type": "skill_canon_dir",
                            "path": "docs/skills",
                            "discovery": "skill_directories",
                            "authority": "local_repo",
                            "status": "active",
                        }
                    ],
                }
            },
        }
        with self.assertRaises(ValueError) as ctx:
            lib.build_index(sources=sources, repo_roots={})
        self.assertIn("Unresolvable active source root", str(ctx.exception))

    def test_schema_rejects_monitored_relationships_blocked_and_absolute_paths(self) -> None:
        sources = {
            "schema_version": 1,
            "repositories": {
                "example/bad": {
                    "portable_identity": "example/bad",
                    "routable": True,
                    "monitored": True,
                    "relationships": [],
                    "role": "product",
                    "local_authority": {"frontdoor": r"D:\Dev\Workspaces\Repos\x"},
                    "capability_sources": [
                        {
                            "id": "primary",
                            "type": "skill_canon_dir",
                            "path": r"D:\skills",
                            "discovery": "skill_directories",
                            "authority": "local_repo",
                            "status": "blocked",
                        }
                    ],
                }
            },
        }
        problems = lib.validate_sources_schema(sources)
        joined = "\n".join(problems)
        self.assertIn("monitored", joined)
        self.assertIn("relationships", joined)
        self.assertIn("role", joined)
        self.assertIn("absolute", joined.lower())
        self.assertIn("status", joined)

    def test_schema_rejects_fixture_paths_in_production_sources(self) -> None:
        sources = {
            "schema_version": 1,
            "repositories": {
                "example/fixture-leak": {
                    "portable_identity": "example/fixture-leak",
                    "routable": True,
                    "local_authority": {"frontdoor": "README.md"},
                    "capability_sources": [
                        {
                            "id": "primary",
                            "type": "skill_canon_dir",
                            "path": "tests/fixtures/cdb-style/docs/skills",
                            "discovery": "skill_directories",
                            "authority": "local_repo",
                            "status": "active",
                        }
                    ],
                }
            },
        }
        problems = lib.validate_sources_schema(sources)
        self.assertTrue(any("tests/fixtures" in p for p in problems))

    def test_drift_detects_stale_and_hand_edited_index(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            index_path = tmp_path / "PORTFOLIO_CAPABILITY_INDEX.yml"
            good = lib.build_index()
            lib.write_index(good, path=index_path)
            self.assertEqual(
                lib.collect_drift_problems(index_path=index_path),
                [],
            )

            stale = copy.deepcopy(good)
            stale["repository_capabilities"].append(
                {
                    "capability_id": "invented",
                    "intent": "should fail",
                    "provider_kind": "skill",
                    "source_id": "missing",
                    "source_path": "docs/skills",
                    "source_type": "skill_canon_dir",
                    "authority": "local_repo",
                    "repository": "example/invented",
                }
            )
            lib.write_index(stale, path=index_path)
            problems = lib.collect_drift_problems(index_path=index_path)
            self.assertTrue(any("Stale or invented" in p for p in problems))

            elevated = copy.deepcopy(good)
            elevated["global_capabilities"][0]["authority"] = "local_repo"
            lib.write_index(elevated, path=index_path)
            problems = lib.collect_drift_problems(index_path=index_path)
            self.assertTrue(any("Authority drift" in p or "Authority" in p for p in problems))

    def test_repo_root_cli_mapping_for_fixture_repo(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(FIXTURES / "cdb-style" / "docs", root / "docs")
            (root / "README.md").write_text("fixture root\n", encoding="utf-8")
            sources = {
                "schema_version": 1,
                "purpose": "test",
                "repositories": {
                    "example/cdb-like": {
                        "portable_identity": "example/cdb-like",
                        "routable": True,
                        "local_authority": {"frontdoor": "README.md"},
                        "capability_sources": [
                            {
                                "id": "skills",
                                "type": "skill_canon_dir",
                                "path": "docs/skills",
                                "discovery": "skill_directories",
                                "authority": "local_repo",
                                "status": "active",
                            }
                        ],
                    }
                },
            }
            index = lib.build_index(
                sources=sources,
                repo_roots={"example/cdb-like": root},
            )
            self.assertEqual(index["global_capabilities"], [])
            ids = {row["capability_id"] for row in index["repository_capabilities"]}
            self.assertEqual(ids, {"fixture-diagnose", "fixture-ship-check"})

    def test_planned_source_skipped_until_active(self) -> None:
        sources = {
            "schema_version": 1,
            "purpose": "test",
            "repositories": {
                "example/planned": {
                    "portable_identity": "example/planned",
                    "routable": True,
                    "local_authority": {"frontdoor": "README.md"},
                    "capability_sources": [
                        {
                            "id": "skills",
                            "type": "skill_canon_dir",
                            "path": "docs/skills",
                            "discovery": "skill_directories",
                            "authority": "local_repo",
                            "status": "planned",
                        }
                    ],
                }
            },
        }
        index = lib.build_index(sources=sources, repo_roots={})
        self.assertEqual(index["repository_capabilities"], [])
        self.assertEqual(index["global_capabilities"], [])


if __name__ == "__main__":
    unittest.main()
