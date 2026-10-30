# n8n Orchestration Decision

Status: **ACCEPTED**  
Decision date: **2026-10-30**

## Scope

This decision applies to Security / Agent Workforce automation and integration design. It does not grant authority over monitored repositories and does not make n8n an implicit runtime dependency of any target repository.

## Decision

n8n is the **preferred default orchestration and integration layer** for new cross-system automations when the task fits its strengths.

Use the following operating split by default:

1. **Agents / LLMs interpret and decide** when judgment, classification, research, planning, or adaptive tool selection is required.
2. **Deterministic n8n workflows execute side effects** such as API calls, notifications, scheduled jobs, data movement, and repeatable multi-step procedures.
3. **Human approval remains the default gate for high-impact writes** until the affected repository or service explicitly authorizes a narrower unattended path.
4. **Generated or agent-edited workflows must be validated before production use.** AI-assisted workflow creation is an acceleration mechanism, not an authority bypass.

The intended direction is therefore:

> Agent decides -> controlled workflow executes -> human approves critical actions -> evidence/logs make the result inspectable.

## Why this is the default

The alternative is repeatedly building bespoke orchestration, connector, scheduling, retry, approval, and observability glue ourselves.

n8n should be preferred when it can materially reduce that custom infrastructure while keeping execution inspectable and bounded. The expected benefits are:

- faster delivery of integrations and recurring automations;
- less custom glue code and fewer one-off service paths;
- reusable workflows that agents can invoke as controlled tools;
- easier inspection, testing, repair, and operational handoff;
- centralized scheduling and integration behavior without moving repository authority into the automation platform;
- a practical bridge between adaptive agent reasoning and deterministic execution.

This is a **reuse-before-build decision**: custom orchestration is the exception, not the starting assumption.

## Authority and truth boundaries

n8n is an execution/orchestration layer, not a source of truth.

The existing authority hierarchy remains unchanged:

- GitHub/repository live state remains authoritative for current repository truth;
- target-repository local `AGENTS`, README, architecture, contracts, CI, issues, and PRs remain authoritative for that repository;
- workforce policy and capability routing remain subordinate to target-repository authority;
- n8n workflow configuration, cached data, agent memory, or execution history must not override repository truth or policy.

A target repository adopts n8n as a concrete runtime dependency only when that repository's own authority explicitly does so.

## State boundary

This decision does **not** change the Agent Workforce V1.1 state model.

In particular:

- Scout and Supervisor durable cursors remain exclusively in the GitHub checkpoint comments defined by `contracts/CHECKPOINT_CONTRACT.md`;
- n8n must not become a second durable Scout/Supervisor state ledger;
- scheduler/task execution metadata may remain transient execution-host state;
- workflow-local state is allowed only when it belongs to the workflow itself and does not duplicate canonical workforce/repository state.

## Security guardrails

For Security automation, prefer least privilege and explicit boundaries:

- give each workflow only the credentials and scopes it actually needs;
- do not embed secrets in workflow text, prompts, logs, or repository files;
- treat external/agent-generated input as untrusted;
- require explicit approval for destructive, privileged, financial, secret-bearing, governance, or broad write actions unless a narrower authority contract explicitly permits unattended execution;
- fail closed when required authority, credentials, target identity, or validation is ambiguous;
- keep audit evidence sufficient to reconstruct what triggered a material action and which workflow/tool performed it.

## Version posture

n8n 3.x is the forward target for this architecture, but production-critical adoption follows the **latest stable supported release**, not preview status alone.

Preview/beta capabilities may be used in controlled experiments. They must not become an unreviewed dependency of critical Security automation.

## When not to use n8n

Choose another implementation when bounded discovery shows that n8n creates more risk or complexity than it removes, for example when:

- ultra-low-latency or high-throughput execution is the primary requirement;
- a repository already has a simpler authoritative primitive that solves the task;
- the workflow would force sensitive state into the wrong trust boundary;
- required functionality cannot be made reliable, testable, or observable enough;
- introducing n8n would violate target-repository authority or deployment constraints.

A custom implementation should therefore have a concrete reason. `BUILD_CUSTOM` is valid, but it is no longer the default instinct for orchestration/integration work.

## Practical default

For a new Security automation, ask in this order:

1. Can an existing repo primitive solve it cleanly?
2. Can n8n orchestrate the process safely and observably?
3. Can an agent use the resulting workflow as a bounded tool instead of receiving broad direct write access?
4. Which actions require human approval?
5. Only if the above is insufficient: what custom component is actually necessary?

This decision is intentionally strong enough to prevent tool-hopping, but narrow enough that repository-local authority and evidence can override it when there is a better concrete solution.
