"""PREFERRED capability decision observability (#57).

Tests pass preferred_match explicitly. No free-text / LLM trigger classification.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import preferred_capability_decision_lib as lib  # noqa: E402
import plugin_skill_routing_lib as routing  # noqa: E402
import yaml  # noqa: E402


class PreferredDecisionInvariantTests(unittest.TestCase):
    """Invariants A–H from issue #57."""

    def test_a_matched_used_preferred(self) -> None:
        result = lib.record_preferred_capability_decision(
            capability_id="deterministic_validation",
            matched=True,
            decision="USED_PREFERRED",
        )
        self.assertTrue(result["ok"])
        self.assertEqual(result["entry"]["capability_id"], "deterministic_validation")
        self.assertEqual(result["entry"]["decision"], "USED_PREFERRED")
        self.assertFalse(result["blocked_required"])

    def test_b_matched_local_equivalent_with_reason(self) -> None:
        result = lib.record_preferred_capability_decision(
            capability_id="deterministic_validation",
            matched=True,
            decision="LOCAL_EQUIVALENT",
            reason=(
                "target repository already owns sufficient deterministic twin "
                "+ pressure cases"
            ),
        )
        self.assertTrue(result["ok"])
        self.assertEqual(result["entry"]["decision"], "LOCAL_EQUIVALENT")
        self.assertIn("twin", result["entry"]["reason"])

    def test_c_matched_local_equivalent_without_reason_fails(self) -> None:
        result = lib.record_preferred_capability_decision(
            capability_id="deterministic_validation",
            matched=True,
            decision="LOCAL_EQUIVALENT",
            reason="",
        )
        self.assertFalse(result["ok"])
        self.assertIn("MISSING_REASON", result["problems"])

    def test_d_matched_not_used_with_reason(self) -> None:
        result = lib.record_preferred_capability_decision(
            capability_id="deterministic_validation",
            matched=True,
            decision="NOT_USED_WITH_REASON",
            reason="preferred provider unavailable on this execution host",
        )
        self.assertTrue(result["ok"])
        self.assertEqual(result["entry"]["decision"], "NOT_USED_WITH_REASON")
        self.assertFalse(result["blocked_required"])

    def test_e_matched_silent_omission_fails(self) -> None:
        """Central RED regression: match without decision must FAIL."""
        result = lib.record_preferred_capability_decision(
            capability_id="deterministic_validation",
            matched=True,
            decision=None,
        )
        self.assertFalse(
            result["ok"],
            msg=(
                "matched PREFERRED without decision must fail; "
                f"got problems={result['problems']}"
            ),
        )
        self.assertIn("SILENT_OMISSION", result["problems"])
        self.assertIsNone(result["entry"])

    def test_f_not_matched_requires_no_decision_and_no_receipt_noise(self) -> None:
        result = lib.record_preferred_capability_decision(
            capability_id="deterministic_validation",
            matched=False,
        )
        self.assertTrue(result["ok"])
        self.assertFalse(result["receipt_required"])
        self.assertIsNone(result["entry"])
        section = lib.render_capability_routing_decisions([result])
        self.assertIsNone(section)

    def test_g_preferred_unavailable_is_non_blocking(self) -> None:
        outcome = lib.preferred_unavailable_outcome(
            matched=True,
            available=False,
            local_equivalent_sufficient=True,
            reason="target repo owns sufficient contract twin and pressure cases",
        )
        self.assertTrue(outcome["ok"])
        self.assertFalse(outcome["blocked_required"])
        self.assertEqual(outcome["decision"], "LOCAL_EQUIVALENT")
        self.assertNotEqual(
            outcome.get("outcome"),
            "BLOCKED_REQUIRED_CAPABILITY_UNAVAILABLE",
        )

        unused = lib.preferred_unavailable_outcome(
            matched=True,
            available=False,
            local_equivalent_sufficient=False,
            reason="preferred capability unauthorized for this host",
        )
        self.assertTrue(unused["ok"])
        self.assertFalse(unused["blocked_required"])
        self.assertEqual(unused["decision"], "NOT_USED_WITH_REASON")

    def test_h_decision_identity_uses_capability_id_not_provider(self) -> None:
        result = lib.record_preferred_capability_decision(
            capability_id="deterministic_validation",
            matched=True,
            decision="USED_PREFERRED",
            resolved_provider="jannekbuengener/arvp",
        )
        self.assertTrue(result["ok"])
        entry = result["entry"]
        self.assertTrue(lib.decision_identity_uses_capability_id(entry))
        self.assertEqual(entry["capability_id"], "deterministic_validation")
        self.assertEqual(entry.get("resolved_provider"), "jannekbuengener/arvp")
        self.assertNotIn("provider", entry)


