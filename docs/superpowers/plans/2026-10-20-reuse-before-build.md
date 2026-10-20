# Reuse Before Build Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a relevance-gated reuse-before-build discovery contract and route relevant planning/implementation tasks through `DISCOVERY_REQUIRED` before custom implementation decisions.

**Architecture:** Keep capability classification in `capabilities/REGISTRY.yml`, put the engineering decision procedure in `docs/REUSE_BEFORE_BUILD.md`, and expose it through the existing capability-routing/front-door surfaces. Do not add runtime state, dependency automation, or external-reference catalogs.

**Tech Stack:** Markdown, YAML, GitHub repository canon.

**Spec:** `docs/superpowers/specs/2026-10-20-reuse-before-build-design.md`

## Global Constraints

- Target-repository live state and local authority remain above workforce routing.
- `reuse_before_build` is `DISCOVERY_REQUIRED`, not `REQUIRED`.
- Discovery is relevance-gated and bounded.
- Existing repo code and existing dependencies are evaluated before external alternatives.
- No automatic dependency installation or OSS adoption.
- Community sources never outrank official/upstream/current repo evidence.
- Issues #12/#13 remain out of scope.

## Review Focus

- Trivial fixes must not trigger broad ecosystem research.
- Existing dependency reuse must be preferred before new external adoption when technically suitable.
- Mature OSS may still be rejected for offline, license, security, compatibility, performance, or architecture reasons.
- Custom implementation remains valid when alternatives are insufficient.
- Adding `reuse_before_build` must not weaken or alter the REA hard gate.

---

### Task 1: Canonical reuse-before-build contract

**Files:**
- Create: `docs/REUSE_BEFORE_BUILD.md`

**Interfaces:**
- Consumes: issue #11 and the approved design spec.
- Produces: the canonical bounded discovery order, evaluation criteria, source hierarchy, and compact decision outcomes.

- [ ] Write the complete contract from the spec.
- [ ] Verify it explicitly covers the seven-step discovery order and three decision outcomes.
- [ ] Verify it states relevance gating, bounded research, and no automatic mutation authority.

### Task 2: Route through capability registry

**Files:**
- Modify: `capabilities/REGISTRY.yml`
- Modify: `docs/CAPABILITY_ROUTING.md`

**Interfaces:**
- Consumes: Task 1 contract path `docs/REUSE_BEFORE_BUILD.md`.
- Produces: `reuse_before_build` as a `DISCOVERY_REQUIRED` registry entry and routing semantics that point relevant tasks to the contract.

- [ ] Add `reuse_before_build` without changing `reverse_engineering` semantics.
- [ ] Define meaningful triggers and exclusions so trivial work does not trigger discovery.
- [ ] Encode the ordered discovery stages and compact outcomes without inventing a mandatory tool.
- [ ] Update capability-routing documentation to state that reuse-before-build is now active and separate from external-reference work.

### Task 3: Front-door integration and validation

**Files:**
- Modify: `WORKFORCE_BOOTSTRAP.md`
- Modify: `AGENTS.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: Tasks 1-2 routing contract and registry entry.
- Produces: discoverability from stable bootstrap/front door while retaining relevance-gated registry loading.

- [ ] Expose the reuse-before-build contract without copying its procedure into scheduler prompts.
- [ ] Verify target-repository authority handoff still occurs before capability matching.
- [ ] Parse the final registry as YAML and confirm exactly two capabilities exist: `reverse_engineering` and `reuse_before_build`.
- [ ] Dry-reason the four issue #11 validation cases.
- [ ] Diff-review for scope leaks into #12/#13, local absolute paths, or REA semantic drift.
