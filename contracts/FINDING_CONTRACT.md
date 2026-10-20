# Finding Contract V1.1

## Identity

A finding represents one underlying root cause or recurring work-pattern identity, not one observation event.

Stable id format:

`health:<repo-slug>:<root-cause-slug>`

Both components use lowercase kebab-case. Example: `health:sample-brain:stale-workflow-docs`.

If both scouts observe the same underlying condition, they reuse the same finding id. A new lens does not create a new identity.

## Required fields

Every `FINDING DELTA` uses exactly these required fields:

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
- `lifecycle`
- `suggested_action`
- `suggested_owner`
- `disposition`

## Vocabularies

Category:

`CORRECTNESS | VALIDATION | CI | SECURITY | DEPENDENCY | ARCHITECTURE | OWNERSHIP | DOCUMENTATION | PROCESS | AUTOMATION | OTHER`

Use exactly one primary category. It describes the root cause / work-risk class, not the Scout identity.

Severity:

`INFO | LOW | MEDIUM | HIGH | CRITICAL`

Confidence:

`LOW | MEDIUM | HIGH`

Lifecycle:

`NEW | RECURRING | WORSENED | IMPROVED | RESOLVED | NO_MATERIAL_CHANGE`

Disposition:

`OBSERVE | FOLLOW_UP_RECOMMENDED | OWNER_DECISION_REQUIRED | ACCEPTED_RISK | RESOLVED`

## Time semantics

- `first_seen` is set when the stable finding is first established and remains unchanged afterwards.
- `last_seen` changes only when materially new evidence confirms or changes the same finding.
- `recurrence` increases only on materially new confirming evidence.
- A checkpoint-only run does not change `first_seen`, `last_seen`, `recurrence`, lifecycle, severity, confidence, or disposition.

## Evidence rules

- Cite current, inspectable evidence whenever possible.
- Historical Health Book comments provide lineage, not current truth.
- Chat memory is never sufficient evidence for current repository state.
- Absence of a new complaint is not evidence of resolution; resolution requires current confirming evidence.
- Tool, repository, authority, identity, or checkpoint blocking states are run outcomes, not findings.

## Deduplication

Before creating a new finding, inspect unresolved Health Book findings for semantic root-cause overlap. Reuse the existing id when the underlying cause is the same, even if symptoms differ slightly.

If the material deviation is clear but root-cause / stable finding identity cannot be determined confidently, do not guess and do not invent an id. Use:

`BLOCKED_FINDING_IDENTITY_AMBIGUOUS`

`BLOCKED_AUTHORITY_AMBIGUOUS` is reserved only for genuinely unclear authority or ownership.

## Checkpoint separation

Checkpoint comments are operational metadata governed by `contracts/CHECKPOINT_CONTRACT.md`. They are never Finding Deltas, never recurrence evidence, and never a substitute for current repository evidence.

## Follow-up linkage

When a scout recommends a separate implementation issue, the recommendation must name the finding id it would resolve. V1.1 scouts do not create that issue automatically.
