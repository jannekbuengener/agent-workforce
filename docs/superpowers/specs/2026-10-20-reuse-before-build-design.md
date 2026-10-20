# Reuse Before Build — Design

## Goal

Make reuse-before-build a canonical, relevance-gated Agent Workforce engineering rule for planning and implementation work that would otherwise introduce new code, dependencies, tooling, or infrastructure.

## Authority

This design implements GitHub issue #11. Target-repository live state and repo-local authority remain above this workforce contract.

## Trigger boundary

Apply reuse-before-build only when a task is making a meaningful implementation-path decision, especially when it would introduce a new capability, dependency, subsystem, service, tool, or infrastructure path.

Do not force ecosystem research for trivial fixes, documentation-only work, straightforward use of an existing repo primitive, or other work where no meaningful build-vs-reuse decision exists.

## Discovery order

When relevant, inspect in this order:

1. reusable implementation/primitives already present in the target repository;
2. dependencies already used by the target repository;
3. established libraries/packages appropriate to the language/runtime;
4. suitable maintained open-source projects/tools;
5. already-registered Agent Workforce capabilities/tools;
6. official documentation, upstream issues/release notes and compatibility constraints;
7. only then choose a new custom implementation when available alternatives are insufficient.

## Decision criteria

Do not select an option by popularity alone. Evaluate the alternatives that matter for the current task against:

- technical fit;
- target-repository architecture and contracts;
- maintenance health;
- offline/local-first or deployment constraints;
- license suitability;
- security and supply-chain risk;
- runtime/platform compatibility;
- performance/latency/resource constraints;
- integration and operational complexity.

## Decision outcomes

The discovery should end in one compact outcome:

- `REUSE_EXISTING` — use an existing repo primitive or already-used dependency;
- `ADOPT_DEPENDENCY_OR_TOOL` — use a suitable external library/tool, subject to repo-local dependency/mutation policy;
- `BUILD_CUSTOM` — implement locally because the evaluated alternatives are unsuitable.

A discovery result is evidence for the implementation-path decision. It never by itself authorizes adding a dependency, changing architecture, or mutating the target repository.

## Source authority

Current repository/live evidence and repo-local canon remain primary. For external evaluation, prefer official specifications/docs and upstream project evidence. Upstream issues/release notes may refine compatibility and defects. Community sources such as Stack Overflow can contribute practical experience but do not override newer official/upstream/current repository evidence.

## Boundedness

Discovery must be sufficient to support the decision, not exhaustive. Stop when the existing repo/dependency path clearly satisfies the requirement, or when enough external evidence exists to make the implementation-path trade-off defensible.

## Relationship to capability routing

Register `reuse_before_build` in `capabilities/REGISTRY.yml` as `DISCOVERY_REQUIRED`. The registry entry routes relevant tasks to this contract. It has no mandatory named execution tool and must not alter the `REQUIRED` REA rule for reverse engineering.

## Out of scope

- automatic dependency installation;
- automatic OSS adoption;
- a package marketplace or dependency database;
- shared external-reference catalogs/manifests from issues #12/#13;
- replacing target-repository architecture/dependency rules;
- making community or awesome-list material canonical truth.
