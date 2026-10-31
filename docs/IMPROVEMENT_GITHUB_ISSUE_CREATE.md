# Improvement GitHub Issue Create (stub)

## Status

`STUB — owned by workforce issue #51`

This document is the Workforce-owned **Capability contract pointer** for
Capability ID `improvement_github_issue_create`. It does **not** yet authorize
live issue creation.

## Purpose

Bound GitHub implementation-issue creation for validated Improvements so that:

- only the Improvement Board Manager specialist may request this capability;
- Quality Scout, Process Scout, and Workforce Supervisor remain denied;
- Management Write never silently upgrades into GitHub mutation;
- target-repository authority wins for ownership and title/body rules.

## Authoritative follow-up

Full preconditions, idempotency, issue body lineage, and tests are defined by:

- https://github.com/jannekbuengener/agent-workforce/issues/51

Until #51 lands and its acceptance criteria are evidenced:

```text
improvement_github_issue_create → HOLD / GITHUB_ISSUE_CREATE_DEFERRED
```

Do not invent a second mutable workforce runtime database for issue-create state.
Idempotency and work-item linkage belong with the owning blackboard / GitHub live
state under the #51 contract.

## Relationship to other capabilities

```text
improvement_read
  < improvement_observation_write
  < improvement_management_write
  < improvement_github_issue_create   # this contract — separate gate
```

`shared_context_evidence` alone never satisfies this capability.
