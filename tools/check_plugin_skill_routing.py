#!/usr/bin/env python3
"""Fail closed when plugin/skill routing production or fixture packs are invalid.

Validates:
1. production registry REQUIRED canonical providers
2. routing test fixtures (unless --skip-fixtures)
3. real production consumer packs under skill_canon (docs/skills/*/consumer.yml)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

import plugin_skill_routing_lib as lib  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skip-fixtures",
        action="store_true",
        help=(
            "Skip fixture packs; still validate production registry REQUIRED "
            "providers and real skill-canon consumer packs"
        ),
    )
    args = parser.parse_args(argv)

    problems: list[str] = []
    try:
        problems.extend(lib.validate_production_registry_required_providers())
        if not args.skip_fixtures:
            problems.extend(lib.validate_fixture_valid_pack())
        problems.extend(lib.validate_production_consumer_packs())
    except (OSError, ValueError) as exc:
        print(f"PLUGIN_SKILL_ROUTING_CHECK: FAIL\n{exc}", file=sys.stderr)
        return 1

    if problems:
        print("PLUGIN_SKILL_ROUTING_CHECK: FAIL")
        for problem in problems:
            print(f"- {problem}")
        return 1

    print("PLUGIN_SKILL_ROUTING_CHECK: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
