# Agent Workforce

Canonical role and policy repository for Jannek's cross-repository AI engineering workforce.

## Purpose

This repository defines cross-repository workforce identity, authority, evidence contracts, portfolio membership, reusable templates, relevance-gated capability/discovery routing, and shared external-reference semantics. It does not own product code, repo-local engineering truth, or product runtime memory.

Primary operating principle:

> Observe work -> collect evidence -> detect recurring need -> create role -> increase authority only after proven value.

## Truth order

1. GitHub live state in the repository being inspected.
2. The inspected repository's local authority: `AGENTS`, README, architecture/canon/contracts, CI, issues and PRs.
3. This repository's workforce role/policy/contracts.
4. Historical Health Book comments.
5. Derived knowledge surfaces such as NotebookLM.
6. Chat memory.

If live access is unavailable, fail closed. Never reconstruct current repository state from stale memory.

## Stable execution bootstrap

Scheduled/external execution hosts must start from [`WORKFORCE_BOOTSTRAP.md`](WORKFORCE_BOOTSTRAP.md) on live `main`.

That bootstrap owns the current downstream read order, execution-mode routing, portfolio derivation, checkpoint routing, capability/reference discovery and fail-closed behavior. Scheduler prompts must not duplicate the full canonical file list, checkpoint contract, capability registry, or reference catalog.

## End-to-End Workforce Execution Flow

```text
Scheduler / Execution Host
        ↓
WORKFORCE_BOOTSTRAP.md
        ↓
Workforce Canon + Role/Policy Contracts
        ↓
Live Portfolio + Target Repository
        ↓
Target Repo Local Authority
        ↓
Conditional Capability / Reference Routing
        ↓
Quality Scout oder Process Scout
        ↓
Repo Health Book
  ├─ Initial Baseline / Finding Delta
  └─ mutable Scout Checkpoint
        ↓
Workforce Supervisor
        ↓
Meta Issue #3
  ├─ material supervisor review comments
  └─ mutable Supervisor Checkpoint
        ↓
Owner Escalation nur bei echtem Interventionsbedarf
```

The diagram is navigation, not a second specification. Detailed behavior remains owned by [`WORKFORCE_BOOTSTRAP.md`](WORKFORCE_BOOTSTRAP.md), [`docs/WORKFORCE_POLICY.md`](docs/WORKFORCE_POLICY.md), the Scout role files, [`contracts/CHECKPOINT_CONTRACT.md`](contracts/CHECKPOINT_CONTRACT.md), [`contracts/FINDING_CONTRACT.md`](contracts/FINDING_CONTRACT.md), the portfolio, Health Book template, and target-repository authority.

Operationally the state model stays deliberately small:

```text
Scout: read checkpoint -> inspect -> write material evidence when needed -> update checkpoint
Supervisor: read cursor -> review newer Scout outputs -> advance cursor
```

No second durable runtime-state mechanism is part of V1.1.

## Capability routing

The canonical routing contract is [`docs/CAPABILITY_ROUTING.md`](docs/CAPABILITY_ROUTING.md). The machine-readable catalog is [`capabilities/REGISTRY.yml`](capabilities/REGISTRY.yml).

Capability routing is relevance-gated and runs only after target-repository local authority is established. It selects specialized tools or discovery obligations; it never changes repository ownership, truth hierarchy, or mutation authority.

Requirement levels are `REQUIRED`, `DISCOVERY_REQUIRED`, `PREFERRED`, and `ADVISORY`. A matching `REQUIRED` capability that is unavailable or unauthorized fails closed with `BLOCKED_REQUIRED_CAPABILITY_UNAVAILABLE` rather than silently substituting another tool.

V1 routes:

- Reverse Engineering -> `REQUIRED` -> REA (`morluto/rea`).
- Reuse Before Build -> `DISCOVERY_REQUIRED` -> [`docs/REUSE_BEFORE_BUILD.md`](docs/REUSE_BEFORE_BUILD.md).

## Repository routing and capability discovery

Stable portfolio routing facts are defined by [`docs/REPOSITORY_ROUTING.md`](docs/REPOSITORY_ROUTING.md).

