# Agent Operating Rules

## Scope

These rules govern agents acting from this workforce repository. They do not override the local authority of a monitored repository.

## Truth and routing

- Determine current state from GitHub/repo live evidence, never from memory.
- For a monitored repository, read and obey that repository's local `AGENTS`/README/canon/contracts before applying generic engineering assumptions.
- Use this repository for workforce role, authority, finding, scheduling, and template contracts.
- Private MCP access is never a worker requirement. Workers receive only the tools/evidence available to their execution host.

## V1 authority

V1 scouts may read/analyze, append evidence-backed observations to the canonical Repo Health Book, recommend follow-up work, and escalate uncertainty.

V1 scouts must not modify product code, create implementation PRs, change governance/branch protection, modify secrets, create specialist agents, or create follow-up implementation issues automatically.

## Fail closed

Terminate with an explicit blocked outcome instead of guessing:

- `BLOCKED_NO_REPO_ACCESS`
- `BLOCKED_TOOL_UNAVAILABLE`
- `BLOCKED_AUTHORITY_AMBIGUOUS`

Infrastructure, connector, scheduler, or budget failures are operational failures, not repository-quality findings.

## Noise control

- Same root cause uses the same stable finding id across scouts.
- `SKIP_NO_DELTA` produces no Health Book comment.
- Unchanged conditions are not reposted solely because another scheduled run occurred.
- Do not treat scout comments or generic bot activity as meaningful engineering activity triggers.
- Do not create write/retry loops in response to agent-generated comments.
