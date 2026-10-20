# German Self-Explanatory Issue Titles Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make German, self-explanatory GitHub issue titles the canonical default for all issue creation authorized through Agent Workforce routing.

**Architecture:** Keep the actual title rule in `docs/WORKFORCE_POLICY.md`, which every execution mode already reads through `WORKFORCE_BOOTSTRAP.md`. Add only lightweight references in agent/bootstrap surfaces so the rule is inherited rather than duplicated.

**Tech Stack:** Markdown repository policy and bootstrap contracts.

**Spec:** Agent Workforce issue #24.

## Global Constraints

- Do not grant new issue-creation authority; the rule applies only when issue creation is already authorized.
- Repo-local authority remains valid and may impose stricter conventions.
- Issue bodies remain free to use the language appropriate to the repository/task.
- Scheduler and worker prompts must not duplicate the title wording.

## Review Focus

- German title requirement must not be mistaken for a German-only issue-body requirement.
- Technical prefixes such as `[BUG]`, `[DOCS]`, `[POLICY]`, `[OPS]` must remain allowed.
- The title must explain purpose/problem without relying on an internal slice number or acronym alone.
- Existing scout prohibition on automatic follow-up issue creation must remain unchanged.
- Central policy must be inherited through bootstrap instead of copied into execution-host prompts.

---

### Task 1: Canonical issue-title policy

**Files:**
- Modify: `docs/WORKFORCE_POLICY.md`
- Modify: `AGENTS.md`
- Modify: `WORKFORCE_BOOTSTRAP.md`

**Interfaces:**
- Consumes: existing Workforce Policy required-read position in the bootstrap.
- Produces: one canonical issue-title rule inherited by authorized workforce issue creation.

- [x] Add a `GitHub issue creation` section to `docs/WORKFORCE_POLICY.md` with German/self-explanatory title rules and positive/negative examples.
- [x] Add a reference-only instruction in `AGENTS.md`; do not duplicate the title wording.
- [x] Add a bootstrap regression invariant that scheduler/worker prompts inherit issue-creation policy from `WORKFORCE_POLICY.md` rather than hard-coding it.
- [x] Verify no existing V1 authority prohibition was weakened.
- [x] Verify no issue-body language restriction was introduced.
- [x] Review branch diff against issue #24 and open a PR with `Closes #24`.