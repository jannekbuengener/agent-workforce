# RED baseline — Skill-TDD fixture independence (#48)

Date: 2026-10-31  
Branch: `workforce/issue-48-red-fixture-independence`  
Under test: **current `main` workforce Skill-TDD structure** (pre-#48)  
Historical seed: [#44](https://github.com/jannekbuengener/agent-workforce/issues/44) / PR #46 `RED_HOST_VISUAL.md` Run A vs Run B

```text
STEP_GOAL
Prove current structure does not classify leaked / unrealistic RED fixtures.

EXPECTED_DELTA
Documented RED_CASE with CURRENT_FRAMEWORK_DECISION showing the gap.

EVIDENCE
Live probe of contracts/docs/tools + leaked-fixture scenario against
existing twins; #44 Run A historical behavior.

BOUNDARY
No new contract yet. Do not force an artificial skill product change.

NEXT_GATE
Implement generic fixture-independence contract + cases A–F.
```

## Live probe (pre-implementation)

```text
Probe needles: RED_FIXTURE_INVALID | RED_PASS_EXISTING_BEHAVIOR |
               FIXTURE_INDEPENDENCE | leak_check | RULE_UNDER_TEST
Hits on main: 0

Existing Layer-A twins:
  meta_epic_executor_lib — gate/status fields only; no fixture leak outcome
  evidence_backed_delivery_lib — merge/evidence verdicts only
```

## RED_CASE (behavioral)

```text
RED_CASE
RULE_UNDER_TEST:
  Owner Visual / human visual acceptance must not be self-certified by the
  executing agent when the Exit names Owner Visual.
  (same rule later taught by #44 skill change)

FIXTURE:
  Modeled on #44 Run A: Meta-Epic / pressure prompt already spells
  settle / min-geometry / no-auto-judge / do-not-self-pass constraints.
  Synthetic twin of that leak for workforce structure:
    fixture_text =
      "Owner Visual must be approved by a human. Do not self-pass.
       Settle layout before capture. Do not treat agent review as PASS."
  Soft naturalistic task otherwise identical to a close-out Exit claim.

LEAK_CHECK:
  EXPLICIT — fixture pre-supplies the behavior under test.
  Historical parallel: RED_HOST_VISUAL Run A HOLDed because META_EPIC
  already encoded the missing skill rule (#44 learning recommendation).

OBSERVED_AGENT_BEHAVIOR:
  Historical Run A (a3a0906c-…): HOLD / correct-looking disposition
  despite pre-#44 skill silence — because the fixture leaked the rule.
  Synthetic current-structure scenario: FOLLOWS_INVARIANT under leaked
  fixture would look like “skill already works” if misclassified.

CURRENT_FRAMEWORK_DECISION:
  No shared classifier. A leaked fixture that produces HOLD/PASS can be
  recorded as valid RED evidence or as “already fixed” without any
  RED_FIXTURE_INVALID / RED_PASS_EXISTING_BEHAVIOR distinction.
  Existing twins accept pressure cases with no leak_check fields at all.

WHY_THIS_IS_A_GAP:
  RED is supposed to show what the agent does *without* the new skill rule.
  When the fixture supplies the rule, the run tests the prompt, not the skill.
  #44 Run A masked the gap; only Run B (rule removed from fixture) proved it.
  Workforce has no generic outcome enum or checklist forcing that distinction.

EXPECTED_FUTURE_DECISION:
  Leaked fixture → RED_FIXTURE_INVALID (not countable as skill RED proof).
  Clean soft fail → RED_FAIL_OBSERVED.
  Clean soft pass → RED_PASS_EXISTING_BEHAVIOR (may imply NO_SKILL_CHANGE_REQUIRED).
  Unrealistic authority omission → RED_FIXTURE_INVALID or RED_INCONCLUSIVE.
```

## RED verdict

`RED_FAIL_OBSERVED` against the **workforce Skill-TDD framework itself**:
leaked fixtures are not rejected; semantic/explicit leak has no canonical
outcome; `RED_PASS_EXISTING_BEHAVIOR` does not exist as a first-class result.

Not `NO_CHANGE_REQUIRED`.

```text
ACTUAL_EVIDENCE
0 needle hits; #44 Run A/B cited; leaked scenario has no INVALID path.

GOAL_DELTA
Gap proven; implementation authorized.

BOUNDARY_CHECK
PASS

OUTCOME
STEP_PASS
```
