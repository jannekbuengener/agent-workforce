# Skill Improvement Blackboard V1 Pilot Evidence

**Exit:** `SKILL_IMPROVEMENT_BLACKBOARD_V1_PILOT_PROVEN`  
**Meta-Epic:** [agent-workforce#54](https://github.com/jannekbuengener/agent-workforce/issues/54)  
**Pilot issue:** [agent-workforce#52](https://github.com/jannekbuengener/agent-workforce/issues/52)  
**Brain epic:** [agent-brain#45](https://github.com/jannekbuengener/agent-brain/issues/45)

## Classification

`PILOT_PROVEN_EXPAND_BOUNDED` — Happy path proven under fail-closed gates.
GitHub create remains Board-Manager-only with separate capability; no scout
authority expansion; no second mutable workforce ledger.

## Authority map (unchanged)

| Concern | Owner |
|---|---|
| Cross-repo routing / capability IDs / Board Manager governance | Agent Workforce |
| Blackboard contracts, observation/management, storage, projection | Agent Brain |
| Product implementation | Target repository |
| Execution truth for issues/PRs/CI | GitHub / repo live state |
| Markdown/Obsidian | Read-only projection only |

KnowledgeStore / MemoryStore remain read-only. Improvement writes use typed
domain contracts only (`improvement_observation_write`,
`improvement_management_write`, `improvement_github_issue_create`).

## Pilot proof matrix

| Criterion | Evidence |
|---|---|
| 3 Skills | `cursor-meta-epic-executor`, `evidence-backed-delivery`, `reuse-before-build` in `agent-brain` `tests/improvement/test_v1_pilot_e2e.py` |
| 10 Improvement Records | Pilot seeds 10 root causes; sqlite concurrent lane adds 20 more durable records |
| ≥20 Observation Events | 21 in-memory (20 + true-dup); sqlite lane 20 with 0 loss |
| 2 concurrent writers | `ThreadPoolExecutor(max_workers=2)` in both pilot tests |
| 0 lost events | Asserted totals after parallel submit |
| Idempotent retries | Same `idempotency_key` retry does not increase observation count |
| ≥1 true duplicate | Exact `root_cause_key` attaches to one Improvement (`recurrence==3`) |
| Similar-but-different, no false merge | Distinct root cause submitted; `auto_merge_allowed is False`; new Improvement created |
| Authority separation | Observation store lacks management methods; `ManagementActor(role=quality-scout)` raises; workforce gates deny scouts for GitHub create |
| Exactly one routed GitHub Implementation Issue | [agent-brain#61](https://github.com/jannekbuengener/agent-brain/issues/61) created under `improvement_github_issue_create` contract (`GITHUB_ISSUE_CREATED`) |
| PR / Merge evidence | [agent-brain#62](https://github.com/jannekbuengener/agent-brain/pull/62) (CLI export + pilot harness) |
| Verification → VERIFIED | Pilot transitions linked issue/PR/verification work-refs to `VERIFIED` only after explicit `record_verification` |
| Rebuildable Markdown/Obsidian projection | `ImprovementMarkdownProjection.export` + CLI `export-projection`; identical `source_hash` on rebuild |
| No second mutable workforce truth | Gates/idempotency use GitHub live + blackboard; no workforce issue-create DB |
| Memory/Knowledge boundaries | Pilot asserts no `remember` / `brain_write` on observation store; knowledge/memory modules lack observation submit |

## Routed implementation issue

- **Title:** `[IMPL] CLI-Export fuer read-only Improvement-Markdown-Projection ergaenzen`
- **Repo:** `jannekbuengener/agent-brain` (#61)
- **Improvement ID:** `improvement:cursor-meta-epic-executor:pilot-cli-projection-export-missing`
- **Create gate:** `BOARD_MANAGER_GITHUB_ALLOWED` / `GITHUB_ISSUE_CREATED`
- **Create operation id:** `pilot-52-cli-projection-export-v1`
- **closed ≠ VERIFIED:** encoded in issue body lineage field

## How to re-run machine evidence

```text
# agent-brain (from repo root, with [dev] extras)
python -m pytest tests/improvement/test_v1_pilot_e2e.py tests/improvement/test_cli_export_projection.py -q

# workforce routing twin
python -m unittest tools.tests.test_improvement_github_issue_create tools.tests.test_improvement_board_manager_authority -q
```

## Non-goals respected

- No skill self-mutation
- No automatic PR creation by Board Manager role contract
- No bidirectional Obsidian sync
- No scout/Supervisor write promotion
