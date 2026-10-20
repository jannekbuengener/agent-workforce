# Repo Health Book Template

Suggested issue title:

`[OPS][HEALTH] Repo-Health-Book — fortlaufende Qualitäts- und Prozessevidenz`

Existing Health Book issues do not need to be renamed solely for this template update.

## Canonical issue body

```markdown
# Repo Health Book

Purpose: long-lived repo-local evidence ledger for the Agent Workforce V1.1 Quality Scout and Process Scout.

This issue is operational evidence, not implementation scope. Current GitHub/repo live state and repo-local canon remain authoritative over historical comments.

Canonical workforce authority:
- `jannekbuengener/agent-workforce/README.md`
- `jannekbuengener/agent-workforce/agents/quality-scout.md`
- `jannekbuengener/agent-workforce/agents/process-scout.md`
- `jannekbuengener/agent-workforce/contracts/CHECKPOINT_CONTRACT.md`
- `jannekbuengener/agent-workforce/contracts/FINDING_CONTRACT.md`
- `jannekbuengener/agent-workforce/templates/REPO_HEALTH_BOOK.md`

Rules:
- first visit by each Scout writes one `INITIAL BASELINE` comment;
- later normal evidence comments contain only material `FINDING DELTA` output;
- same root cause reuses the same stable finding id across both Scouts;
- `SKIP_NO_DELTA` creates no normal evidence comment;
- unchanged `NO_MATERIAL_CHANGE` creates no normal evidence comment;
- the acting Scout still updates its single mutable checkpoint after a completed deep inspection;
- checkpoint comments are operational metadata and never count as Baseline/Finding output or recurrence evidence;
- unchanged recurring findings are not reposted only because another scheduled run occurred;
- Scouts may recommend follow-up work but V1.1 does not create implementation issues/PRs automatically;
- tool/access/checkpoint/budget failures are operational outcomes, not repo defects.
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
- Repo: `<owner/repository>`
- Scout: `<agent_id>`
- Category: `CORRECTNESS | VALIDATION | CI | SECURITY | DEPENDENCY | ARCHITECTURE | OWNERSHIP | DOCUMENTATION | PROCESS | AUTOMATION | OTHER`
- Severity: `INFO | LOW | MEDIUM | HIGH | CRITICAL`
- Confidence: `LOW | MEDIUM | HIGH`
- First seen: `<ISO-8601 timestamp>`
- Last seen: `<ISO-8601 timestamp>`
- Recurrence: `<integer>`
- Lifecycle: `NEW | RECURRING | WORSENED | IMPROVED | RESOLVED | NO_MATERIAL_CHANGE`
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

The field set and vocabularies above are governed by `contracts/FINDING_CONTRACT.md`.

## Scout checkpoint comment

Use exactly the marker/fields/update semantics from `contracts/CHECKPOINT_CONTRACT.md`.

A Health Book contains at most one active checkpoint per Scout identity. Do not duplicate the checkpoint contract here.

Checkpoint comments are excluded from Baseline/Finding accounting and from Supervisor Scout-output review.

## Silence rules

`SKIP_NO_DELTA` produces no normal evidence comment.

Routine unchanged `NO_MATERIAL_CHANGE` produces no normal evidence comment. Use a Finding Delta only when current evidence creates, confirms materially, worsens, improves, resolves, or reclassifies an existing finding.

A completed deep inspection still updates the acting Scout checkpoint so selection state remains deterministic without adding evidence noise.
