# Repo Health Book Template

Exact issue title:

`[OPS][HEALTH] Repo Health Book — continuous quality & process evidence`

## Canonical issue body

```markdown
# Repo Health Book

Purpose: long-lived repo-local evidence ledger for the Agent Workforce V1 Quality Scout and Process Scout.

This issue is operational evidence, not implementation scope. Current GitHub/repo live state and repo-local canon remain authoritative over historical comments.

Canonical workforce authority:
- `jannekbuengener/agent-workforce/README.md`
- `jannekbuengener/agent-workforce/agents/quality-scout.md`
- `jannekbuengener/agent-workforce/agents/process-scout.md`
- `jannekbuengener/agent-workforce/contracts/FINDING_CONTRACT.md`
- `jannekbuengener/agent-workforce/templates/REPO_HEALTH_BOOK.md`

Rules:
- first visit by each scout writes one `INITIAL BASELINE` comment;
- later comments contain only material finding deltas;
- same root cause reuses the same stable finding id across both scouts;
- `SKIP_NO_DELTA` creates no comment;
- unchanged `NO_MATERIAL_CHANGE` creates no comment;
- unchanged recurring findings are not reposted only because another scheduled run occurred;
- scouts may recommend follow-up work but V1 does not create implementation issues/PRs automatically;
- tool/access/budget failures are operational outcomes, not repo defects.
```

## Initial Baseline comment

```markdown
## INITIAL BASELINE

- Scout: `<agent_id>`
- Observed at: `<ISO-8601 timestamp>`
- Repo state: `<short live-state summary>`
- Activity level: `ACTIVE | WATCH | DORMANT_POTENTIAL | ARCHIVED`

### Observed quality mechanisms
- ...

### Observed process mechanisms
- ...

### Known strengths
- ...

### Current deviations
- none, or evidence-backed finding references

### Unknown / not yet measurable
- ...

### Recommended observation focus
- ...
```

## Finding Delta comment

```markdown
## FINDING DELTA

- Finding ID: `health:<repo-slug>:<root-cause-slug>`
- Scout: `<agent_id>`
- Observed at: `<ISO-8601 timestamp>`
- Lifecycle: `NEW | RECURRING | WORSENED | IMPROVED | RESOLVED`
- Severity: `INFO | LOW | MEDIUM | HIGH | CRITICAL`
- Confidence: `LOW | MEDIUM | HIGH`
- Recurrence: `<integer>`
- Disposition: `OBSERVE | FOLLOW_UP_RECOMMENDED | OWNER_DECISION_REQUIRED | ACCEPTED_RISK | RESOLVED`

### Summary
...

### Evidence
- ...

### Suggested action
...

### Suggested owner
...
```

## Silence rules

`SKIP_NO_DELTA` produces no comment.

Routine unchanged `NO_MATERIAL_CHANGE` produces no comment. Use a comment only when current evidence creates, confirms materially, worsens, improves, resolves, or reclassifies an existing finding.
