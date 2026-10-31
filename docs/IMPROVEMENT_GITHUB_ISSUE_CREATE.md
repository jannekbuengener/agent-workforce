# Improvement GitHub Issue Create

## Status

`ACTIVE — Capability contract for improvement_github_issue_create`

Workforce-owned fail-closed routing contract for Capability ID
`improvement_github_issue_create`. Machine twin:
[`tools/improvement_github_issue_create_lib.py`](../tools/improvement_github_issue_create_lib.py).
Pressure fixtures:
[`tests/fixtures/improvement-github-issue-create/`](../tests/fixtures/improvement-github-issue-create/).

This contract does **not** authorize product PRs, scout/Supervisor issue creation,
or a second mutable workforce runtime database. Idempotency and work-item linkage
use GitHub live state plus Agent Brain blackboard linkage (`link_work_item`), not
a workforce-local issue ledger.

## Purpose

Bound GitHub implementation-issue creation for **validated** Improvements so that:

- only the Improvement Board Manager specialist may request this capability;
- Quality Scout, Process Scout, and Workforce Supervisor remain denied;
- Management Write never silently upgrades into GitHub mutation;
- target-repository authority wins for ownership and title/body rules;
- retries and existing work items do not spam duplicate issues;
- a closed GitHub issue is never treated as automatic `VERIFIED`.

## Authority ladder

```text
improvement_read
  < improvement_observation_write
  < improvement_management_write
  < improvement_github_issue_create   # this contract — separate gate
```

`shared_context_evidence` alone never satisfies this capability.
`improvement_management_write` alone never authorizes GitHub issue creation.

## Authorized role

| Role | `improvement_github_issue_create` |
|---|---|
| Improvement Board Manager (`specialist`, `claims_global_routing: false`) | allowed when all gates below pass |
| Quality Scout | denied |
| Process Scout | denied |
| Workforce Supervisor | denied |

Missing REQUIRED capability / authorization →
`BLOCKED_REQUIRED_CAPABILITY_UNAVAILABLE` or `HOLD`. Never silently substitute
another tool or role.

## Preconditions for `GITHUB_ISSUE_CREATE`

All must be true. Any missing gate → `HOLD` / `OWNER_DECISION_REQUIRED` /
explicit deny — never issue spam.

1. **Lifecycle** — Improvement is at least `VALIDATED`
   (`VALIDATED | PLANNED | IMPLEMENTED`). `NEW`, `RECURRING`, and `CLOSED` are
   denied for create.
2. **Identity** — Root cause / Improvement identity is not ambiguous.
3. **Owner** — Owning repository is uniquely derivable from repo-/skill-/
   workforce authority (not from which agent produced the observation).
4. **No active duplicate** — No already-open work item covers the same
   Improvement-/root-cause scope in that owning repo.
5. **Concrete work** — Proposed work is implementable, not merely
   “weiter beobachten”.
6. **Target authority** — Target repo allows issue creation by the executing
   host/agent.
