# Plugin / Skill Routing Contract

## Purpose

This contract defines how ChatGPT plugins, orchestrators, and worker skills express
routing intent through **Capability IDs** resolved by Agent Workforce — without
hard-wiring plugins to each other, copying repo-local skill matrices, or becoming
competing global routers.

It is a **consumer contract**. Runtime capability membership remains owned by:

- [`capabilities/REGISTRY.yml`](../capabilities/REGISTRY.yml) and [`docs/CAPABILITY_ROUTING.md`](../docs/CAPABILITY_ROUTING.md) for global workforce capabilities;
- [`docs/REPOSITORY_CAPABILITY_DISCOVERY.md`](../docs/REPOSITORY_CAPABILITY_DISCOVERY.md) / [`routing/REPOSITORY_CAPABILITY_SOURCES.yml`](../routing/REPOSITORY_CAPABILITY_SOURCES.yml) for repository-local discovery;
- target-repository local authority for behavior once a target is selected.

## Hard separations

```text
Capability != Provider != Plugin != Skill != Tool != Execution Surface != Repository != Authority
```

| Term | Meaning |
|---|---|
| Capability | Abstract ability / routing intent (`reverse_engineering`, `reuse_before_build`, …) |
| Provider | Concrete instance that supplies a capability (REA, ARVP, Agent Brain, repo-local skill, …) |
| Plugin / Skill | Consumer that declares ownership, triggers, and capability requirements |
| Execution Surface | Where work runs (ChatGPT, Cursor, Codex, Claude Code, Jules, CLI, …) |
| Authority | Source that owns behavior or ownership for a given domain |

## Authority domains

Do **not** flatten authority into a single ranking. Use two domains:

1. **Agent Workforce owns cross-repository selection and capability resolution.**  
   It decides which capability applies and which portable provider/route is canonical.
2. **Target repository authority owns behavior and implementation once the target is selected.**  
   Local `AGENTS`/README/canon/contracts win for work inside that repository.
3. **Execution hosts implement, but override neither.**  
   Hosts supply available tools/evidence; they do not redefine Workforce routing policy or target-repo truth.

Private MCP access is never a worker requirement.

## Target routing model

```text
USER INTENT
    ↓
GLOBAL ROUTER
    ↓
AGENT WORKFORCE CAPABILITY RESOLUTION
    ↓
TARGET REPOSITORY AUTHORITY
    ↓
SPECIALIST / PROJECT ORCHESTRATOR / EXECUTION PROVIDER
    ↓
TOOL / MCP / WORKER / PROVIDER
```

No cyclic plugin-to-plugin matrix.

## Consumer kinds

| `kind` | Role |
|---|---|
| `global_router` | Exactly the cross-repository capability-selection front door. Must set `claims_global_routing: true`. |
| `specialist` | Narrow intent ownership; must not claim global routing. |
| `project_orchestrator` | Project-scoped routing inside declared product/authority scope. |
| `execution_provider` | Runs an already selected worker/surface; trigger must be explicit selection, not “any work that could benefit”. |

Specialists and execution providers must declare clear `owns`, `does_not_own`, exclusions, and exit conditions.

## Coupling rule

Consumers reference **Capability IDs**, not other plugin names.

```yaml
requires_capabilities:
  - id: reverse_engineering
    requirement: REQUIRED
  - id: some_repo_local_capability
    requirement: REQUIRED
    relevance:
      - some_relevance_id
optional_capabilities:
  - id: shared_context_evidence
    requirement: ADVISORY
```

Direct provider binding is allowed only when the capability itself is intentionally
bound to that canonical provider in Workforce registry (for example a REQUIRED
provider contract). Agent Workforce resolves which provider serves a capability ID.

Capability IDs may resolve via the global registry **or** the allowed discovery set
from repository capability discovery (for example `skill_canon_dir` rows produced by
[`tools/portfolio_capability_lib.py`](../tools/portfolio_capability_lib.py)). Do not
duplicate skill-identity rules in consumer validators.

### Conditional capability dependencies

Optional structured field on capability refs:

