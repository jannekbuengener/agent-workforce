# Workforce Policy V1.1

## Operating model

V1.1 contains exactly two advisory scouts: Quality Scout and Process Scout. The organization grows only from observed recurring work.

A scheduled run may shallow-preflight all in-scope repositories but deep-inspects exactly one repository.

Portfolio membership and baseline cardinality are derived from [`../portfolio/REPOSITORIES.md`](../portfolio/REPOSITORIES.md). Each active scout requires one initial baseline for every current in-scope repository; no fixed repository count is part of the policy contract.

Operational inspection/review state uses exactly one mechanism: mutable GitHub checkpoint comments defined by [`../contracts/CHECKPOINT_CONTRACT.md`](../contracts/CHECKPOINT_CONTRACT.md). No parallel run-state ledger or runtime database is part of V1.1.

## Selection priority

Choose the first eligible class below; within a class choose the least-recently-inspected repository:

1. missing baseline for the active scout;
2. unresolved `HIGH`/`CRITICAL` finding due for recheck;
3. meaningful new commit/PR/issue/CI activity since the last Scout inspection;
4. periodic sweep candidate that has gone longest without inspection.

`least-recently-inspected` is derived from the active Scout's checkpoint `last_inspected_at`. A repository without that Scout checkpoint is treated as `never inspected in checkpoint model` within its otherwise applicable priority class.

Meaningful activity is evaluated relative to the active Scout checkpoint, not the most recent arbitrary Health Book comment. Generic bot activity, Scout/checkpoint comments, and unchanged automated updates are not meaningful activity by themselves.

Activity labels are derived advisory labels only:

- `ACTIVE` — sustained current work or unresolved material findings;
- `WATCH` — intermittent activity or a condition worth rechecking;
- `DORMANT_POTENTIAL` — quiet but intentionally retained;
- `ARCHIVED` — explicitly retired from normal rotation.

## Cost rule

> Observation must be cheaper than the work it helps avoid.

Use a cheap preflight before deeper inspection. No deep audit is justified when there is no meaningful change, no missing baseline, and no finding due for recheck.

## Evidence and authority

- Live repository/GitHub state beats historical comments, workforce documentation, NotebookLM, and memory.
- Repo-local authority beats generic engineering assumptions when it intentionally defines a valid different rule.
- Shared meta-layer roles are classified in [`META_TOPOLOGY.md`](META_TOPOLOGY.md); those roles never override target-repository authority or create implicit runtime dependencies.
- Every deviation must be supported by concrete evidence.
- Silence is preferable to manufactured findings.
- Infrastructure/tool/budget/checkpoint failures are classified separately from repo quality.

## Anti-noise and convergence

- One underlying root cause has one stable finding identity.
- Both scouts reuse that identity when they observe the same underlying condition.
- `SKIP_NO_DELTA` creates no normal Health Book evidence comment.
- Routine unchanged `NO_MATERIAL_CHANGE` creates no normal evidence comment.
- Both outcomes still update the acting Scout's checkpoint because an inspection occurred.
- Checkpoint-only updates never count as finding recurrence.
- Recurrence increases only on materially new confirming evidence.
- Resolution requires current evidence.
- A recommended follow-up issue must name the finding it would resolve.
- Repeated false positives are evidence to repair the role contract, not a reason to add more machinery.

## Authority V1.1

Allowed: read/analyze live state, append evidence-backed Health Book observations, recommend follow-up work, escalate uncertainty, and create/update only the acting Scout's own checkpoint comment as defined by `CHECKPOINT_CONTRACT.md`.

Forbidden: product-code mutation, implementation PRs, governance changes, secret changes, specialist-agent creation, automatic follow-up issue creation, direct pushes to protected/default branches, or creating a second mutable runtime-state mechanism.

## Authority reconciliation

Invariant id: `AUTHORITY_RECONCILIATION_REQUIRED`.

Producer and planning flows that reach a structural decision after routing must complete this gate **before** `DECIDE` when the relevance gate matches:

```text
UNDERSTAND → VERIFY LIVE → ROUTE → AUTHORITY RECONCILIATION → DECIDE → …
```

This gate prevents recommending, designing, or creating a new durable structuring authority when an existing canonical owner already owns the desired outcome or only needs update/reconciliation/linking. It also requires that structural candidate analysis preserve the original user question and evaluate relevant local same-class precedents as samples before a final create / reconcile / no-change decision. It does not replace target-repository authority and does not grant write permission.

### Relevance gate

Apply `AUTHORITY_RECONCILIATION_REQUIRED` when an agent considers recommending, designing, or creating a new durable structuring / coordination authority, including at least:

