# Agent Workforce — Stable Execution Bootstrap

## Purpose

This file is the stable execution-host entry point for Agent Workforce V1.1.

Execution hosts may hard-code only:

- repository: `jannekbuengener/agent-workforce`;
- branch: `main`;
- bootstrap path: `WORKFORCE_BOOTSTRAP.md`;
- requested execution mode: `quality-scout`, `process-scout`, or `supervisor`.

All downstream workforce paths, portfolio membership, Health Book locations, role contracts, policy, checkpoint semantics, capability/reference routing rules, reporting cardinality, and scheduled-run output rules are discovered from live repository canon through this file.

Do not copy the downstream read list, checkpoint contract, capability registry, or shared reference catalog into scheduler/automation prompts.

## Fail-closed bootstrap rule

Before any repository inspection or GitHub write:

1. fetch this file from live `main`;
2. follow the current required-read order below;
3. resolve the requested execution mode to its live role contract/read set;
4. derive portfolio membership and Health Book URLs from the live portfolio;
5. enter the selected target repository and read its local authority before applying workforce assumptions, capability routing, or external-reference routing.

If this bootstrap file, a required workforce authority file, the requested role contract, or the target repository's required authority cannot be read or resolved, do not reconstruct it from memory or an older prompt. Return an explicit blocked outcome (`BLOCKED_AUTHORITY_AMBIGUOUS`, `BLOCKED_NO_REPO_ACCESS`, or `BLOCKED_TOOL_UNAVAILABLE` as appropriate) and perform no evidence write that depends on the missing authority.

If required checkpoint state cannot be read or updated safely after checkpoint-aware routing begins, return `BLOCKED_CHECKPOINT_STATE_UNAVAILABLE`. Never guess or advance state optimistically.

## Required workforce read order

Read the live `main` versions in this order:

1. `README.md` — workforce front door and truth hierarchy;
2. `AGENTS.md` — operating and fail-closed rules;
3. `docs/META_TOPOLOGY.md` — shared meta-repository/metatool classification;
4. `docs/CAPABILITY_ROUTING.md` — specialized capability requirement levels, relevance gate and registry routing;
5. `docs/WORKFORCE_POLICY.md` — selection, evidence, authority and baseline policy;
6. `contracts/CHECKPOINT_CONTRACT.md` — durable Scout/Supervisor cursor semantics;
7. `contracts/FINDING_CONTRACT.md` — finding identity/lifecycle contract;
8. `portfolio/REPOSITORIES.md` — current monitored membership and canonical Health Books;
9. `templates/REPO_HEALTH_BOOK.md` — evidence ledger format and silence rules;
10. the execution-mode-specific read set below.

The ordering above is canonical. If a downstream file is renamed or replaced, update this bootstrap contract; execution-host prompts remain unchanged.

The following are intentionally **conditional**, not unconditional bootstrap reads:

- `capabilities/REGISTRY.yml` and capability-specific contracts such as `docs/REUSE_BEFORE_BUILD.md` — consult only after target-repository authority handoff and only when the current task matches a capability trigger or local authority explicitly routes to one;
- `contracts/EXTERNAL_REFERENCE_CONTRACT.md`, `references/CATALOG.yml`, and target-repository external-reference manifests — consult only when external documentation, technical precedent or reuse/discovery evidence is materially relevant to the current task.

Do not bulk-load the shared reference catalog or a whole repo-local manifest solely because those files exist.

## Execution modes

### `quality-scout`

Read:

- `agents/quality-scout.md`

Then execute exactly one Quality Scout run according to the live role, policy, checkpoint, portfolio, finding and Health Book contracts.

### `process-scout`

Read:

- `agents/process-scout.md`

Then execute exactly one Process Scout run according to the live role, policy, checkpoint, portfolio, finding and Health Book contracts.

### `supervisor`

Read:

- `agents/quality-scout.md`;
- `agents/process-scout.md`;
- Agent Workforce meta issue `#3`, including newer comments that supersede historical rollout snapshots.

The Supervisor validates Scout output quality and contract adherence; it does not duplicate Scout deep inspections or gain product-code authority.

For each Supervisor run:

1. read the single Supervisor checkpoint defined by `contracts/CHECKPOINT_CONTRACT.md`;
2. for each current Health Book, inspect only `INITIAL BASELINE` / `FINDING DELTA` comments whose comment id is newer than that Health Book's `last_reviewed_output_comment_id` cursor;
3. ignore Scout checkpoint comments and all other non-Scout-output comments as review candidates;
4. for each new Scout output, verify correct scout/repository identity, evidence-backed claims, repo-local authority precedence, no invented findings, stable root-cause identity/deduplication, correct Quality-vs-Process lens separation, and correct classification of tool/access/checkpoint failures;
5. derive the current repository denominator from live `portfolio/REPOSITORIES.md`;
6. if new Scout output exists, append one compact meta-issue comment containing timestamp, current `Quality x/N` and `Process y/N` coverage, reviewed repo/scout/Health-Book references, assessment `PASS | CONCERN | BLOCKED`, touched finding IDs, and at most one next action when action is required;
7. after successful review, advance each affected Health Book cursor in the same Supervisor checkpoint to the highest successfully reviewed Scout-output comment id;
8. if no new Scout output exists, create no normal Supervisor comment; checkpoint maintenance may still update `last_supervisor_run_at`;
9. do not repeat already reviewed outputs;
10. notify Jannek only when a real contract defect, duplicate/noisy behavior, wrong authority use, or blocked condition requires intervention; otherwise update the meta issue silently when an update is warranted.