- [`routing/REPOSITORY_ROUTING.yml`](routing/REPOSITORY_ROUTING.yml) records identity, system role, owns/does-not-own, directional relationships, and local authority frontdoors for routable repositories.
- Cross-repository capability/skill discovery is defined by [`docs/REPOSITORY_CAPABILITY_DISCOVERY.md`](docs/REPOSITORY_CAPABILITY_DISCOVERY.md).
- [`routing/REPOSITORY_CAPABILITY_SOURCES.yml`](routing/REPOSITORY_CAPABILITY_SOURCES.yml) declares where machine-readable capability/skill authority lives.
- [`generated/PORTFOLIO_CAPABILITY_INDEX.yml`](generated/PORTFOLIO_CAPABILITY_INDEX.yml) is a derived discovery view with separate `global_capabilities` and `repository_capabilities` sections.
- Monitored Scout membership remains owned by [`portfolio/REPOSITORIES.md`](portfolio/REPOSITORIES.md); routing and discovery do not duplicate it.
- The generated index copies source-declared authority exactly and never becomes a second source of truth.

## Plugin / skill consumer routing

Plugins, orchestrators, and skills that participate in cross-repository routing must follow [`contracts/PLUGIN_SKILL_ROUTING_CONTRACT.md`](contracts/PLUGIN_SKILL_ROUTING_CONTRACT.md).

- Consumers declare ownership/triggers and reference **Capability IDs**; Agent Workforce resolves providers.
- Agent Workforce owns cross-repository selection and capability resolution; target repositories own behavior once selected; execution hosts override neither.
- Private MCP remains ChatGPT-only and is never a worker dependency.
- Structural validation lives in `tools/check_plugin_skill_routing.py`; fixtures under `tests/fixtures/plugin-skill-routing/` are not a production plugin inventory.
- Evidence-backed consumer status is recorded in [`docs/PLUGIN_SKILL_ROUTING_AUDIT.md`](docs/PLUGIN_SKILL_ROUTING_AUDIT.md).

## ChatGPT Workflows backoffice

Exportable ChatGPT Project bootstrap for the **WorkForce — Executive Planning & Routing Workspace** lives in [`backoffice/chatgpt-workflows/`](backoffice/chatgpt-workflows/).

- The four files (`01_PROJECT_CORE.md`, `02_OPERATING_MODEL.md`, `03_CHATGPT_PROJECT_INSTRUCTIONS.md`, `MANIFEST.json`) are static orientation only.
- Live authority remains [`WORKFORCE_BOOTSTRAP.md`](WORKFORCE_BOOTSTRAP.md) on `jannekbuengener/agent-workforce@main`; this bundle does not copy Workforce canon, repository topology, or capability inventories.
- Structural validation: `python tools/check_chatgpt_workflows_backoffice.py`
- Refresh file hashes / `source_canon_commit`: `python tools/refresh_chatgpt_workflows_manifest.py`

## Reuse before build

For relevant planning/implementation work, check existing repository code and existing accepted dependencies before adding a new library, tool, service, infrastructure path, or custom implementation.

The canonical decision procedure is [`docs/REUSE_BEFORE_BUILD.md`](docs/REUSE_BEFORE_BUILD.md). It is intentionally bounded: trivial fixes, documentation-only changes, straightforward reuse of an existing repo primitive, and tasks with no meaningful build-vs-reuse decision do not trigger broad ecosystem research.

Discovery can conclude `REUSE_EXISTING`, `ADOPT_DEPENDENCY_OR_TOOL`, or `BUILD_CUSTOM`. A discovery outcome is evidence for the engineering decision; it does not itself authorize dependency installation or repository mutation.

## Skill-TDD (RED fixture independence)

When authoring or changing workforce skills, RED pressure fixtures must not
pre-supply the behavior under test. Soft vs adversarial lanes and RED
outcomes (`RED_FAIL_OBSERVED`, `RED_PASS_EXISTING_BEHAVIOR`,
`RED_FIXTURE_INVALID`, `RED_INCONCLUSIVE`) are defined by
[`contracts/SKILL_TDD_RED_FIXTURE_INDEPENDENCE_CONTRACT.md`](contracts/SKILL_TDD_RED_FIXTURE_INDEPENDENCE_CONTRACT.md)
and the front door [`docs/SKILL_TDD.md`](docs/SKILL_TDD.md).

