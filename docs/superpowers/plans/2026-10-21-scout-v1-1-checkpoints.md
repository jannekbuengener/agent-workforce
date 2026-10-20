# Agent Workforce V1.1 Scout Checkpoints Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Scout selection and Supervisor review state durable and deterministic, align the Finding Contract with the Health Book template, and expose one compact end-to-end execution flow without adding roles, a runtime database, or scheduler duplication.

**Architecture:** Keep GitHub as the durable operational evidence surface. Add one reusable mutable checkpoint comment per scout/Health Book and one mutable Supervisor checkpoint in meta issue #3; checkpoint comments are operational metadata and are explicitly excluded from baseline/finding parsing. Keep detailed semantics in one new checkpoint contract, then make Policy, roles, Bootstrap, Finding Contract, Health Book template, and README reference that contract instead of duplicating it.

**Tech Stack:** Markdown contracts, GitHub issues/comments as durable state, existing ChatGPT scheduled execution host, GitHub live state.

**Spec:** `docs/superpowers/specs/2026-10-21-scout-v1-1-checkpoints-design.md`

## Global Constraints

- No new Scout, Manager, or Specialist roles.
- No increase in product/repository mutation authority except creating/updating the acting Scout's own checkpoint and the Supervisor checkpoint.
- No runtime database, event-driven scheduler, Agent Brain runtime dependency, or scheduler prompt hard-coding.
- Current Scout cadence remains unchanged.
- `INITIAL BASELINE` stays one-time per Scout/repo; later normal comments remain material Finding Deltas only.
- `NO_MATERIAL_CHANGE` and `SKIP_NO_DELTA` remain silent with respect to normal evidence comments.
- Existing Health Book history is never rewritten to invent historical inspection timestamps.
- Supervisor cutover must be evidence-based and fail closed when an already-reviewed output cursor cannot be established safely.
- Target-repository authority and GitHub/repo live state remain above Workforce contracts.

## Review Focus

- **Duplicate checkpoint markers:** more than one matching checkpoint for the same Scout/Health Book must fail closed rather than choose one arbitrarily. Covered in Task 1 validation.
- **Partial checkpoint update failure:** a run must not report successful selection-state advancement if the checkpoint write cannot be verified. Covered in Task 2 validation.
- **Historical Supervisor ambiguity:** cutover must not guess a reviewed cursor when meta-issue evidence is insufficient. Covered in Task 6 reconciliation.
- **Checkpoint comments mistaken for Scout output:** Supervisor and baseline accounting must ignore checkpoint markers. Covered in Tasks 1, 2, and 6.
- **Schema drift after V1.1:** Finding Contract and Health Book template must expose the same required fields and category vocabulary. Covered in Task 3 validation.

---

### Task 1: Add one canonical checkpoint contract

**Files:**
- Create: `contracts/CHECKPOINT_CONTRACT.md`
- Modify: `README.md` only to add the contract to the V1 workforce index if needed; the execution-flow prose itself belongs to Task 4.

**Interfaces:**
- Consumes: design decisions from `docs/superpowers/specs/2026-10-21-scout-v1-1-checkpoints-design.md`.
- Produces: canonical marker formats, checkpoint fields, read/update semantics, duplicate handling, migration rules, and operational blocked outcomes used by Tasks 2 and 6.

- [ ] **Step 1: Write a failing contract-presence validation**

Run from the isolated execution worktree before creating the file:

```bash
python - <<'PY'
from pathlib import Path
p = Path('contracts/CHECKPOINT_CONTRACT.md')
assert p.exists(), 'checkpoint contract missing'
text = p.read_text(encoding='utf-8')
for token in [
    'agent-workforce:scout-checkpoint:v1',
    'agent-workforce:supervisor-checkpoint:v1',
    'BLOCKED_CHECKPOINT_STATE_UNAVAILABLE',
    'last_inspected_at',
    'last_reviewed_output_comment_id',
]:
    assert token in text, token
PY
```

Expected: FAIL because the contract does not yet exist.

- [ ] **Step 2: Create `contracts/CHECKPOINT_CONTRACT.md`**

The contract must define exactly:

