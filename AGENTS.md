# Agent Operating Rules

## Scope

These rules govern agents acting from this workforce repository. They do not override the local authority of a monitored repository.

## Truth and routing

- Determine current state from GitHub/repo live evidence, never from memory.
- Scheduled/external execution hosts must bootstrap from live `main` [`WORKFORCE_BOOTSTRAP.md`](WORKFORCE_BOOTSTRAP.md) and follow its current required-read order instead of carrying a duplicated downstream file list.
- If the bootstrap or a required authority path cannot be resolved, fail closed with an explicit blocked outcome; never reconstruct missing authority from an older prompt or memory.
- For a monitored repository, read and obey that repository's local `AGENTS`/README/canon/contracts before applying generic engineering assumptions.
- After target-repository authority is established, use [`docs/CAPABILITY_ROUTING.md`](docs/CAPABILITY_ROUTING.md) to determine whether the current task triggers a specialized capability; consult [`capabilities/REGISTRY.yml`](capabilities/REGISTRY.yml) only for relevant matching capability entries and read any contract referenced by the matching entry.
- For relevant planning/implementation work that would introduce a meaningful new code/dependency/tool/service/infrastructure path, the `reuse_before_build` route is `DISCOVERY_REQUIRED`; follow [`docs/REUSE_BEFORE_BUILD.md`](docs/REUSE_BEFORE_BUILD.md) before selecting a custom implementation.
- Reuse-before-build is bounded and relevance-gated. Do not run broad ecosystem research for trivial fixes, documentation-only work, straightforward use of existing repo primitives, or tasks that do not make a meaningful implementation-path decision.
- Capability routing selects tools/discovery obligations only. It never overrides target-repository truth, ownership, dependency policy, or mutation authority.
- Use this repository for workforce role, authority, finding, scheduling, and template contracts.
- Use [`docs/META_TOPOLOGY.md`](docs/META_TOPOLOGY.md) to classify shared meta repositories and metatools when cross-repository context is relevant.
- Meta-layer membership never grants authority to override target-repository local truth or ownership.
- Do not infer an implicit runtime dependency merely because a repository is listed in the meta topology.
- Private MCP access is never a worker requirement. Workers receive only the tools/evidence available to their execution host.

## V1 authority

V1 scouts may read/analyze, append evidence-backed observations to the canonical Repo Health Book, recommend follow-up work, and escalate uncertainty.

V1 scouts must not modify product code, create implementation PRs, change governance/branch protection, modify secrets, create specialist agents, or create follow-up implementation issues automatically.

## Fail closed

Terminate with an explicit blocked outcome instead of guessing:

- `BLOCKED_NO_REPO_ACCESS`
- `BLOCKED_TOOL_UNAVAILABLE`
- `BLOCKED_AUTHORITY_AMBIGUOUS`
- `BLOCKED_REQUIRED_CAPABILITY_UNAVAILABLE`

`BLOCKED_REQUIRED_CAPABILITY_UNAVAILABLE` applies when a relevant registry entry is `REQUIRED` and the named capability is unavailable or unauthorized. Do not silently substitute another tool.

For `DISCOVERY_REQUIRED`, if the minimum evidence needed to make the engineering decision cannot be obtained with the execution host's authorized sources/tools, use the applicable existing operational blocked outcome instead of guessing.

Infrastructure, connector, scheduler, or budget failures are operational failures, not repository-quality findings.

## Noise control

- Same root cause uses the same stable finding id across scouts.
- `SKIP_NO_DELTA` produces no Health Book comment.
- Unchanged conditions are not reposted solely because another scheduled run occurred.
- Do not treat scout comments or generic bot activity as meaningful engineering activity triggers.
- Do not create write/retry loops in response to agent-generated comments.
