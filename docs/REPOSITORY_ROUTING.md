# Repository Routing

## Purpose

This contract defines Agent Workforce's thin **portfolio routing** surface for cross-repository spawn-point decisions.

It answers:

1. Which repositories are **routable** for identity, ownership and frontdoor decisions?
2. What stable **system role**, **owns / does-not-own**, and directional **relationships** apply?
3. Where is each repository's **local authority** frontdoor?
4. Whether a machine-readable **capability/skill source** is declared, and where?

It does **not** become an org database, a second copy of repo-local AGENTS/README/skill bodies, or Scout monitoring membership.

## Architecture

```text
WORKFORCE_BOOTSTRAP
        ↓
routing/REPOSITORY_ROUTING.yml          ← stable routing facts
        ↓
routing/REPOSITORY_CAPABILITY_SOURCES.yml  ← capability/skill pointers only
        ↓
Target Repository Local Authority
        ↓
generated/PORTFOLIO_CAPABILITY_INDEX.yml   ← derived discovery data
```

| Artifact | Role |
|---|---|
| [`routing/REPOSITORY_ROUTING.yml`](../routing/REPOSITORY_ROUTING.yml) | Hand-authored routing topology: identity, role, ownership, relationships, frontdoors |
| [`routing/REPOSITORY_CAPABILITY_SOURCES.yml`](../routing/REPOSITORY_CAPABILITY_SOURCES.yml) | Pointer contract: where capability/skill authority lives |
| [`generated/PORTFOLIO_CAPABILITY_INDEX.yml`](../generated/PORTFOLIO_CAPABILITY_INDEX.yml) | Derived discovery view only |
| [`portfolio/REPOSITORIES.md`](../portfolio/REPOSITORIES.md) | Monitored Scout portfolio membership only |
| [`docs/META_TOPOLOGY.md`](META_TOPOLOGY.md) | Shared meta/metatool classification prose |

## Hard separations

```text
routable repository != monitored workforce repository
global workforce capability != repository-local capability
Capability != Provider != Skill != Tool != Execution Surface != Authority
```

- **Monitored** membership is owned exclusively by `portfolio/REPOSITORIES.md`. This routing file must not dual-write `monitored`.
- **Capability source pointers** stay in `REPOSITORY_CAPABILITY_SOURCES.yml`. Routing may reference them by portable identity (`capability_source`) or record `capability_discovery: missing_machine_readable_source`.
- **Role / relationships / owns** belong here, not in the capability-sources contract.

## Field rules

Include only stable facts that improve routing:

- `portable_identity`
- `system_role`
- `owns` / `does_not_own` (short evidence-backed summaries)
- directional `relationships` when routing-relevant
- `local_authority` frontdoor and closely related entry docs
- `capability_source` portable identity or `null`
- `capability_discovery` when no machine source exists
- compact `routing_notes`

Do **not** store volatile branch SHAs, open issue/PR counts, CI state, or release versions as durable authority.

Ownership and relationships must be evidence-backed from live target-repository canon (or the shared meta topology for workforce/meta roles) and must keep a clear producer/consumer or support direction.

## Sample Brain ownership (mandatory)

```text
sample-brain-analysis
  owns deterministic Analysis computation + Analysis contracts/package behavior
  ↓ versioned released package
sample-brain
  owns product integration, persistence/catalog, Workbench/UI, consumer acceptance
```

Analysis package defects route to `sample-brain-analysis`. Consumer/integration defects stay in `sample-brain`.

## Validation

```text
python tools/check_repository_routing.py
python tools/generate_portfolio_capability_index.py --repo-root owner/name=PATH
python tools/check_portfolio_capability_drift.py --repo-root owner/name=PATH
python -m unittest tools.tests.test_portfolio_capability_discovery tools.tests.test_repository_routing -v
```

Sibling checkouts next to this repository are auto-discovered for known source identities when `--repo-root` is omitted. Active external sources still fail closed when their checkout cannot be resolved.

## Relevance gate

Consult this routing surface when cross-repository ownership, spawn-point, or meta/metatool routing is materially relevant. Do not bulk-load every local authority document solely because a routing row exists.
