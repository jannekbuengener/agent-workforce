#!/usr/bin/env python3
"""Fail closed when the ChatGPT Workflows backoffice bundle is structurally invalid."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

import chatgpt_workflows_backoffice_lib as lib  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--bundle-dir",
        type=Path,
        default=lib.BUNDLE_DIR,
        help="Path to backoffice/chatgpt-workflows",
    )
    parser.add_argument(
        "--skip-commit-object",
        action="store_true",
        help="Skip local git commit-object existence check for source_canon_commit",
    )
    args = parser.parse_args(argv)

    try:
        problems = lib.validate_bundle(
            bundle_dir=args.bundle_dir,
            require_commit_object=not args.skip_commit_object,
        )
    except (OSError, ValueError) as exc:
        print(f"CHATGPT_WORKFLOWS_BACKOFFICE_CHECK: FAIL\n{exc}", file=sys.stderr)
        return 1

    if problems:
        print("CHATGPT_WORKFLOWS_BACKOFFICE_CHECK: FAIL")
        for problem in problems:
            print(f"- {problem}")
        return 1

    print("CHATGPT_WORKFLOWS_BACKOFFICE_CHECK: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
