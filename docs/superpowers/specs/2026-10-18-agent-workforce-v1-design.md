# Agent Workforce V1 — Design

Status: APPROVED_FOR_IMPLEMENTATION  
Date: 2026-10-18  
Scope: cross-repository engineering workforce for Jannek's software projects

## 1. Intent

Build a minimal, low-cost AI workforce that discovers where sustained engineering attention is actually needed before creating managers, departments, specialist agents, or heavy automation.

The system must optimize for evidence, low operating cost, repo-local truth, and reversible growth. It must not create organizational structure merely because such structure is possible.

Primary operating principle:

> Observe work -> collect evidence -> detect recurring need -> create role -> increase authority only after proven value.

## 2. Current repositories in scope

Initial portfolio:

- `jannekbuengener/sample-brain`
- `jannekbuengener/sample-brain-analysis`
- `jannekbuengener/arvp`
- `jannekbuengener/traum_taenzer`
- `jannekbuengener/Claire_de_Binare`

`gpt-mcp-server` is not part of the initial active portfolio. It can be re-added if meaningful work resumes.

## 3. V1 workforce

V1 has exactly two engineering employees.

### 3.1 Quality Scout

Mission: detect concrete deviations from healthy engineering practice and repo-local contracts.

Primary lenses:

- correctness and regression risk
- test quality and missing validation
- CI/check drift
- dependency/security/repository hygiene
- architecture and ownership drift
- documentation/canon drift
- repeated defects or recurring review findings
- stale or misleading technical surfaces

The Quality Scout does not optimize for finding many problems. It optimizes for accurate, evidence-backed findings.

### 3.2 Process Scout

Mission: detect recurring engineering work and process friction that may justify automation, a specialist agent, or a future manager.

Primary lenses:

- repeated manual work
- repeated agent tasks
- recurring handoffs
- duplicated effort
- decision bottlenecks
- work repeatedly blocked on missing ownership or context
- tasks that should be deterministic automation instead of agent work
- recurring task clusters that may justify a future specialist role

The Process Scout does not invent departments. It identifies repeated work patterns first.

## 4. Shared finding contract

Both scouts use the same evidence schema:

- `finding_id`
- `repo`
- `scout`
- `category`
- `summary`
- `evidence`
- `severity`
- `confidence`
- `first_seen`
- `last_seen`
- `recurrence`
- `suggested_action`
- `suggested_owner`
- `disposition`

Stable vocabularies:

- severity: `INFO | LOW | MEDIUM | HIGH | CRITICAL`
- confidence: `LOW | MEDIUM | HIGH`

A finding represents one underlying problem or work-pattern identity, not one observation event. New evidence for the same root cause updates recurrence/history instead of creating another finding identity.

Lifecycle states:

- `NEW`
- `RECURRING`
- `WORSENED`
- `IMPROVED`
- `RESOLVED`
- `NO_MATERIAL_CHANGE`

A run may finish with no finding. Silence is preferable to manufactured work.

## 5. Repo Health Book

Each monitored repository owns exactly one long-lived GitHub issue:

`[OPS][HEALTH] Repo Health Book — continuous quality & process evidence`

The Health Book belongs to that repository because it describes that repository's operational health and work patterns.

Rules:

- first scout visit writes an `INITIAL BASELINE`
- later visits append only material deltas
- `SKIP_NO_DELTA` creates no Health Book comment
- routine `NO_MATERIAL_CHANGE` creates no comment unless it closes, improves, or reclassifies an existing finding
- findings must cite live evidence whenever possible
- historical comments are evidence, not current truth
- before creating a new finding, the scout checks whether an unresolved finding already covers the same root cause
- if both scouts observe the same underlying condition, they reference the same finding instead of multiplying records
- unchanged recurring findings are not re-posted merely because another scheduled run occurred
- a Health Book is not a substitute for normal implementation issues
- when a finding becomes real work, the scout may recommend a separate issue
- V1 scouts do not create that separate issue automatically
- if a Health Book eventually becomes hard to navigate, create a reviewed rebaseline/successor issue and link the old book; do not build rollover machinery in V1