class RealRoutingScenarioTests(unittest.TestCase):
    """Read-only Run A/B scenarios with explicit preferred_match."""

    def test_run_a_deterministic_validation_match_local_equivalent(self) -> None:
        """Material PASS/FAIL acceptance + target-repo twin → LOCAL_EQUIVALENT."""
        preferred_match = True
        target_repo_owns_sufficient_twin = True
        self.assertTrue(preferred_match and target_repo_owns_sufficient_twin)

        result = lib.record_preferred_capability_decision(
            capability_id="deterministic_validation",
            matched=preferred_match,
            decision="LOCAL_EQUIVALENT",
            reason=(
                "agent-workforce already owns sufficient deterministic contract "
                "twin (tools/preferred_capability_decision_lib.py) + pressure cases; "
                "ARVP not required to replace target-repo authority"
            ),
        )
        self.assertTrue(result["ok"])
        self.assertEqual(result["entry"]["decision"], "LOCAL_EQUIVALENT")
        section = lib.render_capability_routing_decisions([result])
        self.assertIsNotNone(section)
        assert section is not None
        self.assertIn("Capability: deterministic_validation", section)
        self.assertIn("Decision: LOCAL_EQUIVALENT", section)
        self.assertIn("Reason:", section)

    def test_run_b_no_material_match_stays_silent(self) -> None:
        """Ordinary unit tests / trivial validation → no PREFERRED decision noise."""
        preferred_match = False
        result = lib.record_preferred_capability_decision(
            capability_id="deterministic_validation",
            matched=preferred_match,
        )
        self.assertTrue(result["ok"])
        section = lib.render_capability_routing_decisions([result])
        self.assertIsNone(section)
        # Explicitly forbid NO_MATCH noise rows.
        self.assertNotIn("NO_MATCH", str(result.get("entry")))


class CanonSurfaceTests(unittest.TestCase):
    def test_capability_routing_documents_decision_semantics(self) -> None:
        self.assertTrue(lib.routing_md_documents_preferred_decisions())

    def test_meta_epic_run_receipt_includes_capability_routing_decisions(self) -> None:
        self.assertTrue(lib.meta_epic_receipt_includes_capability_routing_decisions())

    def test_evidence_delivery_surfaces_preferred_decision(self) -> None:
        self.assertTrue(lib.evidence_delivery_documents_preferred_decision_surface())

    def test_production_consumers_declaring_preferred_are_known(self) -> None:
        """Only real production consumers with PREFERRED are in scope for #57."""
        found: dict[str, list[str]] = {}
        for skill_dir in (ROOT / "docs" / "skills").iterdir():
            consumer_path = skill_dir / "consumer.yml"
            if not consumer_path.is_file():
                continue
            pack = yaml.safe_load(consumer_path.read_text(encoding="utf-8"))
            for consumer in pack.get("consumers") or []:
                preferred: list[str] = []
                for field in ("requires_capabilities", "optional_capabilities"):
                    for ref in consumer.get(field) or []:
                        if ref.get("requirement") == "PREFERRED":
                            preferred.append(str(ref["id"]))
                if preferred:
                    found[str(consumer["id"])] = preferred
        self.assertEqual(
            found,
            {
                "cursor-meta-epic-executor": ["deterministic_validation"],
                "evidence-backed-delivery": ["deterministic_validation"],
            },
        )
        # Structural packs still validate under #55 production discovery.
        problems = routing.validate_production_consumer_packs()
        self.assertEqual(problems, [])


if __name__ == "__main__":
    unittest.main()
