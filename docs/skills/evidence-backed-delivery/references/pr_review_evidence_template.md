# PR Review Evidence Template (global minimum)

```markdown
## Scope
Issue:
Acceptance covered:
Non-goals:

## Final Head
Head SHA:
Base/Main state:

## Automated Validation
- command / check:
- result:

## Review Evidence
- modality:
- artifact / evidence:
- locator_kind: PR_EMBEDDED | GITHUB_ATTACHMENT | WORKFLOW_ARTIFACT | STABLE_REVIEW_URL | LOCAL_ONLY
- what to inspect:
- result: PASS | FAIL | AWAITING_OWNER | NOT_APPLICABLE

## Review / Findings
- open findings:
- resolved findings:

## Dependency / Merge Order
- depends on:
- blocks:
- relation: INDEPENDENT | UPSTREAM_DEPENDENCY | DOWNSTREAM_DEPENDENCY | SAME_AUTHORITY_CONFLICT | OVERLAPPING_WRITER | MERGE_ORDER_UNCLEAR
- required merge order:
- evidence invalidation risk after upstream merge:

## Remaining Risk / Residual Work
...
```

`LOCAL_ONLY` is never sufficient for human-inspectable evidence.
