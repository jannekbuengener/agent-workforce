#!/usr/bin/env python3
"""Tests for repository routing topology validation."""

from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import portfolio_capability_lib as lib  # noqa: E402


REQUIRED_ROUTABLE = {
    "jannekbuengener/agent-workforce",
    "jannekbuengener/agent-brain",
    "jannekbuengener/arvp",
    "jannekbuengener/sample-brain",
    "jannekbuengener/sample-brain-analysis",
    "jannekbuengener/Claire_de_Binare",
    "jannekbuengener/traum_taenzer",
    "morluto/rea",
}


class RepositoryRoutingTests(unittest.TestCase):
    def test_production_routing_schema(self) -> None:
        routing = lib.load_routing()
        problems = lib.collect_routing_problems(routing=routing)
        self.assertEqual(problems, [])
        repos = set(routing["repositories"])
        self.assertTrue(REQUIRED_ROUTABLE.issubset(repos))
        for key in repos:
            self.assertFalse(str(key).startswith("fixtures/"))
            entry = routing["repositories"][key]
            self.assertNotIn("monitored", entry)

    def test_sample_brain_ownership_relationship(self) -> None:
        routing = lib.load_routing()
        sb = routing["repositories"]["jannekbuengener/sample-brain"]
        sba = routing["repositories"]["jannekbuengener/sample-brain-analysis"]
        self.assertEqual(sb["system_role"], "product_application")
        self.assertEqual(sba["system_role"], "analysis_package")
        self.assertTrue(
            any(
                rel.get("type") == "consumes_package"
                and rel.get("target") == "jannekbuengener/sample-brain-analysis"
                for rel in sb["relationships"]
            )
        )
        self.assertTrue(
            any(
                rel.get("type") == "produces_package_for"
                and rel.get("target") == "jannekbuengener/sample-brain"
                for rel in sba["relationships"]
            )
        )
        owns_blob = " ".join(sb["owns"]).lower()
        self.assertIn("workbench", owns_blob)
        sba_owns = " ".join(sba["owns"]).lower()
        self.assertIn("analysis", sba_owns)

    def test_capability_source_refs_align(self) -> None:
        routing = lib.load_routing()
        sources = lib.load_sources()
        for identity, entry in routing["repositories"].items():
            cap = entry.get("capability_source")
            if cap is None:
                self.assertEqual(
                    entry.get("capability_discovery"),
                    "missing_machine_readable_source",
                )
            else:
                self.assertIn(cap, sources["repositories"])
                self.assertEqual(cap, identity)

    def test_rejects_monitored_dual_write_and_unknown_target(self) -> None:
        routing = lib.load_routing()
        bad = copy.deepcopy(routing)
        first_key = next(iter(bad["repositories"]))
        bad["repositories"][first_key]["monitored"] = True
        bad["repositories"][first_key]["relationships"] = [
            {
                "type": "consumes_package",
                "target": "example/missing",
                "direction": "consumer_to_producer",
                "summary": "invented",
            }
        ]
        problems = "\n".join(lib.validate_routing_schema(bad))
        self.assertIn("monitored", problems)
        self.assertIn("example/missing", problems)

    def test_rejects_volatile_version_truth(self) -> None:
        routing = lib.load_routing()
        bad = copy.deepcopy(routing)
        first_key = next(iter(bad["repositories"]))
        bad["repositories"][first_key]["routing_notes"] = "Pinned to v1.2.3 and #1234"
        problems = "\n".join(lib.validate_routing_schema(bad))
        self.assertIn("volatile", problems.lower())


if __name__ == "__main__":
    unittest.main()
