#!/usr/bin/env python3
"""Structural validation for plugin/skill routing consumer contracts.

Keep validation structural and evidence-based. Do not turn semantic routing
quality into pseudo-deterministic linting.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "PyYAML is required for plugin/skill routing tools. "
        "Install with: pip install -r requirements-dev.txt"
    ) from exc


REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "capabilities" / "REGISTRY.yml"
SOURCES_PATH = REPO_ROOT / "routing" / "REPOSITORY_CAPABILITY_SOURCES.yml"
ROUTING_PATH = REPO_ROOT / "routing" / "REPOSITORY_ROUTING.yml"
FIXTURE_VALID = (
    REPO_ROOT / "tests" / "fixtures" / "plugin-skill-routing" / "valid_consumers.yml"
)
FIXTURE_INVALID = (
    REPO_ROOT / "tests" / "fixtures" / "plugin-skill-routing" / "invalid_cases.yml"
)

ALLOWED_KINDS = {
    "global_router",
    "specialist",
    "project_orchestrator",
    "execution_provider",
}
ALLOWED_REQUIREMENTS = {
    "REQUIRED",
    "DISCOVERY_REQUIRED",
    "PREFERRED",
    "ADVISORY",
}
ALLOWED_PRIVATE_MCP = {"never_worker_dependency"}
ALLOWED_CASE_TYPES = {
    "should_trigger",
    "should_not_trigger",
    "collision_case",
    "dependency_case",
    "missing_required_capability_case",
}
ALLOWED_CASE_EXPECTED = {
    "TRIGGER",
    "NO_TRIGGER",
    "COLLISION",
    "RESOLVE_CAPABILITY",
    "BLOCK",
}
TRIGGER_KEYS = ("explicit", "semantic", "dependency", "authority")
CONSUMER_REQUIRED_FIELDS = (
    "id",
    "kind",
    "intent",
    "owns",
    "does_not_own",
    "triggers",
    "exclusions",
    "requires_capabilities",
    "optional_capabilities",
    "output",
    "exit",
    "private_mcp",
)
FORBIDDEN_DUPLICATION_FIELDS = {
    "repository_capabilities_copy",
    "copied_skill_list",
    "embedded_repo_capabilities",
    "repo_capability_list",
}
# Capability IDs only: snake_case / dotted portable ids. Display names fail here.
CAPABILITY_ID_RE = re.compile(r"^[a-z][a-z0-9_.-]*$")
PORTABLE_IDENTITY_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_registry(path: Path | None = None) -> dict[str, Any]:
    data = load_yaml(path or REGISTRY_PATH)
    if not isinstance(data, dict):
        raise ValueError(f"registry must be a mapping: {path or REGISTRY_PATH}")
    return data


def load_sources(path: Path | None = None) -> dict[str, Any]:
    data = load_yaml(path or SOURCES_PATH)
    if not isinstance(data, dict):
        raise ValueError(f"sources must be a mapping: {path or SOURCES_PATH}")
    return data


def load_routing(path: Path | None = None) -> dict[str, Any]:
    data = load_yaml(path or ROUTING_PATH)
    if not isinstance(data, dict):
        raise ValueError(f"routing must be a mapping: {path or ROUTING_PATH}")
    return data


def known_capability_ids(
    registry: dict[str, Any],
    extra_ids: set[str] | None = None,
) -> set[str]:
    caps = registry.get("capabilities") or {}
    ids = set(caps.keys()) if isinstance(caps, dict) else set()
    if extra_ids:
        ids |= set(extra_ids)
    return ids


def has_canonical_provider(entry: dict[str, Any]) -> bool:
    """Static provider/route presence only — not runtime availability."""
    tool = entry.get("tool")
    if isinstance(tool, dict):
        identity = str(tool.get("identity") or "").strip()
        name = str(tool.get("name") or "").strip()
        if identity or name:
            return True
    contract = str(entry.get("contract") or "").strip()
    return bool(contract)


def _problem(code: str, message: str) -> str:
    return f"{code}: {message}"


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def validate_capability_ref(
    *,
    consumer_id: str,
    field: str,
    ref: Any,
    known_ids: set[str],
) -> list[str]:
    problems: list[str] = []
    if not isinstance(ref, dict):
        problems.append(
            _problem(
                "DIRECT_PLUGIN_COUPLING",
                f"{consumer_id}.{field} entries must be objects with capability id",
            )
        )
        return problems
    cap_id = ref.get("id")
    if not isinstance(cap_id, str) or not cap_id.strip():
        problems.append(
            _problem(
                "DIRECT_PLUGIN_COUPLING",
                f"{consumer_id}.{field} missing capability id",
            )
        )
        return problems
    cap_id = cap_id.strip()
    if not CAPABILITY_ID_RE.fullmatch(cap_id):
        problems.append(
            _problem(
                "DIRECT_PLUGIN_COUPLING",
                f"{consumer_id}.{field} id {cap_id!r} is not a capability id "
                "(dependency fields accept capability ids only)",
            )
        )
        return problems
    requirement = ref.get("requirement")
    if requirement not in ALLOWED_REQUIREMENTS:
        problems.append(
            _problem(
                "UNKNOWN_CAPABILITY",
                f"{consumer_id}.{field} id={cap_id} has invalid requirement "
                f"{requirement!r}",
            )
        )
    if cap_id not in known_ids:
        problems.append(
            _problem(
                "UNKNOWN_CAPABILITY",
                f"{consumer_id}.{field} references unknown capability id {cap_id!r}",
            )
        )
    if "relevance" in ref:
        relevance = ref.get("relevance")
        if not isinstance(relevance, list) or not relevance:
            problems.append(
                _problem(
                    "UNKNOWN_CAPABILITY",
                    f"{consumer_id}.{field} id={cap_id} relevance must be a "
                    "non-empty list of stable relevance ids when present",
                )
            )
        else:
            for item in relevance:
                if not isinstance(item, str) or not CAPABILITY_ID_RE.fullmatch(
                    item.strip()
                ):
                    problems.append(
                        _problem(
                            "UNKNOWN_CAPABILITY",
                            f"{consumer_id}.{field} id={cap_id} relevance entry "
                            f"{item!r} is not a stable relevance id",
                        )
                    )
    return problems


def resolve_capability_dependencies(
    consumer: dict[str, Any],
    active_relevance: set[str] | None = None,
    *,
    fields: tuple[str, ...] = ("requires_capabilities", "optional_capabilities"),
) -> list[str]:
    """Deterministic contract-twin helper for conditional capability refs.

    Not a runtime router. Runtime authority remains Workforce routing →
    repository capability discovery → target-repository authority → provider.
    """
    active = {item.strip() for item in (active_relevance or set()) if item.strip()}
    resolved: list[str] = []
    seen: set[str] = set()
    for field in fields:
        for ref in _as_list(consumer.get(field)):
            if not isinstance(ref, dict):
                continue
            cap_id = ref.get("id")
            if not isinstance(cap_id, str) or not cap_id.strip():
                continue
            cap_id = cap_id.strip()
            relevance = ref.get("relevance")
            if relevance is None:
                applies = True
            elif isinstance(relevance, list):
                declared = {
                    item.strip()
                    for item in relevance
                    if isinstance(item, str) and item.strip()
                }
                applies = bool(declared & active)
            else:
                applies = False
            if applies and cap_id not in seen:
                seen.add(cap_id)
                resolved.append(cap_id)
    return resolved


def validate_consumer_schema(consumer: Any, *, index: int) -> list[str]:
    problems: list[str] = []
    label = f"consumers[{index}]"
    if not isinstance(consumer, dict):
        return [_problem("UNKNOWN_CAPABILITY", f"{label} must be a mapping")]

    consumer_id = consumer.get("id")
    if not isinstance(consumer_id, str) or not consumer_id.strip():
        problems.append(_problem("UNKNOWN_CAPABILITY", f"{label}.id is required"))
        consumer_id = label
    else:
        consumer_id = consumer_id.strip()

    for field in CONSUMER_REQUIRED_FIELDS:
        if field not in consumer:
            problems.append(
                _problem(
                    "UNKNOWN_CAPABILITY",
                    f"{consumer_id} missing required field {field}",
                )
            )

    kind = consumer.get("kind")
    if kind not in ALLOWED_KINDS:
        problems.append(
            _problem(
                "SPECIALIST_OVERREACH",
                f"{consumer_id}.kind must be one of {sorted(ALLOWED_KINDS)}",
            )
        )

    claims = consumer.get("claims_global_routing", False)
    if not isinstance(claims, bool):
        problems.append(
            _problem(
                "SPECIALIST_OVERREACH",
                f"{consumer_id}.claims_global_routing must be a boolean",
            )
        )
    elif claims and kind != "global_router":
        problems.append(
            _problem(
                "SPECIALIST_OVERREACH",
                f"{consumer_id} kind={kind} sets claims_global_routing=true",
            )
        )
    elif kind == "global_router" and claims is False:
        problems.append(
            _problem(
                "SPECIALIST_OVERREACH",
                f"{consumer_id} global_router must set claims_global_routing=true",
            )
        )

    if consumer.get("private_mcp") not in ALLOWED_PRIVATE_MCP:
        problems.append(
            _problem(
                "UNKNOWN_CAPABILITY",
                f"{consumer_id}.private_mcp must be never_worker_dependency",
            )
        )

    triggers = consumer.get("triggers")
    if isinstance(triggers, dict):
        for key in TRIGGER_KEYS:
            if key not in triggers:
                problems.append(
                    _problem(
                        "UNKNOWN_CAPABILITY",
                        f"{consumer_id}.triggers missing {key}",
                    )
                )
            elif not isinstance(triggers[key], list):
                problems.append(
                    _problem(
                        "UNKNOWN_CAPABILITY",
                        f"{consumer_id}.triggers.{key} must be a list",
                    )
                )
        for key in triggers:
            if key not in TRIGGER_KEYS:
                problems.append(
                    _problem(
                        "UNKNOWN_CAPABILITY",
                        f"{consumer_id}.triggers has unknown key {key!r}",
                    )
                )
    elif "triggers" in consumer:
        problems.append(
            _problem("UNKNOWN_CAPABILITY", f"{consumer_id}.triggers must be a mapping")
        )

    for field in ("owns", "does_not_own", "exclusions"):
        if field in consumer and not isinstance(consumer[field], list):
            problems.append(
                _problem("UNKNOWN_CAPABILITY", f"{consumer_id}.{field} must be a list")
            )

    for forbidden in FORBIDDEN_DUPLICATION_FIELDS:
        if forbidden in consumer:
            problems.append(
                _problem(
                    "REPO_CAPABILITY_DUPLICATION",
                    f"{consumer_id} forbids embedded repo capability list field "
                    f"{forbidden}",
                )
            )

    return problems


def validate_competing_global_ownership(consumers: list[dict[str, Any]]) -> list[str]:
    problems: list[str] = []
    ownership: dict[str, list[str]] = {}
    for consumer in consumers:
        if consumer.get("kind") != "global_router":
            continue
        consumer_id = str(consumer.get("id"))
        for item in _as_list(consumer.get("owns")):
            if not isinstance(item, str):
                continue
            key = item.strip()
            if not key:
                continue
            ownership.setdefault(key, []).append(consumer_id)
    for owns_item, holders in ownership.items():
        unique = sorted(set(holders))
        if len(unique) > 1:
            problems.append(
                _problem(
                    "COMPETING_GLOBAL_OWNERSHIP",
                    f"owns entry {owns_item!r} claimed by global routers {unique}",
                )
            )
    return problems


def validate_cycles(edges: list[Any]) -> list[str]:
    """Detect cycles only from structured dependency edges."""
    if not edges:
        return []
    graph: dict[str, set[str]] = {}
    for edge in edges:
        if not isinstance(edge, dict):
            return [
                _problem(
                    "CYCLIC_DEPENDENCY",
                    "capability_dependency_edges entries must be {from, to} mappings",
                )
            ]
        src = edge.get("from")
        dst = edge.get("to")
        if not isinstance(src, str) or not isinstance(dst, str):
            return [
                _problem(
                    "CYCLIC_DEPENDENCY",
                    "capability_dependency_edges require string from/to capability ids",
                )
            ]
        if not CAPABILITY_ID_RE.fullmatch(src.strip()) or not CAPABILITY_ID_RE.fullmatch(
            dst.strip()
        ):
            return [
                _problem(
                    "DIRECT_PLUGIN_COUPLING",
                    f"dependency edge {src!r}->{dst!r} must use capability ids only",
                )
            ]
        graph.setdefault(src.strip(), set()).add(dst.strip())
        graph.setdefault(dst.strip(), set())

    visiting: set[str] = set()
    visited: set[str] = set()

    def dfs(node: str, stack: list[str]) -> str | None:
        if node in visiting:
            cycle_start = stack.index(node)
            return " -> ".join(stack[cycle_start:] + [node])
        if node in visited:
            return None
        visiting.add(node)
        stack.append(node)
        for nxt in sorted(graph.get(node, ())):
            found = dfs(nxt, stack)
            if found:
                return found
        stack.pop()
        visiting.remove(node)
        visited.add(node)
        return None

    for node in sorted(graph):
        found = dfs(node, [])
        if found:
            return [
                _problem(
                    "CYCLIC_DEPENDENCY",
                    f"structured capability dependency cycle: {found}",
                )
            ]
    return []


def validate_required_canonical_providers(
    *,
    consumers: list[dict[str, Any]],
    registry: dict[str, Any],
) -> list[str]:
    problems: list[str] = []
    caps = registry.get("capabilities") or {}
    if not isinstance(caps, dict):
        return problems

    for cap_id, entry in caps.items():
        if not isinstance(entry, dict):
            continue
        if entry.get("requirement") != "REQUIRED":
            continue
        if not has_canonical_provider(entry):
            problems.append(
                _problem(
                    "REQUIRED_WITHOUT_CANONICAL_PROVIDER",
                    f"REQUIRED capability {cap_id!r} has no canonical tool/contract provider",
                )
            )

    for consumer in consumers:
        consumer_id = str(consumer.get("id"))
        for ref in _as_list(consumer.get("requires_capabilities")):
            if not isinstance(ref, dict):
                continue
            cap_id = ref.get("id")
            if not isinstance(cap_id, str):
                continue
            entry = caps.get(cap_id)
            if not isinstance(entry, dict):
                continue
            # Consumer-declared REQUIRED or registry REQUIRED both need a route.
            consumer_req = ref.get("requirement")
            registry_req = entry.get("requirement")
            if consumer_req != "REQUIRED" and registry_req != "REQUIRED":
                continue
            if not has_canonical_provider(entry):
                problems.append(
                    _problem(
                        "REQUIRED_WITHOUT_CANONICAL_PROVIDER",
                        f"{consumer_id} requires {cap_id!r} but registry has no "
                        "canonical tool/contract provider",
                    )
                )
    return problems


def validate_repository_provider_pointers(
    *,
    consumers: list[dict[str, Any]],
    sources: dict[str, Any],
    routing: dict[str, Any],
) -> list[str]:
    problems: list[str] = []
    source_repos = set((sources.get("repositories") or {}).keys())
    routing_repos = routing.get("repositories") or {}
    for consumer in consumers:
        if "repository_provider" not in consumer:
            continue
        consumer_id = str(consumer.get("id"))
        provider = consumer.get("repository_provider")
        if not isinstance(provider, str) or not PORTABLE_IDENTITY_RE.fullmatch(
            provider.strip()
        ):
            problems.append(
                _problem(
                    "MISSING_SOURCE_POINTER",
                    f"{consumer_id}.repository_provider must be owner/name portable identity",
                )
            )
            continue
        identity = provider.strip()
        if identity in source_repos:
            continue
        route = routing_repos.get(identity)
        if isinstance(route, dict) and route.get("capability_source"):
            continue
        problems.append(
            _problem(
                "MISSING_SOURCE_POINTER",
                f"{consumer_id}.repository_provider {identity!r} is not discoverable "
                "via repository capability sources or routing capability_source",
            )
        )
    return problems


def validate_regression_cases(
    cases: list[Any],
    *,
    consumer_ids: set[str],
) -> list[str]:
    problems: list[str] = []
    for index, case in enumerate(cases):
        label = f"routing_regression_cases[{index}]"
        if not isinstance(case, dict):
            problems.append(_problem("UNKNOWN_CAPABILITY", f"{label} must be a mapping"))
            continue
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id.strip():
            problems.append(_problem("UNKNOWN_CAPABILITY", f"{label}.id is required"))
            case_id = label
        if case.get("type") not in ALLOWED_CASE_TYPES:
            problems.append(
                _problem(
                    "UNKNOWN_CAPABILITY",
                    f"{case_id}.type must be one of {sorted(ALLOWED_CASE_TYPES)}",
                )
            )
        if case.get("expected") not in ALLOWED_CASE_EXPECTED:
            problems.append(
                _problem(
                    "UNKNOWN_CAPABILITY",
                    f"{case_id}.expected must be one of {sorted(ALLOWED_CASE_EXPECTED)}",
                )
            )
        consumer_id = case.get("consumer_id")
        if not isinstance(consumer_id, str) or consumer_id not in consumer_ids:
            problems.append(
                _problem(
                    "UNKNOWN_CAPABILITY",
                    f"{case_id}.consumer_id must reference a consumer in the pack",
                )
            )
        if not isinstance(case.get("intent_summary"), str) or not str(
            case.get("intent_summary")
        ).strip():
            problems.append(
                _problem(
                    "UNKNOWN_CAPABILITY",
                    f"{case_id}.intent_summary is required",
                )
            )
    return problems


def collect_consumer_pack_problems(
    pack: dict[str, Any],
    *,
    registry: dict[str, Any],
    sources: dict[str, Any],
    routing: dict[str, Any],
    extra_known_ids: set[str] | None = None,
) -> list[str]:
    problems: list[str] = []
    consumers_raw = pack.get("consumers")
    if not isinstance(consumers_raw, list) or not consumers_raw:
        return [_problem("UNKNOWN_CAPABILITY", "consumers must be a non-empty list")]

    consumers: list[dict[str, Any]] = []
    for index, consumer in enumerate(consumers_raw):
        problems.extend(validate_consumer_schema(consumer, index=index))
        if isinstance(consumer, dict):
            consumers.append(consumer)

    known_ids = known_capability_ids(registry, extra_known_ids)
    for consumer in consumers:
        consumer_id = str(consumer.get("id"))
        for field in ("requires_capabilities", "optional_capabilities"):
            for ref in _as_list(consumer.get(field)):
                problems.extend(
                    validate_capability_ref(
                        consumer_id=consumer_id,
                        field=field,
                        ref=ref,
                        known_ids=known_ids,
                    )
                )
        dep_triggers = ((consumer.get("triggers") or {}) if isinstance(consumer.get("triggers"), dict) else {}).get(
            "dependency"
        )
        for dep_id in _as_list(dep_triggers):
            if not isinstance(dep_id, str):
                problems.append(
                    _problem(
                        "DIRECT_PLUGIN_COUPLING",
                        f"{consumer_id}.triggers.dependency entries must be capability ids",
                    )
                )
                continue
            if not CAPABILITY_ID_RE.fullmatch(dep_id.strip()):
                problems.append(
                    _problem(
                        "DIRECT_PLUGIN_COUPLING",
                        f"{consumer_id}.triggers.dependency id {dep_id!r} is not a capability id",
                    )
                )
            elif dep_id.strip() not in known_ids:
                problems.append(
                    _problem(
                        "UNKNOWN_CAPABILITY",
                        f"{consumer_id}.triggers.dependency references unknown "
                        f"capability id {dep_id!r}",
                    )
                )

    problems.extend(validate_competing_global_ownership(consumers))
    problems.extend(
        validate_required_canonical_providers(consumers=consumers, registry=registry)
    )
    problems.extend(
        validate_repository_provider_pointers(
            consumers=consumers, sources=sources, routing=routing
        )
    )
    edges = pack.get("capability_dependency_edges") or []
    if not isinstance(edges, list):
        problems.append(
            _problem(
                "CYCLIC_DEPENDENCY",
                "capability_dependency_edges must be a list when present",
            )
        )
    else:
        problems.extend(validate_cycles(edges))

    cases = pack.get("routing_regression_cases") or []
    if cases:
        if not isinstance(cases, list):
            problems.append(
                _problem(
                    "UNKNOWN_CAPABILITY",
                    "routing_regression_cases must be a list when present",
                )
            )
        else:
            consumer_ids = {
                str(c.get("id")) for c in consumers if isinstance(c.get("id"), str)
            }
            problems.extend(
                validate_regression_cases(cases, consumer_ids=consumer_ids)
            )

    # Stable unique order while preserving first-seen messages.
    seen: set[str] = set()
    ordered: list[str] = []
    for item in problems:
        if item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered


def problem_codes(problems: list[str]) -> set[str]:
    codes: set[str] = set()
    for problem in problems:
        code = problem.split(":", 1)[0].strip()
        if code:
            codes.add(code)
    return codes


def validate_fixture_valid_pack() -> list[str]:
    pack = load_yaml(FIXTURE_VALID)
    if not isinstance(pack, dict):
        return ["UNKNOWN_CAPABILITY: valid_consumers.yml must be a mapping"]
    registry = load_registry()
    sources = load_sources()
    routing = load_routing()
    return collect_consumer_pack_problems(
        pack, registry=registry, sources=sources, routing=routing
    )


def validate_production_registry_required_providers() -> list[str]:
    registry = load_registry()
    return validate_required_canonical_providers(consumers=[], registry=registry)


def _resolved_under_root(repo_root: Path, relative: str) -> Path | None:
    """Return path if relative resolves inside repo_root; otherwise None."""
    rel = relative.strip().replace("\\", "/")
    if not rel or rel.startswith("/") or (len(rel) > 1 and rel[1] == ":"):
        return None
    parts = Path(rel).parts
    if ".." in parts:
        return None
    root = repo_root.resolve()
    candidate = (root / rel).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        return None
    return candidate


def iter_local_skill_canon_dirs(
    *,
    repo_root: Path | None = None,
    sources: dict[str, Any] | None = None,
) -> list[Path]:
    """Active skill_canon_dir paths from capability sources that exist under repo_root.

    Authority is routing/REPOSITORY_CAPABILITY_SOURCES.yml — not a parallel inventory.
    """
    root = (repo_root or REPO_ROOT).resolve()
    data = sources if sources is not None else load_sources()
    found: list[Path] = []
    seen: set[Path] = set()
    repositories = data.get("repositories") or {}
    if not isinstance(repositories, dict):
        return found
    for entry in repositories.values():
        if not isinstance(entry, dict):
            continue
        for source in _as_list(entry.get("capability_sources")):
            if not isinstance(source, dict):
                continue
            if source.get("status") != "active":
                continue
            if source.get("type") != "skill_canon_dir":
                continue
            path_value = source.get("path")
            if not isinstance(path_value, str):
                continue
            resolved = _resolved_under_root(root, path_value)
            if resolved is None or not resolved.is_dir():
                continue
            if resolved in seen:
                continue
            seen.add(resolved)
            found.append(resolved)
    return found


def discoverable_skill_capability_ids(
    *,
    repo_root: Path | None = None,
    sources: dict[str, Any] | None = None,
) -> set[str]:
    """Capability ids from active local skill_canon_dir sources.

    Identity is owned by portfolio_capability_lib.adapt_skill_canon_dir /
    collect_rows_from_source. This helper only collects ids — it does not
    reimplement skill frontmatter/dir naming rules.
    """
    # Local import keeps the routing lib usable when only structural fixture
    # checks run; portfolio lib remains the single skill-identity authority.
    import portfolio_capability_lib as portfolio

    root = (repo_root or REPO_ROOT).resolve()
    data = sources if sources is not None else load_sources()
    ids: set[str] = set()
    repositories = data.get("repositories") or {}
    if not isinstance(repositories, dict):
        return ids
    for repo_key, entry in repositories.items():
        if not isinstance(entry, dict):
            continue
        for source in _as_list(entry.get("capability_sources")):
            if not isinstance(source, dict):
                continue
            if source.get("status") != "active":
                continue
            if source.get("type") != "skill_canon_dir":
                continue
            path_value = source.get("path")
            if not isinstance(path_value, str):
                continue
            resolved = _resolved_under_root(root, path_value)
            if resolved is None or not resolved.is_dir():
                continue
            try:
                rows = portfolio.collect_rows_from_source(
                    repository=str(repo_key),
                    source=source,
                    root=root,
                )
            except (OSError, ValueError, KeyError, FileNotFoundError):
                continue
            for row in rows:
                cap_id = getattr(row, "capability_id", None)
                if isinstance(cap_id, str) and cap_id.strip():
                    ids.add(cap_id.strip())
    return ids


def discover_production_consumer_pack_paths(
    *,
    repo_root: Path | None = None,
    sources: dict[str, Any] | None = None,
) -> list[Path]:
    """Discover skill-colocated consumer.yml under declared skill_canon directories.

    Does not treat tests/fixtures, generated artifacts, or unrelated YAML as
    production consumer packs.
    """
    root = (repo_root or REPO_ROOT).resolve()
    paths: list[Path] = []
    for skill_canon in iter_local_skill_canon_dirs(repo_root=root, sources=sources):
        try:
            skill_canon.relative_to(root)
        except ValueError:
            continue
        # Defense: never treat a fixtures tree as production skill canon.
        rel_canon = skill_canon.relative_to(root).as_posix()
        if rel_canon == "tests" or rel_canon.startswith("tests/"):
            continue
        if not skill_canon.is_dir():
            continue
        for child in sorted(skill_canon.iterdir(), key=lambda p: p.name):
            if not child.is_dir():
                continue
            consumer = child / "consumer.yml"
            if consumer.is_file():
                paths.append(consumer.resolve())
    return paths


def validate_production_consumer_packs(
    *,
    repo_root: Path | None = None,
    sources: dict[str, Any] | None = None,
    registry: dict[str, Any] | None = None,
    routing: dict[str, Any] | None = None,
    pointer_sources: dict[str, Any] | None = None,
) -> list[str]:
    """Validate real production consumer packs with existing contract rules.

    Discovery uses ``sources`` (skill_canon_dir authority). Repository-provider
    pointer checks use ``pointer_sources`` when provided, else ``sources``.
    """
    root = (repo_root or REPO_ROOT).resolve()
    discovery_sources = sources if sources is not None else load_sources()
    validation_sources = (
        pointer_sources if pointer_sources is not None else discovery_sources
    )
    reg = registry if registry is not None else load_registry()
    route = routing if routing is not None else load_routing()
    discovery_ids = discoverable_skill_capability_ids(
        repo_root=root, sources=discovery_sources
    )

    problems: list[str] = []
    discovered = discover_production_consumer_pack_paths(
        repo_root=root, sources=discovery_sources
    )
    for path in discovered:
        try:
            rel = path.relative_to(root).as_posix()
        except ValueError:
            rel = path.as_posix()
        pack = load_yaml(path)
        if not isinstance(pack, dict):
            problems.append(
                _problem(
                    "UNKNOWN_CAPABILITY",
                    f"{rel} must be a mapping consumer pack",
                )
            )
            continue
        pack_problems = collect_consumer_pack_problems(
            pack,
            registry=reg,
            sources=validation_sources,
            routing=route,
            extra_known_ids=discovery_ids,
        )
        for item in pack_problems:
            # Keep CODE: as the leading token so problem_codes() stays stable.
            code, sep, rest = item.partition(":")
            if sep:
                problems.append(f"{code.strip()}: {rel}:{rest}")
            else:
                problems.append(f"{rel}: {item}")
    return problems
