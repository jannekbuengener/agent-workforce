# Mitarbeiterakte — <Display Name>

## Menschliches Profil

**<Display Name>**  
**Geplante/aktive Position:** <Job Title>  
**Abteilung:** <Department>

<Kurzes Portrait / Mini-Biografie. Dieser Abschnitt dient nur der menschlichen Wiedererkennung.>

### Stärken

- <strength>

### Schwächen / typische Blind Spots

- <weakness or blind spot>

### Fachliches Profil

<Short human-readable competence summary.>

> **Statushinweis:** <State clearly whether this employee actually exists or is only planned.>

---

## MACHINE RECORD

```yaml
schema_version: 1

employee:
  id: workforce.employee.<slug>.v1
  display_name: <Display Name>
  job_title: <Job Title>
  department: <department_id>
  reports_to: <employee_or_owner_id>
  employment_state: PLANNED_ONLY
  runtime_exists: false
  active: false

lifecycle:
  current_state: PLANNED_ONLY
  activation_initial_operating_phase: <phase>

mission:
  purpose: <purpose>
  success_definition: <success definition>

responsibilities: []
competencies: []

organization:
  direct_reports: []
  can_delegate: false
  can_return_for_rework: false
  can_recommend_new_roles: false
  can_create_roles: false

authority:
  decision_rights: []
  approval_rights: []
  forbidden:
    - self_grant_new_authority

knowledge_scope:
  owns: []
  does_not_own: []

capabilities:
  required: []
  optional: []
  status: NOT_ASSIGNED_YET

tools:
  status: NOT_PROVISIONED

memory:
  namespace: NOT_ASSIGNED_YET
  status: NOT_PROVISIONED

communication: {}
reporting: {}
escalation: {}
audit: {}

development:
  current_stage: PROFILE_DEFINED_NOT_HIRED
  activation_date: null
  phase_history: []
  authority_history: []
  staffing_history: []
```

See [`docs/EMPLOYEE_RECORD_STANDARD.md`](../docs/EMPLOYEE_RECORD_STANDARD.md) for canonical semantics.
