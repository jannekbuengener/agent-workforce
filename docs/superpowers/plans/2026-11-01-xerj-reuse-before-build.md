# XERJ Reference Coding in Reuse Before Build Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make XERJ reference coding a mandatory bounded step inside `reuse_before_build` for new features and other meaningful implementation-path decisions.

**Architecture:** Extend the existing registry entry and reuse-before-build contract rather than adding a new Capability ID. Keep execution-host MCP paths local; commit only portable XERJ rules/skills and workforce canon.

**Tech Stack:** Markdown contracts, YAML registry, Python `unittest` structural regression test.

**Spec:** `docs/superpowers/specs/2026-11-01-xerj-reuse-before-build-design.md`

## Global Constraints

- Target-repository authority remains above workforce routing.
- XERJ evidence never authorizes automatic code/dependency adoption.
- Machine-specific executable paths are not committed as workforce canon.
- Existing `reuse_before_build` outcomes remain unchanged.
- Excluded trivial/documentation-only work must not gain broad discovery overhead.

## Review Focus

- New-feature planning must trigger `reuse_before_build`.
- XERJ must occur after repo/dependency inspection but before implementation selection.
- XERJ unavailability must fail closed for a matched route.
- A no-match XERJ result must permit normal discovery to continue.
- Local Cursor/Claude integration must not introduce workstation-specific committed paths.

---

### Task 1: Pin the XERJ gate structurally

**Files:**
- Create: `tools/tests/test_reuse_before_build_xerj.py`
- Modify: `capabilities/REGISTRY.yml`

**Interfaces:**
- Consumes: existing `reuse_before_build` registry entry.
- Produces: machine-readable XERJ reference-coding requirements and trigger semantics.

- [ ] Write structural tests for feature triggers, mandatory XERJ gate, discovery order, evidence outcomes, and blocked behavior.
- [ ] Run the targeted test and verify RED against the current registry.
- [ ] Extend `capabilities/REGISTRY.yml` minimally.
- [ ] Run the targeted test and verify GREEN.

### Task 2: Align human-readable workforce canon

**Files:**
- Modify: `docs/REUSE_BEFORE_BUILD.md`
- Modify: `docs/CAPABILITY_ROUTING.md`
- Modify: `AGENTS.md`
- Modify: `WORKFORCE_BOOTSTRAP.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: Task 1 registry semantics.
- Produces: consistent agent-facing routing and fail-closed instructions.

- [ ] Document the required bounded XERJ step and compact evidence receipt.
- [ ] Document `BLOCKED_TOOL_UNAVAILABLE` when the required XERJ route cannot run.
- [ ] Keep exclusions and authority boundaries explicit.
- [ ] Re-run the targeted structural test.

### Task 3: Preserve portable host integration and regenerate derived data

**Files:**
- Add: `.cursor/rules/xerj.mdc`
- Add: `.cursor/rules/xerj-hub.mdc`
- Add: `.cursor/rules/xerj-reference-coding.mdc`
- Add: `.claude/skills/xerj/SKILL.md`
- Add: `.claude/skills/xerj-hub/SKILL.md`
- Regenerate: `generated/PORTFOLIO_CAPABILITY_INDEX.yml`
- Do not add: `.mcp.json`, `.cursor/mcp.json`, `AGENTS.md.bak`

**Interfaces:**
- Consumes: portable XERJ installer output plus Task 1 registry.
- Produces: editor/agent guidance without host-specific executable paths.

- [ ] Regenerate the portfolio capability index.
- [ ] Verify no committed XERJ file contains `C:\\Users\\janne` or another absolute workstation path.
- [ ] Run repository validation commands and `git diff --check`.
- [ ] Commit the slice on `feat/xerj-reuse-before-build`.
