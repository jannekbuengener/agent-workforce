#!/usr/bin/env python3
"""Generate derived/PORTFOLIO_CAPABILITY_INDEX.yml from repository capability sources."""

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
        "--output",
        type=Path,
        default=lib.INDEX_PATH,
        help="Output path for the generated index",
    )
    args = parser.parse_args(argv)

    try:
        repo_roots = lib.parse_repo_root_args(args.repo_root)
        index = lib.build_index(repo_roots=repo_roots)
        lib.write_index(index, path=args.output)
    except (OSError, ValueError) as exc:
        print(f"PORTFOLIO_CAPABILITY_INDEX_GENERATE: FAIL\n{exc}", file=sys.stderr)
        return 1

    print(f"PORTFOLIO_CAPABILITY_INDEX_GENERATE: PASS\nWrote {args.output}")
    print(
        f"global={len(index['global_capabilities'])} "
        f"repository={len(index['repository_capabilities'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
