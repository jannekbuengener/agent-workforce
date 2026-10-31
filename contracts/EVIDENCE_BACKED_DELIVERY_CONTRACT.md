# Evidence-Backed Delivery Contract

## Purpose

Global Agent Workforce minimum contract for turning an Issue into an
inspectable PR and a PR into an evidenced mergeable delivery.

Applies to all repositories routed by Agent Workforce when they consume this
contract. The **target repository** remains product, test, CI, and merge
authority. Local rules may be stricter; they must not silently undercut this
minimum when the repo consumes the contract.

Canonical skill: [`docs/skills/evidence-backed-delivery/SKILL.md`](../docs/skills/evidence-backed-delivery/SKILL.md).

Machine twin: [`tools/evidence_backed_delivery_lib.py`](../tools/evidence_backed_delivery_lib.py).

Schema shape (documentation; no runtime `jsonschema` dependency):
[`evidence_backed_delivery.v1.schema.json`](evidence_backed_delivery.v1.schema.json).

## Lifecycle

```text
ISSUE → PLAN → PR ROUTING → IMPLEMENTATION → PR → EVIDENCE → REVIEW
  → FINAL HEAD → MERGE ORDER → MERGE → VERIFY MAIN → ISSUE CLOSE → RESIDUAL WORK
```

## Issue Contract

Required fields (or unambiguously resolvable from target-repo authority):

```text
Intent
Goal
Authority
Scope
Constraints
Non-goals
Dependencies
Acceptance Criteria
Required Evidence
Exit
```

Rules:

- An open issue is a **work candidate**, not automatic implementation authority.
- Acceptance must be observable; vague “looks good / sounds better” without an
  evidence definition is incomplete.
- Incomplete / contradictory core fields → `HOLD_ISSUE_CONTRACT_INCOMPLETE`.

## PR Contract

Every delivery PR must answer: delivered issue/slice, acceptance covered,
non-goals, changed areas, tests actually run, review findings + disposition,
exact checked head, dependencies, merge order, residual risks, inspectable
evidence.

Mandatory Review Evidence skeleton:

```markdown
## Scope
Issue:
Acceptance covered:
Non-goals:

## Final Head
Head SHA:
Base/Main state:

## Automated Validation
...

## Review Evidence
Modality:
Artifact / evidence:
Locator kind:
What to inspect:
Result:

## Review / Findings
...

## Dependency / Merge Order
...

## Remaining Risk / Residual Work
...
```

## Evidence by Modality

A PR must not merely claim a result. It must supply the inspectable counterpart
in the correct modality. See
[`docs/skills/evidence-backed-delivery/references/evidence_modalities.yml`](../docs/skills/evidence-backed-delivery/references/evidence_modalities.yml).

### Evidence Locator (machine-checkable)

Every human-inspectable artifact declares exactly one:

| `locator_kind` | Allowed for human-inspectable PR evidence |
|---|---|
| `PR_EMBEDDED` | yes |
| `GITHUB_ATTACHMENT` | yes |
| `WORKFLOW_ARTIFACT` | yes |
| `STABLE_REVIEW_URL` | yes |
| `LOCAL_ONLY` | **no** — hard block |

`LOCAL_ONLY` includes bare paths such as `D:\Temp\...`, Unix absolute paths, and
`file:` URLs. For human-inspectable evidence this yields
`BLOCKED_MISSING_EVIDENCE`.

Large packs require a compact review index and hero artifacts. Dumping many
screenshots without “What to inspect” → `CURRENT_PR_REWORK_REQUIRED`.

### Human Perception Rule

When acceptance involves human perception, automated tests do not replace
perception evidence:

```text
QML test PASS ≠ UI visual PASS
audio unit test PASS ≠ audio sounds correct
animation test PASS ≠ motion feels correct
```

If owner/human acceptance is required → `AWAITING_OWNER`. The executing agent
must never self-declare that gate `PASS`.

## Final-Head Binding

Evidence binds to at least: `repository`, `pr_number`, `head_sha`,
`relevant_base_sha` / main state, `observed_at`, `acceptance_criterion`,
`evidence` / artifact id.

After a new commit or relevant upstream/base change: reassess. If the claim
surface may be affected → `POTENTIALLY_STALE` / `BLOCKED_STALE_EVIDENCE` unless
a documented carry-forward proves non-impact. Historical evidence ≠ final-head
evidence.

## Dependency Graph and Merge Order

Relations:

```text
INDEPENDENT
UPSTREAM_DEPENDENCY
DOWNSTREAM_DEPENDENCY
SAME_AUTHORITY_CONFLICT
OVERLAPPING_WRITER
MERGE_ORDER_UNCLEAR
```

Unclear order → `HOLD_MERGE_ORDER_UNCLEAR` / `BLOCKED_MERGE_ORDER`. Independent
PRs may prepare in parallel. Upstream merge can invalidate downstream evidence;
reconcile base and re-evaluate. This contract never overrides local merge rules.

## PR Acceptance Verdicts

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

Not sufficient alone: PR exists, tests green, review ran, issue already closed.
Unresolved `MUST_FIX` → not a merge candidate.

## Merge / Main / Issue Close

After merge, verify live: PR MERGED, result on `main`, post-merge gates, issue
exit actually met, residual work recorded. Child slice merge with open parent
meta-exit → parent stays open.

## Relationship to other skills

- `cursor-meta-epic-executor` consumes this contract for child Issue→PR→Evidence
  →Merge→Close gates; Step→Lane→Integration→Slice→Meta Goal hierarchy remains.
- Sample Brain `sample-brain-issue-to-session-plan` stays local planning.
- Claire_de_Binare PR-acceptance family stays specialized reference — not replaced.

## Non-goals

No second agent runtime, universal PR router, control plane, or global copy of
local product governance. No forced commit of every binary into git. No
automatic merge solely because evidence is green.