- Scout marker: `<!-- agent-workforce:scout-checkpoint:v1 scout=<agent_id> -->`.
- Supervisor marker: `<!-- agent-workforce:supervisor-checkpoint:v1 -->`.
- Exactly one active Scout checkpoint per Scout/Health Book and one active Supervisor checkpoint in meta issue #3.
- Scout fields: `checkpoint_version`, `scout`, `repo`, `last_inspected_at`, `last_repo_head`, `last_runtime_outcome`, `baseline_complete`, `last_material_output_comment_id`, `last_material_output_at`.
- Supervisor fields: `checkpoint_version`, `last_supervisor_run_at`, and a per-Health-Book `last_reviewed_output_comment_id` map.
- Duplicate matching markers => `BLOCKED_CHECKPOINT_STATE_UNAVAILABLE`; never select one arbitrarily.
- A successful deep inspection updates the same Scout checkpoint after normal evidence behavior completes.
- Checkpoint comments are operational metadata, never `INITIAL BASELINE` or `FINDING DELTA` outputs and never recurrence evidence.
- Scout lazy migration: current run initializes `last_inspected_at` / `last_repo_head`; never backfill them from old comments.
- Supervisor cutover is evidence-based from Health Books plus meta issue #3 and must fail closed on ambiguity.
- Failed checkpoint create/update/read verification => `BLOCKED_CHECKPOINT_STATE_UNAVAILABLE` and no successful state-advance claim.

Use fenced YAML examples only as serialization examples; prose semantics remain authoritative.

- [ ] **Step 3: Run the contract-presence validation again**

Expected: PASS.

- [ ] **Step 4: Validate duplicate/checkpoint-output semantics are explicit**

```bash
python - <<'PY'
from pathlib import Path
text = Path('contracts/CHECKPOINT_CONTRACT.md').read_text(encoding='utf-8')
assert 'duplicate' in text.lower()
assert 'INITIAL BASELINE' in text
assert 'FINDING DELTA' in text
assert 'BLOCKED_CHECKPOINT_STATE_UNAVAILABLE' in text
PY
```

Expected: PASS.

- [ ] **Step 5: Commit Task 1**

```bash
git add contracts/CHECKPOINT_CONTRACT.md README.md
git commit -m "docs: define workforce checkpoint contract"
```

---

### Task 2: Route Scout selection and Supervisor review through checkpoints

**Files:**
- Modify: `docs/WORKFORCE_POLICY.md`
- Modify: `agents/quality-scout.md`
- Modify: `agents/process-scout.md`
- Modify: `WORKFORCE_BOOTSTRAP.md`

**Interfaces:**
- Consumes: `contracts/CHECKPOINT_CONTRACT.md` marker/field/outcome semantics from Task 1.
- Produces: runtime selection/review rules used by scheduled Quality Scout, Process Scout, and Supervisor executions.

- [ ] **Step 1: Write a failing routing validation**

```bash
python - <<'PY'
from pathlib import Path
checks = {
    'docs/WORKFORCE_POLICY.md': ['CHECKPOINT_CONTRACT.md', 'least-recently-inspected'],
    'agents/quality-scout.md': ['BLOCKED_CHECKPOINT_STATE_UNAVAILABLE', 'checkpoint'],
    'agents/process-scout.md': ['BLOCKED_CHECKPOINT_STATE_UNAVAILABLE', 'checkpoint'],
    'WORKFORCE_BOOTSTRAP.md': ['CHECKPOINT_CONTRACT.md', 'supervisor-checkpoint'],
}
for path, tokens in checks.items():
    text = Path(path).read_text(encoding='utf-8')
    for token in tokens:
        assert token in text, f'{path}: {token}'
PY
```

Expected: FAIL on current V1 docs.

- [ ] **Step 2: Update `docs/WORKFORCE_POLICY.md`**

Change only the selection/state semantics:

- Keep the four existing priority classes unchanged.
- Define `least-recently-inspected` from the active Scout's checkpoint `last_inspected_at`.
- A repo without a checkpoint is `never inspected in checkpoint model` within its otherwise applicable priority class.
- Meaningful activity is evaluated relative to the Scout checkpoint rather than the last arbitrary Health Book comment.
- Preserve the cost rule and silence rules.
- Update `State separation`: mutable Scout/Supervisor checkpoint comments are GitHub runtime/evidence metadata, not versioned repo truth and not a separate database.
- Explicitly permit only creating/updating the acting role's checkpoint under V1 authority.

- [ ] **Step 3: Update `agents/quality-scout.md` and `agents/process-scout.md`**

For both roles:

- Add checkpoint read before selection/deep inspection as required by Policy.
- After a successful deep inspection, update the same own checkpoint even when normal evidence outcome is silent.
- Add `BLOCKED_CHECKPOINT_STATE_UNAVAILABLE`.
- Add `BLOCKED_FINDING_IDENTITY_AMBIGUOUS` where finding identity cannot safely be established; keep `BLOCKED_AUTHORITY_AMBIGUOUS` only for authority ambiguity.
- Do not add product-code or follow-up-issue authority.

