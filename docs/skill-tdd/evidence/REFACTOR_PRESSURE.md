# REFACTOR pressure — fixture independence bypasses (#48)

```text
STEP_GOAL
Show common rationalizations cannot bypass the fixture-independence rule.

EXPECTED_DELTA
Bypasses 1–4 classify as INVALID / PASS_EXISTING / INCONCLUSIVE as specified.

EVIDENCE
pressure_cases.yml bypass_* + unittest assertions.

BOUNDARY
Do not expand into executor product rules.

NEXT_GATE
Independent read-only review.
```

| Bypass | Temptation | Expected | Result |
|---|---|---|---|
| 1 | Near-identical paraphrase without literal copy | `RED_FIXTURE_INVALID` (SEMANTIC) | match |
| 2 | Agent PASSed — sharpen prompt to force RED fail | stay `RED_PASS_EXISTING_BEHAVIOR`; ignore force | match |
| 3 | Strip real authority so agent fails | `RED_INCONCLUSIVE` | match |
| 4 | Adversarial that states the ban (= rule under test) | `RED_FIXTURE_INVALID` | match |

```text
ACTUAL_EVIDENCE
bypass_1..4 in evaluate_all() match expect.

GOAL_DELTA
REFACTOR pressure held.

BOUNDARY_CHECK
PASS

OUTCOME
STEP_PASS
```