7. **Title/body policy** — Title/body follow target-repo rules and Workforce
   Policy (German issue titles by default; see
   [`WORKFORCE_POLICY.md`](WORKFORCE_POLICY.md#github-issue-creation)).
8. **Lineage** — Work item receives a stable back-link to `improvement_id`.

## Routing rules

- Owning repo is derived from Skill-/Repository-Authority, never from the
  observation-producing agent.
- Cross-repo improvements may split into multiple work items only when real
  distinct owners exist; each item keeps the same Improvement lineage.
- Governance / workforce policy / routing changes → `agent-workforce`.
- Agent-Brain domain / storage / protocol changes → `agent-brain`.
- Product-specific changes → owning product repository.
- Ambiguous owner → `HOLD` / `HOLD_OWNER_AMBIGUOUS`. Do not invent routing.
- Target-repository authority beats generic workforce assumptions after the
  owning repo is selected.
- This capability is an execution surface, not a second global router
  (`claims_global_routing: false` remains mandatory).

## Issue body lineage fields

Every created implementation issue must include at least:

| Field | Purpose |
|---|---|
| `Improvement ID` | Stable blackboard identity |
| `Root Cause / Problem` | What is wrong |
| `Evidence Summary` | Relevant confirming evidence |
| `Recommended Change` | Concrete implementable change |
| `Expected Benefit` | Why the change matters |
| `Scope / Owner` | Owning repository and bounded scope |
| `Acceptance / Verification` | Observable verification expectation |
| `Improvement Record Ref` | Link/ref to canonical Improvement record |
| `Closed ≠ Verified notice` | Explicit: closing the issue does not auto-`VERIFIED` |

Optional but recommended: parent/meta links, related finding ids, non-goals.

German title rule remains in Workforce Policy; body language may follow the
target repository.

## Idempotency / dedupe

Before create, against GitHub live + blackboard linkage (no workforce DB):

1. Search existing **open and closed** work items with the same
   `improvement_id` (and same owning repo scope).
2. If an **active (open)** work item exists → link/reuse it; do **not** create
   a second issue (`REUSED_EXISTING_WORK_ITEM`).
3. If the same logical `create_operation_id` already produced a work item →
   return that result (`IDEMPOTENT_RETRY_NO_DUPLICATE`); never create again.
4. A prior **closed** work item may be documented as lineage context. A **new**
   `create_operation_id` may create a fresh implementation issue only when all
   other gates still pass — and closing that (or any) issue still never implies
   blackboard `VERIFIED`.

## Rückfluss (closed ≠ verified)

```text
Issue URL/Number  → Agent Brain link_work_item
PR / Merge        → IMPLEMENTED only with real evidence
Verification      → VERIFIED only after current test/run/review evidence
Closed issue      → NOT automatic VERIFIED
```

| GitHub / delivery signal | Blackboard effect |
|---|---|
| Issue created + linked | work item linked; lifecycle may move toward `PLANNED` under management write |
| PR merged with evidence | may support `IMPLEMENTED` |
| Current verification evidence | may support `VERIFIED` |
| Issue closed without verification | **not** `VERIFIED` |

## Outcomes

| Outcome | Meaning |
|---|---|
| `GITHUB_ISSUE_CREATED` | All gates passed; create allowed / performed |
| `REUSED_EXISTING_WORK_ITEM` | Open work item for same Improvement reused |
| `IDEMPOTENT_RETRY_NO_DUPLICATE` | Same create operation retried; no second issue |
| `HOLD_OWNER_AMBIGUOUS` | Owning repo unclear |
| `HOLD_IDENTITY_AMBIGUOUS` | Improvement identity / root cause unclear |
| `DENIED_UNVALIDATED_IMPROVEMENT` | Lifecycle below `VALIDATED` |
| `DENIED_TARGET_AUTHORITY` | Target repo/host forbids create |
| `DENIED_ROLE_LACKS_CAPABILITY` | Scout/Supervisor/other role denied |
| `DENIED_WORK_NOT_CONCRETE` | Recommendation is watch-only / non-actionable |
| `DENIED_LINEAGE_INCOMPLETE` | Required body lineage fields missing |
| `BLOCKED_REQUIRED_CAPABILITY_UNAVAILABLE` | Capability missing/unauthorized |

## Out of scope

- product code or implementation PR creation
- expanding scout or Supervisor authority
- automatic routing when ownership is unclear
- inventing cross-repo product decisions
- bulk issue creation from unvalidated recommendations
- second workforce mutable runtime database for create state

## Relationship to other docs

- Role: [`agents/improvement-board-manager.md`](../agents/improvement-board-manager.md)
- Policy: [`WORKFORCE_POLICY.md`](WORKFORCE_POLICY.md)
- Capability routing: [`CAPABILITY_ROUTING.md`](CAPABILITY_ROUTING.md)
- Registry: [`capabilities/REGISTRY.yml`](../capabilities/REGISTRY.yml)
- Plugin/skill consumer routing: [`contracts/PLUGIN_SKILL_ROUTING_CONTRACT.md`](../contracts/PLUGIN_SKILL_ROUTING_CONTRACT.md)
