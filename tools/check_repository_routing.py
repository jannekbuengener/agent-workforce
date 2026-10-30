#!/usr/bin/env python3
"""Fail closed when repository routing topology is invalid or inconsistent."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

import portfolio_capability_lib as lib  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--routing",
        type=Path,
        default=lib.ROUTING_PATH,
        help="Path to repository routing topology",
    )
    parser.add_argument(
        "--sources",
        type=Path,
        default=lib.SOURCES_PATH,
        help="Path to repository capability sources",
    )
    args = parser.parse_args(argv)

    try:
        routing = lib.load_routing(args.routing)
        sources = lib.load_sources(args.sources)
        problems = lib.collect_routing_problems(routing=routing, sources=sources)
    except (OSError, ValueError) as exc:
        print(f"REPOSITORY_ROUTING_CHECK: FAIL\n{exc}", file=sys.stderr)
        return 1

    if problems:
        print("REPOSITORY_ROUTING_CHECK: FAIL")
        for problem in problems:
            print(f"- {problem}")
        return 1

    print("REPOSITORY_ROUTING_CHECK: PASS")
    print(f"routable={len(routing.get('repositories') or {})}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
