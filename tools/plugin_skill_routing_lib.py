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
    return problems


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