```yaml
relevance:
  - stable_relevance_id
```

Semantics:

```text
relevance absent
→ requirement applies unconditionally

relevance present
→ non-empty list of stable machine-readable relevance ids
→ requirement applies only when the caller supplies a matching active relevance id
```

Relevance ids use the same portable id shape as capability ids
(`^[a-z][a-z0-9_.-]*$`). Validation is structural only. Do not invent keyword,
LLM, or free-text matching over skill prose. Do not special-case individual
capability ids in this contract.

Forbidden for global consumers:

- copying complete repo-local skill lists into the consumer;
- treating private ChatGPT MCP as a worker capability or worker dependency;
- silently substituting another tool when a matching `REQUIRED` capability is unavailable.

## Requirement semantics

Reuse the existing Workforce levels only:

| Level | Meaning |
|---|---|
| `REQUIRED` | If applicable and provider/capability unavailable or unauthorized → **BLOCK**. No silent substitute. |
| `DISCOVERY_REQUIRED` | Discovery must complete before the relevant build/routing decision. |
| `PREFERRED` | Use when relevant, available, and authorized; justified local alternatives allowed. Matched decisions must be compactly visible on the consumer's existing receipt (`USED_PREFERRED` / `LOCAL_EQUIVALENT` / `NOT_USED_WITH_REASON`); unmatched preferred capabilities stay silent. Decision semantics are owned by [`docs/CAPABILITY_ROUTING.md`](../docs/CAPABILITY_ROUTING.md), not by this consumer contract. |
| `ADVISORY` | Optional value; no blocked outcome by itself. |

## Trigger semantics

Routing is **intent-first**, not keyword-first. Keywords may amplify signals; they are not the whole route.

Structured trigger classes:

| Class | Meaning |
|---|---|
| `explicit` | User names the skill/plugin/capability. |
| `semantic` | Task intent matches the declared scope. |
| `dependency` | An already selected router/specialist requests a Capability ID. |
| `authority` | Target-repo canon prescribes a relevant route. |

Every routable consumer must also declare `exclusions` / `does_not_own` so negative bounds exist.

## Consumer field set (minimal)

Machine-readable consumer packs (fixtures / future migration manifests) use:

```yaml
id: string
kind: global_router | specialist | project_orchestrator | execution_provider
intent: string
claims_global_routing: bool   # true only for global_router
owns: [string]
does_not_own: [string]
triggers:
  explicit: [string]
  semantic: [string]
  dependency: [capability_id]   # capability ids only
  authority: [string]
exclusions: [string]
requires_capabilities:
  - id: capability_id
    requirement: REQUIRED|DISCOVERY_REQUIRED|PREFERRED|ADVISORY
    relevance: [relevance_id]   # optional; conditional applicability
optional_capabilities:
  - id: capability_id
    requirement: REQUIRED|DISCOVERY_REQUIRED|PREFERRED|ADVISORY
    relevance: [relevance_id]   # optional; conditional applicability
output: string
exit: string
private_mcp: never_worker_dependency
repository_provider: owner/name   # optional; must be discoverable via #32/#33 routing
```

Capability **definitions** are not duplicated here. Map global capability-side
concerns to [`capabilities/REGISTRY.yml`](../capabilities/REGISTRY.yml).
Repository-local capability ids remain discoverable via
[`docs/REPOSITORY_CAPABILITY_DISCOVERY.md`](../docs/REPOSITORY_CAPABILITY_DISCOVERY.md).

| Suggested capability field | Workforce home |
|---|---|
| `id` / `intent` / `triggers` / `exclusions` / `requirement` | registry entry |
| `provider` / `source` | `tool` or `contract` |
| `fallback` / `validation` | `availability` outcomes |

Optional structured pack field for cycle tests only:

```yaml
capability_dependency_edges:
  - from: capability_id
    to: capability_id
```

Do not invent cycles from prose.

## Private MCP boundary

```text
PRIVATE MCP = CHATGPT ONLY
```

Private ChatGPT MCP connections must not be modeled as:

