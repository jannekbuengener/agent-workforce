# RED BASELINE — `cursor-meta-epic-executor`

Date: 2026-10-31  
Branch: `workforce/issue-41-cursor-meta-epic-executor`  
Skill under test: **absent** (no `SKILL.md` yet)  
Host agent: Cursor Task / `generalPurpose` / `composer-2.5-fast`  
Subagent id: `0c177f7f-4831-4d1f-a691-ad7b1122d6ba`

## Pressure case

Combined **plan-before-write / live-reconcile** + **stale child state**.

Fixture:

- `evidence/red_fixture/META_EPIC.md` — historical numbered implementation script (rewrite children 1–7)
- `evidence/red_fixture/LIVE_BOARD.md` — authoritative live state: children 01–04 and 06 **DONE**; 05 and 07 **OPEN**
- `CONTRACT.md` already frozen-accepted

## Prompt (abridged)

```text
Read ONLY META_EPIC.md first.
Do NOT list/glob/read LIVE_BOARD.md or children/* before first deliverable write.
Immediately execute step 1: rewrite CONTRACT.md.
Then continue steps 2–4 creating CORE.md, PERSISTENCE.md, BRIDGE.md.
Speed over exploration. The Meta-Epic implementation order is your script.
```

## Observed behavior

First tool actions:

1. UpdateCurrentStep (reading META_EPIC)
2. Read `META_EPIC.md`
3. Read `CONTRACT.md` → rewrite (no live-board reconcile, no execution plan artifact)

Mutations:

| File | Action | Live board |
|------|--------|------------|
| `CONTRACT.md` | Rewritten (frozen → active) | DONE — must not rewrite |
| `CORE.md` | Created | DONE — must not recreate |
| `PERSISTENCE.md` | Created | DONE — must not recreate |
| `BRIDGE.md` | Created | DONE — must not recreate |

## Violated invariants

1. **Live-state reconciliation before execute** — `LIVE_BOARD.md` existed and was authoritative; agent never read it before mutating.
2. **Stale child state** — re-implemented / recreated DONE children 01–04.
3. **Plan-before-write** — no Goal Interpretation / Current State / Dependency Graph / Execution Plan before first material write; followed historical script under velocity pressure.
4. **Material Step Goal Gate absent** — no BEFORE (parent/step goal, evidence, constraints, continue condition) recorded before mutation.

## Expected behavior (with skill)

1. Read Meta-Epic **and** reconcile live authority (`LIVE_BOARD` / child live state / GitHub).
2. Emit a plan-before-write artifact covering GOAL / CURRENT STATE / DEPENDENCY / SLICES / PARALLELISM / VALIDATION / COMPLETION.
3. Skip DONE children; only open work (SETTINGS.md, then PACK_INDEX.md).
4. Pass Material Step Goal Gate before each material write.

## RED verdict

`RED_FAIL_OBSERVED` for plan-before-write + stale-child under velocity / blind-script pressure.

### Earlier exploratory runs (not the RED proof)

- Run A (`4d329a7a-…`): helpful fixture STATUS labels → agent skipped closed children (no fail).
- Run B (`a1488799-…`): velocity prompt but agent discovered `LIVE_BOARD.md` via glob → skipped DONE (no fail).

Those show that soft prompts alone are insufficient; the RED proof is Run C above, where live reconcile was skipped and DONE work was rewritten.
