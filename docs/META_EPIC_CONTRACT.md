# Meta-Epic Contract

## Purpose

Defines the minimum fields a Meta-Epic must carry when it mandates
[`cursor-meta-epic-executor`](skills/cursor-meta-epic-executor/SKILL.md).

Product repositories may **reference** this contract. They must not duplicate
the skill body.

## Required fields

### Execution Skill

```text
Required execution skill: cursor-meta-epic-executor
```

### Intent

Which real user/product problem must be solved.

### Goal

Which verifiable end-state must be true. Outcome, not implementation recipe.

### Authority

Which repo/canon/contract/issue sources own truth. The Meta-Epic must not
replace target-repository authority.

Planning that would **invent** a new Meta-Epic or Goal must first satisfy
`AUTHORITY_RECONCILIATION_REQUIRED` in
[`docs/WORKFORCE_POLICY.md`](WORKFORCE_POLICY.md#authority-reconciliation).
The executor skill still does not invent Meta-Epics; it executes an already
defined one after live reconcile.

### Constraints

Invariants and bounds that must hold.

### Non-goals

What the agent must not inflate or additionally build.

### Evidence

Objective evidence that can prove the Goal.

### Exit

A unique completion condition / exit token.

## Optional but recommended

### Dependencies / Children

May describe dependencies and children. They are **not** a blind script.
Live state decides what is still required.

## Authority domains

1. Agent Workforce — cross-repo selection and capability resolution.
2. Target repository — product/implementation truth once selected.
3. Execution host (Cursor) — tools and primitives; overrides neither.

## Related

- Skill: [`docs/skills/cursor-meta-epic-executor/SKILL.md`](skills/cursor-meta-epic-executor/SKILL.md)
- Child delivery contract: [`contracts/EVIDENCE_BACKED_DELIVERY_CONTRACT.md`](../contracts/EVIDENCE_BACKED_DELIVERY_CONTRACT.md) / [`docs/skills/evidence-backed-delivery/SKILL.md`](skills/evidence-backed-delivery/SKILL.md)
- Consumer kind: `project_orchestrator` per [`contracts/PLUGIN_SKILL_ROUTING_CONTRACT.md`](../contracts/PLUGIN_SKILL_ROUTING_CONTRACT.md)
- Distribution: [`docs/CURSOR_META_EPIC_EXECUTOR.md`](CURSOR_META_EPIC_EXECUTOR.md)
