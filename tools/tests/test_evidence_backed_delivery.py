"""Layer A contract tests + structural skill/consumer checks for #43."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import evidence_backed_delivery_lib as lib  # noqa: E402
import plugin_skill_routing_lib as routing  # noqa: E402
import yaml  # noqa: E402


REQUIRED_BEHAVIORAL = {
    "ui_green_missing_screenshot",
    "ui_local_only_temp_path",
    "ui_embedded_current_head",
    "audio_unit_test_only",
    "audio_with_audible_artifact",
    "stale_screenshot_after_ui_change",
    "docs_only_carry_forward",
    "independent_prs_parallel",
    "upstream_merge_invalidates_downstream",
    "owner_visual_agent_self_pass",
    "child_merged_parent_exit_open",
    "green_tests_unresolved_must_fix",
    "screenshot_dump_without_index",
    "bugfix_missing_before_fail",
}


class PressureCaseContractTests(unittest.TestCase):
    def test_all_pressure_cases_match_expect(self) -> None:
        results = lib.evaluate_all()
        self.assertGreaterEqual(len(results), 14)
        failed = [
            {"id": r["id"], "actual": r}
            for r in results
            if not r.get("matches_expect")
        ]
        self.assertEqual(failed, [], msg=f"mismatched cases: {failed}")

    def test_behavioral_required_cases_are_marked(self) -> None:
        pack = lib.load_pressure_cases()
        required = {
            c["id"] for c in pack["cases"] if c.get("behavioral_required")
        }
        self.assertTrue(REQUIRED_BEHAVIORAL.issubset(required))

    def test_local_only_locator_inferred_from_windows_path(self) -> None:
        kind = lib.classify_locator(
            {"locator": r"D:\Temp\ui-after.png"}
        )
        self.assertEqual(kind, "LOCAL_ONLY")

    def test_local_only_hard_blocks_human_inspectable(self) -> None:
        result = lib.classify_evidence(
            {
                "claim_modality": "ui_visual",
                "human_perception_required": True,
                "artifacts": [
                    {
                        "id": "shot",
                        "modality": "ui_visual",
                        "locator_kind": "LOCAL_ONLY",
                        "locator": r"D:\Temp\x.png",
                        "head_sha": "abc",
                    }
                ],
                "head_sha": "abc",
                "evidence_head_sha": "abc",
            }
        )
        self.assertEqual(result["verdict"], "BLOCKED_MISSING_EVIDENCE")
        self.assertEqual(result["locator_kind"], "LOCAL_ONLY")

    def test_agent_cannot_self_pass_owner_gate(self) -> None:
        result = lib.evaluate_acceptance(
            {
                "claim_modality": "ui_visual",
                "human_perception_required": True,
                "owner_acceptance_required": True,
                "agent_declares_owner_pass": True,
                "artifacts": [
                    {
                        "id": "shot",
                        "modality": "ui_visual",
                        "locator_kind": "PR_EMBEDDED",
                        "locator": "![x](https://example/x.png)",
                        "head_sha": "abc",
                        "what_to_inspect": "layout",
                    }
                ],
                "head_sha": "abc",
                "evidence_head_sha": "abc",
                "tests_green": True,
                "unresolved_must_fix": [],
                "merge_order": "INDEPENDENT",
                "issue_contract_complete": True,
            }
        )
        self.assertEqual(result["verdict"], "AWAITING_OWNER")
        self.assertFalse(result["merge_candidate"])
        self.assertFalse(result["agent_may_self_pass_owner"])


class SchemaAndDocumentTests(unittest.TestCase):
    def test_schema_file_exists_and_is_structural(self) -> None:
        self.assertTrue(lib.SCHEMA_JSON.is_file())
        self.assertTrue(lib.structural_schema_keys_present())

    def test_contract_md_exists(self) -> None:
        self.assertTrue(lib.CONTRACT_MD.is_file())
        body = lib.CONTRACT_MD.read_text(encoding="utf-8")
        self.assertIn("LOCAL_ONLY", body)
        self.assertIn("Evidence by Modality", body)
        self.assertIn("MERGE_CANDIDATE", body)

    def test_skill_md_encodes_delivery_contract(self) -> None:
        self.assertTrue(lib.SKILL_MD.is_file())
        self.assertTrue(lib.skill_mandates_delivery_contract())

    def test_modalities_declare_locator_kinds(self) -> None:
        data = lib.load_modalities()
        kinds = set((data.get("locator_kinds") or {}).keys())
        self.assertTrue(
            {
                "PR_EMBEDDED",
                "GITHUB_ATTACHMENT",
                "WORKFLOW_ARTIFACT",
                "STABLE_REVIEW_URL",
                "LOCAL_ONLY",
            }.issubset(kinds)
        )
        self.assertFalse(data["locator_kinds"]["LOCAL_ONLY"]["human_inspectable_ok"])


class ConsumerPackTests(unittest.TestCase):
    def test_skill_colocated_consumer_validates(self) -> None:
        pack = yaml.safe_load(lib.CONSUMER_YML.read_text(encoding="utf-8"))
        problems = routing.collect_consumer_pack_problems(
            pack,
            registry=routing.load_registry(),
            sources=routing.load_sources(),
            routing=routing.load_routing(),
        )
        self.assertEqual(problems, [])


if __name__ == "__main__":
    unittest.main()
