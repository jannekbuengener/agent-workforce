#!/usr/bin/env python3
"""Portfolio capability discovery: sources, adapters, index generation, drift checks.

Discovery infrastructure only. Generated index is never authority.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - exercised when dep missing
    raise SystemExit(
        "PyYAML is required for portfolio capability discovery tools. "
        "Install with: pip install -r requirements-dev.txt"
    ) from exc


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCES_PATH = REPO_ROOT / "routing" / "REPOSITORY_CAPABILITY_SOURCES.yml"
ROUTING_PATH = REPO_ROOT / "routing" / "REPOSITORY_ROUTING.yml"
PORTFOLIO_PATH = REPO_ROOT / "portfolio" / "REPOSITORIES.md"
INDEX_PATH = REPO_ROOT / "generated" / "PORTFOLIO_CAPABILITY_INDEX.yml"
GENERATOR_NAME = "tools/generate_portfolio_capability_index.py"

ALLOWED_SOURCE_TYPES = {
    "workforce_capability_registry",
    "capability_registry_json",
    "skill_canon_dir",
}
ALLOWED_DISCOVERY = {"registry_entries", "skill_directories"}
ALLOWED_STATUS = {"active", "planned"}
FORBIDDEN_SOURCE_KEYS = {"monitored", "relationships", "role", "blocked"}
FORBIDDEN_ROUTING_KEYS = {"monitored", "blocked"}
ALLOWED_RELATIONSHIP_TYPES = {
    "consumes_package",
    "produces_package_for",
    "navigates_meta",
    "may_use_metatool",
}
ALLOWED_CAPABILITY_DISCOVERY = {
    "missing_machine_readable_source",
}
VOLATILE_ROUTING_HINT_RE = re.compile(
    r"(?i)\b(sha-?256|commit\s+[0-9a-f]{7,}|#"
    r"\d{1,5}\b|pull request #\d+|pr #\d+|v?\d+\.\d+\.\d+)\b"
)
ABSOLUTE_PATH_RE = re.compile(r"^(?:[A-Za-z]:[\\/]|/|\\\\)")
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?", re.DOTALL)
PORTFOLIO_REPO_RE = re.compile(
    r"\|\s*`(?P<identity>[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)`\s*\|"
)


@dataclass(frozen=True)
class CapabilityRow:
    section: str  # global_capabilities | repository_capabilities
    repository: str | None
    capability_id: str
    intent: str
    source_id: str
    source_path: str
    source_type: str
    authority: str
    provider_kind: str
    category: str | None = None
    lifecycle: str | None = None
    requirement: str | None = None

    def as_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "capability_id": self.capability_id,
            "intent": self.intent,
            "provider_kind": self.provider_kind,
            "source_id": self.source_id,
            "source_path": self.source_path,
            "source_type": self.source_type,
            "authority": self.authority,
        }
        if self.repository is not None:
            data["repository"] = self.repository
        if self.category is not None:
            data["category"] = self.category
        if self.lifecycle is not None:
            data["lifecycle"] = self.lifecycle
        if self.requirement is not None:
            data["requirement"] = self.requirement
        return data


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def dump_yaml(data: Any) -> str:
    return yaml.safe_dump(
        data,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
        width=1000,
    )


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    return re.sub(r"\s+", " ", text)


def is_absolute_path(value: str) -> bool:
    return bool(ABSOLUTE_PATH_RE.match(value.strip()))


def parse_repo_root_args(values: list[str] | None) -> dict[str, Path]:
    roots: dict[str, Path] = {}
    for item in values or []:
        if "=" not in item:
            raise ValueError(f"Invalid --repo-root value (expected owner/name=PATH): {item}")
        identity, raw_path = item.split("=", 1)
        identity = identity.strip()
        raw_path = raw_path.strip()
        if not identity or not raw_path:
            raise ValueError(f"Invalid --repo-root value: {item}")
        roots[identity] = Path(raw_path).expanduser().resolve()
    return roots


def load_sources(path: Path = SOURCES_PATH) -> dict[str, Any]:
    data = load_yaml(path)
    if not isinstance(data, dict):
        raise ValueError(f"Sources file must be a mapping: {path}")
    return data


def validate_sources_schema(sources: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if sources.get("schema_version") != 1:
        problems.append("schema_version must be 1")
    repositories = sources.get("repositories")
    if not isinstance(repositories, dict):
        problems.append("repositories must be a mapping")
        return problems

    for repo_key, entry in repositories.items():
        prefix = f"repositories[{repo_key}]"
        if not isinstance(entry, dict):
            problems.append(f"{prefix} must be a mapping")
            continue
        for forbidden in FORBIDDEN_SOURCE_KEYS:
            if forbidden in entry:
                problems.append(f"{prefix} must not declare '{forbidden}'")
        portable = entry.get("portable_identity")
        if portable != repo_key:
            problems.append(
                f"{prefix}.portable_identity must equal mapping key '{repo_key}'"
            )
        if entry.get("routable") is not True:
            problems.append(f"{prefix}.routable must be true for declared sources in V1")
        local_authority = entry.get("local_authority")
        if not isinstance(local_authority, dict) or not local_authority.get("frontdoor"):
            problems.append(f"{prefix}.local_authority.frontdoor is required")
        else:
            for key, value in local_authority.items():
                if isinstance(value, str) and is_absolute_path(value):
                    problems.append(
                        f"{prefix}.local_authority.{key} must not be an absolute path"
                    )

        caps = entry.get("capability_sources")
        if not isinstance(caps, list) or not caps:
            problems.append(f"{prefix}.capability_sources must be a non-empty list")
            continue
        seen_ids: set[str] = set()
        for index, source in enumerate(caps):
            sp = f"{prefix}.capability_sources[{index}]"
            if not isinstance(source, dict):
                problems.append(f"{sp} must be a mapping")
                continue
            for forbidden in ("monitored", "relationships", "blocked"):
                if forbidden in source:
                    problems.append(f"{sp} must not declare '{forbidden}'")
            source_id = source.get("id")
            if not isinstance(source_id, str) or not source_id:
                problems.append(f"{sp}.id is required")
            elif source_id in seen_ids:
                problems.append(f"{sp}.id duplicates '{source_id}'")
            else:
                seen_ids.add(source_id)
            source_type = source.get("type")
            if source_type not in ALLOWED_SOURCE_TYPES:
                problems.append(f"{sp}.type must be one of {sorted(ALLOWED_SOURCE_TYPES)}")
            discovery = source.get("discovery")
            if discovery not in ALLOWED_DISCOVERY:
                problems.append(f"{sp}.discovery must be one of {sorted(ALLOWED_DISCOVERY)}")
            path = source.get("path")
            if not isinstance(path, str) or not path:
                problems.append(f"{sp}.path is required")
            elif is_absolute_path(path):
                problems.append(f"{sp}.path must be repository-relative, not absolute")
            elif path.replace("\\", "/").startswith("tests/fixtures"):
                problems.append(
                    f"{sp}.path must not point at tests/fixtures (fixtures are test-only)"
                )
            authority = source.get("authority")
            if not isinstance(authority, str) or not authority.strip():
                problems.append(f"{sp}.authority is required")
            status = source.get("status")
            if status not in ALLOWED_STATUS:
                problems.append(f"{sp}.status must be one of {sorted(ALLOWED_STATUS)}")
    return problems


def resolve_repo_root(
    identity: str,
    repo_roots: dict[str, Path],
    default_workforce_root: Path = REPO_ROOT,
) -> Path | None:
    if identity in repo_roots:
        return repo_roots[identity]
    if identity == "jannekbuengener/agent-workforce":
        return default_workforce_root
    return None


def discover_sibling_repo_roots(
    identities: list[str] | set[str],
    *,
    workforce_root: Path = REPO_ROOT,
) -> dict[str, Path]:
    """Map portable identities to sibling checkouts next to agent-workforce.

    No absolute paths are stored in contracts; this is runtime discovery only.
    """
    parent = workforce_root.resolve().parent
    roots: dict[str, Path] = {}
    for identity in identities:
        if identity == "jannekbuengener/agent-workforce":
            continue
        name = identity.split("/", 1)[-1]
        candidate = parent / name
        if candidate.is_dir() and (candidate / ".git").exists():
            roots[identity] = candidate.resolve()
    return roots


def merge_repo_roots(
    explicit: dict[str, Path] | None,
    *,
    sources: dict[str, Any] | None = None,
    workforce_root: Path = REPO_ROOT,
) -> dict[str, Path]:
    sources = sources if sources is not None else load_sources()
    identities = set((sources.get("repositories") or {}).keys())
    merged = discover_sibling_repo_roots(identities, workforce_root=workforce_root)
    if explicit:
        merged.update(explicit)
    return merged


def _section_for_type(source_type: str) -> str:
    if source_type == "workforce_capability_registry":
        return "global_capabilities"
    return "repository_capabilities"


def adapt_workforce_capability_registry(
    *,
    repository: str,
    source: dict[str, Any],
    root: Path,
) -> list[CapabilityRow]:
    path = root / source["path"]
    if not path.is_file():
        raise FileNotFoundError(f"Missing workforce registry: {path}")
    data = load_yaml(path)
    capabilities = data.get("capabilities") if isinstance(data, dict) else None
    if not isinstance(capabilities, dict):
        raise ValueError(f"Invalid workforce registry shape: {path}")
    rows: list[CapabilityRow] = []
    for cap_id, entry in capabilities.items():
        if not isinstance(entry, dict):
            raise ValueError(f"Invalid capability entry '{cap_id}' in {path}")
        rows.append(
            CapabilityRow(
                section="global_capabilities",
                repository=None,
                capability_id=str(cap_id),
                intent=normalize_text(entry.get("description")),
                source_id=source["id"],
                source_path=source["path"],
                source_type=source["type"],
                authority=source["authority"],
                provider_kind="registry_entry",
                requirement=entry.get("requirement"),
            )
        )
    return rows


def adapt_capability_registry_json(
    *,
    repository: str,
    source: dict[str, Any],
    root: Path,
) -> list[CapabilityRow]:
    path = root / source["path"]
    if not path.is_file():
        raise FileNotFoundError(f"Missing capability registry JSON: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    capabilities = data.get("capabilities") if isinstance(data, dict) else None
    if not isinstance(capabilities, list):
        raise ValueError(f"Invalid capability_registry_json shape: {path}")
    rows: list[CapabilityRow] = []
    for entry in capabilities:
        if not isinstance(entry, dict) or "id" not in entry:
            raise ValueError(f"Invalid capability entry in {path}")
        rows.append(
            CapabilityRow(
                section="repository_capabilities",
                repository=repository,
                capability_id=str(entry["id"]),
                intent=normalize_text(entry.get("purpose")),
                source_id=source["id"],
                source_path=source["path"],
                source_type=source["type"],
                authority=source["authority"],
                provider_kind="registry_entry",
                category=entry.get("type"),
                lifecycle=entry.get("lifecycle"),
            )
        )
    return rows


def _parse_skill_frontmatter(text: str) -> dict[str, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    meta: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip("\"'")
    return meta


def adapt_skill_canon_dir(
    *,
    repository: str,
    source: dict[str, Any],
    root: Path,
) -> list[CapabilityRow]:
    path = root / source["path"]
    if not path.is_dir():
        raise FileNotFoundError(f"Missing skill canon directory: {path}")
    rows: list[CapabilityRow] = []
    for child in sorted(path.iterdir(), key=lambda p: p.name):
        if not child.is_dir():
            continue
        skill_md = child / "SKILL.md"
        if not skill_md.is_file():
            continue
        meta = _parse_skill_frontmatter(skill_md.read_text(encoding="utf-8"))
        skill_id = meta.get("name") or child.name
        rows.append(
            CapabilityRow(
                section="repository_capabilities",
                repository=repository,
                capability_id=skill_id,
                intent=normalize_text(meta.get("description")),
                source_id=source["id"],
                source_path=source["path"],
                source_type=source["type"],
                authority=source["authority"],
                provider_kind="skill",
            )
        )
    return rows


ADAPTERS = {
    "workforce_capability_registry": adapt_workforce_capability_registry,
    "capability_registry_json": adapt_capability_registry_json,
    "skill_canon_dir": adapt_skill_canon_dir,
}


def collect_rows_from_source(
    *,
    repository: str,
    source: dict[str, Any],
    root: Path,
) -> list[CapabilityRow]:
    adapter = ADAPTERS[source["type"]]
    rows = adapter(repository=repository, source=source, root=root)
    expected_section = _section_for_type(source["type"])
    for row in rows:
        if row.section != expected_section:
            raise ValueError(
                f"Adapter for {source['type']} produced wrong section {row.section}"
            )
        if row.authority != source["authority"]:
            raise ValueError(
                f"Authority mutation detected for {row.capability_id}: "
                f"{row.authority!r} != {source['authority']!r}"
            )
    return rows


def fingerprint_inputs(
    sources: dict[str, Any],
    artifact_blobs: list[bytes],
) -> str:
    hasher = hashlib.sha256()
    hasher.update(dump_yaml(sources).encode("utf-8"))
    for blob in artifact_blobs:
        hasher.update(b"\0")
        hasher.update(blob)
    return hasher.hexdigest()


def build_index(
    *,
    sources: dict[str, Any] | None = None,
    repo_roots: dict[str, Path] | None = None,
    include_planned: bool = False,
    auto_discover_siblings: bool = True,
) -> dict[str, Any]:
    sources = sources if sources is not None else load_sources()
    if auto_discover_siblings:
        repo_roots = merge_repo_roots(repo_roots, sources=sources)
    else:
        repo_roots = repo_roots or {}
    schema_problems = validate_sources_schema(sources)
    if schema_problems:
        raise ValueError("Invalid sources schema:\n- " + "\n- ".join(schema_problems))

    global_capabilities: list[dict[str, Any]] = []
    repository_capabilities: list[dict[str, Any]] = []
    artifact_blobs: list[bytes] = []
    problems: list[str] = []

    repositories = sources.get("repositories", {})
    for repo_key, entry in repositories.items():
        root = resolve_repo_root(repo_key, repo_roots)
        for source in entry["capability_sources"]:
            status = source["status"]
            if status == "planned" and not include_planned:
                continue
            if root is None:
                problems.append(
                    f"Unresolvable active source root for {repo_key} "
                    f"(source id={source['id']}). Pass --repo-root {repo_key}=PATH"
                )
                continue
            try:
                # Fingerprint resolved artifacts for active sources.
                source_path = root / source["path"]
                if source["type"] == "skill_canon_dir":
                    if source_path.is_dir():
                        for skill_md in sorted(source_path.glob("*/SKILL.md")):
                            artifact_blobs.append(skill_md.read_bytes())
                elif source_path.is_file():
                    artifact_blobs.append(source_path.read_bytes())
                rows = collect_rows_from_source(
                    repository=repo_key,
                    source=source,
                    root=root,
                )
            except (OSError, ValueError, json.JSONDecodeError, yaml.YAMLError) as exc:
                problems.append(
                    f"Failed to load {repo_key} source '{source['id']}': {exc}"
                )
                continue
            for row in rows:
                target = (
                    global_capabilities
                    if row.section == "global_capabilities"
                    else repository_capabilities
                )
                target.append(row.as_dict())

    if problems:
        raise ValueError("Source resolution failures:\n- " + "\n- ".join(problems))

    global_capabilities.sort(key=lambda row: row["capability_id"])
    repository_capabilities.sort(
        key=lambda row: (row.get("repository", ""), row["capability_id"])
    )

    return {
        "schema_version": 1,
        "generated": True,
        "generator": GENERATOR_NAME,
        "source_fingerprint": fingerprint_inputs(sources, artifact_blobs),
        "authority_note": (
            "Derived discovery data only. Copy authority exactly from source "
            "declarations. Never treat this index as repository or workforce authority."
        ),
        "global_capabilities": global_capabilities,
        "repository_capabilities": repository_capabilities,
    }


def write_index(index: dict[str, Any], path: Path = INDEX_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dump_yaml(index), encoding="utf-8", newline="\n")


def load_index(path: Path = INDEX_PATH) -> dict[str, Any]:
    data = load_yaml(path)
    if not isinstance(data, dict):
        raise ValueError(f"Index must be a mapping: {path}")
    return data


def validate_index_structure(index: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if index.get("generated") is not True:
        problems.append("index.generated must be true")
    if index.get("generator") != GENERATOR_NAME:
        problems.append(f"index.generator must be {GENERATOR_NAME}")
    if "source_fingerprint" not in index:
        problems.append("index.source_fingerprint is required")
    if "global_capabilities" not in index or "repository_capabilities" not in index:
        problems.append("index must contain global_capabilities and repository_capabilities")
        return problems
    if not isinstance(index["global_capabilities"], list):
        problems.append("global_capabilities must be a list")
    if not isinstance(index["repository_capabilities"], list):
        problems.append("repository_capabilities must be a list")

    for row in index.get("global_capabilities", []) or []:
        if not isinstance(row, dict):
            problems.append("global_capabilities entries must be mappings")
            continue
        if "repository" in row:
            problems.append(
                f"global capability '{row.get('capability_id')}' must not set repository"
            )
        if row.get("source_type") != "workforce_capability_registry":
            problems.append(
                f"global capability '{row.get('capability_id')}' has wrong source_type"
            )
    for row in index.get("repository_capabilities", []) or []:
        if not isinstance(row, dict):
            problems.append("repository_capabilities entries must be mappings")
            continue
        if not row.get("repository"):
            problems.append(
                f"repository capability '{row.get('capability_id')}' missing repository"
            )
        if row.get("source_type") == "workforce_capability_registry":
            problems.append(
                f"repository capability '{row.get('capability_id')}' must not use "
                "workforce_capability_registry"
            )
    return problems


def collect_drift_problems(
    *,
    sources: dict[str, Any] | None = None,
    repo_roots: dict[str, Path] | None = None,
    index_path: Path = INDEX_PATH,
    auto_discover_siblings: bool = True,
) -> list[str]:
    sources = sources if sources is not None else load_sources()
    problems = validate_sources_schema(sources)
    if problems:
        return [f"schema: {p}" for p in problems]

    try:
        expected = build_index(
            sources=sources,
            repo_roots=repo_roots,
            auto_discover_siblings=auto_discover_siblings,
        )
    except ValueError as exc:
        return [str(exc)]

    if not index_path.is_file():
        return [f"Missing generated index: {index_path}"]

    try:
        actual = load_index(index_path)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        return [f"Unreadable index: {exc}"]

    problems.extend(validate_index_structure(actual))

    # Authority exact-copy and source traceability against expected rebuild.
    expected_by_key = {
        (
            "global" if row_section == "global_capabilities" else row.get("repository"),
            row["capability_id"],
            row["source_id"],
        ): row
        for row_section, rows in (
            ("global_capabilities", expected["global_capabilities"]),
            ("repository_capabilities", expected["repository_capabilities"]),
        )
        for row in rows
    }
    actual_by_key = {
        (
            "global" if row_section == "global_capabilities" else row.get("repository"),
            row["capability_id"],
            row["source_id"],
        ): row
        for row_section, rows in (
            ("global_capabilities", actual.get("global_capabilities") or []),
            ("repository_capabilities", actual.get("repository_capabilities") or []),
        )
        for row in rows
        if isinstance(row, dict)
    }

    for key in sorted(set(expected_by_key) - set(actual_by_key)):
        problems.append(f"Missing index entry for {key}")
    for key in sorted(set(actual_by_key) - set(expected_by_key)):
        problems.append(f"Stale or invented index entry for {key}")

    for key in sorted(set(expected_by_key) & set(actual_by_key)):
        exp = expected_by_key[key]
        act = actual_by_key[key]
        if act.get("authority") != exp.get("authority"):
            problems.append(
                f"Authority drift/mutation for {key}: "
                f"{act.get('authority')!r} != {exp.get('authority')!r}"
            )
        if act != exp:
            problems.append(f"Index row drift for {key}")

    if actual.get("source_fingerprint") != expected.get("source_fingerprint"):
        problems.append("source_fingerprint drift between sources and committed index")

    # Full structural equality of derived sections after normalizing via rebuild.
    if (
        actual.get("global_capabilities") != expected.get("global_capabilities")
        or actual.get("repository_capabilities") != expected.get("repository_capabilities")
    ):
        if "Index row drift" not in " ".join(problems):
            problems.append("Generated capability sections diverge from sources")

    return problems


def load_routing(path: Path = ROUTING_PATH) -> dict[str, Any]:
    data = load_yaml(path)
    if not isinstance(data, dict):
        raise ValueError(f"Routing file must be a mapping: {path}")
    return data


def parse_portfolio_identities(path: Path = PORTFOLIO_PATH) -> set[str]:
    if not path.is_file():
        return set()
    text = path.read_text(encoding="utf-8")
    return {match.group("identity") for match in PORTFOLIO_REPO_RE.finditer(text)}


def _routing_text_fields(entry: dict[str, Any]) -> list[str]:
    values: list[str] = []
    for key in ("system_role", "routing_notes", "capability_discovery"):
        value = entry.get(key)
        if isinstance(value, str):
            values.append(value)
    for key in ("owns", "does_not_own"):
        items = entry.get(key) or []
        if isinstance(items, list):
            values.extend(str(item) for item in items)
    for rel in entry.get("relationships") or []:
        if isinstance(rel, dict):
            for key in ("type", "direction", "summary"):
                if isinstance(rel.get(key), str):
                    values.append(rel[key])
    local_authority = entry.get("local_authority") or {}
    if isinstance(local_authority, dict):
        values.extend(str(v) for v in local_authority.values() if isinstance(v, str))
    return values


def validate_routing_schema(
    routing: dict[str, Any],
    *,
    sources: dict[str, Any] | None = None,
    portfolio_identities: set[str] | None = None,
) -> list[str]:
    problems: list[str] = []
    if routing.get("schema_version") != 1:
        problems.append("schema_version must be 1")
    repositories = routing.get("repositories")
    if not isinstance(repositories, dict) or not repositories:
        problems.append("repositories must be a non-empty mapping")
        return problems

    sources = sources if sources is not None else load_sources()
    source_repos = set((sources.get("repositories") or {}).keys())
    if portfolio_identities is None:
        portfolio_identities = parse_portfolio_identities()

    for repo_key, entry in repositories.items():
        prefix = f"repositories[{repo_key}]"
        if not isinstance(entry, dict):
            problems.append(f"{prefix} must be a mapping")
            continue
        for forbidden in FORBIDDEN_ROUTING_KEYS:
            if forbidden in entry:
                problems.append(
                    f"{prefix} must not declare '{forbidden}' "
                    "(monitored membership stays in portfolio/REPOSITORIES.md)"
                )
        if entry.get("portable_identity") != repo_key:
            problems.append(
                f"{prefix}.portable_identity must equal mapping key '{repo_key}'"
            )
        if not isinstance(entry.get("system_role"), str) or not entry["system_role"].strip():
            problems.append(f"{prefix}.system_role is required")
        for list_key in ("owns", "does_not_own"):
            items = entry.get(list_key)
            if not isinstance(items, list) or not items:
                problems.append(f"{prefix}.{list_key} must be a non-empty list")
            elif not all(isinstance(item, str) and item.strip() for item in items):
                problems.append(f"{prefix}.{list_key} entries must be non-empty strings")
        local_authority = entry.get("local_authority")
        if not isinstance(local_authority, dict) or not local_authority.get("frontdoor"):
            problems.append(f"{prefix}.local_authority.frontdoor is required")
        else:
            for key, value in local_authority.items():
                if isinstance(value, str) and is_absolute_path(value):
                    problems.append(
                        f"{prefix}.local_authority.{key} must not be an absolute path"
                    )

        cap_source = entry.get("capability_source", "__missing__")
        if cap_source is None:
            discovery = entry.get("capability_discovery")
            if discovery not in ALLOWED_CAPABILITY_DISCOVERY:
                problems.append(
                    f"{prefix}.capability_discovery must be one of "
                    f"{sorted(ALLOWED_CAPABILITY_DISCOVERY)} when capability_source is null"
                )
        elif cap_source == "__missing__":
            problems.append(f"{prefix}.capability_source is required (portable id or null)")
        elif not isinstance(cap_source, str) or not cap_source:
            problems.append(f"{prefix}.capability_source must be a portable identity or null")
        elif cap_source not in source_repos:
            problems.append(
                f"{prefix}.capability_source '{cap_source}' missing from "
                "REPOSITORY_CAPABILITY_SOURCES.yml"
            )
        elif cap_source != repo_key:
            problems.append(
                f"{prefix}.capability_source must equal this repository's "
                f"portable identity when set (got '{cap_source}')"
            )

        relationships = entry.get("relationships")
        if relationships is None:
            problems.append(f"{prefix}.relationships must be a list (empty allowed)")
        elif not isinstance(relationships, list):
            problems.append(f"{prefix}.relationships must be a list")
        else:
            for index, rel in enumerate(relationships):
                rp = f"{prefix}.relationships[{index}]"
                if not isinstance(rel, dict):
                    problems.append(f"{rp} must be a mapping")
                    continue
                rel_type = rel.get("type")
                if rel_type not in ALLOWED_RELATIONSHIP_TYPES:
                    problems.append(
                        f"{rp}.type must be one of {sorted(ALLOWED_RELATIONSHIP_TYPES)}"
                    )
                target = rel.get("target")
                if not isinstance(target, str) or not target:
                    problems.append(f"{rp}.target is required")
                elif target not in repositories:
                    problems.append(
                        f"{rp}.target '{target}' must be a routable repository "
                        "declared in REPOSITORY_ROUTING.yml"
                    )
                if not isinstance(rel.get("direction"), str) or not rel["direction"].strip():
                    problems.append(f"{rp}.direction is required")
                if not isinstance(rel.get("summary"), str) or not rel["summary"].strip():
                    problems.append(f"{rp}.summary is required")

        for text in _routing_text_fields(entry):
            if is_absolute_path(text):
                problems.append(f"{prefix} must not embed absolute paths ({text!r})")
            if VOLATILE_ROUTING_HINT_RE.search(text):
                problems.append(
                    f"{prefix} appears to embed volatile SHA/version/issue/PR truth "
                    f"({text!r})"
                )

    # Capability sources that exist must be routable in topology.
    for source_id in sorted(source_repos):
        if source_id not in repositories:
            problems.append(
                f"capability source '{source_id}' is not declared in REPOSITORY_ROUTING.yml"
            )

    # Portfolio members should be routable so scouts have a frontdoor map.
    for identity in sorted(portfolio_identities):
        if identity not in repositories:
            problems.append(
                f"monitored portfolio member '{identity}' missing from "
                "REPOSITORY_ROUTING.yml (routable map; not a monitored dual-write)"
            )

    return problems


def collect_routing_problems(
    *,
    routing: dict[str, Any] | None = None,
    sources: dict[str, Any] | None = None,
) -> list[str]:
    routing = routing if routing is not None else load_routing()
    sources = sources if sources is not None else load_sources()
    return validate_routing_schema(routing, sources=sources)