- [ ] **Step 4: Update `WORKFORCE_BOOTSTRAP.md`**

- Add `contracts/CHECKPOINT_CONTRACT.md` to the unconditional required-read order before execution-mode-specific routing.
- Quality/Process mode must follow checkpoint-aware Policy + role semantics.
- Supervisor mode must ignore checkpoint comments as reviewable Scout outputs and use only the Supervisor checkpoint cursor after cutover.
- Keep active scheduler prompts unchanged; they continue to point only at live `WORKFORCE_BOOTSTRAP.md` plus execution mode.

- [ ] **Step 5: Run the routing validation again**

Expected: PASS.

- [ ] **Step 6: Verify authority did not widen accidentally**

```bash
python - <<'PY'
from pathlib import Path
for path in ['agents/quality-scout.md', 'agents/process-scout.md', 'docs/WORKFORCE_POLICY.md']:
    text = Path(path).read_text(encoding='utf-8').lower()
    assert 'automatic follow-up issue' not in text or 'forbidden' in text or 'do not' in text
    assert 'product code' in text or 'product-code' in text
PY
```

Expected: PASS, with checkpoint mutation the only new write permission.

- [ ] **Step 7: Commit Task 2**

```bash
git add docs/WORKFORCE_POLICY.md agents/quality-scout.md agents/process-scout.md WORKFORCE_BOOTSTRAP.md
git commit -m "docs: route workforce runs through durable checkpoints"
```

---

### Task 3: Make Finding Contract and Health Book template exactly consistent

**Files:**
- Modify: `contracts/FINDING_CONTRACT.md`
- Modify: `templates/REPO_HEALTH_BOOK.md`

**Interfaces:**
- Consumes: checkpoint filtering rules from Task 1.
- Produces: one exact Finding V1.1 field set, category vocabulary, ambiguity outcome semantics, and Health Book templates used by both Scouts.

- [ ] **Step 1: Write a failing schema-equivalence validation**

Use the exact V1.1 field/category sets from the spec:

```bash
python - <<'PY'
from pathlib import Path
required = [
 'finding_id','repo','scout','category','summary','evidence','severity','confidence',
 'first_seen','last_seen','recurrence','lifecycle','suggested_action','suggested_owner','disposition'
]
categories = ['CORRECTNESS','VALIDATION','CI','SECURITY','DEPENDENCY','ARCHITECTURE','OWNERSHIP','DOCUMENTATION','PROCESS','AUTOMATION','OTHER']
contract = Path('contracts/FINDING_CONTRACT.md').read_text(encoding='utf-8').lower()
template = Path('templates/REPO_HEALTH_BOOK.md').read_text(encoding='utf-8').lower()
assert len(required) == 15
for field in required:
    assert field in contract, f'contract missing {field}'
    assert field.replace('_',' ') in template or field in template, f'template missing {field}'
for category in categories:
    assert category.lower() in contract
    assert category.lower() in template
assert 'BLOCKED_FINDING_IDENTITY_AMBIGUOUS'.lower() in contract
PY
```

Expected: FAIL against current V1 template/contract.

- [ ] **Step 2: Update `contracts/FINDING_CONTRACT.md`**

Required fields become exactly these 15 fields:

`finding_id`, `repo`, `scout`, `category`, `summary`, `evidence`, `severity`, `confidence`, `first_seen`, `last_seen`, `recurrence`, `lifecycle`, `suggested_action`, `suggested_owner`, `disposition`.

Add exact category vocabulary:

`CORRECTNESS | VALIDATION | CI | SECURITY | DEPENDENCY | ARCHITECTURE | OWNERSHIP | DOCUMENTATION | PROCESS | AUTOMATION | OTHER`.

Clarify:

- one primary category per Finding;
- category follows root cause/work-risk class, not Scout identity;
- `first_seen` immutable after first stable Finding;
- `last_seen` and `recurrence` change only on materially new confirming evidence;
- checkpoint-only runs never change Finding lifecycle timestamps/recurrence;
- `BLOCKED_AUTHORITY_AMBIGUOUS` is authority only;
- `BLOCKED_FINDING_IDENTITY_AMBIGUOUS` is identity/root-cause uncertainty and creates no invented stable ID.

- [ ] **Step 3: Update `templates/REPO_HEALTH_BOOK.md`**

