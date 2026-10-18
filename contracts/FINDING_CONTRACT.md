# Finding Contract V1

## Identity

A finding represents one underlying root cause or recurring work-pattern identity, not one observation event.

Stable id format:

`health:<repo-slug>:<root-cause-slug>`

Both components use lowercase kebab-case. Example: `health:sample-brain:stale-workflow-docs`.

If both scouts observe the same underlying condition, they reuse the same finding id. A new lens does not create a new identity.

## Required fields

- `finding_id`
- `repo`
- `scout`
- `category`
- `summary`
- `evidence`
- `severity`
- `confidence`
- `first_seen`
- `last_seen`
- `recurrence`
- `suggested_action`
- `suggested_owner`
- `disposition`

## Vocabularies

Severity:

`INFO | LOW | MEDIUM | HIGH | CRITICAL`

Confidence:

`LOW | MEDIUM | HIGH`

Lifecycle:

`NEW | RECURRING | WORSENED | IMPROVED | RESOLVED | NO_MATERIAL_CHANGE`

Disposition:

`OBSERVE | FOLLOW_UP_RECOMMENDED | OWNER_DECISION_REQUIRED | ACCEPTED_RISK | RESOLVED`

## Evidence rules

- Cite current, inspectable evidence whenever possible.
- Historical Health Book comments provide lineage, not current truth.
- Chat memory is never sufficient evidence for current repository state.
- Recurrence increases only when materially new evidence confirms the same root cause again.
- Absence of a new complaint is not evidence of resolution; resolution requires current confirming evidence.
- A blocked tool/repository/authority state is a run outcome, not a finding.

## Deduplication

Before creating a new finding, inspect unresolved Health Book findings for semantic root-cause overlap. Reuse the existing id when the underlying cause is the same, even if symptoms differ slightly.

If root-cause identity cannot be determined confidently, do not guess. Use `BLOCKED_AUTHORITY_AMBIGUOUS` or record the observation without creating a stable finding until the evidence is sufficient.

## Follow-up linkage

When a scout recommends a separate implementation issue, the recommendation must name the finding id it would resolve. V1 scouts do not create that issue automatically.
