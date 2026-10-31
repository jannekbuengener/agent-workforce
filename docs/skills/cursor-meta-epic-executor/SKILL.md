---
name: cursor-meta-epic-executor
description: >-
  Goal-gated Meta-Epic executor for Cursor. Use when the user or a Meta-Epic
  explicitly requires cursor-meta-epic-executor, or when an already-selected
  target repository has a multi-step Meta-Epic / program issue with a
  verifiable Goal and Exit and dependent or parallelizable slices may be
  needed. Do not use for a small single-change bug/fix, research-only
  analysis, inventing the product goal, or when target-repo/authority is
  unclear.
icon: rocket
color: blue
---

# cursor-meta-epic-executor

Thin Cursor `project_orchestrator` playbook. Agent Workforce owns cross-repo
capability routing. The **target repository** owns product/implementation truth.
Cursor is the execution host only.

This skill does **not** invent Meta-Epics or product goals. The Meta-Epic is
already defined (Intent, Goal, Authority, Constraints, Non-goals, Evidence, Exit).

Reuse-before-build outcome for this skill itself: `REUSE_EXISTING + BUILD_THIN_SKILL`.
Do not build a new router, agent runtime, control plane, or database.

## When to use

- Explicit request for `cursor-meta-epic-executor` / Meta-Epic execution.
- Selected target repo has a multi-step Meta-Epic with verifiable Goal + Exit.
- Outcome matters more than a prescribed implementation recipe.

## When not to use

- Small bug/fix with one clear change.
- Meta-Epic lacks verifiable Goal/Exit.
- Target repository or authority not yet selected.
- Research/analysis only (no execution mandate).
- Agent would have to invent the product goal.

## Hard operating loop

```text
READ → UNDERSTAND → RECONCILE LIVE → PLAN → EXECUTE → VERIFY
→ RE-EVALUATE → REPLAN / CONTINUE → EXIT → LEARN
```

**Never execute before authority, documentation, and planning are complete.**

**Every material action must earn the right to continue by passing an
evidence-backed goal gate. Task completion is not goal completion.**

## Material Step Goal Gate (universal)

A **Material Step** is any action that materially changes code, repo/runtime
state, architecture, issue/PR state, the dependency graph, or the next
execution decision. Ordinary orientation reads are not material.

```text
BEFORE
- Parent Goal
- Step Goal
- Expected Evidence
- Constraints / Boundaries
- Continue Condition

EXECUTE

AFTER
- Actual Evidence
- Goal Delta
- Constraint Check
- Outcome:
  STEP_PASS | STEP_REWORK | STEP_BLOCKED
  | STEP_SUPERSEDED_BY_LIVE_STATE | STEP_OWNER_DECISION_REQUIRED
```

Only `STEP_PASS` or cleanly evidenced `STEP_SUPERSEDED_BY_LIVE_STATE` may
advance a dependent chain.

Hierarchy (never inherit PASS upward from task status alone):

```text
Step Gate → Lane Gate → Integration Gate → Slice Gate → Meta Goal Gate
```

```text
Subtask DONE ≠ Slice PASS
all Slices DONE ≠ Meta Goal PASS
PR created/merged ≠ Meta Goal PASS
```

### Child delivery (evidence-backed-delivery)

For child Issue → PR → Evidence → Merge Order → Merge → Verify main →
Issue close, consume the global
[`evidence-backed-delivery`](../evidence-backed-delivery/SKILL.md) skill and
[`EVIDENCE_BACKED_DELIVERY_CONTRACT`](../../../contracts/EVIDENCE_BACKED_DELIVERY_CONTRACT.md).

Use it for modality-matched PR evidence, final-head binding, merge-order
classification, and honest close/residual gates. Do **not** invent a second
gate hierarchy; Step→Lane→Integration→Slice→Meta remains authoritative for
Meta-Epic progress.

### Slice Gate

A **Slice** is a bounded execution unit toward the Meta Goal (one child,
one coherent deliverable cluster, or one planned dependency cut).

Before closing a slice as PASS:

1. Every material step in the slice is `STEP_PASS` or
   `STEP_SUPERSEDED_BY_LIVE_STATE`.
2. Slice Expected Evidence from the plan is inspectable.
3. Slice Boundaries / Non-goals held.
4. If the slice used parallel lanes, Integration Gate already passed.
5. Parent Meta Goal is re-evaluated; next slice is chosen from live state,
   not from a stale script.

Outcomes: `SLICE_PASS` | `SLICE_REWORK` | `SLICE_BLOCKED` |
`SLICE_SUPERSEDED_BY_LIVE_STATE` | `SLICE_OWNER_DECISION_REQUIRED`.

### Lane / Multitask gates

Each parallel lane declares `LANE_GOAL`, `LANE_EVIDENCE`, `LANE_BOUNDARY`,
then `LANE_PASS|HOLD`. After lanes finish, run an **Integration Goal Gate**
before parent re-evaluation. **Subagent-DONE is not Parent-PASS.**

## Cursor host primitives (use; do not reinvent)

Prefer current official Cursor docs over memory.

