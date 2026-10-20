# Capability Routing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a canonical relevance-gated capability-routing contract with a hard `REQUIRED` gate for REA-based reverse engineering.

**Architecture:** Keep a small human-readable routing contract in `docs/CAPABILITY_ROUTING.md` and a machine-readable registry in `capabilities/REGISTRY.yml`. The stable bootstrap always discovers the routing contract, but the registry is consulted only after target-repository authority handoff and only for relevant task triggers.

**Tech Stack:** Markdown, YAML, GitHub repository canon.

**Spec:** `docs/superpowers/specs/2026-10-20-capability-routing-design.md`

## Global Constraints

- Target-repository local authority remains above generic workforce capability routing.
- `REQUIRED` unavailable or unauthorized means `BLOCKED_REQUIRED_CAPABILITY_UNAVAILABLE`; no silent substitute.
- The registry contains portable identities only; no machine-local absolute paths or transient install state.
- Capability routing is relevance-gated; unrelated tasks must not load or invoke REA.
- Scheduler/worker prompts must not duplicate the registry.

## Review Focus

- Ambiguous trigger wording accidentally routes ordinary web research through REA.
- A missing REA installation silently falls back to another reverse-engineering tool.
- Registry fields leak workstation-specific paths or transient host state.
- Bootstrap ordering causes capability routing to run before target-repository authority.
- Front-door docs describe capability routing as ownership/authority rather than tool selection.

---

### Task 1: Canonical capability contract and registry

**Files:**
- Create: `docs/CAPABILITY_ROUTING.md`
- Create: `capabilities/REGISTRY.yml`

**Interfaces:**
- Consumes: approved requirement levels and Reverse Engineering V1 decisions from the spec.
- Produces: one human-readable routing contract and one machine-readable `reverse_engineering` entry used by bootstrap/front-door routing.

- [ ] **Step 1:** Create the routing contract defining authority order, relevance gating, requirement-level semantics, registry ownership, availability/authorization behavior, and the hard REQUIRED failure outcome.
- [ ] **Step 2:** Create `REGISTRY.yml` with schema version, allowed requirement levels, and the single `reverse_engineering` capability using REA / `morluto/rea` / canonical upstream URL.
- [ ] **Step 3:** Verify the YAML parses and contains no absolute Windows path pattern, credentials, or host-specific installation field.
- [ ] **Step 4:** Read both files back from the topic branch and compare them against Issue #10 acceptance criteria.

### Task 2: Bootstrap and front-door integration

**Files:**
- Modify: `WORKFORCE_BOOTSTRAP.md`
- Modify: `README.md`
- Modify: `AGENTS.md`

**Interfaces:**
- Consumes: `docs/CAPABILITY_ROUTING.md` and `capabilities/REGISTRY.yml` from Task 1.
- Produces: discoverability from the stable bootstrap/front door without copying registry contents into scheduler prompts.

- [ ] **Step 1:** Add `docs/CAPABILITY_ROUTING.md` to the bootstrap required-read order.
- [ ] **Step 2:** Extend target-repository authority handoff so capability classification occurs only after local authority is read; consult the registry only when a trigger is relevant.
- [ ] **Step 3:** Expose routing contract and registry from README.
- [ ] **Step 4:** Add capability-routing precedence and `BLOCKED_REQUIRED_CAPABILITY_UNAVAILABLE` to AGENTS fail-closed rules.
- [ ] **Step 5:** Read all three modified files back and verify repo-local authority still wins.

### Task 3: Whole-slice validation and delivery

**Files:**
- Review all files changed by this plan.

**Interfaces:**
- Consumes: Tasks 1-2.
- Produces: evidence that Issue #10 is satisfied without scope leakage into #11-#13.

- [ ] **Step 1:** Compare the branch against `main`; expected scope is spec/plan plus capability contract, registry, bootstrap, README and AGENTS only.
- [ ] **Step 2:** Dry-reason four cases: REA available; REA unavailable; target repo forbids/overrides generic capability use; unrelated task does not consult REA.
- [ ] **Step 3:** Search active changed canon for `D:\\` or other committed host-specific path assumptions; expected no production-canon matches.
- [ ] **Step 4:** Confirm no scheduler prompt or portfolio membership was changed.
- [ ] **Step 5:** Open a PR with `Closes #10`, verify mergeability/checks/reviews, merge exact head when gates allow, then verify `main` and Issue #10 closed live.