Before the first V1.1 Supervisor run, initialize the Supervisor checkpoint with the evidence-based cutover procedure in `contracts/CHECKPOINT_CONTRACT.md`. Never initialize historical review cursors by guessing or blanket `null` values.

The Supervisor may create/update only its own checkpoint in meta issue `#3`. It must not modify product code, create implementation issues/PRs, promote Scout authority, create managers/specialists, or alter workforce policy automatically.

## Scheduled-run output policy

For `quality-scout` and `process-scout`, return a compact run receipt containing:

- selected repository;
- runtime outcome;
- canonical Repo Health Book URL;
- finding IDs touched, if any.

Notify Jannek only for initial baseline completion, material findings, or blocked runs. Do not notify for noise-only or unchanged outcomes.

For `supervisor`, follow the Supervisor-specific notification and comment rules above.

## Portfolio and baseline derivation

`portfolio/REPOSITORIES.md` is the only canonical source of current monitored membership and Repo Health Book URLs.

Never hard-code a repository count in an execution-host prompt. For reporting, derive the current denominator from the live in-scope portfolio. Baseline completion is `active scout roles × current in-scope repositories`.

A newly added portfolio repository automatically enters missing-baseline priority for every active Scout without a scheduler-prompt edit.

## Target-repository authority handoff

After selecting a target repository:

1. use GitHub/repository live state as current truth;
2. read the target repository's local `AGENTS.md` when present;
3. read its README/front door and relevant canon/architecture/contracts/rules;
4. use the portfolio row to locate its canonical Repo Health Book;
5. classify the current task against `docs/CAPABILITY_ROUTING.md` only after the local authority above is established;
6. if and only if a capability trigger matches or local authority explicitly routes to one, consult the matching entry in `capabilities/REGISTRY.yml`, read any contract referenced by that entry, and enforce its requirement/availability/discovery rules;
7. when external documentation, engineering precedent, or external reuse evidence is materially relevant, follow `contracts/EXTERNAL_REFERENCE_CONTRACT.md`; use the target repository's canonical external-reference manifest when one exists, and consult only matching entries from `references/CATALOG.yml` as reusable discovery/reference anchors;
8. only then apply the selected workforce role's analytical lens.

Target-repository local authority outranks generic workforce assumptions, capability routing, repo-local external-reference manifests, and external sources. The meta layer does not grant implementation ownership or create implicit runtime dependencies. Capability/reference routing selects tools, discovery obligations, or evidence sources; it does not create repository authority or mutation permission.

For relevant planning/implementation work, a `DISCOVERY_REQUIRED` route such as `reuse_before_build` must complete before selecting a new custom implementation path. Trivial or unrelated work must not trigger broad discovery solely because the registry or shared reference catalog exists.

A shared reference catalog entry never proves that the target repository uses that technology/source. Repo-local `P0`/`P1` relevance must be backed by current repository signals; `P2` remains parked until concrete scope activates it.

## Execution-host boundary

Private MCP access is never a worker requirement. Use only tools/evidence available to the execution host. Tool, connector, scheduler or budget failures are operational failures, not repository defects.

When a matching registry entry is `REQUIRED`, unavailability or lack of authorization produces `BLOCKED_REQUIRED_CAPABILITY_UNAVAILABLE`; do not silently substitute another tool.

The scheduler owns cadence and transient task execution only. Durable Scout/Supervisor cursors live exclusively in the GitHub checkpoint comments defined by `CHECKPOINT_CONTRACT.md`; do not introduce a second mutable state store, machine-local capability paths, or machine-local reference paths to support routing.

## Regression invariants

The bootstrap contract is correct only while all of these remain true:

- adding/removing a portfolio member requires changing the live portfolio, not each scheduler prompt;
- renaming a downstream canon file requires changing this bootstrap, not each scheduler prompt;
- an unreadable bootstrap or required authority blocks instead of falling back to memory;
- one checkpoint mechanism is the only durable Scout/Supervisor cursor state;
- checkpoint comments are never treated as Baseline/Finding outputs;
- already reviewed Scout outputs are excluded by the Supervisor cursor rather than by prose-memory heuristics;
- target-repository local authority remains above workforce assumptions, capability routing and external references;
- capability/reference matching occurs after target-repository authority handoff;
- matching registry entries can route to a capability-specific contract without adding that contract to every scheduler prompt;
- relevant new implementation-path decisions honor `DISCOVERY_REQUIRED` before custom build choices;
- shared catalog membership never becomes target-repository usage/dependency evidence;
- repo-local manifests use concrete relevance signals and keep inactive material parked;
- unrelated tasks do not load or invoke registered capabilities/references solely because they exist;
- no execution-host prompt carries a second full copy of the downstream canonical read list, checkpoint contract, capability registry, or shared reference catalog;
- authorized GitHub issue creation inherits its canonical issue-creation rules from `docs/WORKFORCE_POLICY.md`; scheduler/worker prompts do not duplicate those rules.