- Replace the old Finding Delta shape with all 15 required fields using readable Markdown labels.
- Include the same exact category vocabulary.
- Add Scout checkpoint example/marker by reference to `contracts/CHECKPOINT_CONTRACT.md`; do not duplicate full semantics.
- State checkpoint comments are excluded from baseline/finding accounting.
- Keep silence rules unchanged for normal evidence comments.
- Change the template's suggested Health Book title to German and self-explanatory, for example: `[OPS][HEALTH] Repo-Health-Book — fortlaufende Qualitäts- und Prozessevidenz`. Existing Health Book issues are not renamed in this slice unless separately justified.

- [ ] **Step 4: Run schema-equivalence validation again**

Expected: PASS.

- [ ] **Step 5: Verify the old ambiguity conflation is gone**

```bash
python - <<'PY'
from pathlib import Path
text = Path('contracts/FINDING_CONTRACT.md').read_text(encoding='utf-8')
assert 'BLOCKED_FINDING_IDENTITY_AMBIGUOUS' in text
assert 'BLOCKED_AUTHORITY_AMBIGUOUS' in text
PY
```

Expected: PASS with separate semantics for both outcomes.

- [ ] **Step 6: Commit Task 3**

```bash
git add contracts/FINDING_CONTRACT.md templates/REPO_HEALTH_BOOK.md
git commit -m "docs: align finding and health book contracts"
```

---

### Task 4: Add one compact end-to-end execution map

**Files:**
- Modify: `README.md`

**Interfaces:**
- Consumes: canonical detail locations from Tasks 1-3 and existing meta topology/capability/reference contracts.
- Produces: one human-readable frontdoor execution chain without duplicating detailed downstream rules.

- [ ] **Step 1: Write a failing execution-flow validation**

```bash
python - <<'PY'
from pathlib import Path
text = Path('README.md').read_text(encoding='utf-8')
for token in [
 'Scheduler / Execution Host',
 'WORKFORCE_BOOTSTRAP.md',
 'Target Repo Local Authority',
 'Capability / Reference Routing',
 'Repo Health Book',
 'Workforce Supervisor',
 'Meta Issue #3',
 'CHECKPOINT_CONTRACT.md',
]:
    assert token in text, token
PY
```

Expected: FAIL because the complete chain is not yet present in one place.

- [ ] **Step 2: Add `End-to-End Workforce Execution Flow` to `README.md`**

Use this exact conceptual chain, with links to the existing canonical files rather than copied detail rules:

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

Below the diagram, state that the diagram is navigation only and does not override Bootstrap, Policy, role, checkpoint, Finding, portfolio, or target-repo authority contracts.

- [ ] **Step 3: Run the execution-flow validation again**

Expected: PASS.

- [ ] **Step 4: Commit Task 4**

```bash
git add README.md
git commit -m "docs: document workforce execution chain"
```

---

### Task 5: Validate the branch and deliver the canonical contract changes

**Files:**
- Verify all files changed by Tasks 1-4.
- No new runtime dependency or workflow file.

**Interfaces:**
- Consumes: completed canonical contract changes.
- Produces: reviewable PR for issue #26 and a merged `main` only after all repo merge gates pass.

- [ ] **Step 1: Run all focused validations from Tasks 1-4**

Expected: all PASS.

- [ ] **Step 2: Run cross-file invariant checks**

Verify:

- every Scout runtime outcome documented in role files is either pre-existing or one of `BLOCKED_CHECKPOINT_STATE_UNAVAILABLE` / `BLOCKED_FINDING_IDENTITY_AMBIGUOUS`;
- checkpoint markers appear only where contract/template/bootstrap/policy intentionally reference them;
- no scheduler prompt text, local machine path, product repo code, workflow, dependency file, or unrelated portfolio membership is changed;
- `git diff main...HEAD` contains only the approved V1.1 docs/contracts/spec/plan surfaces.

- [ ] **Step 3: Open a PR with a German, self-explanatory title**

Suggested title:

`[SCOUTS] V1.1-Checkpoints und Finding-Contract konsistent einführen`

Body must reference issue #26, the design spec, the implementation plan, validation evidence, and explicitly state that scheduler cadence/roles/product authority are unchanged. Use `Relates to #26`; do **not** use `Closes #26`, because the issue must remain open until the live cutover in Task 6 is verified.

- [ ] **Step 4: Review the exact final PR head**

Check:

- mergeability;
- required status checks / active ruleset;
- review findings and unresolved threads;
- exact changed-file set;
- no accidental second source of truth.

Repair any in-scope finding on the PR branch and re-run Step 4 on the new exact head.

