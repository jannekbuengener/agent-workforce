# External Reference Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a generic external-reference contract, compact shared catalog, and reusable repo-local manifest template without performing the portfolio rollout owned by issue #13.

**Architecture:** Keep cross-repository source discovery in a small workforce-owned YAML catalog while repository-specific relevance stays in each target repository's own manifest. Route both through a contract that separates P0/P1/P2 relevance from source authority and requires relevance-gated loading after target-repository authority handoff.

**Tech Stack:** Markdown, YAML, GitHub repository canon.

**Spec:** `docs/superpowers/specs/2026-10-20-external-reference-contract-design.md`

## Global Constraints

- GitHub/repository live truth and target-repository local authority remain above external references.
- Priority (`P0`/`P1`/`P2`) expresses repository relevance, not truth authority.
- Shared catalog membership never proves target-repository relevance.
- No workstation-specific absolute paths, credentials, private endpoints or transient installation state.
- No target-repository rollout in this slice; issue #13 owns rollout.
- Community/example sources may assist discovery/experience but never override official/upstream/current repo evidence.

## Review Focus

- A global catalog entry must not silently become a repo-local technology/dependency assertion.
- `P2` must stay parked and must not activate implementation assumptions.
- Source authority must be independent from P0/P1/P2 priority.
- Relevance gating must prevent whole-catalog context dumps.
- Template/catalog must remain portable and free of machine-local paths.

---

### Task 1: Canonical external-reference contract

**Files:**
- Create: `contracts/EXTERNAL_REFERENCE_CONTRACT.md`

**Interfaces:**
- Consumes: issue #12 and `docs/superpowers/specs/2026-10-20-external-reference-contract-design.md`.
- Produces: canonical semantics consumed by catalog, template, bootstrap/front-door guidance and issue #13 rollout.

- [ ] Define shared-catalog vs repo-local ownership.
- [ ] Define P0/P1/P2 independently from source-authority precedence.
- [ ] Define inclusion rule, relevance-gated loading, repo-signal requirement and parked semantics.
- [ ] Define live-repo authority and privacy/path boundaries.
- [ ] Read back the file and verify every issue #12 acceptance criterion represented by the contract.

### Task 2: Shared catalog and repo-local template

**Files:**
- Create: `references/CATALOG.yml`
- Create: `templates/EXTERNAL_REFERENCE_INDEX.md`

**Interfaces:**
- Consumes: Task 1 contract enums/semantics.
- Produces: small cross-repo seed catalog and generic manifest schema for issue #13.

- [ ] Seed only GitHub Docs, GitHub CLI, Python docs, Stack Overflow, Awesome Python and Awesome System Design.
- [ ] Give every catalog entry source type, authority, purpose and `when_to_use`; make clear catalog entries do not imply repo relevance.
- [ ] Template must represent name, URL/portable identity, priority, source type/authority, category, purpose, concrete `repo_signal`, `when_to_use`, and parked state.
- [ ] Template must include separate active and parked guidance and prohibit local absolute paths.
- [ ] Parse YAML and verify allowed authority/priority values.

### Task 3: Workforce discovery integration

**Files:**
- Modify: `README.md`
- Modify: `AGENTS.md`
- Modify: `WORKFORCE_BOOTSTRAP.md`
- Modify: `docs/REUSE_BEFORE_BUILD.md` only if needed to link external-reference discovery without changing its decision contract.

**Interfaces:**
- Consumes: Tasks 1-2.
- Produces: discoverability without scheduler prompt duplication or unconditional catalog loading.

- [ ] Expose contract/catalog/template from README.
- [ ] Tell agents when to consult repo-local manifests and shared catalog after local-authority handoff.
- [ ] Keep catalog/manifests outside unconditional scheduler read sets.
- [ ] Preserve current REA and reuse-before-build semantics.
- [ ] Do not create any target-repo manifest.

### Task 4: Validation and delivery

**Files:**
- Review all branch changes.

**Interfaces:**
- Consumes: Tasks 1-3.
- Produces: PR satisfying issue #12.

- [ ] Compare branch to live `main` and confirm only generic contract/catalog/template/front-door/spec/plan files changed.
- [ ] Dry-run: Python docs as official; Stack Overflow as community; Awesome Python as example/discovery; direct runtime dependency as P0/P1 with repo signal; future inactive technology as P2 parked.
- [ ] Verify no `D:\`/Windows absolute path appears in contract/catalog/template/front-door files.
- [ ] Verify no Claire-specific technologies were bulk-copied into `references/CATALOG.yml`.
- [ ] Open PR with `Closes #12`, inspect merge gates, merge when clean, then verify live `main` and issue closure.
