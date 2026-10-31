# Workforce Policy V1.1

## Operating model

V1.1 contains exactly two advisory scouts: Quality Scout and Process Scout. The organization grows only from observed recurring work.

Separately, and only by explicit policy change, Agent Workforce may authorize a
bounded specialist such as the Improvement Board Manager. Specialists do not
replace or promote the advisory scouts; scout V1.1 authority remains unchanged.

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


Scout and Supervisor V1.1 authority is intentionally unchanged by specialist
authorization below. Quality Scout, Process Scout, and Workforce Supervisor gain
**no** Improvement Blackboard Observation Write, Management Write, or GitHub
Issue Create authority from the Board Manager role.

## Improvement Board Manager (specialist)

Canonical role: [../agents/improvement-board-manager.md](../agents/improvement-board-manager.md).

The Improvement Board Manager is an authorized specialist
(claims_global_routing: false) for the Skill Improvement Blackboard. It is not
a second global router, not a Repo Manager, and not a general Agent Brain
Memory/Knowledge writer.

Authority grows capability-by-capability only:

`	ext
READ                      → improvement_read
OBSERVATION_WRITE         → improvement_observation_write
MANAGEMENT_WRITE          → improvement_management_write
GITHUB_ISSUE_CREATE       → improvement_github_issue_create  (#51 contract)
`

shared_context_evidence alone does **not** authorize Observation Write,
Management Write, or GitHub Issue Create on the Improvement Blackboard.

Allowed for the Board Manager within blackboard scope when the matching
Capability ID is available and authorized: read improvements and evidence;
append observations; validate dedupe; merge with audited lineage; set priority;
transition lifecycle with evidence; link related work; record verification.

GitHub implementation-issue creation requires the separate Capability ID
improvement_github_issue_create and [IMPROVEMENT_GITHUB_ISSUE_CREATE.md](IMPROVEMENT_GITHUB_ISSUE_CREATE.md)
(workforce issue #51). Until that contract's gates are complete → HOLD.

Forbidden for the Board Manager: expanding Scout/Supervisor authority; overriding
target-repository ownership; inventing routing when the owner is unclear;
auto-merging when improvement identity is ambiguous; general Agent Brain
Memory/Knowledge writes; skill-code mutation; implementation PRs from this role
contract; secrets/governance/protected-branch mutation; creating new specialist
roles; inventing a second mutable workforce runtime database for blackboard state.

## Authority reconciliation

Invariant id: `AUTHORITY_RECONCILIATION_REQUIRED`.

Producer and planning flows that reach a structural decision after routing must complete this gate **before** `DECIDE` when the relevance gate matches:

```text
UNDERSTAND → VERIFY LIVE → ROUTE → AUTHORITY RECONCILIATION → DECIDE → …
```

This gate prevents recommending, designing, or creating a new durable structuring authority when an existing canonical owner already owns the desired outcome or only needs update/reconciliation/linking. It does not replace target-repository authority and does not grant write permission.

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

Do **not** inflate ordinary delivery work with this gate. Ordinary implementation children, small bugfix slices, documentation-only edits, and other bounded child work under an already-settled parent do not trigger a new authority-structure search merely because planning language appears in the request.

Reads remain relevance-gated. Do not inventory every parent or open issue in the portfolio solely because a planning ask arrived.

### Required order before CREATE NEW

When the relevance gate matches, complete this order before any `CREATE_NEW_AUTHORITY` recommendation or creation:

1. **Existing owner discovery** — identify existing authorities that already claim the desired outcome in whole or in part (for example Product Authority, Umbrella, Goal, Epic, Meta-Epic, Coordinator, Completion Gate, Parent Owner). Relevant candidates must be **fully read**. Title or search snippets alone are insufficient for the final create-new decision.
2. **Scope overlap check** — state explicitly what the existing authority already owns and what would actually be new on the proposed owner. Thematic relatedness alone is not proof that authority is missing.
3. **Freshness / delta reconciliation** — check chronology. An older parent plus a newer child, dependency, epic, or owner decision often requires reconciling the existing authority rather than inventing a new meta-owner. Default question: is the existing authority merely older than newer relevant decisions? If yes, evaluate update/reconcile first. A newer issue strand does not automatically justify a new meta-layer.
4. **Update / reconcile / link test** — score these as real competing paths, not as a checklist mention:
   - `UPDATE_EXISTING`
   - `RECONCILE_EXISTING`
   - `LINK_EXISTING`
   - `NO_STRUCTURAL_CHANGE`
5. **Missing-authority proof** — name the necessary outcome/scope that **no** existing authority can truthfully own without ownership distortion.
6. **Create new authority** — only if step 5 proves a real ownership gap.

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

Fail closed on premature create-new behavior: designing a new Epic/Meta-Epic/Goal first and reconciling afterward; mentioning an existing owner without comparing scopes; skipping update/link/no-change as real alternatives; or recommending create-new from thematic clustering alone.

### Relationship to issue creation

When issue creation is already authorized and the proposed issue would itself be a Goal, Epic, Meta-Epic, Coordinator, or other durable structuring authority, this gate must pass before creation. Title and body rules below remain unchanged and grant no write authority by themselves.

## GitHub issue creation

This section governs issue creation **only when the acting role, operator, or target-repository authority already permits creating an issue**. It grants no new write authority and does not weaken the V1.1 prohibition on automatic follow-up issue creation for Quality Scout, Process Scout, or Workforce Supervisor. The Improvement Board Manager may create implementation issues only when Capability ID improvement_github_issue_create and issue #51 gates are satisfied.

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

The Improvement Board Manager is the first evidence-backed specialist authorized
under this rule for Skill-Learning blackboard consolidation. Its existence does
not auto-promote scouts and does not grant other roles Management Write or
GitHub Issue Create.

No role gains write authority automatically from age, run count, or personality.

## Improvement Board Manager (bounded specialist)

Canonical role: [`agents/improvement-board-manager.md`](../agents/improvement-board-manager.md).

V1.1 Quality Scout, Process Scout, and Supervisor remain advisory for follow-up issue creation. This specialist is the **only** workforce role authorized for:

1. `improvement_management_write` on the Agent Brain Improvement Blackboard;
2. `improvement_github_issue_create` under the bounded routing contract (issue #51 / `docs/IMPROVEMENT_GITHUB_ISSUE_CREATE.md` when present).

It does **not** receive general Agent Brain Memory/Knowledge write authority, does not become a `global_router`, and does not create a second mutable workforce runtime database. Capability IDs live in [`capabilities/REGISTRY.yml`](../capabilities/REGISTRY.yml).
