# Reuse Before Build

## Purpose

Before planning or implementing a new feature, or introducing another meaningful implementation, dependency, tool, service, subsystem, or infrastructure path, determine whether the target repository already has a suitable solution and inspect relevant worked reference implementations before custom code is selected.

This is a relevance-gated engineering discovery contract. When it matches, one bounded XERJ reference-code check is mandatory. It is not a mandate to research the ecosystem for every edit, and it does not grant authority to install dependencies, copy external code, or mutate a target repository.

## Authority order

Use this contract only after the target repository's current authority is established.

1. GitHub / repository live state;
2. target-repository local authority and architecture/dependency rules;
3. this reuse-before-build contract;
4. external libraries, tools, projects, documentation and community evidence.

Repo-local dependency, licensing, security, offline, architecture or governance rules always win over generic reuse preferences.

## Relevance gate

Apply this contract when a planning or implementation task would make a meaningful build-vs-reuse decision, including:

- planning a new feature;
- implementing a new feature;
- a new implementation path or subsystem;
- a new dependency/package;
- a new external tool or service;
- new infrastructure or runtime machinery;
- substantial custom functionality where an established solution may already exist.

Do not trigger broad external discovery for:

- trivial fixes where the required change is already clear;
- documentation-only changes;
- straightforward use of an existing repository primitive;
- small refactors that do not create a meaningful dependency/tool/build decision;
- unrelated analysis where no implementation path is being selected.

When this contract matches, local repository code and accepted dependencies are checked first, then the bounded XERJ reference-code step still runs before the implementation path is finalized. After that step, discovery may stop early when an existing repository primitive or accepted dependency clearly satisfies the requirement.

## Required discovery order

When the relevance gate matches, evaluate in this order:

1. **Existing repository implementation** — search for reusable modules, helpers, contracts, patterns, adapters, services, tests, scripts or other primitives already owned by the target repository.
2. **Existing repository dependencies** — determine whether a package/tool already used and accepted by the repository solves the problem without introducing a new dependency surface.
3. **XERJ reference coding** — search an authorized indexed peer corpus or the XERJ Hub for worked implementations of the same problem before selecting the implementation path.
4. **Established libraries/packages** — identify maintained language/runtime-appropriate libraries with a strong technical fit.
5. **Maintained open-source projects/tools** — consider broader OSS solutions when a library-level primitive is insufficient.
6. **Agent Workforce capabilities/tools** — check registered capabilities for an existing specialized route before inventing parallel tooling.
7. **Official/upstream evidence** — verify relevant specifications, official documentation, release notes, upstream issues and compatibility constraints for serious candidates.
8. **Custom implementation** — choose new local code only when the prior options are insufficient, incompatible, unsafe, unmaintained, operationally unsuitable, or otherwise worse for the target repository.

The order is intentional: prefer what the repository already owns or already depends on, then inspect worked reference implementations through XERJ, before expanding the dependency/operational surface or inventing custom code.

## Required XERJ reference-coding gate

When this contract matches, XERJ is a required discovery step, not an optional inspiration source.

Use an execution-host-authorized XERJ route:

- an already indexed local/peer corpus via XERJ search/definition lookup; or
- the public XERJ Hub via corpus discovery and question/definition lookup.

Keep the search bounded to the actual engineering problem. Query using the domain terms, symbols, protocols or behavior being implemented. A single relevant worked implementation is often enough; `NO_RELEVANT_REFERENCE` is a valid result and does not block normal engineering once the search itself completed.

Record one compact reference-coding receipt:

```text
XERJ_REFERENCE_CHECK
Result: REFERENCE_FOUND | NO_RELEVANT_REFERENCE
Query: <problem intent>
Corpus/Prefix: <source>
Pin/Revision: <when available>
License: <when available>
Reference: <file:line when found>
Decision impact: <reuse/adapt/no change and why>
```

A XERJ result is evidence only. Before copying or adapting code, verify target-repository architecture, license compatibility, security and operational constraints. `REFERENCE_FOUND` never grants dependency, vendoring, architecture or mutation authority by itself.

