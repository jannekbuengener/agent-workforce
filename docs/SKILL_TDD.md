# Skill-TDD — Workforce front door

## Purpose

How Agent Workforce authors prove skill changes with **RED → GREEN → REFACTOR**
without confusing prompt compliance for skill effectiveness.

## Canonical rule (#48)

> RED pressure fixtures must not pre-supply the behavior under test.

Contract:

```text
contracts/SKILL_TDD_RED_FIXTURE_INDEPENDENCE_CONTRACT.md
```

Checklist:

```text
docs/skill-tdd/references/fixture_independence_checklist.md
```

Pressure cases (A–F + bypass):

```text
docs/skill-tdd/references/pressure_cases.yml
```

Deterministic twin (structure + declared classification; not full semantic proof):

```text
tools/skill_tdd_red_fixture_lib.py
python -m unittest tools.tests.test_skill_tdd_red_fixture
```

## Dual lanes

| Lane | What it is | What it is not |
|---|---|---|
| Soft / naturalistic | Realistic task; observe natural gap | Artificial bans that encode the target rule |
| Adversarial | Pressure without revealing the rule | “Here is the correct policy — obey it” |

## RED outcomes

```text
RED_FAIL_OBSERVED
RED_PASS_EXISTING_BEHAVIOR
RED_FIXTURE_INVALID
RED_INCONCLUSIVE
```

`RED_PASS_EXISTING_BEHAVIOR` may justify `NO_SKILL_CHANGE_REQUIRED`.
Do not sharpen fixtures solely to manufacture a fail.

## Relationship to per-skill twins

Skill-specific Layer-A packs (`docs/skills/*/references/pressure_cases.yml`)
remain product-behavior twins. This contract governs **how RED fixtures for
those skills are designed and classified**. It does not replace them.

## Host skill format note

Cursor Agent Skills remain `SKILL.md` folders with `name` + `description`
frontmatter ([Cursor Skills docs](https://cursor.com/docs/skills)). This
workforce contract does not redefine host packaging; it constrains RED
evidence quality when changing those skills.

## Lineage

- #41 — skill TDD + dual-lane RED note
- #44 / PR #46 — host-visual learning; fixture leak observation
- #48 — this generic fixture-independence rule

Exit: `SKILL_TDD_RED_FIXTURE_INDEPENDENCE_LANDED`