- Goal;
- Epic;
- Meta-Epic;
- Coordinator;
- Foundation Owner;
- Program Owner;
- Manager;
- other durable organizational or planning owner structures.

Do **not** inflate ordinary delivery work with this gate. Ordinary implementation children, small bugfix slices, documentation-only edits, and other bounded child work under an already-settled parent do not trigger a new authority-structure search, same-class precedent ceremony, or candidate-reconciliation bureaucracy merely because planning language appears in the request.

Reads remain relevance-gated. Do not inventory every parent or open issue in the portfolio solely because a planning ask arrived.

### Preserve original structural intent

When the user asks a structural candidate / clustering question (for example which open issues could justify a Goal or Meta-Epic), capture that original structural intent explicitly before reconciliation analysis.

Reconciliation may change the **solution**. Reconciliation must not silently replace the **question** with a different task such as owner cleanup only.

An existing owner is reconciliation evidence. Finding an existing owner must not automatically end structural candidate analysis or collapse the work into cleanup-only.

### Local same-class precedents

When the relevance gate matches and the ask is structural candidate analysis or create-new for a durable structure class, discover bounded relevant **same-class** local precedents in the target repository (Goals for Goal candidates, Epics for Epic candidates, Meta-Epics for Meta-Epic candidates, comparable roles for Manager/Coordinator candidates, comparable contracts for structural Contract candidates).

- Read materially relevant samples fully enough to extract the recurring local structural pattern. Do not treat titles or issue-table placement as pattern evaluation.
- Derive the pattern from real local examples. Do not impose a universal Meta-Epic template or import structure from other repositories unprompted.
- Discovery stays bounded and relevance-gated. Do not load every historical artifact of the class.
- If bounded discovery finds no relevant local same-class sample, record `NONE_FOUND` and continue using local authority plus the applicable contract. Absence of local samples is evidence, not an error, and must not block. `NONE_FOUND` means discovery ran; it does not mean discovery was skipped.

### Required order before CREATE NEW

When the relevance gate matches, complete this order before any `CREATE_NEW_AUTHORITY` recommendation or creation:

1. **Preserve original structural intent** — state the user's structural question when the ask is candidate analysis or create-new for a durable structure. Do not silently narrow it later.
2. **Existing owner discovery** — identify existing authorities that already claim the desired outcome in whole or in part (for example Product Authority, Umbrella, Goal, Epic, Meta-Epic, Coordinator, Completion Gate, Parent Owner). Relevant candidates must be **fully read**. Title or search snippets alone are insufficient for the final create-new decision. Existing owner discovery alone does not satisfy the gate when same-class precedents or candidate clusters still need evaluation.
3. **Local same-class precedent discovery and pattern extraction** — when structural candidate analysis or create-new for that class is in scope, evaluate relevant local same-class samples as samples and extract the local pattern. If none exist after bounded discovery, record `NONE_FOUND` and continue.
4. **Candidate / cluster fit and candidate reconciliation** — for each serious structural candidate, reconcile against the local pattern and existing authority. An overarching existing owner must not globally terminate all candidate evaluation. Each material candidate gets its own outcome among the allowed decisions below.
5. **Scope overlap check** — state explicitly what the existing authority already owns and what would actually be new on the proposed owner. Thematic relatedness alone is not proof that authority is missing.
6. **Freshness / delta reconciliation** — check chronology. An older parent plus a newer child, dependency, epic, or owner decision often requires reconciling the existing authority rather than inventing a new meta-owner. Default question: is the existing authority merely older than newer relevant decisions? If yes, evaluate update/reconcile first. A newer issue strand does not automatically justify a new meta-layer.
7. **Update / reconcile / link test** — score these as real competing paths, not as a checklist mention:
   - `UPDATE_EXISTING`
   - `RECONCILE_EXISTING`
   - `LINK_EXISTING`
   - `NO_STRUCTURAL_CHANGE`
8. **Missing-authority proof** — name the necessary outcome/scope that **no** existing authority can truthfully own without ownership distortion.
9. **Create new authority** — only if step 8 proves a real ownership gap.

Default when the gap cannot be proven:

```text
DO NOT CREATE NEW AUTHORITY
→ UPDATE_EXISTING | RECONCILE_EXISTING | LINK_EXISTING | NO_STRUCTURAL_CHANGE
```

Allowed structural decisions after the gate:

```text
UPDATE_EXISTING
RECONCILE_EXISTING
LINK_EXISTING
NO_STRUCTURAL_CHANGE
CREATE_NEW_AUTHORITY   # only with documented missing-authority proof
```

