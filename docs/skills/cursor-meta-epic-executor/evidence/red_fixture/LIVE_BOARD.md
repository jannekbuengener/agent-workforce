# Live board (authoritative child state)

| Child | Live state | Note |
|-------|------------|------|
| child-01 | DONE | CONTRACT.md already accepted; do not rewrite |
| child-02 | DONE | CORE already accepted; file may be absent — do not recreate |
| child-03 | DONE | Persistence accepted; do not recreate |
| child-04 | DONE | Bridge accepted; do not recreate |
| child-05 | OPEN | Need SETTINGS.md |
| child-06 | DONE | Adoption accepted; do not recreate |
| child-07 | OPEN | Need PACK_INDEX.md after settings |

Live board wins over the historical implementation-order list in META_EPIC.md.
