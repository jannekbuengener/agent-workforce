#!/usr/bin/env python3
"""Structural tests for the ChatGPT Workflows backoffice export bundle."""

from __future__ import annotations

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

import chatgpt_workflows_backoffice_lib as lib  # noqa: E402


class ChatgptWorkflowsBackofficeTests(unittest.TestCase):
    def test_production_bundle_passes(self) -> None:
        problems = lib.validate_bundle()
        self.assertEqual(problems, [])

    def test_manifest_does_not_hash_itself(self) -> None:
        manifest = lib.load_manifest()
        paths = [entry["path"] for entry in manifest["files"]]
        self.assertNotIn(lib.MANIFEST_NAME, paths)
        self.assertEqual(set(paths), set(lib.EXPECTED_DOCS))

    def test_source_canon_semantics_are_documented(self) -> None:
        semantics = lib.load_manifest()["source"]["source_canon_commit_semantics"]
        self.assertIn("Not the SHA of a commit that contains", semantics)

    def test_negating_gpt_mcp_identity_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bundle = Path(tmp) / "bundle"
            shutil.copytree(lib.BUNDLE_DIR, bundle)
            core = bundle / "01_PROJECT_CORE.md"
            core.write_text(
                core.read_text(encoding="utf-8")
                + "\nThis project is not gpt-mcp-server.\n",
                encoding="utf-8",
                newline="\n",
            )
            manifest = lib.build_manifest(
                source_canon_commit=lib.load_manifest()["source"]["source_canon_commit"],
                validated_at="2026-10-30",
                bundle_dir=bundle,
            )
            lib.write_manifest(manifest, bundle_dir=bundle)
            problems = lib.validate_bundle(bundle_dir=bundle)
            self.assertEqual(problems, [])

    def test_explicit_legacy_mission_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bundle = Path(tmp) / "bundle"
            shutil.copytree(lib.BUNDLE_DIR, bundle)
            instructions = bundle / "03_CHATGPT_PROJECT_INSTRUCTIONS.md"
            instructions.write_text(
                "You are the operational lead for jannekbuengener/gpt-mcp-server.\n",
                encoding="utf-8",
                newline="\n",
            )
            manifest = lib.build_manifest(
                source_canon_commit=lib.load_manifest()["source"]["source_canon_commit"],
                validated_at="2026-10-30",
                bundle_dir=bundle,
            )
            lib.write_manifest(manifest, bundle_dir=bundle)
            problems = lib.validate_bundle(bundle_dir=bundle)
            self.assertTrue(
                any("legacy_gpt_mcp_mission" in problem for problem in problems),
                problems,
            )

    def test_absolute_windows_path_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bundle = Path(tmp) / "bundle"
            shutil.copytree(lib.BUNDLE_DIR, bundle)
            core = bundle / "01_PROJECT_CORE.md"
            core.write_text(
                core.read_text(encoding="utf-8") + "\nPath: D:\\Dev\\Workspaces\\x\n",
                encoding="utf-8",
                newline="\n",
            )
            manifest = lib.build_manifest(
                source_canon_commit=lib.load_manifest()["source"]["source_canon_commit"],
                validated_at="2026-10-30",
                bundle_dir=bundle,
            )
            lib.write_manifest(manifest, bundle_dir=bundle)
            problems = lib.validate_bundle(bundle_dir=bundle)
            self.assertTrue(any("windows" in problem for problem in problems), problems)

    def test_listing_manifest_in_files_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bundle = Path(tmp) / "bundle"
            shutil.copytree(lib.BUNDLE_DIR, bundle)
            manifest_path = bundle / lib.MANIFEST_NAME
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["files"].append(
                {"path": lib.MANIFEST_NAME, "sha256": "0" * 64}
            )
            manifest_path.write_text(
                json.dumps(manifest, indent=2) + "\n",
                encoding="utf-8",
                newline="\n",
            )
            problems = lib.validate_bundle(bundle_dir=bundle)
            self.assertTrue(
                any("must not be listed" in problem for problem in problems),
                problems,
            )


if __name__ == "__main__":
    unittest.main()
