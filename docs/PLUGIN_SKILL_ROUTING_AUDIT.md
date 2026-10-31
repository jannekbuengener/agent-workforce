# Plugin / Skill Routing Audit

## Purpose

Evidence-backed audit of known orchestrator/plugin consumers against
[`contracts/PLUGIN_SKILL_ROUTING_CONTRACT.md`](../contracts/PLUGIN_SKILL_ROUTING_CONTRACT.md).

Rules:

- audit only with real source evidence;
- never invent plugin state from chat memory;
- mark missing sources as `SOURCE_UNAVAILABLE` / `NOT_EVALUATED`;
- do not migrate plugin packages inside `agent-workforce`;
- do not record private MCP endpoints, host paths, tokens, or connector secrets.

## Audit checklist

For each consumer with available source:

1. `kind` clear (`global_router` / `specialist` / `project_orchestrator` / `execution_provider`)?
2. Capability IDs used instead of hard-wired plugin names?
3. Workforce requirement levels reused (`REQUIRED` / `DISCOVERY_REQUIRED` / `PREFERRED` / `ADVISORY`)?
4. Positive triggers and exclusions / `does_not_own` present?
5. `claims_global_routing` consistent with `kind`?
6. Repo-local skills discovered rather than copied?
7. Private MCP treated as ChatGPT-only surface, never as worker capability?
8. REQUIRED capabilities not silently substituted?
9. Exit condition declared?

## Matrix

| Consumer | Status | Source evidence | Notes |
|---|---|---|---|
| Security Business MiroFish | `EVALUATED` | `jannekbuengener/security-business` live tree `integrations/chatgpt-mirofish/` containing `plugin.json`, `mcp.json`, and `skills/` | Domain specialist for Security Business MiroFish simulation/analysis. MCP exists as a ChatGPT/plugin execution surface and is **not** a worker capability. No private MCP endpoints, tokens, or connector details recorded here. Does not claim global Workforce routing. Gap: does not yet declare Workforce Capability IDs via the consumer contract. No migration in this repository. |
| Agent Capability Router | `SOURCE_UNAVAILABLE` | No plugin package / `plugin.json` found in accessible repos or Drive for this audit | Design hypothesis (global capability router) remains unproven. |
| Reverse Engineering Orchestrator | `SOURCE_UNAVAILABLE` | No plugin package found | Design hypothesis (specialist over `reverse_engineering`) remains unproven. |
| Sample Brain Orchestrator | `SOURCE_UNAVAILABLE` | No ChatGPT plugin package found | Do not confuse with repo-local Cursor agent `sample-brain-control-orchestrator` in Sample Brain; that is not ChatGPT plugin evidence for this matrix. |
| Jules Supervisor | `SOURCE_UNAVAILABLE` | No plugin package found | Design hypothesis (execution provider with narrow explicit trigger) remains unproven. |
| cursor-meta-epic-executor | `EVALUATED` | `jannekbuengener/agent-workforce` `docs/skills/cursor-meta-epic-executor/` (`SKILL.md` + skill-colocated `consumer.yml`) | Cursor `project_orchestrator` for already-defined Meta-Epics (#41). Capability IDs optional (`reuse_before_build` DISCOVERY_REQUIRED, `deterministic_validation` PREFERRED). Does not claim global routing. Private MCP never a worker dependency. Consumer pack is skill-colocated intentionally — not a new `capabilities/consumers/` inventory tree. |
| evidence-backed-delivery | `EVALUATED` | `jannekbuengener/agent-workforce` `docs/skills/evidence-backed-delivery/` (`SKILL.md` + skill-colocated `consumer.yml`) | Cursor `project_orchestrator` for global Issue→PR→Evidence→Merge→Close (#43). Optional Capability IDs (`reuse_before_build` DISCOVERY_REQUIRED, `deterministic_validation` PREFERRED). Does not claim global routing. Does not replace target-repo merge authority or CDB acceptance skills. Private MCP never a worker dependency. |

## MiroFish architecture boundary (evidence-backed)

Observed on `security-business` main:

- real Desktop plugin package under `integrations/chatgpt-mirofish/`;
- plugin metadata (`plugin.json`), local MCP wiring (`mcp.json`), and at least one skill under `skills/`;
- purpose is Security Business MiroFish simulation operation/analysis;
- synthetic simulation output is not customer evidence (repo-local business canon).

Workforce conclusion:

```text
MiroFish MCP surface = ChatGPT/plugin only
MiroFish MCP surface != worker capability
MiroFish MCP surface != worker requirement
```

Follow-up (outside #34): migrate the plugin's routing declaration to Capability IDs under Security Business plugin authority when ready.

## Non-evaluations

`SOURCE_UNAVAILABLE` rows are intentionally empty of design speculation presented as fact.
Issue #34 must not canonicalize invented plugin state into GitHub.
