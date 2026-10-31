# Skill Improvement Blackboard V1 Pilot — Plan

**Issue:** [#52](https://github.com/jannekbuengener/agent-workforce/issues/52)  
**Meta-Epic:** [#54](https://github.com/jannekbuengener/agent-workforce/issues/54)  
**Exit:** `SKILL_IMPROVEMENT_BLACKBOARD_V1_PILOT_PROVEN`

## GOAL INTERPRETATION

Prove the full Skill Learning → Blackboard → Board Manager → GitHub Issue →
PR/Merge → VERIFIED → Markdown Projection path with the Meta-Epic pilot
thresholds, without inventing a second mutable workforce truth or relaxing
Memory/Knowledge read-only boundaries.

## CURRENT STATE

| Slice | Live state |
|---|---|
| Brain #46–#52, #50, #51 | Merged on `agent-brain` main |
| Workforce #50 Board Manager | Merged (PR #60/#62) |
| Workforce #51 GitHub routing | Merged (PR #63) |
| Workforce #52 Pilot | This slice |
| Live GitHub hand-off | [agent-brain#60](https://github.com/jannekbuengener/agent-brain/issues/60) |

## DEPENDENCY GRAPH

```text
Brain contracts/store/dedupe/management/protocol/projection
        → Workforce board-manager + github-issue-create
                → Pilot harness + live issue #60 + PR/Merge + VERIFIED
```

## EXECUTION SLICES

1. Layer-A workforce authority/routing pressure (this pack)
2. Brain V1 pilot pytest harness + CLI `project` export (agent-brain PR for #60)
3. Link #60, merge PR, attach verification → VERIFIED
4. Fill live evidence in `V1_PILOT_EVIDENCE.md` → close #52 / #45 / #54

## reuse_before_build

`REUSE_EXISTING + BUILD_THIN`: reuse `improvement_github_issue_create_lib`,
`improvement_board_authority_lib`, Brain Observation/Management/Projection
primitives. No new DB, service, or Memory write path.

## COMPLETION GATE

All checklist rows in `V1_PILOT_EVIDENCE.md` green with inspectable locators;
classifier `PILOT_PROVEN_*` recorded; Exit string set on Meta-Epic #54.
