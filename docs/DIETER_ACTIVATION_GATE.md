# Dieter Activation Gate (`PLANNED_ONLY` → `ACTIVE`)

## Purpose

Fail-closed gate for provisioning Dieter Datenbank. Documentation alone must
never flip lifecycle. Issue: #71. Parent: #68.

## Required evidence before `ACTIVE` / `runtime_exists: true`

1. **Identity** — `workforce.employee.dieter-datenbank.v1` unique in employee record.
2. **Authority resolved** — #70 Capability IDs present in registry + employee record
   (`knowledge_department_decision`, `knowledge_owner_report`, preferred reads,
   explicit deny-list).
3. **Owner report contract** — #73 contract marked `CONTRACT_COMPLETE`.
4. **Org wiring** — Board Manager `reports_to` Head of Knowledge (#72).
5. **Execution surface** — `docs/skills/head-of-knowledge/SKILL.md` +
   `consumer.yml` exist and structurally validate under
   `PLUGIN_SKILL_ROUTING_CONTRACT`.
6. **Denied/ambiguous gates green** — Knowledge Department authority pressure
   cases pass.
7. **No target-repo authority override** encoded in surface owns/does_not_own.
8. **Audit trail** — development history records activation evidence (PR/SHA).

## Machine twin

[`tools/dieter_activation_lib.py`](../tools/dieter_activation_lib.py)

Outcomes:

```text
GATE_PASS → may set ACTIVE + runtime_exists true + FOUNDING_SOLO
GATE_HOLD → keep PLANNED_ONLY / runtime_exists false
```

## After activation

- `employment_state: ACTIVE`
- `runtime_exists: true`
- `active: true`
- operating phase `FOUNDING_SOLO`
- tools status bound to head-of-knowledge skill surface
- memory namespace bound without generic write authority

## Exit token

`DIETER_FOUNDING_SOLO_PROVISIONED`
