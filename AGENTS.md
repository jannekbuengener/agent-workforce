# Agent Operating Rules

## Scope

These rules govern agents acting from this workforce repository. They do not override the local authority of a monitored repository.

## Truth and routing

- Determine current state from GitHub/repo live evidence, never from memory.
- Scheduled/external execution hosts must bootstrap from live `main` [`WORKFORCE_BOOTSTRAP.md`](WORKFORCE_BOOTSTRAP.md) and follow its current required-read order instead of carrying a duplicated downstream file list.
- If the bootstrap or a required authority path cannot be resolved, fail closed with an explicit blocked outcome; never reconstruct missing authority from an older prompt or memory.
- For a monitored repository, read and obey that repository's local `AGENTS`/README/canon/contracts before applying generic engineering assumptions.
- After target-repository authority is established, use [`docs/CAPABILITY_ROUTING.md`](docs/CAPABILITY_ROUTING.md) to determine whether the current task triggers a specialized capability; consult [`capabilities/REGISTRY.yml`](capabilities/REGISTRY.yml) only for relevant matching capability entries and read any contract referenced by the matching entry.
- When cross-repository ownership, spawn-point, or meta/metatool routing is materially relevant, consult [`docs/REPOSITORY_ROUTING.md`](docs/REPOSITORY_ROUTING.md) and [`routing/REPOSITORY_ROUTING.yml`](routing/REPOSITORY_ROUTING.yml) for stable routing facts. Do not treat that topology as monitored membership or product canon.
- When cross-repository capability/skill discovery is materially relevant, follow [`docs/REPOSITORY_CAPABILITY_DISCOVERY.md`](docs/REPOSITORY_CAPABILITY_DISCOVERY.md): locate authority via [`routing/REPOSITORY_CAPABILITY_SOURCES.yml`](routing/REPOSITORY_CAPABILITY_SOURCES.yml), treat [`generated/PORTFOLIO_CAPABILITY_INDEX.yml`](generated/PORTFOLIO_CAPABILITY_INDEX.yml) as derived discovery data only, and load the declared repo-local source selectively. Do not treat the generated index as authority.
- When plugin/skill/orchestrator consumer routing is materially relevant, follow [`contracts/PLUGIN_SKILL_ROUTING_CONTRACT.md`](contracts/PLUGIN_SKILL_ROUTING_CONTRACT.md): consumers reference Capability IDs resolved by Agent Workforce; specialists must not become a second global router; private MCP is never a worker dependency. Validation stays structural — do not invent semantic routing scores.
- For planning or implementing a new feature, or other relevant work that would introduce a meaningful new code/dependency/tool/service/infrastructure path, the `reuse_before_build` route is `DISCOVERY_REQUIRED`; follow [`docs/REUSE_BEFORE_BUILD.md`](docs/REUSE_BEFORE_BUILD.md) before finalizing the implementation path. A matched route must complete the bounded XERJ reference-code check and record `REFERENCE_FOUND` or `NO_RELEVANT_REFERENCE`; if no authorized XERJ route is available, return `BLOCKED_TOOL_UNAVAILABLE` rather than silently substituting another search path.
- When recommending, designing, or creating a new durable structuring authority (Goal, Epic, Meta-Epic, Coordinator, or equivalent owner structure), `AUTHORITY_RECONCILIATION_REQUIRED` applies; follow [`docs/WORKFORCE_POLICY.md`](docs/WORKFORCE_POLICY.md#authority-reconciliation) before create-new. Ordinary implementation children and small bugfix slices do not trigger that gate.
- Reuse-before-build is bounded and relevance-gated. Do not run broad ecosystem research for trivial fixes, documentation-only work, straightforward use of existing repo primitives, or tasks that do not make a meaningful implementation-path decision.
- When external documentation or engineering precedent is materially relevant, follow [`contracts/EXTERNAL_REFERENCE_CONTRACT.md`](contracts/EXTERNAL_REFERENCE_CONTRACT.md): use the target repo's own external-reference manifest when present, then consult [`references/CATALOG.yml`](references/CATALOG.yml) only for applicable shared discovery/reference anchors.
- Never infer target-repository usage, dependency adoption, or implementation scope merely because a source exists in the shared reference catalog.
- Repo-local `P0`/`P1` references require concrete current repo signals; `P2` is parked/reference-only. Load only entries relevant to the current task.
- Official/upstream external sources outrank community/example material, but all external references remain below target-repository live truth/canon for claims about the repository itself.
- Capability/reference routing selects tools, discovery obligations, or evidence sources only. It never overrides target-repository truth, ownership, dependency policy, or mutation authority.
- Use this repository for workforce role, authority, finding, scheduling, and template contracts.
- Use [`docs/META_TOPOLOGY.md`](docs/META_TOPOLOGY.md) to classify shared meta repositories and metatools when cross-repository context is relevant.
- Meta-layer membership never grants authority to override target-repository local truth or ownership.
- Do not infer an implicit runtime dependency merely because a repository is listed in the meta topology.
- Private MCP access is never a worker requirement. Workers receive only the tools/evidence available to their execution host.

## V1 authority

V1 scouts may read/analyze, append evidence-backed observations to the canonical Repo Health Book, recommend follow-up work, and escalate uncertainty.

V1 scouts must not modify product code, create implementation PRs, change governance/branch protection, modify secrets, create specialist agents, or create follow-up implementation issues automatically.

When issue creation is otherwise authorized by the acting role/operator and target-repository authority, follow the canonical [`GitHub issue creation`](docs/WORKFORCE_POLICY.md#github-issue-creation) section of the Workforce Policy. Durable Goal / Epic / Meta-Epic / Coordinator-class issues also require [`Authority reconciliation`](docs/WORKFORCE_POLICY.md#authority-reconciliation) first. These references do not grant issue-write authority.

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

## XERJ (reference coding)

XERJ supplies the mandatory reference-code step inside matched `reuse_before_build` work. Use an authorized execution-host route: an indexed peer corpus with `xerj search` / `xerj def`, or the public Hub with `xerj hub find` / `xerj ask`.

Do not hard-code workstation paths, local data directories, or prefix names into workforce canon. Those belong to execution-host configuration.

For a matched route, record `REFERENCE_FOUND` or `NO_RELEVANT_REFERENCE`; when a concrete reference is found, cite `file:line` and capture pin/revision and licence when available. The reference is evidence only and never bypasses repository authority or licence checks.

After using XERJ, send the field report through the available XERJ feedback route unless the execution host has explicitly disabled feedback.
