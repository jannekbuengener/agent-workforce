# Workforce Policy V1

## Operating model

V1 contains exactly two advisory scouts: Quality Scout and Process Scout. The organization grows only from observed recurring work.

A scheduled run may shallow-preflight all in-scope repositories but deep-inspects exactly one repository.

## Selection priority

Choose the first eligible class below; within a class choose the least-recently-inspected repository:

1. missing baseline for the active scout;
2. unresolved `HIGH`/`CRITICAL` finding due for recheck;
3. meaningful new commit/PR/issue/CI activity since the last material scout observation;
4. periodic sweep candidate that has gone longest without inspection.

Generic bot activity, scout comments, and unchanged automated updates are not meaningful activity by themselves.

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
- Every deviation must be supported by concrete evidence.
- Silence is preferable to manufactured findings.
- Infrastructure/tool/budget failures are classified separately from repo quality.

## Anti-noise and convergence

- One underlying root cause has one stable finding identity.
- Both scouts reuse that identity when they observe the same underlying condition.
- `SKIP_NO_DELTA` creates no Health Book comment.
- Routine unchanged `NO_MATERIAL_CHANGE` creates no comment.
- Recurrence increases only on materially new confirming evidence.
- Resolution requires current evidence.
- A recommended follow-up issue must name the finding it would resolve.
- Repeated false positives are evidence to repair the role contract, not a reason to add more machinery.

## Authority V1

Allowed: read/analyze live state, append evidence-backed Health Book observations, recommend follow-up work, escalate uncertainty.

Forbidden: product-code mutation, implementation PRs, governance changes, secret changes, specialist-agent creation, automatic follow-up issue creation, direct pushes to protected/default branches.

## State separation

| Class | Examples | Authority |
|---|---|---|
| Versioned workforce canon | roles, policy, portfolio, templates | this repo |
| Repo-live evidence | code, issues, PRs, CI, Health Book | owning repo / GitHub live |
| Runtime metadata | task history, connector errors, transient scheduler state | execution host only |
| Derived knowledge | NotebookLM | convenience only |

V1 has no dedicated mutable scheduling database and no committed `last_run` ledger. If future hosts need durable mutable state that cannot be reconstructed safely, it requires a separate runtime-state design.

## Role promotion

Create a future manager or specialist only when recurring evidence shows sustained coordination work, repeated specialist judgment, recurring manual/agent tasks, ownership bottlenecks, or repeated failures that deterministic automation cannot solve more cheaply and reliably.

No role gains write authority automatically from age, run count, or personality.
