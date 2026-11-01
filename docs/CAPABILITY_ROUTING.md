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
4. enforce that entry's requirement level and availability/authorization or discovery behavior.

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

A `DISCOVERY_REQUIRED` entry may route to a contract rather than a named execution tool. Discovery remains bounded and relevance-gated; it is not a requirement to perform broad research for unrelated or trivial work.

### `PREFERRED`

Use the named capability when available and suitable. A technically equivalent alternative is allowed when the agent records why the preferred capability is unsuitable or unavailable and the replacement does not violate repo-local authority.

`PREFERRED` is never `REQUIRED`. Unavailability or a justified local equivalent must **not** produce `BLOCKED_REQUIRED_CAPABILITY_UNAVAILABLE`.

#### PREFERRED decision observability

Only when normal relevance/trigger routing produces a **material match** for a `PREFERRED` capability must the acting orchestrator leave compact, inspectable decision evidence. Unmatched `PREFERRED` capabilities stay silent — no receipt rows, no `Match: no` noise, and no per-task sweep of every registered preferred capability.

```text
normal relevance / trigger routing
→ no match = silence
→ material match = compact decision evidence
```

Canonical decision record (Capability ID first; provider optional evidence only):

```text
PREFERRED_CAPABILITY_DECISION
Capability: <capability_id>
Decision: USED_PREFERRED | LOCAL_EQUIVALENT | NOT_USED_WITH_REASON
Reason: <required for LOCAL_EQUIVALENT and NOT_USED_WITH_REASON>
```

| Decision | Meaning |
|---|---|
| `USED_PREFERRED` | The matched preferred capability (or its currently resolved provider) was actually used. |
| `LOCAL_EQUIVALENT` | A target-repo / local equivalent route sufficiently covers the needed purpose. Short reason required. Target-repository authority remains stronger than generic workforce routing. |
| `NOT_USED_WITH_REASON` | The trigger matched, but the capability was consciously not used (unsuitable, unavailable, unauthorized, or no material benefit after inspection). Reason required. `NOT_USED != BLOCK`. |

Decision identity is the **Capability ID**. An optional resolved provider may appear as evidence; Capability ≠ Provider remains binding.

Surface matched decisions in the consumer's **existing** run/delivery receipt under `CAPABILITY ROUTING DECISIONS`. Omit that section entirely when no preferred capability matched. Do not invent a separate telemetry database, router, or second global contract for this evidence.

Machine twin for deterministic invariants: [`tools/preferred_capability_decision_lib.py`](../tools/preferred_capability_decision_lib.py).

### `ADVISORY`

The capability or source may help the task but is optional. It grants no authority and creates no blocked outcome by itself.

## Registry contract

[`capabilities/REGISTRY.yml`](../capabilities/REGISTRY.yml) is the machine-readable capability catalog.

Registry entries may contain:

- stable capability id;
- requirement level;
- relevance triggers and exclusions;
- a canonical contract path and/or tool identity;
- ordered discovery behavior and compact outcomes where applicable;
- availability/authorization expectations;
- blocked outcome for mandatory capabilities.

The registry must not contain:

- workstation-specific absolute paths;
- credentials, tokens, private endpoints or secrets;
- transient installation state;
- duplicated target-repository truth;
- speculative tools added only to make the registry look complete.

Execution hosts may discover a local checkout, CLI, MCP, plugin, package or other authorized installation at runtime. That host-local location is operational state, not workforce canon.

## Standard shared capability routes

The following shared repositories are first-class routing targets in the workforce registry. They are standard **discovery/routing options**, not unconditional dependencies that must be invoked on every task.

### Agent Brain — shared context/evidence

`shared_context_evidence` is registered as `PREFERRED`.

Canonical capability:

- **Name:** Agent Brain
- **Portable identity:** `jannekbuengener/agent-brain`
- **Upstream:** https://github.com/jannekbuengener/agent-brain

Route to Agent Brain when the task materially benefits from shared or cross-repository knowledge, context, provenance-aware evidence, durable decision context, memory/retrieval infrastructure, or structured ingestion for agent work.

Do not route ordinary repository live-state inspection, simple source-code reading, or GitHub issue/PR truth through Agent Brain when the authoritative target repository or GitHub already supplies the needed evidence.

Agent Brain remains context/evidence infrastructure. It does not become product authority or an implicit runtime dependency merely because it is registered.