Initial baseline fields:

- repository state
- activity level
- observed quality mechanisms
- observed process mechanisms
- known strengths
- current deviations
- unknown / not yet measurable
- recommended observation focus

## 6. Baseline philosophy

Do not create large bespoke health-policy documents before the first run.

A scout evaluates against two layers:

1. durable engineering fundamentals such as correctness, testability, security hygiene, clear ownership, non-stale documentation, deterministic validation, maintainability, and avoidance of repeated manual failure;
2. repo-local authority such as `README`, `AGENTS`, architecture/canon/contracts, CI definitions, issues, PRs, and current live state.

Repo-local authority wins over generic assumptions whenever the repository intentionally defines a different valid rule.

The first run establishes an observed baseline. Future runs compare against that baseline and current live truth.

## 7. Scheduling and cost control

V1 uses scheduled ChatGPT runs as the execution host.

Each scout gets two scheduled run opportunities per week. One run may perform a shallow portfolio preflight across all in-scope repositories for selection, but it performs deep inspection of exactly one repository.

Every run begins with a cheap activity preflight. Deep inspection happens only when the selected repo is due for baseline coverage, shows meaningful activity, has unresolved recurring findings, or needs a periodic full sweep.

Activity classes:

- `ACTIVE`
- `WATCH`
- `DORMANT_POTENTIAL`
- `ARCHIVED`

Initial rollout:

1. Quality Scout visits all five repositories once.
2. Process Scout visits all five repositories once.
3. These ten runs create the first comparable evidence set.
4. After that, repo selection becomes adaptive.

Adaptive policy:

Selection priority is deterministic and intentionally simple:

1. repository not yet covered by the current scout's initial baseline round;
2. repository with an unresolved HIGH/CRITICAL finding that is due for recheck;
3. repository with meaningful new commit/PR/issue/CI activity since its last material scout observation;
4. periodic sweep candidate that has gone longest without inspection.

Within the same priority class, choose the least-recently-inspected eligible repository so one active repo cannot permanently starve the others.

Activity classes are derived advisory labels, not a second repository-status authority:

- `ACTIVE`: sustained current engineering activity or unresolved material findings
- `WATCH`: intermittent activity or a condition worth periodic recheck
- `DORMANT_POTENTIAL`: currently quiet but intentionally retained for future work
- `ARCHIVED`: explicitly retired from normal scout rotation

The scouts derive selection from GitHub/repo live evidence and Health Book history. V1 does not maintain a separate mutable scheduling database or committed `last_run` ledger.

Cost principle:

> Observation must be cheaper than the work it helps avoid.

No expensive deep audit is justified when the preflight shows no meaningful change and no unresolved risk requiring recheck.

## 8. Authority and safety

V1 scouts are advisory employees in a probationary authority state.

Allowed:

- read repository and GitHub state
- inspect code/docs/CI/issues/PRs
- reason about quality or process
- append evidence-backed Health Book observations
- recommend a follow-up issue
- escalate uncertainty or a blocked inspection

Not allowed in V1:

- modify product code
- repair findings automatically
- open implementation PRs
- change branch protection or governance
- modify secrets or credentials
- create specialist agents autonomously
- create follow-up implementation issues without a later authority increase
- push directly to protected branches

If required repo access is unavailable, the run terminates as `BLOCKED_NO_REPO_ACCESS`. It must not infer live state from stale memory.

## 9. Employee identity

Employee identity is secondary to function but intentionally persistent.

Each V1 agent role has a compact role contract containing:

- stable `agent_id` and name
- job title and mission
- responsibilities and non-responsibilities
- authority level
- evidence standard
- output contract
- escalation rules
- manager
- working mentality / personality traits
- communication style
- known role biases

Personality may influence perspective and communication. It must never override evidence, safety, authority, or repo-local truth.

Examples:

