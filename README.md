# Agent Workforce

Canonical role and policy repository for Jannek's cross-repository AI engineering workforce.

## Purpose

This repository defines cross-repository workforce identity, authority, evidence contracts, portfolio membership, reusable templates, relevance-gated capability/discovery routing, and shared external-reference semantics. It does not own product code, repo-local engineering truth, mutable scheduler state, or runtime memory.

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

That bootstrap owns the current downstream read order, execution-mode routing, portfolio derivation, capability/reference discovery and fail-closed behavior. Scheduler prompts must not duplicate the full canonical file list, capability registry, or reference catalog.

## Capability routing

The canonical routing contract is [`docs/CAPABILITY_ROUTING.md`](docs/CAPABILITY_ROUTING.md). The machine-readable catalog is [`capabilities/REGISTRY.yml`](capabilities/REGISTRY.yml).

Capability routing is relevance-gated and runs only after target-repository local authority is established. It selects specialized tools or discovery obligations; it never changes repository ownership, truth hierarchy, or mutation authority.

Requirement levels are `REQUIRED`, `DISCOVERY_REQUIRED`, `PREFERRED`, and `ADVISORY`. A matching `REQUIRED` capability that is unavailable or unauthorized fails closed with `BLOCKED_REQUIRED_CAPABILITY_UNAVAILABLE` rather than silently substituting another tool.

V1 routes:

- Reverse Engineering -> `REQUIRED` -> REA (`morluto/rea`).
- Reuse Before Build -> `DISCOVERY_REQUIRED` -> [`docs/REUSE_BEFORE_BUILD.md`](docs/REUSE_BEFORE_BUILD.md).

## Reuse before build

For relevant planning/implementation work, check existing repository code and existing accepted dependencies before adding a new library, tool, service, infrastructure path, or custom implementation.

The canonical decision procedure is [`docs/REUSE_BEFORE_BUILD.md`](docs/REUSE_BEFORE_BUILD.md). It is intentionally bounded: trivial fixes, documentation-only changes, straightforward reuse of an existing repo primitive, and tasks with no meaningful build-vs-reuse decision do not trigger broad ecosystem research.

Discovery can conclude `REUSE_EXISTING`, `ADOPT_DEPENDENCY_OR_TOOL`, or `BUILD_CUSTOM`. A discovery outcome is evidence for the engineering decision; it does not itself authorize dependency installation or repository mutation.

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

## V1 workforce

- [Stable execution bootstrap](WORKFORCE_BOOTSTRAP.md)
- [Capability routing](docs/CAPABILITY_ROUTING.md)
- [Capability registry](capabilities/REGISTRY.yml)
- [Reuse before build](docs/REUSE_BEFORE_BUILD.md)
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
- [NotebookLM guidance](docs/NOTEBOOKLM.md)

## Authority boundaries

`agent-workforce` owns versioned workforce canon only. Each monitored repository owns its own code, repository rules, CI, issues, PRs, Repo Health Book, and repository-specific external-reference relevance. V1 intentionally has no runtime database, scheduler ledger, generated dashboard, or hosted GitHub Actions workflow.

Mutable execution metadata and machine-local capability/reference locations belong to the execution host and are never copied into role, policy, capability, or reference files as canonical truth.
