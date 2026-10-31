# Placement decision — #48 RED fixture independence

```text
STEP_GOAL
Decide the smallest stable placement for a generic Skill-TDD rule:
RED pressure fixtures must not pre-supply the behavior under test.

EXPECTED_DELTA
Documented PLACEMENT_DECISION with reuse_before_build outcome before mutation.

EVIDENCE
This file + live search of contracts/, docs/, docs/skills/, tools/.

BOUNDARY
No executor product logic. No sample-brain rules. No new agent-test runtime.

NEXT_GATE
RED baseline against current workforce structure.
```

```text
PLACEMENT_DECISION
Existing reusable primitive:
  Per-skill Layer-A pressure_cases.yml + contract-twin libs
  (cursor-meta-epic-executor, evidence-backed-delivery).
  Shared contracts/ + docs/ front-door pattern (#43).
  Historical #44 RED_HOST_VISUAL Run A/B evidence of fixture leak.

Chosen location:
  contracts/SKILL_TDD_RED_FIXTURE_INDEPENDENCE_CONTRACT.md  (canon)
  docs/SKILL_TDD.md                                         (front door)
  docs/skill-tdd/references/fixture_independence_checklist.md
  docs/skill-tdd/references/pressure_cases.yml              (A–F + bypass)
  tools/skill_tdd_red_fixture_lib.py + tools/tests/...      (deterministic twin)

Why:
  No generic Skill-TDD surface existed on main (probe: zero hits for
  RED_FIXTURE_INVALID / RED_PASS_EXISTING_BEHAVIOR / RULE_UNDER_TEST).
  Rule is authoring/methodology — not an agent-invokable product skill —
  so a contract + checklist + Layer-A twin matches #43 shape without a
  new SKILL.md / consumer pack / control plane.

Rejected alternatives:
  - Fold only into cursor-meta-epic-executor: not generic; violates #48 scope.
  - New agent-test runtime / LLM harness: non-goal; overbuild.
  - Regex-only semantic-leak detector as sole proof: forbidden by acceptance.
  - Full agent skill + consumer.yml: unnecessary for a testing-quality rule.

reuse_before_build outcome:
  REUSE_EXISTING (pressure-case + contract-twin pattern) + BUILD_THIN_CONTRACT
  No new dependency. No new subsystem beyond shared contract + twin.
```

```text
ACTUAL_EVIDENCE
Live main probe 2026-10-31: 0 hits for fixture-independence outcomes;
meta_epic / evidence_backed_delivery twins have no leak classifier.

GOAL_DELTA
Placement decided; ready for RED.

BOUNDARY_CHECK
PASS — no product/executor mutation in this step.

OUTCOME
STEP_PASS
```
