# Agent Workforce V1.1 Scout Checkpoints Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make Scout selection and Supervisor review deterministic with one GitHub-native checkpoint mechanism, align Finding/Health-Book contracts, and document the complete execution chain.

**Architecture:** One mechanism only. Scouts keep one mutable checkpoint per Health Book; the Supervisor keeps one mutable review checkpoint in meta issue #3. Normal Baseline/Finding evidence stays separate. No runtime database, no new role, no scheduler duplication.

**Tech Stack:** Markdown contracts, GitHub issues/comments, current scheduled execution host.

**Spec:** `docs/superpowers/specs/2026-10-21-scout-v1-1-checkpoints-design.md`

## Global Constraints

- No new Scout, Manager, or Specialist roles.
- No product/repository write authority beyond each role maintaining its own checkpoint.
- No runtime database, event-driven scheduler, Agent Brain runtime dependency, or scheduler prompt duplication.
- Current Scout cadence stays unchanged.
- `INITIAL BASELINE` remains one-time; later normal comments remain material `FINDING DELTA` output only.
- `NO_MATERIAL_CHANGE` and `SKIP_NO_DELTA` remain silent as evidence, but still advance the Scout checkpoint.
- Historical inspection timestamps are never invented.
- Supervisor cutover is evidence-based and fails closed on ambiguity.
- Target-repository authority and GitHub live state remain authoritative.

## Review Focus

- Duplicate checkpoint markers must block instead of being guessed through.
- Failed checkpoint writes must not count as successful state advancement.
- Supervisor cutover must not replay already-reviewed historical output.
- Checkpoint comments must never be interpreted as Baseline/Finding output.
- Finding Contract and Health Book template must use the same 15 fields and category vocabulary.

---

### Task 1: Canonical checkpoint contract

**Files:**
- Create: `contracts/CHECKPOINT_CONTRACT.md`

**Produces:**
- one Scout checkpoint marker/field set;
- one Supervisor checkpoint marker/cursor map;
- duplicate/failure semantics;
- lazy Scout initialization;
- evidence-based Supervisor cutover;
- `BLOCKED_CHECKPOINT_STATE_UNAVAILABLE`.

**Validation:** file exists; both markers, required cursor fields, duplicate handling, and Baseline/Finding exclusion are explicit.

---

### Task 2: Route runtime behavior through checkpoints

**Files:**
- Modify: `docs/WORKFORCE_POLICY.md`
- Modify: `agents/quality-scout.md`
- Modify: `agents/process-scout.md`
- Modify: `WORKFORCE_BOOTSTRAP.md`

**Produces:**
- `least-recently-inspected` derives from the active Scout checkpoint;
- meaningful activity is evaluated relative to that checkpoint;
- every completed deep inspection updates the same Scout checkpoint;
- Supervisor reviews only Scout outputs newer than its stored cursor;
- checkpoint comments are ignored as reviewable output;
- `BLOCKED_FINDING_IDENTITY_AMBIGUOUS` is separate from authority ambiguity;
- checkpoint maintenance is the only new write permission.

**Validation:** scheduler prompts unchanged; no product-code/follow-up-issue authority added; Bootstrap requires the checkpoint contract.

---

### Task 3: One Finding schema

**Files:**
- Modify: `contracts/FINDING_CONTRACT.md`
- Modify: `templates/REPO_HEALTH_BOOK.md`

**Required fields — exactly 15:**

`finding_id`, `repo`, `scout`, `category`, `summary`, `evidence`, `severity`, `confidence`, `first_seen`, `last_seen`, `recurrence`, `lifecycle`, `suggested_action`, `suggested_owner`, `disposition`.

**Category vocabulary:**

`CORRECTNESS | VALIDATION | CI | SECURITY | DEPENDENCY | ARCHITECTURE | OWNERSHIP | DOCUMENTATION | PROCESS | AUTOMATION | OTHER`.

**Validation:** Contract and template expose the same fields/categories; checkpoint-only runs never modify Finding recurrence/time semantics; Health-Book template references checkpoint semantics rather than duplicating them.

---

### Task 4: One end-to-end map

**Files:**
- Modify: `README.md`

**Produces:**

```text
Scheduler / Execution Host
        ↓
WORKFORCE_BOOTSTRAP.md
        ↓
Workforce Canon + Role/Policy Contracts
        ↓
Live Portfolio + Target Repository
        ↓
Target Repo Local Authority
        ↓
Conditional Capability / Reference Routing
        ↓
Quality Scout oder Process Scout
        ↓
Repo Health Book
  ├─ Initial Baseline / Finding Delta
  └─ mutable Scout Checkpoint
        ↓
Workforce Supervisor
        ↓
Meta Issue #3
  ├─ material supervisor review comments
  └─ mutable Supervisor Checkpoint
        ↓
Owner Escalation nur bei echtem Interventionsbedarf
```

The diagram is navigation only; detailed contracts stay in their owning files.

---

### Task 5: Branch validation and PR

Validate the branch against `main`:

- only Workforce canon/spec/plan files changed;
- no scheduler prompt or product repository changed;
- no second runtime-state mechanism introduced;
- no new role or expanded product authority introduced;
- checkpoint contract is referenced from Bootstrap/Policy/roles/template/README;
- Finding Contract and Health Book template are consistent.

Open a German, self-explanatory PR for #26. Do **not** use `Closes #26`; the issue remains open until live cutover validation succeeds.

---

### Task 6: Post-merge live cutover

1. Re-read live `main`, portfolio, Health Books, checkpoint contract, and meta issue #3.
2. Build one Supervisor checkpoint by reconciling existing Scout outputs with existing Supervisor review comments.
3. Never guess an ambiguous cursor; block instead.
4. Do not fabricate historical Scout inspection timestamps or bulk-seed Scout checkpoints. Each Scout creates/updates its own checkpoint on its next real deep inspection.
5. Verify the next Quality run, Process run, and Supervisor run use the checkpoint model correctly.
6. Close #26 only after this runtime behavior is live-verified.

## Golden Cases

1. Missing baseline remains highest priority in its class.
2. `NO_MATERIAL_CHANGE` stays evidence-silent but advances Scout checkpoint.
3. `SKIP_NO_DELTA` stays evidence-silent but advances Scout checkpoint.
4. Finding Delta and checkpoint stay separate.
5. Already-reviewed Supervisor output is not reviewed again.
6. Supervisor cutover derives cursors from evidence, never guesses.
7. Checkpoint comments never count as Baseline/Finding output.
8. Finding Contract and Health Book template use the same 15 fields/categories.
9. Finding identity ambiguity is distinct from authority ambiguity.
10. Checkpoint permission does not widen product/repository authority.
11. README flow remains navigation, not a second detailed contract.
