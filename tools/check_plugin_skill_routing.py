#!/usr/bin/env python3
"""Fail closed when plugin/skill routing fixtures or REQUIRED providers are invalid."""

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
        help="Only validate production registry REQUIRED canonical providers",
    )
    args = parser.parse_args(argv)

    problems: list[str] = []
    try:
        problems.extend(lib.validate_production_registry_required_providers())
        if not args.skip_fixtures:
            problems.extend(lib.validate_fixture_valid_pack())
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
