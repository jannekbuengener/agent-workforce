# Host visual evidence checklist

Host-agnostic companion to `cursor-meta-epic-executor` Independent quality
gate. Not product canon. Do **not** add target-repo harness APIs, UI object
names, toolkit findChild types, or product-specific visual baselines here.

## Before treating a capture as acceptance evidence

- [ ] Relevant UI/layout/geometry has settled (not first unstable frame).
- [ ] Viewport is user-reachable under product-enforced size/geometry floors.
- [ ] Capture labels match actual geometry (no “narrow-N” when clamped to min).
- [ ] Deterministic gates (tests/CI) are separate from visual judgment.
- [ ] Ambiguous or weak visual deltas are recorded as notes, not auto PASS/FAIL.
- [ ] If Exit names Owner Visual / human visual acceptance: pack is ready for
      owner review; agent has **not** self-set that PASS.
- [ ] Material ambiguity → `HOLD_OWNER_DECISION_REQUIRED`.

## Explicit non-contents

This checklist must remain free of target-product Appearance, toolkit Popup
discovery rules, SoftRenderer harness code, and fixed pixel floors from any
one repository.
