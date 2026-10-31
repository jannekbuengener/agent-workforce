# Head of Knowledge — execution surface

## Canonical skill

```text
docs/skills/head-of-knowledge/SKILL.md
docs/skills/head-of-knowledge/consumer.yml
```

Employee: [`agents/dieter-datenbank.md`](../agents/dieter-datenbank.md)  
Activation: [`docs/DIETER_ACTIVATION_GATE.md`](DIETER_ACTIVATION_GATE.md)  
Authority: [`docs/KNOWLEDGE_DEPARTMENT_AUTHORITY.md`](KNOWLEDGE_DEPARTMENT_AUTHORITY.md)  
Owner report: [`docs/HEAD_OF_KNOWLEDGE_OWNER_REPORT.md`](HEAD_OF_KNOWLEDGE_OWNER_REPORT.md)

## Local Cursor install (user-level)

Copy or sync the skill directory to:

```text
~/.cursor/skills/head-of-knowledge/SKILL.md
```

(and colocated `consumer.yml` when distributing the full pack).

Workforce `docs/skills/head-of-knowledge/` remains authority. User-level install
is a host binding for Cursor invocation (`/head-of-knowledge`).

## Runtime meaning

Presence of the validated skill+consumer pack is the Workforce-owned execution
surface that justifies `runtime_exists: true` after the activation gate passes.
It is not a second mutable runtime database.
