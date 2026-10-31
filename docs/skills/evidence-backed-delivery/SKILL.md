---
name: evidence-backed-delivery
description: >-
  Global Agent Workforce Issue→PR→Evidence→Merge→Close delivery contract.
  Use when delivering implementation work that must produce inspectable PR
  evidence bound to a final head, clear merge order, and honest issue close.
  Do not use to invent product goals, replace target-repo merge authority,
  build a second PR router/runtime, or copy CDB lane/lock/trading rules.
icon: clipboard-check
color: green
---

# evidence-backed-delivery

Thin Cursor `project_orchestrator` playbook. Agent Workforce owns the **global
minimum delivery contract**. The **target repository** owns product, tests,
CI, and merge authority.

**Naming:** skill id `evidence-backed-delivery` matches issue #43. Do not rename
without updating consumer id, distribution doc, and portfolio index.

Canonical contract:
[`contracts/EVIDENCE_BACKED_DELIVERY_CONTRACT.md`](../../../contracts/EVIDENCE_BACKED_DELIVERY_CONTRACT.md).

## When to use

- Explicit request for `evidence-backed-delivery`.
- Delivery of an Issue/PR that must meet Workforce evidence/merge gates.
- Child delivery under `cursor-meta-epic-executor` (consume this contract; do
  not invent a competing gate hierarchy).
- Cross-repo work where modality-matched, PR-visible evidence is required.

## Do not use

- Inventing the product goal or Meta-Epic.
- Replacing target-repo AGENTS/canon/merge rules.
- Building a second universal PR router, agent runtime, or control plane.
- Globalizing CDB lane/lock/LR/trading/batch rules.
- Declaring owner visual/audio PASS yourself.

## Lifecycle

```text
ISSUE → PLAN → PR ROUTING → BRANCH/WORKTREE → IMPLEMENTATION → PR
  → EVIDENCE → REVIEW → FINAL HEAD → MERGE ORDER → MERGE
  → VERIFY MAIN → ISSUE CLOSE → RESIDUAL WORK
```

## Issue Contract Gate

Resolve or extract:

```text
Intent | Goal | Authority | Scope | Constraints | Non-goals
Dependencies | Acceptance Criteria | Required Evidence | Exit
```

Open issue = work candidate ≠ implement authorization. Incomplete →
`HOLD_ISSUE_CONTRACT_INCOMPLETE`.

## PR Contract Gate

PR body must include Scope, Final Head, Automated Validation, Review Evidence
(with modality + locator + what to inspect), Review/Findings, Dependency/Merge
Order, Remaining Risk. Templates:
[`references/pr_review_evidence_template.md`](references/pr_review_evidence_template.md),
[`references/issue_contract_template.md`](references/issue_contract_template.md).

## Evidence by Modality (hard)

Match claim → modality artifact. Matrix:
[`references/evidence_modalities.yml`](references/evidence_modalities.yml).

### Evidence Locator (machine-checkable)

Every human-inspectable artifact MUST declare `locator_kind`:

| Kind | Human-inspectable OK |
|---|---|
| `PR_EMBEDDED` | yes |
| `GITHUB_ATTACHMENT` | yes |
| `WORKFLOW_ARTIFACT` | yes |
| `STABLE_REVIEW_URL` | yes |
| `LOCAL_ONLY` | **no** |

`LOCAL_ONLY` (including `D:\Temp\...`) → `BLOCKED_MISSING_EVIDENCE`.

Large packs without review index → `CURRENT_PR_REWORK_REQUIRED`.

### Human Perception Rule

Tests do not replace perception evidence when acceptance is perceptual.
Owner/human gate → stay `AWAITING_OWNER`. Agent must not self-PASS.

## Final-Head Binding

Bind evidence to repository, PR number, head SHA, base/main state, observed_at,
acceptance criterion, evidence id. New commit / upstream change → reassess.
Touches claim surface without fresh evidence → `BLOCKED_STALE_EVIDENCE`.
Documented docs-only non-touch may carry forward. Historical ≠ final-head.

