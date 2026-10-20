# External Reference Rollout Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Roll out the approved external-reference manifest contract to every repository in the live Agent Workforce portfolio, with repository-local ownership and evidence-backed relevance.

**Architecture:** Derive scope from live `portfolio/REPOSITORIES.md`, then treat each repository as an independent docs-only delivery slice. New manifests use `docs/external-docs/index.md` unless local canon already owns an equivalent surface; existing manifests are normalized rather than replaced. `agent-workforce` coordinates only the contract and rollout evidence and never centralizes target-repository technology inventories.

**Tech Stack:** Markdown, GitHub repository docs/canon, existing repo-local validation.

**Spec:** `contracts/EXTERNAL_REFERENCE_CONTRACT.md` plus issue #13.

## Global Constraints

- GitHub/repository live truth and target-repository local authority remain above external references.
- Current portfolio membership is derived from `portfolio/REPOSITORIES.md`, never from a permanent hard-coded count.
- `P0`/`P1` require concrete current repo signals; `P2` is parked/reference-only.
- Source authority is independent from relevance priority.
- No dependency, runtime, CI, governance, provider, security-policy, trading or product-scope mutation.
- No workstation-specific absolute paths, credentials, private endpoints, private samples/data or transient installation state.
- CDB-specific technology lists remain CDB-owned and are not copied into other repositories.
- Every target repository accepts its own changes through its normal PR/review/CI rules.

## Review Focus

- Shared catalog entries must not become repo usage/dependency claims without local evidence.
- Existing repo-local docs/canon organization must be preserved where it already provides the canonical surface.
- P2/future references must not activate implementation or runtime claims.
- Community/example sources must not outrank official/upstream/live repo evidence.
- The rollout must not introduce machine-local or private data.

---

### Task 1: Sample Brain

**Files:**
- Create: `docs/external-docs/index.md`
- Modify: `docs/README.md`

**Interfaces:**
- Consumes: `sample-brain#1198`, root/docs `AGENTS.md`, `pyproject.toml`, live CI/canon.
- Produces: Sample Brain-owned manifest discoverable from its docs front door.

- [ ] Build a compact P0/P1/P2 list from current Python/audio/data/UI/dev-tooling signals only.
- [ ] Include concrete repo signals for every P0/P1 row.
- [ ] Link the manifest from `docs/README.md`.
- [ ] Run/verify docs/canon drift gates applicable to docs changes.
- [ ] Open, review, and merge a docs-only PR; verify issue closure live.

### Task 2: Sample Brain Analysis

**Files:**
- Create: `docs/external-docs/index.md`
- Modify: `docs/README.md`

**Interfaces:**
- Consumes: `sample-brain-analysis#12`, `AGENTS.md`, `PROJECT_META.yaml`, `pyproject.toml`.
- Produces: frontmatter-compliant package-owned reference manifest.

- [ ] Add valid docs frontmatter.
- [ ] Use current package/build/test/CI signals only.
- [ ] Link from `docs/README.md`.
- [ ] Run PROJECT_META quality gates relevant to docs and knowledge graph.
- [ ] Open, review, and merge PR; verify issue closure live.

### Task 3: ARVP

**Files:**
- Create: `docs/external-docs/index.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: `arvp#31`, README, `pyproject.toml`, schemas/tests/workflows.
- Produces: domain-neutral ARVP reference manifest.

- [ ] Keep trading, Sample Brain, Docker and database technology out unless live ARVP state proves relevance.
- [ ] Reference current Python/test/lint/type/schema/build/release tooling with repo evidence.
- [ ] Link from README documentation section.
- [ ] Run applicable docs/test/lint validation.
- [ ] Open, review, and merge PR; verify issue closure live.

### Task 4: Traumtänzer

**Files:**
- Create: `docs/external-docs/index.md`
- Modify: `README.md` only for discoverability.

**Interfaces:**
- Consumes: `traum_taenzer#97`, README, CONTRIBUTING, governance/canon and local harness evidence.
- Produces: governance/evidence-first manifest with no unauthorized provider/runtime claims.

- [ ] Include only current repository/governance/harness/CI references with concrete signals.
- [ ] Keep provider/pilot/live-product references parked or omitted unless local canon proves active scope.
- [ ] Preserve Safety/Privacy/Claims hierarchy.
- [ ] Run CI/security checks required by local contribution rules.
- [ ] Open, review, and merge PR; verify issue closure live.

### Task 5: Claire de Binare

**Files:**
- Modify: `docs/external-docs/index.md`

**Interfaces:**
- Consumes: `Claire_de_Binare#4605`, current CDB index and live CDB authority.
- Produces: normalized CDB index using P0/P1/P2 plus source authority without losing valid CDB-specific signals.

- [ ] Convert `required/secondary/parked` semantics to `P0/P1/P2`.
- [ ] Add/clarify source-type and authority semantics.
- [ ] Preserve valid current CDB repo signals and relevance-gated lookup behavior.
- [ ] Avoid runtime/control-plane/trading/live-readiness mutations.
- [ ] Open, review, and merge docs-only PR; verify issue closure live.

### Task 6: Agent Brain

**Files:**
- Modify: `docs/external-docs/index.md`
- Modify: `AGENTS.md` only where legacy status wording must be reconciled.

**Interfaces:**
- Consumes: `agent-brain#28`, AGENTS, README/start/extraction canon, `pyproject.toml` and CI.
- Produces: normalized Agent Brain manifest using P0/P1/P2 + source authority without converting planned extraction technologies into runtime claims.

- [ ] Replace/align `ACTIVE/NEXT/REFERENCE/PARKED` semantics with contract-compliant relevance semantics.
- [ ] Preserve current Python/build/test/CI evidence.
- [ ] Keep SurrealDB/MCP/other future technologies parked unless local canon proves current usage.
- [ ] Reconcile AGENTS read-path wording.
- [ ] Open, review, and merge PR; verify issue closure live.

### Task 7: Portfolio acceptance and closeout

**Files:**
- Update this plan only if delivery evidence materially changes the implementation route.

**Interfaces:**
- Consumes: all six merged owning PRs and live `portfolio/REPOSITORIES.md`.
- Produces: closure evidence for `agent-workforce#13` and tracker #18.

- [ ] Re-read live portfolio membership after all merges.
- [ ] Verify every in-scope repo has a canonical manifest/equivalent and correct discoverability.
- [ ] Spot-check P0/P1 entries against live repo files/config/dependencies/workflows.
- [ ] Verify P2 remains parked and manifests contain no private absolute paths.
- [ ] Verify owning issues are closed/completed.
- [ ] Close #18 and #13 only after live acceptance is satisfied.