#!/usr/bin/env python3
"""Refresh MANIFEST.json hashes and source_canon_commit without hashing the manifest itself."""

from __future__ import annotations

import argparse
import sys
from datetime import date
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
        "--source-canon-commit",
        help="Explicit 40-char source_canon_commit (default: origin/main, then main, then HEAD)",
    )
    parser.add_argument(
        "--validated-at",
        help="YYYY-MM-DD (default: today UTC date via local date())",
    )
    args = parser.parse_args(argv)

    try:
        commit = args.source_canon_commit or lib.resolve_source_canon_commit()
        validated_at = args.validated_at or date.today().isoformat()
        manifest = lib.build_manifest(
            source_canon_commit=commit,
            validated_at=validated_at,
            bundle_dir=args.bundle_dir,
        )
        path = lib.write_manifest(manifest, bundle_dir=args.bundle_dir)
    except (OSError, ValueError) as exc:
        print(f"CHATGPT_WORKFLOWS_MANIFEST_REFRESH: FAIL\n{exc}", file=sys.stderr)
        return 1

    print(f"CHATGPT_WORKFLOWS_MANIFEST_REFRESH: PASS\nWrote {path}")
    print(f"source_canon_commit={commit}")
    print(f"validated_at={validated_at}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
