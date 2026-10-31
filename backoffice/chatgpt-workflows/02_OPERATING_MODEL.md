# WorkForce — Operating Model (Bootstrap)

> **Live-truth override:** Live Agent Workforce canon, GitHub evidence, and target-repository authority override this snapshot whenever they conflict.

## How Jannek and ChatGPT work here

Focus on decisions and slices, not on becoming a second copy of Agent Workforce or a second copy of the long ChatGPT charter.

```text
UNDERSTAND
→ VERIFY LIVE
→ ROUTE
→ AUTHORITY RECONCILIATION
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

### AUTHORITY RECONCILIATION

When considering a new durable structuring authority (Goal, Epic, Meta-Epic, Coordinator, or equivalent owner structure), complete live `AUTHORITY_RECONCILIATION_REQUIRED` from:

```text
docs/WORKFORCE_POLICY.md#authority-reconciliation
```

Inside that single gate (no parallel authority):

- preserve original structural intent;
- discover existing owners;
- evaluate relevant local same-class precedents as samples (`NONE_FOUND` is allowed after bounded discovery);
- reconcile material candidates individually against existing authority;
- then decide update / reconcile / link / no structural change / create-new.

Do not copy that procedure into this backoffice. Prefer update / reconcile / link / no structural change over create-new unless a missing-authority proof is documented. An existing owner is evidence, not an automatic stop for structural candidate analysis. Ordinary implementation children and small bugfix slices do not trigger this gate.

### DECIDE

Use a compact executive decision layer. Activate only lenses that matter for the task:

- **CEO / strategy** — real problem, beneficiary, value, core vs distraction, differentiation vs commodity, leverage vs maintenance, validation speed.
- **CTO / technology** — feasibility, architecture consequences, build/operate cost, debt, security, lock-in, reliability, reversibility, worker/agent fitness, time-to-value. Elegance without strategic or economic value is not enough.
- **Product** — jobs-to-be-done, workflow fit, alternatives, adoption/retention, must-have vs nice-to-have vs differentiator vs commodity.
- **Business / investment** — value, customer, alternatives, cost, return, risk, time, reversibility, opportunity cost, evidence quality.

Prefer:

```text
hypothesis → smallest experiment → measurable success criterion → real evidence → scale decision
```

before large irreversible programs. Prefer reuse / buy / partner when the function is commodity; build when differentiation, control, or strategic know-how requires it. Prefer the simplest reliable automation; AI is not an end in itself.

Mark evidence clearly as verified fact, plausible conclusion, hypothesis, or speculation. No false precision.

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

**Agent Sovereignty:** Give the worker the outcome and boundaries, not unnecessary micromanagement. New findings inside the same goal/scope do not automatically require a new mandate.

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
