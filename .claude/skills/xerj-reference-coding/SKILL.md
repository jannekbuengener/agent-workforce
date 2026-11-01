---
name: xerj-reference-coding
description: Use whenever Agent Workforce reuse_before_build matches, including planning or implementing a new feature, before the implementation path is finalized.
---

# XERJ reference coding

Follow `docs/REUSE_BEFORE_BUILD.md` and `capabilities/REGISTRY.yml` as authority.

When `reuse_before_build` matches:

1. inspect existing repository implementation and accepted dependencies first;
2. run one bounded XERJ reference-code search through an authorized indexed peer corpus or the XERJ Hub;
3. record `REFERENCE_FOUND` or `NO_RELEVANT_REFERENCE`;
4. for a found reference, capture `file:line`, pin/revision and licence when available, plus the decision impact;
5. treat the result as evidence only — never as automatic permission to copy code, add a dependency or override repository authority;
6. if no authorized XERJ CLI/MCP route can perform the check, stop with `BLOCKED_TOOL_UNAVAILABLE`.

Do not hard-code workstation paths, data directories or local prefix names into durable workforce canon. Those are execution-host configuration.