- [ ] **Step 5: Merge only when gates are satisfied**

Use the repository-allowed merge method with exact-head lease. Verify the merge SHA is live on `main`. Issue #26 intentionally remains open until Task 6 completes.

---

### Task 6: Perform the one-time live checkpoint cutover and acceptance run

**Files / live surfaces:**
- Read: `portfolio/REPOSITORIES.md` on merged `main`.
- Read: all six canonical Repo Health Books.
- Read/write: Agent Workforce meta issue #3.
- Read/write: whichever Health Books are selected by the live Quality/Process contracts during acceptance runs.
- Do not edit product code or repo-local canon.

**Interfaces:**
- Consumes: merged V1.1 contracts from Task 5.
- Produces: one evidence-based Supervisor checkpoint plus real Scout checkpoint evidence created only by real Scout runs.

- [ ] **Step 1: Reconcile the Supervisor cutover before activating cursor-based review**

For each current Health Book:

1. enumerate only `INITIAL BASELINE` and `FINDING DELTA` comments;
2. read existing Workforce Supervisor comments in meta issue #3;
3. determine the highest Scout-output comment ID for that Health Book whose review is explicitly evidenced by existing Supervisor comments;
4. if any Health Book's reviewed cursor is ambiguous, stop with `BLOCKED_CHECKPOINT_STATE_UNAVAILABLE` and do not guess.

- [ ] **Step 2: Create exactly one Supervisor checkpoint comment in meta issue #3**

Use marker:

```text
<!-- agent-workforce:supervisor-checkpoint:v1 -->
```

Store `checkpoint_version: 1`, current cutover timestamp as `last_supervisor_run_at`, and the reconciled `last_reviewed_output_comment_id` map for all current Health Books. Verify the comment can be re-read and the map matches Step 1 evidence.

- [ ] **Step 3: Execute one Quality Scout acceptance run under merged live canon**

Do not hard-code a target repository. Let the merged selection policy choose from the live portfolio. At run completion verify:

- a real deep inspection occurred or the run correctly blocked;
- if successful, exactly one Quality Scout checkpoint marker exists in the selected Health Book;
- `last_inspected_at`, `last_repo_head`, `last_runtime_outcome`, and `baseline_complete` match the run;
- a normal evidence comment exists only if baseline/finding rules require it.

If Agent Brain still lacks its Quality baseline, the expected selection class is `missing baseline`; do not override live selection if state changed before execution.

- [ ] **Step 4: Execute one Process Scout acceptance run under merged live canon**

Apply the same assertions as Step 3 for the Process Scout marker. If Agent Brain still lacks its Process baseline, the expected selection class is `missing baseline`; again do not force the target when live state differs.

- [ ] **Step 5: Execute one Supervisor acceptance run**

The Supervisor must:

- treat only Scout `INITIAL BASELINE` / `FINDING DELTA` comments after the reconciled per-Health-Book cursors as new;
- ignore Scout checkpoint comments;
- append at most one material Supervisor review comment when new reviewable output exists;
- update the same Supervisor checkpoint comment to the new reviewed cursors;
- on an immediate second no-new-output pass, produce no duplicate material review comment.

- [ ] **Step 6: Validate all 11 Golden Cases against live/contracts evidence**

Record compact evidence for:

1. missing baseline priority;
2. silent run checkpoint update semantics;
3. `SKIP_NO_DELTA` semantics;
4. material finding/checkpoint separation;
5. Supervisor dedup;
6. Supervisor cutover;
7. checkpoint filtering;
8. Finding schema equivalence;
9. identity-vs-authority ambiguity;
10. checkpoint-only authority boundary;
11. end-to-end execution-flow documentation.

Cases not naturally exercised by the two acceptance runs are validated by contract/readback dry cases; do not manufacture a repository defect merely to create runtime evidence.

- [ ] **Step 7: Close out issue #26**

Add a compact delivery comment with PR, merge SHA, Supervisor checkpoint comment ID, acceptance-run selected repos/outcomes, and Golden Case result. Close #26 as `completed` only now.

- [ ] **Step 8: Final live verification**

Verify:

- `agent-workforce/main` contains the merged V1.1 contracts;
- scheduled Quality Scout, Process Scout, and Workforce Supervisor prompts still bootstrap only from `WORKFORCE_BOOTSTRAP.md` plus execution mode;
- no scheduler cadence changed;
- no product repository code/canon was modified by this slice;
- no duplicate active checkpoint marker exists in any surface touched during acceptance.