| Need | Primitive |
|------|-----------|
| Durable playbook | This skill as **Custom Mode** (Option/Alt+Enter) |
| Long-lived outcome | `/goal <meta exit>` when available (rolling out) |
| Parallel work | Subagents / parallel Task calls; `/multitask` in Agents Window when available |
| Writer isolation | Worktrees / isolated env when parallel writers risk overlap |
| Cloud skill availability | Sync Skills for Cloud Agents (`~/.cursor/skills`); automations need project skills |
| Independent verify | Separate read-only reviewer/verifier subagent or target-repo gatekeeper |

If a run **requires** `/goal` (or another named mode) and it is unavailable on
the host, stop with `BLOCKED_GOAL_EXECUTION_MODE_UNAVAILABLE`. Do not pretend
it is active. When `/multitask` is unavailable, use explicit parallel
Subagent/Task launches with the same dependency/overlap rules.

## Phase procedure

### 1. Read Meta-Epic

Extract Intent, Goal, Authority, Constraints, Non-goals, Evidence, Exit,
Dependencies/Children. Confirm this skill is required or appropriate.
Do **not** treat the child list as a blind sequential script.

If Goal/Exit are materially unclear and unresolvable from authority:
`HOLD_OWNER_DECISION_REQUIRED`.

### 2. Read target authority

Follow the target repo frontdoor (`AGENTS.md`, bootstrap, canon). Load only
task-relevant docs. Discover local agents/skills/gatekeepers. Target-repo
authority beats skill assumptions.

### 3. Reconcile live state

Before planning, establish what is already closed/merged/superseded/deferred,
what is still goal-relevant, existing PRs/checks, and what is already on
`main`. Prefer live evidence over historical issue text. **Never re-implement
completed children.**

### 4. Plan before write

Before the first material mutation, produce:

```text
GOAL INTERPRETATION
CURRENT STATE
DEPENDENCY GRAPH
EXECUTION SLICES
PARALLELISM
VALIDATION
COMPLETION GATE
```

Plans are disposable; new live evidence triggers replanning.

### 5. Multitask / subagent routing

Parallelize when slices are independent, non-overlapping on state/files, and
isolation is available for writers. Do **not** parallelize dependent slices,
competing writers on the same authority, or unfrozen architecture decisions.
Read-only research/verify lanes are preferred for parallelism.

### 6. Slice execution

Smallest useful goal progress; reuse existing primitives; use target-repo
skills/agents when routing says so; keep scope reversible; produce tests /
evidence with the change; honor target completion contracts. New meaningful
build paths trigger `reuse_before_build`.

### 7. Independent quality gate

Implementer must not be sole final judge. Use deterministic tests/CI/runtime
evidence plus target-repo gatekeeper or a separate read-only verifier.
`PR created` is never `DONE`.

> Evidence is the judge; the agent controls the iteration.

### 8. Re-evaluate / replan

After each material slice: re-read Goal, refresh live state, check which
acceptance/exit conditions remain unproven, replan if superseded.

### 9. Completion

Meta-Epic is done only when Exit is objectively evidenced, relevant children
are complete or owner-deferred, target gates pass, and live state is
re-read after close-out. HOLD instead of guessing on real owner decisions.

Pilot / skill-build exit tokens are **not** interchangeable with product
Meta-Epic exits. A clean HOLD is a valid run result; it is **not** automatic
proof of a `*_PILOT_PROVEN` exit.

### 10. Learning loop

After complete or legitimately blocked runs, emit **exactly one**:

```text
SKILL_LEARNING_RECOMMENDATION
Observation:
Evidence:
Recommended change:
Expected benefit:
Risk / trade-off:
```

or `NO_SKILL_CHANGE_RECOMMENDED`.

**Hard limit:** this skill must not mutate itself during its own run.

## Blocked / Hold codes

- `HOLD_OWNER_DECISION_REQUIRED`
- `BLOCKED_AUTHORITY_AMBIGUOUS`
- `BLOCKED_REQUIRED_CAPABILITY_UNAVAILABLE`
- `BLOCKED_GOAL_EXECUTION_MODE_UNAVAILABLE`
- `BLOCKED_EXTERNAL_DEPENDENCY`
- `HOLD_QUALITY_GATE_FAILED`

## Run receipt

```text
GOAL
FINAL STATUS
LIVE EXIT EVIDENCE
WORK COMPLETED
GATES PASSED / FAILED
REMAINING BLOCKER (if any)
SKILL LEARNING RECOMMENDATION
```

## References

- Meta-Epic field contract: [`docs/META_EPIC_CONTRACT.md`](../../META_EPIC_CONTRACT.md)
- Child delivery: [`docs/skills/evidence-backed-delivery/SKILL.md`](../evidence-backed-delivery/SKILL.md)
- Pressure cases: [`references/pressure_cases.yml`](references/pressure_cases.yml)
- Distribution: [`docs/CURSOR_META_EPIC_EXECUTOR.md`](../../CURSOR_META_EPIC_EXECUTOR.md)
- Consumer declaration: [`consumer.yml`](consumer.yml)
- Plugin/skill consumer contract: [`contracts/PLUGIN_SKILL_ROUTING_CONTRACT.md`](../../../contracts/PLUGIN_SKILL_ROUTING_CONTRACT.md)
