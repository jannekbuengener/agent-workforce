#!/usr/bin/env python3
"""Structural validation for the ChatGPT Workflows backoffice export bundle."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BUNDLE_DIR = ROOT / "backoffice" / "chatgpt-workflows"
MANIFEST_NAME = "MANIFEST.json"
EXPECTED_DOCS = (
    "01_PROJECT_CORE.md",
    "02_OPERATING_MODEL.md",
    "03_CHATGPT_PROJECT_INSTRUCTIONS.md",
)

BUNDLE_NAME = "chatgpt-workflows-backoffice"
BUNDLE_KIND = "chatgpt_workflows_backoffice"
SOURCE_REPOSITORY = "jannekbuengener/agent-workforce"
SOURCE_BRANCH = "main"

# Exact forbidden patterns only — no broad semantic guessing.
FORBIDDEN_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("openai_api_key_prefix", re.compile(r"\bsk-[A-Za-z0-9]{20,}\b")),
    ("github_token_prefix", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]+\b")),
    ("github_pat_prefix", re.compile(r"\bgithub_pat_[A-Za-z0-9_]+\b")),
    ("aws_access_key_prefix", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("trycloudflare_tunnel", re.compile(r"https://[a-z0-9-]+\.trycloudflare\.com", re.I)),
    ("windows_dev_path", re.compile(r"[A-Za-z]:\\(?:Dev|Users|Workspaces|Config)\\")),
    ("windows_worktrees_path", re.compile(r"\bY:\\Worktrees\b")),
    ("windows_d_dev_workspaces", re.compile(r"\bD:\\Dev\\Workspaces\b")),
    (
        "legacy_gpt_mcp_mission",
        re.compile(
            r"(?i)(?:act as|you are the)\s+operational lead for\s+"
            r"`?jannekbuengener/gpt-mcp-server`?"
        ),
    ),
)

REQUIRED_ACROSS_BUNDLE: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("workforce_spawn_point", re.compile(r"Agent Workforce", re.I)),
    ("bootstrap_front_door", re.compile(r"WORKFORCE_BOOTSTRAP\.md")),
    ("private_mcp_boundary", re.compile(r"PRIVATE MCP\s*=\s*CHATGPT ONLY")),
    (
        "capability_id_consumer_rule",
        re.compile(r"Consumers reference Capability IDs", re.I),
    ),
    (
        "plugin_skill_contract_pointer",
        re.compile(r"PLUGIN_SKILL_ROUTING_CONTRACT\.md"),
    ),
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_manifest(path: Path | None = None) -> dict[str, Any]:
    manifest_path = path or (BUNDLE_DIR / MANIFEST_NAME)
    try:
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"{MANIFEST_NAME} is missing") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"{MANIFEST_NAME} is invalid JSON: {exc}") from exc


def dump_manifest(manifest: dict[str, Any]) -> str:
    return json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"


def git_output(args: list[str], *, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def resolve_source_canon_commit(repo_root: Path = ROOT) -> str:
    for ref in ("origin/main", "main", "HEAD"):
        result = git_output(["rev-parse", "--verify", ref], cwd=repo_root)
        if result.returncode == 0:
            commit = result.stdout.strip()
            if re.fullmatch(r"[0-9a-f]{40}", commit):
                return commit
    raise ValueError("Unable to resolve a 40-char source_canon_commit from git")


def commit_object_exists(commit: str, *, repo_root: Path = ROOT) -> bool:
    result = git_output(["cat-file", "-t", f"{commit}^{{commit}}"], cwd=repo_root)
    return result.returncode == 0 and result.stdout.strip() == "commit"


def build_manifest(
    *,
    source_canon_commit: str,
    validated_at: str,
    bundle_dir: Path = BUNDLE_DIR,
) -> dict[str, Any]:
    files = []
    for name in EXPECTED_DOCS:
        path = bundle_dir / name
        if not path.is_file():
            raise ValueError(f"Missing bundle file: {name}")
        files.append({"path": name, "sha256": sha256_file(path)})
    return {
        "schema_version": 1,
        "bundle_name": BUNDLE_NAME,
        "bundle_kind": BUNDLE_KIND,
        "purpose": (
            "Static ChatGPT Project bootstrap for Workflows meta planning; "
            "not live operational truth."
        ),
        "source": {
            "repository": SOURCE_REPOSITORY,
            "branch": SOURCE_BRANCH,
            "source_canon_commit": source_canon_commit,
            "source_canon_commit_semantics": (
                "Agent Workforce canon tip against which this bundle was "
                "authored/validated. Not the SHA of a commit that contains "
                "this MANIFEST.json."
            ),
        },
        "validated_at": validated_at,
        "files": files,
    }


def write_manifest(manifest: dict[str, Any], *, bundle_dir: Path = BUNDLE_DIR) -> Path:
    path = bundle_dir / MANIFEST_NAME
    path.write_text(dump_manifest(manifest), encoding="utf-8", newline="\n")
    return path


def _scan_text(label: str, text: str, problems: list[str]) -> None:
    for name, pattern in FORBIDDEN_PATTERNS:
        if pattern.search(text):
            problems.append(f"{label}: forbidden pattern matched ({name})")


def validate_bundle(
    *,
    bundle_dir: Path = BUNDLE_DIR,
    repo_root: Path = ROOT,
    require_commit_object: bool = True,
) -> list[str]:
    problems: list[str] = []

    if not bundle_dir.is_dir():
        return [f"Bundle directory missing: {bundle_dir}"]

    on_disk = sorted(p.name for p in bundle_dir.iterdir() if not p.name.startswith("."))
    expected_names = set(EXPECTED_DOCS) | {MANIFEST_NAME}
    for name in EXPECTED_DOCS:
        if name not in on_disk:
            problems.append(f"Missing bundle file: {name}")
    if MANIFEST_NAME not in on_disk:
        problems.append(f"Missing bundle file: {MANIFEST_NAME}")
    for name in on_disk:
        if name not in expected_names:
            problems.append(f"Unlisted bundle file present: {name}")

    try:
        manifest = load_manifest(bundle_dir / MANIFEST_NAME)
    except ValueError as exc:
        problems.append(str(exc))
        return problems

    if manifest.get("schema_version") != 1:
        problems.append("MANIFEST.schema_version must be 1")
    if manifest.get("bundle_name") != BUNDLE_NAME:
        problems.append(f"MANIFEST.bundle_name must be {BUNDLE_NAME}")
    if manifest.get("bundle_kind") != BUNDLE_KIND:
        problems.append(f"MANIFEST.bundle_kind must be {BUNDLE_KIND}")

    purpose = manifest.get("purpose")
    if not isinstance(purpose, str) or "not live operational truth" not in purpose:
        problems.append("MANIFEST.purpose must declare static bootstrap / not live truth")

    source = manifest.get("source")
    if not isinstance(source, dict):
        problems.append("MANIFEST.source is required")
        source = {}
    else:
        if source.get("repository") != SOURCE_REPOSITORY:
            problems.append(f"MANIFEST.source.repository must be {SOURCE_REPOSITORY}")
        if source.get("branch") != SOURCE_BRANCH:
            problems.append(f"MANIFEST.source.branch must be {SOURCE_BRANCH}")
        commit = source.get("source_canon_commit")
        if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}", commit):
            problems.append("MANIFEST.source.source_canon_commit must be a 40-char hex SHA")
        elif require_commit_object and not commit_object_exists(commit, repo_root=repo_root):
            problems.append(
                "MANIFEST.source.source_canon_commit is not present as a local commit object"
            )
        semantics = source.get("source_canon_commit_semantics")
        if not isinstance(semantics, str) or "Not the SHA of a commit that contains" not in semantics:
            problems.append(
                "MANIFEST.source.source_canon_commit_semantics must document non-self-referential meaning"
            )

    validated_at = manifest.get("validated_at")
    if not isinstance(validated_at, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", validated_at):
        problems.append("MANIFEST.validated_at must be YYYY-MM-DD")

    files = manifest.get("files")
    if not isinstance(files, list) or not files:
        problems.append("MANIFEST.files must be a non-empty array")
        files = []

    listed_paths = [entry.get("path") if isinstance(entry, dict) else None for entry in files]
    for name in EXPECTED_DOCS:
        if name not in listed_paths:
            problems.append(f"MANIFEST.files missing {name}")
    if MANIFEST_NAME in listed_paths:
        problems.append("MANIFEST.json must not be listed in MANIFEST.files (hash recursion)")

    for entry in files:
        if not isinstance(entry, dict):
            problems.append("MANIFEST.files entry must be an object")
            continue
        rel = entry.get("path")
        expected_hash = entry.get("sha256")
        if not isinstance(rel, str) or not rel:
            problems.append("MANIFEST.files entry missing path")
            continue
        if rel == MANIFEST_NAME:
            continue
        if not isinstance(expected_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_hash):
            problems.append(f"MANIFEST.files {rel} has invalid sha256")
            continue
        path = bundle_dir / rel
        if not path.is_file():
            problems.append(f"MANIFEST.files path missing on disk: {rel}")
            continue
        actual = sha256_file(path)
        if actual != expected_hash:
            problems.append(f"MANIFEST.files {rel} sha256 mismatch")

    corpus_parts: list[str] = []
    for name in EXPECTED_DOCS:
        path = bundle_dir / name
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            corpus_parts.append(text)
            _scan_text(name, text, problems)
    _scan_text(MANIFEST_NAME, dump_manifest(manifest), problems)

    corpus = "\n".join(corpus_parts)
    for name, pattern in REQUIRED_ACROSS_BUNDLE:
        if not pattern.search(corpus):
            problems.append(f"Bundle missing required orientation marker ({name})")

    return problems
