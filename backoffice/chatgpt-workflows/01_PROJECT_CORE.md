# Workflows — Project Core (Bootstrap)

> **Live-truth override:** Live Agent Workforce canon and target-repository state override this snapshot whenever they conflict. Treat this document as orientation only, not as frozen operational truth.

## What is this project?

**Workflows — Meta Planning / Execution Workspace**

This ChatGPT project is Jannek’s daily cross-repository planning room. Jannek and ChatGPT structure work across repositories, make decisions, cut slices, route capabilities, and hand work to suitable workers.

**Agent Workforce** (`jannekbuengener/agent-workforce`) is the global spawn point / routing front door.

This project is **not**:

- `gpt-mcp-server`;
- Sample Brain;
- Claire de Binare;
- Traumtänzer;
- Agent Brain;
- ARVP;
- any single product repository.

## Mission

From unstructured ideas, problems, issues, or goals:

```text
understand
→ verify live truth
→ resolve owner / repo / capability
→ decide
→ plan smallest useful slice
→ delegate or execute
→ validate
→ close
```

## Truth model

Static project files in this bundle are **bootstrap only**.

For current cross-repository information, start from live:

```text
jannekbuengener/agent-workforce
main
WORKFORCE_BOOTSTRAP.md
```

Then load further Workforce canon **relevance-gated** as that bootstrap directs.

For product/domain details after routing: target-repository live state and local authority win over Workforce meta knowledge.

## Authority domains

### Agent Workforce owns

- cross-repository selection;
- repository routing;
- capability resolution;
- workforce operating policy;
- plugin / skill consumer routing.

### Target repository owns (after selection)

- domain behavior;
- local implementation;
- local agent / skill rules;
- local contracts;
- product / component truth.

### Execution host (ChatGPT, Cursor, Codex, …)

- executes with host-available tools and evidence;
- overrides neither Workforce routing nor target-repository authority.

## Stable live pointers

Use GitHub identities and repo-relative paths. Do not assume a local workstation checkout path.

| Need | Live pointer |
|------|----------------|
| Workforce spawn / bootstrap | `jannekbuengener/agent-workforce@main/WORKFORCE_BOOTSTRAP.md` |
| Agent operating rules | `AGENTS.md` |
| Meta topology | `docs/META_TOPOLOGY.md` |
| Capability routing | `docs/CAPABILITY_ROUTING.md`, `capabilities/REGISTRY.yml` |
| Repository routing | `docs/REPOSITORY_ROUTING.md`, `routing/REPOSITORY_ROUTING.yml` |
| Capability / skill discovery | `docs/REPOSITORY_CAPABILITY_DISCOVERY.md`, `routing/REPOSITORY_CAPABILITY_SOURCES.yml` |
| Plugin / skill consumers | `contracts/PLUGIN_SKILL_ROUTING_CONTRACT.md` |

Do not copy those documents into this bundle. Point and load live.

## What does not belong here

Do not hard-code drifting inventories into this project:

- full repository inventories;
- skill lists;
- plugin lists;
- capability tables;
- current SHAs;
- issue counts;
- release versions;
- workstation-specific absolute paths.

When those facts matter, verify them live through Agent Workforce and the target repository.
