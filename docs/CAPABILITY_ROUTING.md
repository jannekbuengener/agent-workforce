# Capability Routing

## Purpose

This contract tells Agent Workforce agents when a specialized capability must, should, or may be used.

Capability routing selects tools and discovery obligations. It does **not** change repository ownership, truth hierarchy, mutation authority, or target-repository canon.

## Authority order

Apply capability routing only after current repository authority is established:

1. GitHub / repository live state;
2. target-repository local authority (`AGENTS.md`, README, canon, contracts, CI/rules as applicable);
3. this capability-routing contract;
4. the execution host's current capability availability and authorization.

A target repository may narrow, forbid, or replace a generic capability rule for work inside that repository. Generic workforce routing never overrides local repository authority.

## Relevance gate

Do not load or invoke every registered capability for every task.

After reading target-repository authority:

1. classify the task intent;
2. determine whether it matches a documented capability trigger or an explicit repo-local route;
3. only then consult the matching entry in [`capabilities/REGISTRY.yml`](../capabilities/REGISTRY.yml);
4. enforce that entry's requirement level and availability/authorization behavior.

If no capability trigger matches, continue under normal repository/workforce rules without loading unrelated capability details.

## Requirement levels

### `REQUIRED`

The named capability is mandatory for matching work.

- Verify that the capability is available to the execution host.
- Verify that use is authorized for the current task and target.
- If either check fails, stop with `BLOCKED_REQUIRED_CAPABILITY_UNAVAILABLE`.
- Do not silently substitute another tool or ad-hoc workflow.

### `DISCOVERY_REQUIRED`

The documented discovery step must be completed before choosing an implementation path.

This level requires evidence that the relevant discovery occurred; it does not itself authorize dependency installation, code mutation, or adoption of a discovered tool.

### `PREFERRED`

Use the named capability when available and suitable. A technically equivalent alternative is allowed when the agent records why the preferred capability is unsuitable or unavailable and the replacement does not violate repo-local authority.

### `ADVISORY`

The capability or source may help the task but is optional. It grants no authority and creates no blocked outcome by itself.

## Registry contract

[`capabilities/REGISTRY.yml`](../capabilities/REGISTRY.yml) is the machine-readable capability catalog.

Registry entries may contain:

- stable capability id;
- requirement level;
- relevance triggers and exclusions;
- canonical tool name and portable upstream identity;
- availability/authorization expectations;
- blocked outcome for mandatory capabilities.

The registry must not contain:

- workstation-specific absolute paths;
- credentials, tokens, private endpoints or secrets;
- transient installation state;
- duplicated target-repository truth;
- speculative tools added only to make the registry look complete.

Execution hosts may discover a local checkout, CLI, MCP, plugin, package or other authorized installation at runtime. That host-local location is operational state, not workforce canon.

## Reverse Engineering V1

`reverse_engineering` is the first registered capability and is `REQUIRED`.

Canonical tool:

- **Name:** REA
- **Portable identity:** `morluto/rea`
- **Upstream:** https://github.com/morluto/rea

Use the registry's `reverse_engineering` entry when the task intent is to inspect or reconstruct implementation/behavior through reverse engineering, including matching binary, native, Electron/JavaScript, .NET, runtime-behavior, proprietary-application, or website-behavior reconstruction work.

Ordinary web research, documentation lookup, or source-available code review does not become reverse engineering merely because the target is an application or website.

For matching reverse-engineering work:

```text
REA available AND authorized
    -> use REA under target-repository authority

REA unavailable OR unauthorized
    -> BLOCKED_REQUIRED_CAPABILITY_UNAVAILABLE
    -> no silent substitute
```

## Execution-host boundary

Capability availability belongs to the execution host. This repository records only portable routing policy.

Private MCP access is never assumed. A worker must not be told that a private operator capability is mandatory unless that capability is actually available to that worker under an authorized contract.

The one exception is an explicitly `REQUIRED` registered capability: if that capability is not available or authorized on the current execution host, the correct result is the registry's blocked outcome, not an invented replacement.

## Relationship to future capability work

This contract owns tool/capability routing semantics. Reuse-before-build discovery, shared external-reference catalogs, and repo-local external-doc manifests are separate contracts/issues and must not be folded into this V1 registry until their own scopes are approved.