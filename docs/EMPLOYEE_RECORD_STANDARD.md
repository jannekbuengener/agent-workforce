# Digital Employee Record Standard

## Purpose

Defines the canonical structure for durable digital employee records in Agent Workforce.

An employee record is a single Markdown document with two layers:

1. a short human-readable profile at the top for fast recognition by the Owner;
2. a canonical machine-readable YAML record below for roles, lifecycle, authority and operations.

The human profile is descriptive only. It is never authority, never evidence and never a source for permission decisions.

## Required document shape

```text
# Mitarbeiterakte — <Display Name>

## Menschliches Profil
<short human-readable profile>

---

## MACHINE RECORD
```yaml
<canonical machine-readable record>
```
```

## Human-readable profile

The top section is intentionally compact and may include:

- display name and job title;
- short portrait / mini-biography;
- personality and working style;
- strengths;
- weaknesses / typical blind spots;
- memorable personal traits or harmless backstory used by the Owner to distinguish employees;
- a short note explaining how the person generally behaves at work.

Rules:

- human profile content must not grant rights;
- human profile content must not be treated as technical evidence;
- personality traits must not override factual, safety, authority or quality rules;
- invented or decorative biographical details must stay clearly in the human profile and must not leak into machine decisions;
- communication constraints that materially affect work may additionally appear in the machine record.

## Machine record

The `MACHINE RECORD` YAML block is canonical for all operational interpretation.

Minimum fields:

```yaml
schema_version: 1
employee:
  id: string
  display_name: string
  job_title: string
  department: string
  reports_to: string
  employment_state: PLANNED_ONLY | ACTIVE | SUSPENDED | RETIRED
  runtime_exists: false

lifecycle:
  current_state: string
  activation_initial_operating_phase: string

mission:
  purpose: string
  success_definition: string

responsibilities: []
competencies: []

organization:
  direct_reports: []
  can_delegate: false
  can_recommend_new_roles: false

authority:
  decision_rights: []
  approval_rights: []
  forbidden: []

knowledge_scope:
  owns: []
  does_not_own: []

capabilities:
  required: []
  optional: []

tools: []
memory: {}
communication: {}
reporting: {}
escalation: {}
audit: {}
development: {}
```

Repositories may add fields, but they must not silently redefine these meanings.

## Lifecycle truth

A documented employee is not automatically an existing employee.

The record must distinguish at least:

- `PLANNED_ONLY`: role/profile/document exists, but no live agent/runtime/account/automation has been provisioned;
- `ACTIVE`: employee has actually been instantiated and can perform work through authorized execution surfaces;
- `SUSPENDED`: employee exists but is intentionally not allowed to operate;
- `RETIRED`: employee is no longer an active workforce member.

For `PLANNED_ONLY` records, `runtime_exists` must be `false`.

No document, issue, persona, role name or planned capability may be treated as proof that an employee is active.

## Operating phases

An employee may have a future first operating phase that differs from the current lifecycle state.

Example:

```yaml
lifecycle:
  current_state: PLANNED_ONLY
  activation_initial_operating_phase: FOUNDING_SOLO
```

This means the employee does not exist yet, but once activated will initially operate alone until additional staff are actually created.

Recommended phase semantics:

- `FOUNDING_SOLO`: Head performs necessary operational work personally because no specialist team exists yet;
- `BUILDING_TEAM`: specialist roles are added progressively and operational tasks move to them;
- `DEPARTMENT_HEAD`: Head primarily prioritizes, delegates, decides, reviews and reports.

Phases describe operating reality, not aspiration. Transition only when live workforce state supports it.

## Authority and rights

Hierarchy does not imply technical permissions.

The machine record must distinguish:

- organizational position;
- decision authority;
- delegated responsibility;
- technical capability IDs;
- concrete tool/data access.

Employees must never infer additional authority merely from job title, seniority or direct reports.

An employee must not be able to grant itself new authority.

## Management roles

For `Head of ...` roles, the record should define:

- department-wide decision responsibility;
- what the Head delegates versus performs directly;
- how contradictory evidence is resolved;
- when work is returned for rework;
- when the Owner is escalated;
- how new staffing needs are recommended;
- reporting cadence;
- current operating phase.

A Head may start in `FOUNDING_SOLO`. This does not change the long-term role design; it only documents that the future department is not staffed yet.

## Development history

The `development` section should be able to record later changes such as:

- activation date;
- phase changes;
- newly assigned direct reports;
- capability promotions or revocations;
- changed responsibilities;
- observed recurring strengths or failure patterns;
- retirement/suspension decisions.

Historical changes should be auditable rather than silently overwritten when they materially affect authority.

## Canonical rule

Human-readable profile answers:

> Who is this employee for Jannek?

Machine record answers:

> What exists, what does this role own, what may it decide, what may it do, and what is its current real operating state?

When the two conflict, the machine record controls operational behavior.
