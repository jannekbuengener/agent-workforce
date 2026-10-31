# cursor-meta-epic-executor — Distribution & Host Usage

## Canonical source

Workforce-owned skill body:

```text
docs/skills/cursor-meta-epic-executor/SKILL.md
```

Do **not** copy the skill body into product repositories. Product repos may
reference [`docs/META_EPIC_CONTRACT.md`](META_EPIC_CONTRACT.md) and name the
required execution skill.

Machine-readable consumer declaration (skill-colocated, not a new global
inventory tree):

```text
docs/skills/cursor-meta-epic-executor/consumer.yml
```

## Local Cursor install (user-level)

Install from the workforce checkout into the user skill directory Cursor
discovers:

```text
~/.cursor/skills/cursor-meta-epic-executor/SKILL.md
```

Recommended: copy or symlink the whole skill folder from canon so
`references/` remains available.

After install, invoke with `/cursor-meta-epic-executor` or keep it on for the
session as a **Custom Mode** (Option+Enter / Alt+Enter).

## Long-running Meta-Epics

1. Activate the skill as Custom Mode.
2. If available, set `/goal <Meta-Epic Exit token>`.
3. Follow the skill loop: authority → live reconcile → plan-before-write →
   gated execute → independent verify → replan → exit → learn.

If `/goal` is required by the run contract and unavailable, stop with
`BLOCKED_GOAL_EXECUTION_MODE_UNAVAILABLE`.

## Multitask / isolation

- Prefer parallel Subagent/Task launches for independent read-only or
  non-overlapping work.
- Use `/multitask` in the Agents Window when that surface is available.
- Isolate parallel writers with worktrees / isolated environments.

## Cloud Agents

- User-level `~/.cursor/skills` reaches Cloud Agents only after **Sync Skills
  for Cloud Agents** is enabled (Settings → Agents).
- Automations do not load synced personal skills; they need project skills if
  a skill must be present — still without duplicating this skill into every
  product repo as a second canon. Prefer sync for operator-started Cloud
  Agents; keep workforce `docs/skills/` as authority.

## Related

- Skill: [`skills/cursor-meta-epic-executor/SKILL.md`](skills/cursor-meta-epic-executor/SKILL.md)
- Meta-Epic contract: [`META_EPIC_CONTRACT.md`](META_EPIC_CONTRACT.md)
- Issue #41 exit: `CURSOR_META_EPIC_EXECUTOR_PILOT_PROVEN`