If the route matches but no authorized XERJ CLI/MCP route can perform the required check, stop with `BLOCKED_TOOL_UNAVAILABLE`. Do not silently replace the required XERJ step with memory, generic web search or an unrelated search tool.

## Evaluation criteria

Evaluate only the criteria material to the current decision, but do not choose by popularity alone.

At minimum consider, when relevant:

- technical fit and completeness;
- consistency with target-repository architecture/contracts;
- maintenance health and project longevity;
- offline/local-first or deployment constraints;
- license compatibility and reuse obligations;
- security and supply-chain exposure;
- language/runtime/platform compatibility;
- performance, latency and resource behavior;
- integration complexity and failure modes;
- operational burden, upgrade path and testability.

A popular library that violates an offline requirement, license boundary, security policy, latency target or architecture contract is not automatically preferable to custom code.

## Source hierarchy

External evidence should normally be weighted in this order:

1. official specifications / official documentation;
2. upstream project documentation;
3. upstream issues, release notes and maintainer evidence;
4. established technical knowledge;
5. community sources such as Stack Overflow;
6. examples, blog posts and awesome-list discovery sources.

Community knowledge can expose real-world edge cases and debugging experience, but it does not override newer official/upstream evidence or target-repository live truth.

For shared source classification, repo-local relevance manifests and reusable discovery anchors, follow [`../contracts/EXTERNAL_REFERENCE_CONTRACT.md`](../contracts/EXTERNAL_REFERENCE_CONTRACT.md). That contract does not change the reuse-before-build decision order above.

## Bounded discovery

Discovery must be sufficient to support the engineering decision, not exhaustive. For a matched route, complete the required XERJ reference-code check before using an early-stop condition.

After that check, stop when one of these is true:

- an existing repo primitive clearly satisfies the requirement;
- an existing accepted dependency clearly satisfies the requirement;
- enough viable external candidates have been evaluated to make the trade-off defensible;
- external options are clearly ruled out by a target-repository constraint;
- additional searching is unlikely to change the decision.

Do not produce ecosystem surveys merely to prove that research occurred.

## Decision outcomes

End relevant discovery with one compact outcome:

### `REUSE_EXISTING`

Use an existing target-repository primitive or already-accepted dependency.

Record what is reused and why it satisfies the requirement.

### `ADOPT_DEPENDENCY_OR_TOOL`

An external library/tool is the strongest technical option.

Record the candidate, the material fit/risk evidence, and any repo-local approval or mutation gate that still applies. Discovery does not itself authorize adoption.

### `BUILD_CUSTOM`

Implement locally because the evaluated reuse/adoption options are insufficient or conflict with important repository constraints.

Record the alternatives considered and the decisive reason custom code is the better engineering choice.

## Minimum decision evidence

The final decision should be compact and include only what materially supports it:

- selected outcome;
- existing repo/dependency option checked first;
- the `XERJ_REFERENCE_CHECK` receipt;
- external candidate(s) considered when relevant;
- decisive technical constraints/trade-offs;
- why the selected route wins.

Do not turn this into a permanent research ledger unless the target repository explicitly requires one.

## Mutation boundary

This contract is decision support only.

It does not by itself authorize:

- installing a package;
- adding or vendoring OSS code;
- changing architecture or governance;
- enabling a cloud/runtime service;
- modifying secrets or deployment configuration;
- bypassing target-repository review/approval rules.

Any selected implementation still follows the target repository's normal authority, review, validation and security rules.

## Relationship to capability routing

`reuse_before_build` is registered in `capabilities/REGISTRY.yml` as `DISCOVERY_REQUIRED`.

The registry entry routes matching work to this contract and names XERJ as the mandatory reference-coding provider inside the discovery procedure. This does not create a second global Capability ID. Specialized `REQUIRED` capabilities remain independent; for example, reverse-engineering work still follows the REA hard gate when that trigger applies.

The shared external-reference catalog may provide bounded discovery anchors when external evidence is relevant. Repo-local external-reference manifests remain owned by each target repository; issue #13 owns the portfolio rollout and normalization of those manifests.
