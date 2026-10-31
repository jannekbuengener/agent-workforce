# Skill-TDD — RED Fixture Independence Contract

## Purpose

Generic Agent Workforce quality rule for skill authoring and Skill-TDD:

> **RED pressure fixtures must not pre-supply the behavior under test.**

A RED run must show what the agent does **without** the new/updated skill
rule. If the fixture already states or paraphrases that rule, the run tests
the prompt — not the skill.

This contract is methodology for skill authors and reviewers. It is not a
product runtime, not an agent-invokable delivery skill, and not
target-repository product canon.

Front door: [`docs/SKILL_TDD.md`](../docs/SKILL_TDD.md)  
Checklist: [`docs/skill-tdd/references/fixture_independence_checklist.md`](../docs/skill-tdd/references/fixture_independence_checklist.md)  
Pressure cases: [`docs/skill-tdd/references/pressure_cases.yml`](../docs/skill-tdd/references/pressure_cases.yml)  
Machine twin: [`tools/skill_tdd_red_fixture_lib.py`](../tools/skill_tdd_red_fixture_lib.py)

## Core invariant

```text
TEST TARGET RULE
      ↓
REMOVE RULE FROM RED FIXTURE
      ↓
RUN WITHOUT NEW/UPDATED SKILL
      ↓
OBSERVE NATURAL AGENT BEHAVIOR
      ↓
FAIL = VALID RED SIGNAL (RED_FAIL_OBSERVED)
PASS = investigate native / existing-skill coverage
       (RED_PASS_EXISTING_BEHAVIOR → may be NO_SKILL_CHANGE_REQUIRED)
LEAKED / UNREALISTIC FIXTURE = not countable (RED_FIXTURE_INVALID)
```

Hard rule: if the RED prompt explicitly states or semantically pre-empts the
rule under test, the run must not count as proof of skill effectiveness.

## Fixture Independence checklist (required before RED)

```text
RULE_UNDER_TEST
Which concrete behavior should the skill supply?

FIXTURE_TEXT
What does the agent receive without the new/updated skill rule?

LEAK_CHECK
Is the rule already present explicitly or semantically in the fixture?
  NONE | EXPLICIT | SEMANTIC

REALISM_CHECK
Was natural authority/context artificially removed only to force a fail?
  REALISTIC | UNREALISTIC_OMISSION

RED_VALIDITY
Can the outcome be causally attributed to the agent / existing skill,
or did the fixture dictate it?
```

`LEAK_CHECK` other than `NONE` → outcome `RED_FIXTURE_INVALID`; baseline
does not count.

## Pressure lanes

### Soft / Naturalistic

Realistic task. No target rule. No artificial bans that encode the rule.

Purpose: observe natural decisions; check whether the gap is real.

### Adversarial

Raise decision pressure (time, sunk cost, convenience, scope, close-out,
reviewer/CI pressure) **without revealing the target rule**.

Adversarial ≠ writing the correct answer (or “do not do X” when X **is**
the rule under test) into the prompt.

## RED outcomes

```text
RED_FAIL_OBSERVED
RED_PASS_EXISTING_BEHAVIOR
RED_FIXTURE_INVALID
RED_INCONCLUSIVE
```

| Outcome | Meaning |
|---|---|
| `RED_FAIL_OBSERVED` | Clean fixture; agent violates the target invariant → valid skill-gap RED. |
| `RED_PASS_EXISTING_BEHAVIOR` | Clean fixture; agent already correct → skill change may be unnecessary (`NO_SKILL_CHANGE_REQUIRED` is legitimate). |
| `RED_FIXTURE_INVALID` | Rule leaked (explicit/semantic) and/or unrealistic omission broke causality → not countable. |
| `RED_INCONCLUSIVE` | Outcome not cleanly attributable to skill / native behavior / fixture. |

There is **no** dogma that RED must always fail. An unexpected clean PASS is
evidence, not an automatic test failure.

## Deterministic twin vs review

The machine twin validates structure and declared classification consistency
(required fields, enums, outcome coherence, optional explicit-substring
support for direct leaks).

**Semantic leakage is primarily a behavioral / human-review judgment.**
Do not treat regex or paraphrase matching as a complete proof of semantic
leak absence. Authors must set `leak_check: SEMANTIC` when a paraphrase
still hands the agent the rule.

## Historical evidence

[#44](https://github.com/jannekbuengener/agent-workforce/issues/44) /
[`docs/skills/cursor-meta-epic-executor/evidence/RED_HOST_VISUAL.md`](../docs/skills/cursor-meta-epic-executor/evidence/RED_HOST_VISUAL.md):

- Run A — fixture already spelled settle / min-geometry / no-auto-judge →
  HOLD despite skill silence → **fixture leak masked the gap**.
- Run B — rule removed from fixture → agent self-PASS → true
  `RED_FAIL_OBSERVED`.

That learning is generalized here; it is not re-implemented as
executor product logic.

## Non-goals

- No new LLM/agent test runtime or control plane.
- No product-specific fixture rules in this global contract.
- No requirement to force every RED to fail.
- No change to `cursor-meta-epic-executor` behavior beyond optional
  references to this shared contract.
