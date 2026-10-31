# GREEN — Skill-TDD RED fixture independence (#48)

```text
STEP_GOAL
Prove cases A–F + bypasses classify correctly under the new contract twin.

EXPECTED_DELTA
All skill-tdd pressure cases match expect; existing skill twins remain green.

EVIDENCE
python -m unittest tools.tests.test_skill_tdd_red_fixture
python -m unittest tools.tests.test_meta_epic_executor
python -m unittest tools.tests.test_evidence_backed_delivery

BOUNDARY
No executor product logic. No sample-brain rules.

NEXT_GATE
REFACTOR pressure + independent review.
```

## Cases A–F

| Case | Expected | Twin outcome |
|---|---|---|
| A direct leak | `RED_FIXTURE_INVALID` | match |
| B semantic leak | `RED_FIXTURE_INVALID` | match (author-declared; not regex-only) |
| C clean soft fail | `RED_FAIL_OBSERVED` | match |
| D existing correct | `RED_PASS_EXISTING_BEHAVIOR` + no forced skill change | match |
| E adversarial non-leak | valid behavioral evidence (`RED_FAIL_OBSERVED`) | match |
| F unrealistic omission | `RED_FIXTURE_INVALID` | match |

Historical #44 Run A reclassified as `RED_FIXTURE_INVALID` via
`historical_44_run_a_fixture_leak`.

```text
ACTUAL_EVIDENCE
unittest tools.tests.test_skill_tdd_red_fixture (and sibling skill twins).

GOAL_DELTA
GREEN for A–F + structural docs.

BOUNDARY_CHECK
PASS

OUTCOME
STEP_PASS
```
