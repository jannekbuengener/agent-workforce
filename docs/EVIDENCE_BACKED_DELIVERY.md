# evidence-backed-delivery — Distribution & Host Usage

## Canonical source

Workforce-owned skill body:

```text
docs/skills/evidence-backed-delivery/SKILL.md
```

Contract:

```text
contracts/EVIDENCE_BACKED_DELIVERY_CONTRACT.md
contracts/evidence_backed_delivery.v1.schema.json
```

Do **not** copy the skill body into product repositories. Product repos may
reference the contract and name the skill. Local skills may be stricter.

Machine-readable consumer declaration (skill-colocated):

```text
docs/skills/evidence-backed-delivery/consumer.yml
```

## Local Cursor install (user-level)

```text
~/.cursor/skills/evidence-backed-delivery/SKILL.md
```

Copy or symlink the whole skill folder from canon so `references/` remains
available. Invoke with `/evidence-backed-delivery` or as a Custom Mode.

## Consumer / pilot paths (no body copy)

| Repo shape | How to consume |
|---|---|
| Sample Brain (visual + runtime) | Keep `sample-brain-issue-to-session-plan` local; reference this contract for Required Evidence / modality / PR handoff fields |
| Claire_de_Binare (strong PR family) | Keep CDB acceptance/router/session-close skills; treat this contract as global floor, not a replacement |
| Non-visual / governance / API | Reference contract + use matching modality (tests, logs, schema validation) |

Live adoption runs that mutate product repos are follow-up work. Layer-A
pressure cases plus dogfooding PRs in Agent Workforce prove the contract shape.

## Validation without new dependencies

- Pressure cases: `docs/skills/evidence-backed-delivery/references/pressure_cases.yml`
- Twin: `tools/evidence_backed_delivery_lib.py`
- Tests: `python -m unittest tools.tests.test_evidence_backed_delivery`
- JSON Schema file is a **shape contract**; structural checks are in the lib.
  Do not add a `jsonschema` package solely to validate it.

## Independent review

Use Bugbot, Codex Review, or an equivalent independent reviewer available on
the execution host. Merge gate: **0 unresolved MUST_FIX findings on Final Head**.

## Related

- Skill: [`skills/evidence-backed-delivery/SKILL.md`](skills/evidence-backed-delivery/SKILL.md)
- Contract: [`../contracts/EVIDENCE_BACKED_DELIVERY_CONTRACT.md`](../contracts/EVIDENCE_BACKED_DELIVERY_CONTRACT.md)
- Meta-Epic executor: [`skills/cursor-meta-epic-executor/SKILL.md`](skills/cursor-meta-epic-executor/SKILL.md)
- Issue #43 exit: `GLOBAL_EVIDENCE_BACKED_DELIVERY_CONTRACT_PROVEN`