### ARVP — deterministic validation/evaluation

`deterministic_validation` is registered as `PREFERRED`.

Canonical capability:

- **Name:** ARVP
- **Portable identity:** `jannekbuengener/arvp`
- **Upstream:** https://github.com/jannekbuengener/arvp

Route to ARVP when acceptance materially depends on deterministic evaluation, reproducible evidence bundles, baseline comparisons, PASS/FAIL/HOLD gates, stability/resampling validation, or portable validation contracts beyond ordinary repository tests.

Do not invoke ARVP merely to decorate routine unit tests, lint, formatting, or tasks where the target repository already owns a sufficient equivalent validation contract.

ARVP evidence supports acceptance; it does not override target-repository canon, CI, or release authority.

## Reverse Engineering V1

`reverse_engineering` is registered as `REQUIRED`.

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

## Reuse Before Build V1

`reuse_before_build` is registered as `DISCOVERY_REQUIRED` and routes to [`docs/REUSE_BEFORE_BUILD.md`](REUSE_BEFORE_BUILD.md).

Use it when planning or implementing a new feature, or when another planning/implementation task would make a meaningful build-vs-reuse decision such as adding a new subsystem, dependency, external tool/service, infrastructure path, or substantial custom capability.

Do not trigger broad ecosystem research for trivial bug fixes, documentation-only work, straightforward use of existing repository primitives, small refactors without an implementation-path decision, or analysis that selects no implementation path.

The discovery order checks existing repo code and accepted dependencies first, then requires one bounded XERJ reference-code search across an authorized indexed peer corpus or the XERJ Hub before external libraries, OSS projects, workforce capabilities, or custom implementation are selected. The XERJ step records `REFERENCE_FOUND` or `NO_RELEVANT_REFERENCE`; a no-match result permits normal discovery to continue.

If the route matches but the execution host has no authorized XERJ CLI/MCP route for the required check, return `BLOCKED_TOOL_UNAVAILABLE` rather than silently substituting memory or another search mechanism. The final reuse decision remains `REUSE_EXISTING`, `ADOPT_DEPENDENCY_OR_TOOL`, or `BUILD_CUSTOM` with material decision evidence.

Reference discovery does not itself authorize code copying, dependency installation, OSS adoption, architecture changes, or any other target-repository mutation.

## Improvement Blackboard capabilities

Four Capability IDs separate Improvement Blackboard authority. Do **not** collapse
them into shared_context_evidence.

