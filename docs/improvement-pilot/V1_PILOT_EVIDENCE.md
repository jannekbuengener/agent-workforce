# Skill Improvement Blackboard V1 Pilot — Evidence

**Exit target:** `SKILL_IMPROVEMENT_BLACKBOARD_V1_PILOT_PROVEN`  
**Issues:** workforce [#52](https://github.com/jannekbuengener/agent-workforce/issues/52) / [#54](https://github.com/jannekbuengener/agent-workforce/issues/54), brain [#45](https://github.com/jannekbuengener/agent-brain/issues/45)

## reuse_before_build

`REUSE_EXISTING + BUILD_THIN` — Layer-A twins + Brain Improvement primitives; no workforce DB.

## Checklist

| Criterion | Evidence locator | Status |
|---|---|---|
| 3 Skills | Brain `tests/improvement/test_v1_pilot_loop.py` (`PILOT_SKILLS`) | TBD_LIVE: brain PR |
| 10 Improvement Records | same pilot test | TBD_LIVE: brain PR |
| ≥20 Observation Events | same pilot test | TBD_LIVE: brain PR |
| 2 concurrent writers / 0 lost | same + barrier test | TBD_LIVE: brain PR |
| Idempotent retries | same pilot test | TBD_LIVE: brain PR |
| True duplicate recognized | dual seed same root → recurrence=2 | TBD_LIVE: brain PR |
| Similar-but-different no false merge | `assess_observation` ≠ EXACT_IDENTITY + separate record | TBD_LIVE: brain PR |
| Authority separation Observation/Management/GitHub | Board/GitHub Layer-A + ManagementActor deny | Layer-A: `tools/skill_improvement_blackboard_pilot_lib.py` |
| Exactly one routed GitHub Implementation Issue | [agent-brain#60](https://github.com/jannekbuengener/agent-brain/issues/60) | LIVE |
| PR / Merge evidence | TBD_LIVE: PR closing #60 | TBD_LIVE |
| Verification → VERIFIED | pilot lifecycle path + post-merge verification | TBD_LIVE |
| Rebuildable Markdown/Obsidian projection | pilot projection + CLI `project` | TBD_LIVE: brain PR |
| No second mutable workforce truth | Layer-A `mutable_workforce_db: false` | PASS (unit) |
| Memory/Knowledge read-only intact | pilot scans improvement package | TBD_LIVE: brain PR |
| closed ≠ verified | github create pressure + management path | PASS (Layer-A) |

## Layer-A command

```bash
python -m unittest tools.tests.test_skill_improvement_blackboard_pilot -v
```

## Classifier (fill after live PR/merge)

- [ ] `PILOT_PROVEN_EXPAND_BOUNDED`
- [ ] `PILOT_PROVEN_KEEP_MANUAL_GITHUB_GATE`
- [ ] `PILOT_REWORK_REQUIRED`
- [ ] `PILOT_REJECT_ARCHITECTURE`

Exit string on Meta-Epic only after all rows PASS with locators.
