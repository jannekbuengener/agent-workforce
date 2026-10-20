# Agent Workforce — Stable Execution Bootstrap

## Purpose

This file is the stable execution-host entry point for Agent Workforce V1.

Execution hosts may hard-code only:

- repository: `jannekbuengener/agent-workforce`;
- branch: `main`;
- bootstrap path: `WORKFORCE_BOOTSTRAP.md`;
- requested execution mode: `quality-scout`, `process-scout`, or `supervisor`.

All downstream workforce paths, portfolio membership, Health Book locations, role contracts, policy, capability-routing rules, reporting cardinality, and scheduled-run output rules are discovered from live repository canon through this file.

Do not copy the downstream read list or capability registry into scheduler/automation prompts.

## Fail-closed bootstrap rule

Before any repository inspection or GitHub write:

1. fetch this file from live `main`;
2. follow the current required-read order below;
3. resolve the requested execution mode to its live role contract/read set;
4. derive portfolio membership and Health Book URLs from the live portfolio;
5. enter the selected target repository and read its local authority before applying workforce assumptions or capability routing.

If this bootstrap file, a required workforce authority file, the requested role contract, or the target repository's required authority cannot be read or resolved, do not reconstruct it from memory or an older prompt. Return an explicit blocked outcome (`BLOCKED_AUTHORITY_AMBIGUOUS`, `BLOCKED_NO_REPO_ACCESS`, or `BLOCKED_TOOL_UNAVAILABLE` as appropriate) and perform no evidence write that depends on the missing authority.

## Required workforce read order

Read the live `main` versions in this order:

1. `README.md` — workforce front door and truth hierarchy;
2. `AGENTS.md` — operating and fail-closed rules;
3. `docs/META_TOPOLOGY.md` — shared meta-repository/metatool classification;
4. `docs/CAPABILITY_ROUTING.md` — specialized capability requirement levels, relevance gate and registry routing;
5. `docs/WORKFORCE_POLICY.md` — selection, evidence, authority and baseline policy;
6. `contracts/FINDING_CONTRACT.md` — finding identity/lifecycle contract;
7. `portfolio/REPOSITORIES.md` — current monitored membership and canonical Health Books;
8. `templates/REPO_HEALTH_BOOK.md` — evidence ledger format and silence rules;
9. the execution-mode-specific read set below.

The ordering above is canonical. If a downstream file is renamed or replaced, update this bootstrap contract; execution-host prompts remain unchanged.

`capabilities/REGISTRY.yml` is intentionally not part of the unconditional read set. Consult it only after target-repository authority handoff and only when the current task matches a capability trigger or the target repository explicitly routes to a registered capability.

## Execution modes

### `quality-scout`

Read:

- `agents/quality-scout.md`

Then execute exactly one Quality Scout run according to the live role, policy, portfolio, finding and Health Book contracts.

### `process-scout`

Read:

- `agents/process-scout.md`

Then execute exactly one Process Scout run according to the live role, policy, portfolio, finding and Health Book contracts.

### `supervisor`

Read:

- `agents/quality-scout.md`;
- `agents/process-scout.md`;
- Agent Workforce meta issue `#3`, including newer comments that supersede historical rollout snapshots.

The supervisor validates scout output quality and contract adherence; it does not duplicate scout deep inspections or gain product-code authority.

For each supervisor run:

1. determine whether new scout output has appeared since the most recent Workforce Supervisor comment in meta issue `#3`;
2. for each new baseline or finding delta, verify correct scout/repository identity, evidence-backed claims, repo-local authority precedence, no invented findings, stable root-cause identity/deduplication, correct Quality-vs-Process lens separation, and correct classification of tool/access failures;
3. derive the current repository denominator from live `portfolio/REPOSITORIES.md`;
4. if new scout output exists, append one compact meta-issue comment containing timestamp, current `Quality x/N` and `Process y/N` coverage, reviewed repo/scout/Health-Book references, assessment `PASS | CONCERN | BLOCKED`, touched finding IDs, and at most one next action when action is required;
5. do not comment when nothing materially new has appeared and do not repeat already reviewed outputs;
6. notify Jannek only when a real contract defect, duplicate/noisy behavior, wrong authority use, or blocked condition requires intervention; otherwise update the meta issue silently when an update is warranted.

The supervisor must not modify product code, create implementation issues/PRs, promote scout authority, create managers/specialists, or alter workforce policy automatically.

## Scheduled-run output policy

For `quality-scout` and `process-scout`, return a compact run receipt containing:

- selected repository;
- runtime outcome;
- canonical Repo Health Book URL;
- finding IDs touched, if any.

Notify Jannek only for initial baseline completion, material findings, or blocked runs. Do not notify for noise-only or unchanged outcomes.

For `supervisor`, follow the supervisor-specific notification and comment rules above.

## Portfolio and baseline derivation

`portfolio/REPOSITORIES.md` is the only canonical source of current monitored membership and Repo Health Book URLs.

Never hard-code a repository count in an execution-host prompt. For reporting, derive the current denominator from the live in-scope portfolio. Baseline completion is `active scout roles × current in-scope repositories`.

A newly added portfolio repository automatically enters missing-baseline priority for every active scout without a scheduler-prompt edit.

## Target-repository authority handoff

After selecting a target repository:

1. use GitHub/repository live state as current truth;
2. read the target repository's local `AGENTS.md` when present;
3. read its README/front door and relevant canon/architecture/contracts/rules;
4. use the portfolio row to locate its canonical Repo Health Book;
5. classify the current task against `docs/CAPABILITY_ROUTING.md` only after the local authority above is established;
6. if and only if a capability trigger matches or local authority explicitly routes to one, consult the matching entry in `capabilities/REGISTRY.yml` and enforce its requirement/availability rules;
7. only then apply the selected workforce role's analytical lens.

Target-repository local authority outranks generic workforce assumptions and generic capability routing. The meta layer does not grant implementation ownership or create implicit runtime dependencies. Capability routing selects tools; it does not create repository authority.

## Execution-host boundary

Private MCP access is never a worker requirement. Use only tools/evidence available to the execution host. Tool, connector, scheduler or budget failures are operational failures, not repository defects.

When a matching registry entry is `REQUIRED`, unavailability or lack of authorization produces `BLOCKED_REQUIRED_CAPABILITY_UNAVAILABLE`; do not silently substitute another tool.

The scheduler owns cadence and transient run metadata only. This repository owns versioned workforce canon. Do not persist mutable scheduler state or machine-local capability paths here merely to support routing.

## Regression invariants

The bootstrap contract is correct only while all of these remain true:

- adding/removing a portfolio member requires changing the live portfolio, not each scheduler prompt;
- renaming a downstream canon file requires changing this bootstrap, not each scheduler prompt;
- an unreadable bootstrap or required authority blocks instead of falling back to memory;
- target-repository local authority remains above workforce assumptions and capability routing;
- capability matching occurs after target-repository authority handoff;
- unrelated tasks do not load or invoke registered capabilities solely because they exist;
- no execution-host prompt carries a second full copy of the downstream canonical read list or capability registry.
