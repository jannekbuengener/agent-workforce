# Capability Routing Design

**Issue:** #10

## Goal

Add a canonical, relevance-gated capability-routing layer to Agent Workforce so an agent can determine which specialized capability is required, preferred, advisory, or requires discovery without relying on chat memory, machine-local paths, or duplicated execution-host prompts.

## Authority

Capability routing selects tools and discovery obligations. It does not change repository ownership, truth hierarchy, or mutation authority.

Order of authority:

1. GitHub/repository live state;
2. target-repository local authority;
3. Agent Workforce capability-routing contract;
4. execution-host capability availability.

A target repository may narrow or forbid a generic capability rule. Generic workforce routing may not override local authority.

## Requirement levels

- `REQUIRED`: the named capability is mandatory. If unavailable or unauthorized, fail closed with `BLOCKED_REQUIRED_CAPABILITY_UNAVAILABLE`. No silent substitute.
- `DISCOVERY_REQUIRED`: the defined discovery step must happen before an implementation choice is made.
- `PREFERRED`: use the named capability when available; a technically equivalent substitute is allowed when justified.
- `ADVISORY`: useful tool/source only; no execution requirement and no authority elevation.

## Relevance gating

Agents must not load or invoke every registered capability for every task.

After target-repository authority has been read, classify the current task against the capability-routing contract. Consult a registry entry only when the task matches that capability's documented triggers or the target repository explicitly routes to it.

Unrelated tasks do not load or invoke REA merely because REA exists in the registry.

## Registry

`capabilities/REGISTRY.yml` is the machine-readable catalog. It contains portable capability identities, triggers, requirement levels, canonical tools, upstream sources, and unavailable outcomes.

It must not contain workstation-specific absolute paths, credentials, private endpoints, transient installation state, or duplicated repository truth.

## Reverse Engineering V1

Register `reverse_engineering` as the first capability.

- Requirement: `REQUIRED`
- Tool: `REA`
- Portable identity: `morluto/rea`
- Canonical upstream: `https://github.com/morluto/rea`
- Unavailable/unauthorized outcome: `BLOCKED_REQUIRED_CAPABILITY_UNAVAILABLE`

Triggers include reverse engineering of binaries, proprietary/application behavior reconstruction, native binaries, Electron/JavaScript applications, .NET assemblies, runtime behavior, and website behavior reconstruction when the intent is reverse engineering rather than ordinary web research.

If REA is unavailable or unauthorized, stop rather than silently substituting ad-hoc reverse-engineering tools.

## Bootstrap integration

`WORKFORCE_BOOTSTRAP.md` must expose the routing contract as workforce canon while preserving relevance-gated registry loading.

The bootstrap should require the small routing contract in its read order, then direct agents to consult the registry only after target-repository authority is established and a relevant capability trigger is identified.

Scheduler/worker prompts must not copy the registry.

## Front door and operating rules

`README.md` should expose the routing contract and registry.

`AGENTS.md` should state that capability routing happens after repo-local authority and should include `BLOCKED_REQUIRED_CAPABILITY_UNAVAILABLE` among fail-closed outcomes.

## Non-goals

- install or configure REA;
- create a runtime capability database or plugin manager;
- commit local paths such as `D:\\...`;
- populate the registry with speculative tools;
- make capabilities a new truth or ownership layer.

## Acceptance

The design is complete when the routing contract, registry, bootstrap/frontdoor integration, and fail-closed semantics satisfy Issue #10 and read-after-write validation shows no machine-local paths or conflicting capability authority.