- Quality Scout: skeptical, precise, persistent, uncomfortable with unexplained drift; must not manufacture findings to satisfy that personality.
- Process Scout: curious, systems-oriented, impatient with repeated manual work; must not automate work merely because repetition exists.

Strengths and weaknesses become evidence-backed over time. They are not treated as true merely because they are written into the initial persona.

## 10. Workforce authority location

Cross-repository employee identity does not belong inside a product repository.

Target structure after design approval:

- one small private GitHub repository named `agent-workforce` owns role contracts and cross-repo workforce policy; repository creation is an implementation step after design approval
- each product/component repository owns its own Repo Health Book
- product repositories do not duplicate employee identity files
- Google Drive is not required for V1

### NotebookLM knowledge surface

NotebookLM is an optional derived knowledge surface for employee and organization documentation. It is intended to give Jannek a fast, structured place to query the workforce documentation and to give compatible agent hosts an additional retrieval surface.

Authority rules:

- Git/GitHub remains the canonical source for role contracts, workforce policy and versioned employee documentation.
- NotebookLM consumes canonical sources by direct link where practical, or by explicitly dated uploaded snapshots when a static copy is more useful.
- V1 requires no synchronization service, importer, or NotebookLM write-back automation.
- NotebookLM does not become a second source of truth. Changes or notes created there are proposals until they are written back through normal repo governance.
- Agents may use NotebookLM when their execution host has the MCP configured; agents without that MCP must remain fully functional from repo-local/canonical sources.
- NotebookLM availability is therefore never a V1 execution dependency or blocker.
- Repo Health Books remain in their owning repositories rather than being relocated into NotebookLM.

Candidate NotebookLM source set after the workforce repo exists:

- workforce overview / handbook
- Quality Scout role contract
- Process Scout role contract
- employee profiles and later evidence-backed development notes
- management / authority map
- cross-repo portfolio orientation

This design file is a neutral planning artifact until that workforce authority exists.

## 11. Management model

Initial hierarchy:

```text
Jannek — Owner
    <->
ChatGPT — Technical / Operations Lead
    |
    +-- Quality Scout
    +-- Process Scout
```

The lead may challenge priorities, identify deferred obligations, and recommend against owner ideas when evidence indicates low value or unnecessary complexity. Final goal/permission decisions remain with Jannek.

A dedicated Repo Manager is created only when evidence shows sustained workload that justifies one.

Possible later structure:

```text
Technical / Operations Lead
    |
    +-- Sample Brain Manager
    |      +-- QA specialist
    |      +-- Architecture specialist
    |      +-- Release specialist
    |
    +-- ARVP Manager
           +-- future specialists only when justified by ARVP evidence
```

No manager or specialist is created preemptively.

## 12. Promotion criteria for new roles

A future role must be justified by observed work, not organizational aesthetics.

A new role becomes a serious candidate when one or more are repeatedly evidenced:

- recurring finding class across multiple runs
- recurring manual/agent task with meaningful time or failure cost
- sustained repo workload requiring repeated coordination
- recurring specialist judgment not well served by current scouts
- repeated handoff or ownership bottleneck
- recurring problem where deterministic automation alone is insufficient

Before creating an agent, always ask whether a deterministic check, script, workflow, or contract would solve the problem more cheaply and reliably.

## 13. Future execution hosts

ChatGPT is the initial host because repository access and scheduling are already available and V1 should avoid new infrastructure cost.

Hermes is a future candidate execution host for multiple specialized agents. It is not part of V1 architecture. Before adoption, its current multi-agent, LLM, tool, persistence, scheduling, security, and repository capabilities must be verified live.

Other agent platforms are evaluated only when they solve an evidenced limitation of the current host.

## 14. Explicit non-goals for V1

- no departments
- no per-repo manager agents yet
- no large KPI framework
- no arbitrary health score
- no autonomous code repair
- no autonomous issue/PR factory
- no dedicated database
- no Google Drive dependency
- no CDB control-plane copy
- no heavy plugin/MCP build
- no Hermes migration
- no requirement to use OpsTruth or any external evidence provider
- no event-driven orchestration until scheduled runs establish useful evidence

