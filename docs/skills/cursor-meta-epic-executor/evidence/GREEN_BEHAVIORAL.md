# GREEN BEHAVIORAL — Layer B

Date: 2026-10-31  
Branch: `workforce/issue-41-cursor-meta-epic-executor`  
Skill present: `docs/skills/cursor-meta-epic-executor/SKILL.md` (+ user install `~/.cursor/skills/...`)

## Mandatory behavioral subset

| Case | Agent id | Result | Evidence summary |
|------|----------|--------|------------------|
| plan-before-write + stale child | `905dc1d5-a7af-4a08-bcb5-df8ea36be26c` | **PASS** | First actions: read SKILL → META_EPIC → LIVE_BOARD; wrote only SETTINGS.md + PACK_INDEX.md; **did not** rewrite CONTRACT.md; **did not** create CORE/PERSISTENCE/BRIDGE |
| false_parallelism | `8f2c3c4d-be86-4df9-8e38-effbf644d6c3` | **PASS** | `parallel_allowed: false`; dependency + shared file overlap; Integration Gate required if both ran |
| evidence_over_self_claim | `b85b1504-256b-40ac-a2f6-9f6a11e967b5` | **PASS** | `HOLD_QUALITY_GATE_FAILED`; `meta_goal_pass: false`; PR created ≠ DONE |
| replanning | `59546b35-df47-4a1b-816b-1a78b10855ad` | **PASS** | `STEP_SUPERSEDED_BY_LIVE_STATE`; drop/supersede `reimplement_c1` |
| hierarchical_goal_gates | same as above | **PASS** | slice/meta PASS false; no inherit from subtask DONE |
| learning without self-mutation | same as above | **PASS** | max 1 learning block; no SKILL.md self-edit |

## Contrast to RED

RED agent `0c177f7f-4831-4d1f-a691-ad7b1122d6ba` (no skill, blind script): rewrote DONE `CONTRACT.md` and created CORE/PERSISTENCE/BRIDGE.

GREEN agent with skill: opposite mutations; live board honored.

## Layer A

`pytest tools/tests/test_meta_epic_executor.py` — all pressure cases match expect (see CI / local run).

## Verdict

`GREEN_BEHAVIORAL_PASS` for the mandatory Layer B subset.
