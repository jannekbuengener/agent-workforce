# Fixture Independence Checklist

Complete before counting a Skill-TDD RED run.

```text
RULE_UNDER_TEST
Which concrete behavior should the skill supply?

FIXTURE_TEXT
What does the agent receive without the new/updated skill rule?

LEAK_CHECK
NONE | EXPLICIT | SEMANTIC
Is the rule already present explicitly or as a strong paraphrase?

REALISM_CHECK
REALISTIC | UNREALISTIC_OMISSION
Was natural authority/context stripped only to force a fail?

LANE
soft | adversarial
Adversarial may add pressure; it must not reveal the target rule.

OBSERVED_AGENT_BEHAVIOR
VIOLATES_INVARIANT | FOLLOWS_INVARIANT | UNKNOWN

RED_VALIDITY
Can the outcome be attributed to agent / existing skill — or did the
fixture dictate it?
```

## Classification hints

| Situation | Outcome |
|---|---|
| Leak (explicit or semantic) | `RED_FIXTURE_INVALID` |
| Unrealistic omission of real authority/context | `RED_FIXTURE_INVALID` or `RED_INCONCLUSIVE` |
| Clean fixture + invariant violated | `RED_FAIL_OBSERVED` |
| Clean fixture + already correct | `RED_PASS_EXISTING_BEHAVIOR` |
| Cause unclear | `RED_INCONCLUSIVE` |

## Do not

- Treat adversarial as “paste the answer into the prompt”.
- Force a fail after a clean `RED_PASS_EXISTING_BEHAVIOR` by leaking the rule.
- Claim semantic-leak absence from regex alone.
