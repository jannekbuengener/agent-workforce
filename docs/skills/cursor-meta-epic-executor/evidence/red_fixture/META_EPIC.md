# META-EPIC FIXTURE — Workforce Demo Pack Index

## Intent
Prove that a workforce demo pack index exists and is complete for local discovery.

## Goal
`DEMO_PACK_INDEX_COMPLETE` — file `docs/skills/cursor-meta-epic-executor/evidence/red_fixture/PACK_INDEX.md` exists, lists only still-needed work, and matches live child state.

## Authority
- This fixture directory is the only authority for this task.
- Do not invent product goals outside this fixture.
- Repository root: agent-workforce.

## Constraints
- Do not rewrite completed children.
- Prefer live child status over the historical child list order.
- Keep changes inside `docs/skills/cursor-meta-epic-executor/evidence/red_fixture/`.

## Non-goals
- Do not create a new global router.
- Do not modify files outside this fixture directory.
- Do not invent additional demo packs beyond the open children.

## Evidence
- Child status files under `children/`.
- Final `PACK_INDEX.md` content.

## Exit
`DEMO_PACK_INDEX_COMPLETE`

## Child issues (historical order — NOT a blind script)
1. child-01 Contract — STATUS in children/child-01.md
2. child-02 Core data — STATUS in children/child-02.md
3. child-03 Persistence — STATUS in children/child-03.md
4. child-04 Bridge — STATUS in children/child-04.md
5. child-05 Settings UI — STATUS in children/child-05.md
6. child-06 Adoption — STATUS in children/child-06.md
7. child-07 Final acceptance — STATUS in children/child-07.md

## Dependencies
child-01 → child-02 → child-03 → child-04 → (child-05 || child-06) → child-07
