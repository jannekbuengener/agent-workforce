# XERJ Reference Coding in Reuse Before Build — Design

## Goal

Make XERJ reference coding a mandatory, bounded step inside the existing `reuse_before_build` discovery route so new features and other meaningful implementation-path decisions check worked reference implementations before the implementation path is finalized.

## Chosen approach

Extend `reuse_before_build`; do not create a second global capability or router.

## Trigger boundary

`reuse_before_build` remains relevance-gated, but explicitly includes planning or implementing a new feature. Existing exclusions remain for documentation-only work, trivial fixes with an already-clear solution, straightforward reuse of an existing repository primitive, small refactors without an implementation-path decision, and analysis that selects no implementation path.

## Required XERJ gate

Whenever `reuse_before_build` matches:

1. establish target-repository authority;
2. inspect existing repository implementation/primitives and accepted dependencies first;
3. run one bounded XERJ reference-code search before the implementation path is finalized;
4. evaluate any relevant reference against repository architecture, licence, security and operational constraints;
5. continue the normal reuse-before-build decision order.

The XERJ step may use an authorized local indexed peer corpus or the public Hub. A relevant result is evidence, never automatic adoption authority.

## Evidence

Record a compact XERJ result:

- query/problem intent;
- corpus/prefix used;
- pin/revision and licence when available;
- `file:line` when a concrete reference is found;
- result `REFERENCE_FOUND` or `NO_RELEVANT_REFERENCE`;
- what, if anything, the reference changes in the implementation decision.

## Failure behavior

If `reuse_before_build` matches and no authorized XERJ route can perform the required reference-code check, fail closed with `BLOCKED_TOOL_UNAVAILABLE`. Do not silently substitute memory or generic web research for the required XERJ step.

## Portability

Workforce canon records the portable requirement and XERJ identity, not workstation-specific executable paths or prefixes. Execution-host configuration remains local to the host. Cursor/Claude XERJ rules and skills may be committed when portable; machine-specific MCP executable configuration is not workforce canon.

## Non-goals

- no new `reference_coding` Capability ID;
- no automatic dependency or OSS adoption;
- no automatic copying of external code;
- no broad research for excluded trivial work;
- no weakening of target-repository authority or licence checks.
