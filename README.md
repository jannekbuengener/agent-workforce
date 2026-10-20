# Agent Workforce

Canonical role and policy repository for Jannek's cross-repository AI engineering workforce.

## Purpose

This repository defines cross-repository workforce identity, authority, evidence contracts, portfolio membership, and reusable templates. It does not own product code, repo-local engineering truth, mutable scheduler state, or runtime memory.

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

That bootstrap owns the current downstream read order, execution-mode routing, portfolio derivation and fail-closed behavior. Scheduler prompts must not duplicate the full canonical file list.

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
- [Quality Scout](agents/quality-scout.md)
- [Process Scout](agents/process-scout.md)
- [Finding contract](contracts/FINDING_CONTRACT.md)
- [Repo Health Book template](templates/REPO_HEALTH_BOOK.md)
- [Portfolio](portfolio/REPOSITORIES.md)
- [Workforce policy](docs/WORKFORCE_POLICY.md)
- [Meta topology](docs/META_TOPOLOGY.md)
- [NotebookLM guidance](docs/NOTEBOOKLM.md)

## Authority boundaries

`agent-workforce` owns versioned workforce canon only. Each monitored repository owns its own code, repository rules, CI, issues, PRs, and Repo Health Book. V1 intentionally has no runtime database, scheduler ledger, generated dashboard, or hosted GitHub Actions workflow.

Mutable execution metadata belongs to the execution host and is never copied into role or policy files as canonical truth.
