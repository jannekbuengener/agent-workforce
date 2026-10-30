#!/usr/bin/env python3
"""Fail closed when repository capability sources and generated index drift."""

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
        "--repo-root",
        action="append",
        default=[],
        help="Map portable identity to a local checkout: owner/name=PATH",
    )
    parser.add_argument(
        "--index",
        type=Path,
        default=lib.INDEX_PATH,
        help="Path to committed generated index",
    )
    args = parser.parse_args(argv)

    try:
        repo_roots = lib.parse_repo_root_args(args.repo_root)
        problems = lib.collect_drift_problems(repo_roots=repo_roots, index_path=args.index)
    except (OSError, ValueError) as exc:
        print(f"PORTFOLIO_CAPABILITY_DRIFT_CHECK: FAIL\n{exc}", file=sys.stderr)
        return 1

    if problems:
        print("PORTFOLIO_CAPABILITY_DRIFT_CHECK: FAIL")
        for problem in problems:
            print(f"- {problem}")
        return 1

    print("PORTFOLIO_CAPABILITY_DRIFT_CHECK: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