## 15. Success criteria for V1

V1 is successful when:

1. both scout roles have stable role contracts;
2. all five repositories have an initialized Repo Health Book;
3. both scouts complete at least one baseline run per repo;
4. findings are evidence-backed and distinguish new, recurring, improved, resolved, and unchanged states;
5. quiet repos produce little or no noise;
6. active repos naturally receive more attention after the baseline round;
7. follow-up work is recommended only when concrete evidence justifies it;
8. after several weeks, the accumulated evidence can answer which repos need more attention and whether a repo manager or specialist role is actually justified.

## 16. Design principles frozen by this document

- evidence before organization
- repo-local truth before generic assumptions
- one deep inspection = one repo; portfolio preflight may stay shallow
- cheap preflight before deep inspection
- personality is subordinate to role/evidence
- Health Book stays with its repo
- employee identity is cross-repo authority
- advisory before autonomous mutation
- deterministic automation before agent labor where sufficient
- increase attention and authority only when evidence warrants it
- build the organization from observed work rather than designing departments first

## 17. Runtime outcomes and validation

Each scout run must terminate in one explicit outcome:

- `FINDING_RECORDED`
- `NO_MATERIAL_CHANGE`
- `SKIP_NO_DELTA`
- `BLOCKED_NO_REPO_ACCESS`
- `BLOCKED_TOOL_UNAVAILABLE`
- `BLOCKED_AUTHORITY_AMBIGUOUS`

The scout must distinguish an infrastructure/tool failure from an engineering finding. A failed connector or unavailable repo must never be reported as a repo-quality defect.

Validation strategy for rollout:

1. create role contracts before scheduling live runs;
2. initialize one Health Book per in-scope repo;
3. execute the ten baseline runs as the first controlled evidence round;
4. Technical / Operations Lead reviews early output quality for false positives, duplicated findings, weak evidence, and unnecessary noise;
5. adjust role contracts only when observed failures justify it;
6. do not expand write authority until the V1 evidence quality is acceptable;
7. after several weeks, review recurrence data before proposing Repo Managers, specialist roles, event-driven triggers, plugins, or another execution host.

No V1 success claim is based solely on a scheduled task having executed. Success requires useful, correctly scoped evidence in the relevant Repo Health Book.

## 18. Authority and state separation

V1 separates durable canon, repo-live evidence, runtime execution metadata, and convenience retrieval so agent memory cannot silently become a second authority.

| Class | Examples | Authority rule |
|---|---|---|
| Versioned workforce canon | role contracts, workforce policy, portfolio membership | Git/GitHub in `agent-workforce` |
| Repo-live evidence | code, issues, PRs, CI, Repo Health Book | owning repository / GitHub live |
| Runtime execution metadata | scheduler/task history, transient tool state, connector errors | operational only; never product/workforce canon |
| Derived knowledge surface | NotebookLM | read/retrieval convenience only |

Mutable run history must not be copied into versioned role-contract files as if it were canonical policy. V1 deliberately derives scheduling decisions from live repository evidence plus Health Book history instead of maintaining a second mutable workforce database.

If a future execution host requires durable mutable state that cannot be reconstructed safely from GitHub/task history, that state must get an explicit runtime-state design before use. It must not be silently stored inside deploy-synced code or role files.

## 19. Anti-noise and convergence rules

The scouts are successful when their signal becomes clearer over time, not when their output volume grows.

- no duplicate finding for an already-covered root cause
- no new comment for an unchanged condition solely because another run occurred
- recurrence increases only when new evidence materially confirms repetition
- resolution requires current evidence, not absence of a new complaint
- infrastructure/tool/budget failure is classified separately from repository quality
- a proposed follow-up issue must state which existing finding it would resolve
- repeated false positives are themselves evidence that the scout role contract needs correction
- V1 never triggers a write/retry loop in response to its own comments or another bot's generic activity