Fail closed on premature create-new behavior: designing a new Epic/Meta-Epic/Goal first and reconciling afterward; mentioning an existing owner without comparing scopes; skipping update/link/no-change as real alternatives; recommending create-new from thematic clustering alone; collapsing a structural candidate question into owner-cleanup-only after finding an existing owner; or skipping same-class precedent evaluation when relevant local samples exist.

### Relationship to issue creation

When issue creation is already authorized and the proposed issue would itself be a Goal, Epic, Meta-Epic, Coordinator, or other durable structuring authority, this gate must pass before creation. Title and body rules below remain unchanged and grant no write authority by themselves.

## GitHub issue creation

This section governs issue creation **only when the acting role, operator, or target-repository authority already permits creating an issue**. It grants no new write authority and does not weaken the V1.1 prohibition on automatic follow-up issue creation by scouts. The bounded Improvement Board Manager exception for validated Improvements is defined only by [`IMPROVEMENT_GITHUB_ISSUE_CREATE.md`](IMPROVEMENT_GITHUB_ISSUE_CREATE.md).

When the proposed issue is a durable structuring authority (Goal, Epic, Meta-Epic, Coordinator, or equivalent owner structure), complete [`Authority reconciliation`](#authority-reconciliation) first. Ordinary implementation or bugfix issues under an existing parent do not inherit that gate.

For every new GitHub issue created through Agent Workforce routing or by a workforce-directed agent in a target repository:

- write the issue title in German by default;
- make the title as self-explanatory as practical so that the concrete technical purpose, change, or problem is understandable without opening the issue body;
- short technical prefixes such as `[BUG]`, `[DOCS]`, `[POLICY]`, `[OPS]` may remain, but the meaningful title text after the prefix must be German and descriptive;
- do not use titles that depend only on internal acronyms, slice numbers, issue numbers, or generic wording such as `Fix issue`, `Update docs`, or `Slice 5`;
- the issue body may use whichever language is most appropriate for the repository, contract, or technical task;
- target-repository title conventions remain authoritative and may add stricter requirements; if a local convention conflicts materially with this generic default, follow the target repository's explicit authority and document the exception when needed.

Examples:

- Good: `[DOCS] Externe Referenzliste an den Workforce-Contract anpassen`
- Good: `[BUG] Audio-Vorschau stoppt nach Sample-Wechsel nicht zuverlässig`
- Bad: `[BUG] Fix issue 42`
- Bad: `Slice 5`

The canonical wording lives here. Scheduler prompts, worker prompts, and role files should reference this policy rather than carry their own copied version of the title rule.

## State separation

| Class | Examples | Authority |
|---|---|---|
| Versioned workforce canon | roles, policy, portfolio, templates, contracts, meta topology | this repo |
| Repo-live truth/evidence | code, issues, PRs, CI, Baselines, Finding Deltas | owning repo / GitHub live |
| Mutable operational checkpoint state | Scout checkpoints in Health Books, Supervisor checkpoint in meta issue #3 | acting Scout/Supervisor under `CHECKPOINT_CONTRACT.md` |
| Transient execution metadata | connector errors, scheduler task history, temporary host state | execution host only |
| Derived knowledge | NotebookLM | convenience only |

V1.1 has no dedicated runtime database and no committed `last_run` ledger. Durable inspection/review cursors are only the GitHub checkpoint comments defined by `CHECKPOINT_CONTRACT.md`.

## Role promotion

Create a future manager or specialist only when recurring evidence shows sustained coordination work, repeated specialist judgment, recurring manual/agent tasks, ownership bottlenecks, or repeated failures that deterministic automation cannot solve more cheaply and reliably.

No role gains write authority automatically from age, run count, or personality.

## Improvement Board Manager (bounded specialist)

Canonical role: [`agents/improvement-board-manager.md`](../agents/improvement-board-manager.md).

V1.1 Quality Scout, Process Scout, and Supervisor remain advisory for follow-up issue creation. This specialist is the **only** workforce role authorized for:

1. `improvement_management_write` on the Agent Brain Improvement Blackboard;
2. `improvement_github_issue_create` under the bounded routing contract [`docs/IMPROVEMENT_GITHUB_ISSUE_CREATE.md`](IMPROVEMENT_GITHUB_ISSUE_CREATE.md).

It does **not** receive general Agent Brain Memory/Knowledge write authority, does not become a `global_router`, and does not create a second mutable workforce runtime database. Capability IDs live in [`capabilities/REGISTRY.yml`](../capabilities/REGISTRY.yml).
