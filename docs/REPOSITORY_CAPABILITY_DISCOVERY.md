# Repository Capability Discovery

## Purpose

This contract defines Agent Workforce's thin discovery layer for repository capability and skill sources.

It answers:

1. Which repositories are **routable** for capability/skill discovery?
2. Where does each repository's capability/skill **authority** live?
3. Which compact capability facts can be derived for selective loading?

It does **not** become a second copy of repo-local skill bodies, contracts, or ownership rules.

## Architecture

```text
WORKFORCE_BOOTSTRAP
        ↓
routing/REPOSITORY_CAPABILITY_SOURCES.yml
        ↓
Target Repository Authority
        ↓
Repo-local Capability Registry / Skill Canon
        ↓
generated/PORTFOLIO_CAPABILITY_INDEX.yml
        ↓
Selective Capability / Skill Loading
```

| Artifact | Role |
|---|---|
| [`routing/REPOSITORY_ROUTING.yml`](../routing/REPOSITORY_ROUTING.yml) | Stable routing topology: role, ownership, relationships, frontdoors |
| [`routing/REPOSITORY_CAPABILITY_SOURCES.yml`](../routing/REPOSITORY_CAPABILITY_SOURCES.yml) | Hand-authored pointer contract: where capability/skill authority lives |
| [`generated/PORTFOLIO_CAPABILITY_INDEX.yml`](../generated/PORTFOLIO_CAPABILITY_INDEX.yml) | Derived discovery view only; regenerate to update |
| [`capabilities/REGISTRY.yml`](../capabilities/REGISTRY.yml) | Global workforce capability routing obligations |
| [`portfolio/REPOSITORIES.md`](../portfolio/REPOSITORIES.md) | Monitored Scout portfolio membership only |
| [`docs/REPOSITORY_ROUTING.md`](REPOSITORY_ROUTING.md) | Routing topology contract |

## Hard separations

```text
Capability != Provider != Skill != Tool != Execution Surface != Authority
routable repository != monitored workforce repository
global workforce capabilities != repository-local capabilities
```

- **Monitored** membership is owned exclusively by `portfolio/REPOSITORIES.md`. This discovery contract stores only `routable`.
- **Producer/consumer relationships** and portfolio role taxonomy belong to [`routing/REPOSITORY_ROUTING.yml`](../routing/REPOSITORY_ROUTING.yml), not this pointer contract.
- **Runtime blocked state** does not belong in the durable source contract. Source `status` is only `active` or `planned`. An `active` source that cannot be resolved fails closed in validation.
- **Fixtures** under `tests/fixtures/` exercise adapters only. They must never appear as production `repositories:` entries.

## Authority rules

1. Target-repository local authority outranks workforce discovery data.
2. The generated index **MUST copy `authority` exactly** from the source declaration.
3. The generated index **MUST NOT** transform, interpret, or elevate authority.
4. The generated index is never source of truth for skills, ownership, or mutation permission.

## Source contract (V1)

Minimal per-repository shape:

```yaml
repositories:
  owner/repo:
    portable_identity: owner/repo
    routable: true
    local_authority:
      frontdoor: AGENTS.md
    capability_sources:
      - id: primary
        type: capability_registry_json
        path: docs/operations/CAPABILITY_REGISTRY.json
        discovery: registry_entries
        authority: local_repo
        status: active
```

No absolute workstation paths. No `monitored`, `relationships`, or role enums — those live in the routing topology.

### Supported source types

| `type` | Typical repo pattern | Index section |
|---|---|---|
| `workforce_capability_registry` | Agent Workforce `capabilities/REGISTRY.yml` | `global_capabilities` |
| `capability_registry_json` | Sample Brain `docs/operations/CAPABILITY_REGISTRY.json` | `repository_capabilities` |
| `skill_canon_dir` | Claire de Binare `docs/skills/` | `repository_capabilities` |

Different repo-local formats are supported through adapters. They are not forced into one internal skill format.

## Generated index

[`generated/PORTFOLIO_CAPABILITY_INDEX.yml`](../generated/PORTFOLIO_CAPABILITY_INDEX.yml) is derived discovery data.

```yaml
global_capabilities: []       # workforce routing capabilities
repository_capabilities: []   # repo-local capabilities/skills
```

Do not hand-edit the index. Regenerate it after source or resolved artifact changes.

`global_capabilities` and `repository_capabilities` remain separate. Real repository sources (for example Sample Brain JSON registry and Claire de Binare skill canon) populate `repository_capabilities` after regeneration against live checkouts.

## Commands

Requires Python 3 and PyYAML (sole small optional/dev dependency; see [`requirements-dev.txt`](../requirements-dev.txt)).

```text
python tools/check_repository_routing.py
python tools/generate_portfolio_capability_index.py
python tools/check_portfolio_capability_drift.py
python -m unittest tools.tests.test_portfolio_capability_discovery tools.tests.test_repository_routing -v
```

Optional live checkout mapping (sibling checkouts next to this repo are auto-discovered when omitted):

```text
python tools/generate_portfolio_capability_index.py --repo-root owner/name=PATH
python tools/check_portfolio_capability_drift.py --repo-root owner/name=PATH
```

`jannekbuengener/agent-workforce` resolves to this repository checkout by default.

## Validation

The drift checker fails closed when:

- a source pointer is missing or invalid for an `active` source;
- the index contains a capability without a declared source;
- sources and the committed index drift;
- deleted/renamed sources leave stale index rows;
- an index row mutates or elevates authority;
- schema rejects forbidden fields, absolute paths, or fixture topology leakage;
- global workforce capabilities are mixed into `repository_capabilities` or the reverse.

## Relevance gate

Consult this discovery layer only when cross-repository capability/skill discovery is materially relevant.

Do not bulk-load the generated index or every declared source for ordinary single-repo Scout work that does not need portfolio capability discovery.

After discovering a relevant source pointer, read the target repository's local authority and then the declared local source. Selective loading follows local canon.

## Relationship to capability routing

[`docs/CAPABILITY_ROUTING.md`](CAPABILITY_ROUTING.md) owns when global workforce capabilities such as REA or reuse-before-build must/should/may be used.

This discovery contract owns where repository-local capability/skill authority can be found and how a compact derived index is produced. It does not replace requirement levels, relevance triggers, or blocked outcomes in the global registry.

## Relationship to repository routing

[`docs/REPOSITORY_ROUTING.md`](REPOSITORY_ROUTING.md) owns stable portfolio routing facts (system role, owns/does-not-own, relationships, frontdoors).

This discovery contract owns only capability/skill source pointers and the derived index. Repositories may be routable in the topology without a machine-readable capability source; those rows set `capability_source: null` and `capability_discovery: missing_machine_readable_source` instead of inventing adapters.
