# Workflows — Operating Model (Bootstrap)

> **Live-truth override:** Live Agent Workforce canon, GitHub evidence, and target-repository authority override this snapshot whenever they conflict.

## How Jannek and ChatGPT work here

Focus on decisions and slices, not on becoming a second copy of Agent Workforce.

```text
UNDERSTAND
→ VERIFY LIVE
→ ROUTE
→ DECIDE
→ SLICE
→ HANDOFF / EXECUTE
→ VERIFY
→ CLOSE
```

### UNDERSTAND

Determine the real goal, problem, owner, scope, and desired outcome. Do not generate technical activity first.

### VERIFY LIVE

When a decision depends on current state, verify live:

- Workforce canon;
- GitHub;
- the target repository.

Memory and these static backoffice files are not volatile truth sources.

### ROUTE

Through Agent Workforce, determine:

- target repository;
- relevant capability;
- requirement level;
- specialist / provider;
- target-repository authority front door.

Load only what the current task needs. Do not bulk-load the whole portfolio, capability index, topology, skill set, or plugin set.

### DECIDE

Check strategically: value, cost, risk, reversibility, opportunity cost, and the smallest validatable step.

### SLICE

A slice should have one clear goal, bounded scope, acceptance criteria, independent validation, and as little unnecessary architecture as possible.

### HANDOFF / EXECUTE

Worker handoffs define:

- goal;
- scope;
- hard boundaries;
- relevant authority;
- evidence;
- acceptance;
- exit state.

Do not prescribe every shell line.

**Agent Sovereignty:** Give the worker the outcome and boundaries, not unnecessary micromanagement.

### VERIFY / CLOSE

“PR created” is not automatically completion. When the relevant repository contract requires it:

```text
implement
→ test
→ review
→ commit
→ push
→ PR
→ gates
→ merge
→ issue close
```

Live authority decides the concrete completion contract.

## Private MCP boundary

```text
PRIVATE MCP = CHATGPT ONLY
```

Private ChatGPT MCP connections must not be passed to workers as a requirement, capability, expected infrastructure, or private endpoint / connector metadata.

ChatGPT may use private MCP internally to gather information. Workers receive only:

- sanitized facts;
- evidence;
- public / allowed source references;
- tools actually available on the worker host.

No secrets. No connector metadata.

## Plugin / skill routing

Do not maintain a plugin inventory in this backoffice.

Live contract:

```text
jannekbuengener/agent-workforce@main/contracts/PLUGIN_SKILL_ROUTING_CONTRACT.md
```

Backoffice rule:

> Consumers reference Capability IDs. Agent Workforce resolves providers.

Not:

```text
Plugin A calls Plugin B calls Plugin C
```

Specialists stay narrow. Repo-local skills are discovered through Workforce discovery pointers, then read from the owning repository.

## Process test cases (discover live — do not copy topology)

### Sample Brain ownership

If the user says something like “we need to change Sample Brain analysis,” bootstrap through Agent Workforce and discover live ownership via repository routing / capability discovery. Do not hard-code Sample Brain topology into this bundle. Expect live routing to distinguish package/analysis ownership from product-consumer ownership, then enter the selected target repository’s authority.

### Reverse Engineering capability

If reverse engineering is needed, do not hard-code today’s provider in this backoffice. Route:

```text
intent
→ Agent Workforce
→ capability id
→ requirement level
→ provider resolution
```

Fail closed on a missing `REQUIRED` capability. Do not invent a substitute.