| Capability ID | Level | Provider / contract | Who may use write tiers |
|---|---|---|---|
| improvement_read | PREFERRED | Agent Brain (jannekbuengener/agent-brain) | read-only for authorized roles |
| improvement_observation_write | REQUIRED | Agent Brain | Improvement Board Manager scope (not scouts/Supervisor) |
| improvement_management_write | REQUIRED | Agent Brain | Improvement Board Manager only |
| improvement_github_issue_create | REQUIRED | [docs/IMPROVEMENT_GITHUB_ISSUE_CREATE.md](IMPROVEMENT_GITHUB_ISSUE_CREATE.md) (#51) | Board Manager only, separate gate |

`	ext
READ < OBSERVATION_WRITE < MANAGEMENT_WRITE < GITHUB_ISSUE_CREATE
`

Quality Scout, Process Scout, and Workforce Supervisor remain denied for
Observation Write, Management Write, and GitHub Issue Create on the blackboard.
shared_context_evidence may still supply ordinary shared context but never
substitutes for the REQUIRED improvement write capabilities
(silent_substitution: false).

GitHub issue handoff is intentionally a Workforce-owned contract capability, not
an Agent Brain Memory write. Matching work must obey
[`IMPROVEMENT_GITHUB_ISSUE_CREATE.md`](IMPROVEMENT_GITHUB_ISSUE_CREATE.md):
fail closed on missing gates; reuse active work items; idempotent retries;
never treat a closed GitHub issue as automatic `VERIFIED`.

Role canon: [../agents/improvement-board-manager.md](../agents/improvement-board-manager.md).

## Knowledge Department capabilities (Head of Knowledge)

Head of Knowledge FOUNDING_SOLO authority is defined by
[`docs/KNOWLEDGE_DEPARTMENT_AUTHORITY.md`](KNOWLEDGE_DEPARTMENT_AUTHORITY.md)
(#70). Hierarchy does not inherit Board Manager write capabilities.

| Capability ID | Level | Contract / provider | Who |
|---|---|---|---|
| shared_context_evidence | PREFERRED | Agent Brain | Head of Knowledge (read/shared context when available) |
| improvement_read | PREFERRED | Agent Brain | Head of Knowledge (prioritization visibility only) |
| knowledge_department_decision | REQUIRED when deciding | [KNOWLEDGE_DEPARTMENT_AUTHORITY.md](KNOWLEDGE_DEPARTMENT_AUTHORITY.md) | Head of Knowledge when ACTIVE |
| knowledge_owner_report | REQUIRED when reporting | [HEAD_OF_KNOWLEDGE_OWNER_REPORT.md](HEAD_OF_KNOWLEDGE_OWNER_REPORT.md) (#73) | Head of Knowledge when ACTIVE |

Explicitly **not** granted to the Head by title alone:

- `improvement_management_write`
- `improvement_github_issue_create`
- generic Memory/Knowledge write
- raw database admin
- target-repository product mutation
- self-grant of authority

Operational use requires `employment_state: ACTIVE` and `runtime_exists: true`.
Defining the matrix does not activate the employee.

Role canon: [../agents/dieter-datenbank.md](../agents/dieter-datenbank.md).

## External references during discovery

External-reference semantics are defined by [`contracts/EXTERNAL_REFERENCE_CONTRACT.md`](../contracts/EXTERNAL_REFERENCE_CONTRACT.md).

When external documentation, technical precedent, or external reuse evidence is materially relevant after target-repository authority has been established:

- use the target repository's own canonical external-reference manifest when present;
- consult [`references/CATALOG.yml`](../references/CATALOG.yml) only for matching shared discovery/reference anchors;
- load only sources relevant to the current task;
- treat shared catalog membership as source discovery, never as evidence that the target repository uses or should adopt a technology;
- prefer official/upstream evidence over community/example sources for consequential claims.

The external-reference contract supplies evidence sources; it does not alter capability requirement levels or the reuse-before-build discovery order.

## Execution-host boundary

Capability availability belongs to the execution host. This repository records only portable routing policy.

Private MCP access is never assumed. A worker must not be told that a private operator capability is mandatory unless that capability is actually available to that worker under an authorized contract.

The one exception is an explicitly `REQUIRED` registered capability: if that capability is not available or authorized on the current execution host, the correct result is the registry's blocked outcome, not an invented replacement.

For `DISCOVERY_REQUIRED`, an execution host must use the evidence sources actually available and authorized to it. If the minimum evidence required to make the implementation-path decision cannot be obtained, use the existing operational blocked outcomes rather than guessing.

## Relationship to repository routing and capability discovery

Global workforce capability routing (this contract + [`capabilities/REGISTRY.yml`](../capabilities/REGISTRY.yml)) is separate from portfolio routing topology and per-repository capability/skill source discovery.

- Use this contract to decide whether a **global** workforce capability such as REA, ARVP, Agent Brain, or reuse-before-build applies.
- Use [`docs/REPOSITORY_ROUTING.md`](REPOSITORY_ROUTING.md) for stable ownership, relationships and frontdoors when spawn-point routing matters.
- Use [`docs/REPOSITORY_CAPABILITY_DISCOVERY.md`](REPOSITORY_CAPABILITY_DISCOVERY.md) to locate **repository-local** capability/skill authority and the derived portfolio capability index.
- The generated index keeps `global_capabilities` and `repository_capabilities` in separate sections so the two layers are not flattened into one truth.
- Use [`contracts/PLUGIN_SKILL_ROUTING_CONTRACT.md`](../contracts/PLUGIN_SKILL_ROUTING_CONTRACT.md) when plugins/skills/orchestrators must declare how they consume Capability IDs without becoming a second registry or global router.

Authority domains: Agent Workforce owns cross-repository selection and capability resolution; target-repository authority owns behavior once selected; execution hosts implement but override neither.

Monitored Scout portfolio membership remains owned by [`portfolio/REPOSITORIES.md`](../portfolio/REPOSITORIES.md), not by repository routing or capability sources.

## Relationship to repo-local reference rollout

This contract owns capability/tool and discovery routing semantics. The external-reference contract and shared catalog are available now as conditional evidence-routing surfaces. Repository-specific manifest ownership remains local to each target repository, and issue #13 owns the portfolio-wide rollout/normalization of those manifests.
