# Head of Knowledge — Weekly Owner Report

## Purpose

Canonical weekly Owner-facing report produced by Dieter Datenbank (Head of
Knowledge) under Capability ID `knowledge_owner_report`.

Machine twin: [`tools/knowledge_owner_report_lib.py`](../tools/knowledge_owner_report_lib.py).

Employee record: [`agents/dieter-datenbank.md`](../agents/dieter-datenbank.md).

Parent: #68. Delivery issue: #73.

## Status

```text
CONTRACT_COMPLETE
capability_id: knowledge_owner_report
exit: HEAD_OF_KNOWLEDGE_OWNER_REPORT_DEFINED
```

## Cadence and channel

| Field | Value |
|---|---|
| Cadence | weekly |
| Primary channel | email (Owner) |
| Actor | `workforce.employee.dieter-datenbank.v1` |
| Delivery surface | abstract — content/contract first; no provider hardcoding |

Immediate escalations are **not** part of this weekly artifact. Use the
employee `escalation` path when uncertainty blocks work now.

## Required sections (machine + human)

Stable section ids (YAML / receipt) and human headings:

| id | Human heading |
|---|---|
| `what_happened` | Was ist passiert? |
| `what_is_critical` | Was ist kritisch? |
| `what_was_decided` | Was wurde entschieden? |
| `current_data_quality_situation` | Aktuelle Datenqualität |
| `relevant_uncertainties` | Relevante Unsicherheiten |
| `concrete_action_recommendations` | Konkrete Handlungsempfehlungen |

Optional but allowed inside recommendations:

- staffing need for a durable recurring specialist function (recommend only;
  may not create/authorize employees).

## Machine-readable schema

```yaml
schema_version: 1
report_kind: head_of_knowledge_weekly_owner_report
capability_id: knowledge_owner_report
actor_employee_id: workforce.employee.dieter-datenbank.v1
period:
  start: YYYY-MM-DD
  end: YYYY-MM-DD
channel: email
sections:
  what_happened: string
  what_is_critical: string
  what_was_decided: string
  current_data_quality_situation:
    summary: string
    quantifiable: false
    # percentage only when method_id is set and reproducible
    percentage: null
    method_id: null
    band: null   # optional: gut | okay | schlecht — only with percentage+method
  relevant_uncertainties: [string]
  concrete_action_recommendations:
    - type: trend | recurring_pattern | staffing | other
      text: string
evidence_refs: [string]
immediate_escalation_included: false
```

## Data-quality rule (fail-closed)

No percentage without a documented, reproducible method id that the twin can
verify as present.

Until such a method exists in Workforce canon:

```text
Datenqualität: nicht belastbar quantifizierbar
```

Illustrative Owner-facing examples (not canonical thresholds, not KPIs):

- `92 % – gut`
- `76 % – okay`
- `58 % – schlecht`

These examples may appear in documentation only. Emitting them as factual
scores without `method_id` is denied (`INVENTED_QUALITY_KPI`).

## Forbidden

- inventing unreproducible quality percentages;
- including immediate escalation content as a substitute for the escalation path;
- generic Memory/Knowledge writes under this capability;
- target-repository product mutation;
- claiming the report proves Dieter is ACTIVE (lifecycle is separate).

## Operational gate

Producing a productive report requires:

- Capability `knowledge_owner_report` authorized;
- employee `ACTIVE` with `runtime_exists: true` (activation owned by #71);
- all required sections present and non-empty;
- data-quality block obeying the fail-closed rule;
- `immediate_escalation_included: false`.

Defining this contract does **not** activate Dieter.

## Exit token

`HEAD_OF_KNOWLEDGE_OWNER_REPORT_DEFINED`
