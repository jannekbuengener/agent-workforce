# Cross-Repository Meta Topology

## Purpose

This document is the canonical map for Jannek's shared agent meta layer and metatools.

It answers one question: which shared repositories provide workforce, context/evidence, or validation capabilities around repository work?

It does **not** replace target-repository authority. GitHub/repository live state and the target repository's local `AGENTS.md`, README, canon, contracts, issues, PRs and CI remain authoritative inside that repository.

## METAEBENE

### `jannekbuengener/agent-workforce`

Role: cross-repository workforce identity, authority, routing, portfolio and operating policy.

Owns:

- workforce role contracts;
- cross-repository workforce policy;
- scout/supervisor authority boundaries;
- bounded Improvement Board Manager governance and GitHub-issue routing policy for validated Improvements;
- monitored-repository portfolio membership;
- shared finding and Repo Health Book contracts;
- workforce bootstrap/routing rules.

Does not own:

- product or component implementation;
- repository-local engineering truth;
- Agent Brain implementation;
- ARVP implementation;
- mutable scheduler/runtime state as canonical Git state.

### `jannekbuengener/agent-brain`

Role: generic knowledge, context, evidence, decision, memory and retrieval infrastructure for agents.

Owns product-neutral Agent Brain capabilities under its own repository canon, including the Improvement Blackboard implementation (contracts, observation/management ports, storage, projection).

Does not own:

- GitHub or repository live truth;
- workforce identity, authority or routing policy (including Board Manager role authorization);
- product/application state in consumer repositories;
- ARVP validation/evaluation contracts.

Agent Brain is shared context/evidence infrastructure, not an implicit mandatory runtime dependency. Use it only when a target repository or authorized orchestration contract explicitly routes to it.

Improvement Blackboard observation and management writes are Agent Brain domain
capabilities routed by Workforce Capability IDs
(improvement_observation_write, improvement_management_write). Workforce
authorizes **who** may request those capabilities (Improvement Board Manager);
Agent Brain owns the blackboard implementation. General Memory/Knowledge write
authority is not implied. Quality Scout, Process Scout, and Supervisor remain
denied for those write capabilities.

## METATOOLS

### `jannekbuengener/arvp`

Role: domain-neutral deterministic validation, evaluation, gates and evidence framework.

Owns its portable validation/evaluation contract surface, including deterministic identities, metrics, comparisons, PASS/FAIL/HOLD gates, provenance, stability and Evidence Bundle contracts.

Does not own:

- product behavior;
- workforce routing or authority;
- Agent Brain knowledge/memory/retrieval behavior;
- domain-specific consumer runtime state.

ARVP may support acceptance when the owning repository explicitly adopts it. ARVP evidence never replaces target-repository canon, CI or release authority.

## Routing and authority

Use this order:

```text
TASK INTENT
    ↓
GITHUB / REPOSITORY LIVE STATE
    ↓
OWNING TARGET REPOSITORY
    ↓
TARGET REPOSITORY LOCAL AUTHORITY
    ↓
OPTIONAL RELEVANT META LAYER / METATOOL
    ↓
WORK + VALIDATION
```

Rules:

1. Meta membership never grants authority to override a target repository.
2. Do not route implementation into a meta repository merely because it is globally relevant.
3. `agent-workforce` defines workforce behavior, not product truth.
4. `agent-brain` supplies context/evidence capabilities, not live-state authority.
5. `arvp` supplies deterministic validation/evidence capabilities, not product ownership.
6. No repository listed here becomes an implicit runtime dependency of another repository.
7. Volatile facts such as branch SHAs, issue status, CI state or scheduler state do not belong in this topology contract.
8. The Improvement Board Manager is a Workforce specialist role only; it does not
   move product ownership into gent-workforce and does not grant scouts or the
   Supervisor blackboard Management Write or GitHub Issue Create.

## Relationship to the monitored portfolio

This topology classifies shared repositories by architectural role. It does not define which repositories are currently monitored by the workforce.

Current monitored membership is owned exclusively by [`portfolio/REPOSITORIES.md`](../portfolio/REPOSITORIES.md).

Machine-readable routing facts for these and other spawn-point repositories live in [`routing/REPOSITORY_ROUTING.yml`](../routing/REPOSITORY_ROUTING.yml) ([contract](REPOSITORY_ROUTING.md)). Capability/skill source pointers remain in [`routing/REPOSITORY_CAPABILITY_SOURCES.yml`](../routing/REPOSITORY_CAPABILITY_SOURCES.yml).