- worker capabilities;
- worker requirements;
- plugin dependencies for external workers;
- expected agent infrastructure on non-ChatGPT hosts.

ChatGPT may pass sanitized evidence. Workers use only tools/sources actually available to their host.

## Repo-local skills

Agent Workforce knows where to discover them and where authority begins (#32/#33).
It does **not** copy complete `SKILL.md` bodies, full repo skill lists into every
plugin, or repo-local governance into Workforce canon.

## Routing regression testcase contract

Each consumer should eventually be testable with structured cases:

| `type` | `expected` |
|---|---|
| `should_trigger` | `TRIGGER` |
| `should_not_trigger` | `NO_TRIGGER` |
| `collision_case` | `COLLISION` |
| `dependency_case` | `RESOLVE_CAPABILITY` |
| `missing_required_capability_case` | `BLOCK` |

Case fields: `id`, `consumer_id`, `type`, `intent_summary`, `expected`.

This enables later precision/recall/collision measurements. This slice defines the
testcase contract and fixtures only — it does **not** invent scores or an LLM eval service.

## Structural validation

Leitprinzip:

> Keep validation structural and evidence-based. Do not turn semantic routing quality into pseudo-deterministic linting.

Deterministic checks (see `tools/plugin_skill_routing_lib.py`):

| Code | Structural meaning |
|---|---|
| `UNKNOWN_CAPABILITY` | Capability ID in require/optional/dependency fields is not resolvable via registry (or allowed discovery set); or a `relevance` value is missing/invalid as a stable relevance id. |
| `REQUIRED_WITHOUT_CANONICAL_PROVIDER` | A `REQUIRED` registry capability lacks a defined tool/contract provider route. Runtime availability/authorization is **out of scope** for this static check. |
| `CYCLIC_DEPENDENCY` | Cycle in structured `capability_dependency_edges` only. |
| `COMPETING_GLOBAL_OWNERSHIP` | Two+ `global_router` consumers share an identical `owns` entry. |
| `SPECIALIST_OVERREACH` | Non-`global_router` sets `claims_global_routing: true` (or invalid kind/`claims` pairing). |
| `DIRECT_PLUGIN_COUPLING` | Require/optional/dependency fields contain a non-capability-id value. No freetext plugin-name parsing. |
| `REPO_CAPABILITY_DUPLICATION` | Forbidden embedded list fields such as `repository_capabilities_copy`. No semantic text equality. |
| `MISSING_SOURCE_POINTER` | Structured `repository_provider` is not present in capability sources / routing `capability_source`. |

Explicitly **not** validated here:

- semantic trigger quality;
- keyword heuristics for over-broad triggers;
- runtime provider availability/authorization;
- invented routing precision/recall scores.

## Commands

```text
python tools/check_plugin_skill_routing.py
python -m unittest tools.tests.test_plugin_skill_routing -v
```

The official checker validates three classes:

1. production registry REQUIRED canonical providers;
2. routing test fixtures under `tests/fixtures/plugin-skill-routing/` (test packs only — not a production plugin inventory);
3. real production consumer packs discovered from active `skill_canon_dir` sources in [`routing/REPOSITORY_CAPABILITY_SOURCES.yml`](../routing/REPOSITORY_CAPABILITY_SOURCES.yml) (typically skill-colocated `docs/skills/*/consumer.yml`).

Production discovery reuses that capability-source authority. It must not invent a second consumer inventory, and it must not treat fixtures, generated artifacts, or unrelated YAML as production consumers. A contract-invalid production `consumer.yml` is a deterministic FAIL even when fixtures are green.

## Audit and migration

Evidence-backed consumer audits live in [`docs/PLUGIN_SKILL_ROUTING_AUDIT.md`](../docs/PLUGIN_SKILL_ROUTING_AUDIT.md).

Issue #34 defines this contract. Migrating ChatGPT plugin packages remains a
separate consumer change under each plugin's owning authority. Agent Workforce
must not become a mirror of those plugin packages. Issue #31 may consume this
contract as the ChatGPT meta front door.