## External references

The canonical semantics are [`contracts/EXTERNAL_REFERENCE_CONTRACT.md`](contracts/EXTERNAL_REFERENCE_CONTRACT.md). A small shared discovery/reference catalog lives at [`references/CATALOG.yml`](references/CATALOG.yml), and [`templates/EXTERNAL_REFERENCE_INDEX.md`](templates/EXTERNAL_REFERENCE_INDEX.md) defines the default repo-local manifest shape.

The two layers are intentionally separate:

- the shared catalog records reusable public sources/discovery anchors;
- a target repository's own external-reference manifest records which sources are actually relevant to that repository and why.

Repo-local references use `P0` / `P1` / `P2` for **relevance**, independently from external source authority. `P0`/`P1` require concrete repo signals; `P2` is parked/reference-only. Shared catalog membership never proves that a repository uses a technology or should adopt a dependency.

References are loaded relevance-first after target-repository authority handoff. Official/upstream evidence outranks community/example sources, while GitHub/repo live truth and target-repository canon remain higher than all external references.

## Cross-repository meta topology

The canonical shared meta-layer map is [`docs/META_TOPOLOGY.md`](docs/META_TOPOLOGY.md).

Current classes:

- **METAEBENE**
  - `jannekbuengener/agent-workforce` — workforce identity, authority, routing, portfolio and operating policy.
  - `jannekbuengener/agent-brain` — shared knowledge, context, evidence, decision, memory and retrieval infrastructure.
- **METATOOLS**
  - `jannekbuengener/arvp` — domain-neutral deterministic validation, evaluation, gates and evidence framework.

The topology describes shared capabilities and ownership boundaries only. It does not override target-repository authority and does not create implicit runtime dependencies.

## V1.1 workforce

- [Stable execution bootstrap](WORKFORCE_BOOTSTRAP.md)
- [Checkpoint contract](contracts/CHECKPOINT_CONTRACT.md)
- [Capability routing](docs/CAPABILITY_ROUTING.md)
- [Capability registry](capabilities/REGISTRY.yml)
- [Repository routing](docs/REPOSITORY_ROUTING.md)
- [Repository routing topology](routing/REPOSITORY_ROUTING.yml)
- [Repository capability discovery](docs/REPOSITORY_CAPABILITY_DISCOVERY.md)
- [Repository capability sources](routing/REPOSITORY_CAPABILITY_SOURCES.yml)
- [Portfolio capability index](generated/PORTFOLIO_CAPABILITY_INDEX.yml)
- [Reuse before build](docs/REUSE_BEFORE_BUILD.md)
- [Skill-TDD / RED fixture independence](docs/SKILL_TDD.md)
- [External reference contract](contracts/EXTERNAL_REFERENCE_CONTRACT.md)
- [Shared reference catalog](references/CATALOG.yml)
- [External reference manifest template](templates/EXTERNAL_REFERENCE_INDEX.md)
- [Quality Scout](agents/quality-scout.md)
- [Process Scout](agents/process-scout.md)
- [Finding contract](contracts/FINDING_CONTRACT.md)
- [Repo Health Book template](templates/REPO_HEALTH_BOOK.md)
- [Portfolio](portfolio/REPOSITORIES.md)
- [Workforce policy](docs/WORKFORCE_POLICY.md)
- [Meta topology](docs/META_TOPOLOGY.md)
- [ChatGPT Workflows backoffice](backoffice/chatgpt-workflows/)
- [NotebookLM guidance](docs/NOTEBOOKLM.md)

## Authority boundaries

`agent-workforce` owns versioned workforce canon only. Each monitored repository owns its own code, repository rules, CI, issues, PRs, Repo Health Book, and repository-specific external-reference relevance.

V1.1 intentionally has no runtime database, hosted dashboard, or hosted GitHub Actions workflow. The portfolio capability index is committed derived discovery data under generator/drift control, not a second authority store or interactive dashboard. Durable Scout/Supervisor cursors are limited to the mutable GitHub checkpoint comments defined by the Checkpoint Contract; transient scheduler/task metadata remains execution-host state.

Machine-local capability/reference locations are never copied into role, policy, capability, or reference files as canonical truth.