## Dependency / Merge Order

Classify: `INDEPENDENT`, `UPSTREAM_DEPENDENCY`, `DOWNSTREAM_DEPENDENCY`,
`SAME_AUTHORITY_CONFLICT`, `OVERLAPPING_WRITER`, `MERGE_ORDER_UNCLEAR`.
Unclear → `HOLD_MERGE_ORDER_UNCLEAR` / `BLOCKED_MERGE_ORDER`. After upstream
merge affecting shared authority: reconcile + re-evaluate evidence.

## Acceptance Verdicts

```text
MERGE_CANDIDATE
CURRENT_PR_REWORK_REQUIRED
PR_SPLIT_REQUIRED
FOLLOWUP_REQUIRED
AWAITING_OWNER
BLOCKED_MISSING_EVIDENCE
BLOCKED_STALE_EVIDENCE
BLOCKED_REVIEW_FINDINGS
BLOCKED_MERGE_ORDER
BLOCKED_REPO_GATE
```

Green tests + unresolved `MUST_FIX` → `BLOCKED_REVIEW_FINDINGS`.
PR exists / tests green / review ran / issue closed alone ≠ mergeable.

Independent review may be Bugbot, Codex Review, or an equivalent independent
reviewer available on the host. Gate: **0 unresolved MUST_FIX on Final Head**.

## Merge / Close

Verify live MERGED + main contains result + exit met before closing. Child
merged with parent meta-exit open → parent stays open. Capture residual work;
dedupe before creating follow-ups.

## Relationship to `cursor-meta-epic-executor`

Existing hierarchy remains:

```text
Step Gate → Lane Gate → Integration Gate → Slice Gate → Meta Goal Gate
```

Use this skill/contract for child Issue delivery, PR evidence, merge order,
final-head evidence, and merge/close gates. Do not invent a parallel hierarchy.

## Delivery receipt

When this skill completes a delivery attempt, leave compact delivery evidence
covering issue/PR verdict, locator-checked evidence, final-head binding, merge
order, and residual work.

If a declared `PREFERRED` capability materially matches for the run (today:
`deterministic_validation` from [`consumer.yml`](consumer.yml)), also include:

```text
CAPABILITY ROUTING DECISIONS
PREFERRED_CAPABILITY_DECISION
Capability: <capability_id>
Decision: USED_PREFERRED | LOCAL_EQUIVALENT | NOT_USED_WITH_REASON
Reason: <required for LOCAL_EQUIVALENT and NOT_USED_WITH_REASON>
```

Omit `CAPABILITY ROUTING DECISIONS` entirely when no preferred capability
matched. Do not emit `NO_MATCH` rows. Target-repo local twins remain valid
`LOCAL_EQUIVALENT` routes. Semantics:
[`docs/CAPABILITY_ROUTING.md`](../../CAPABILITY_ROUTING.md).

## Pressure cases

Layer A twin: [`references/pressure_cases.yml`](references/pressure_cases.yml)
+ [`tools/evidence_backed_delivery_lib.py`](../../../tools/evidence_backed_delivery_lib.py).

## References

- Contract: [`contracts/EVIDENCE_BACKED_DELIVERY_CONTRACT.md`](../../../contracts/EVIDENCE_BACKED_DELIVERY_CONTRACT.md)
- Schema shape: [`contracts/evidence_backed_delivery.v1.schema.json`](../../../contracts/evidence_backed_delivery.v1.schema.json)
- Distribution: [`docs/EVIDENCE_BACKED_DELIVERY.md`](../../EVIDENCE_BACKED_DELIVERY.md)
- Consumer: [`consumer.yml`](consumer.yml)
- Plugin/skill routing: [`contracts/PLUGIN_SKILL_ROUTING_CONTRACT.md`](../../../contracts/PLUGIN_SKILL_ROUTING_CONTRACT.md)
