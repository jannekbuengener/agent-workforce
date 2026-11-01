# History Backfill Contract V1

## Purpose

This contract defines the binding limits and invariants of the one-off, local **AWH History Backfill**: a neutral, complete collection of historical GitHub work for the in-scope portfolio repositories, performed once before the Scouts' observation history begins.

It does not describe the implementation. It exists so that later implementers and agents cannot dilute the rules below. Where an implementation choice is not constrained here, it is a technical decision of the implementer.

The backfill is a temporary stage-1 collector. It does not change the V1.1 Scout/Supervisor model, the Finding contract, or any Health Book rule.

## Status and lifecycle

- This contract applies only to the single historical backfill described here.
- It ends when the portfolio gate reaches `PORTFOLIO_BACKFILL_COMPLETE`; afterwards the collector is a no-op and this contract is retained as history.
- Changing an invariant below requires a reviewed change to this file. An implementation, prompt, or run configuration must not weaken an invariant by itself.
- Authority order: live GitHub/repository state, then this contract, then the local handoff and run configuration. Cloud, Google Drive, Google OAuth, W1 and earlier capability probes are **historical evidence only** and create no current requirement.

## 1. Workflow state

Historical Backfill workflow state is workflow-local collection state and is not a second Scout/Supervisor checkpoint mechanism.

- The collector ledger is temporary workflow state of this one backfill.
- Scout and Supervisor checkpoints remain exactly as defined by [`CHECKPOINT_CONTRACT.md`](CHECKPOINT_CONTRACT.md): mutable GitHub Health Book comments.
- Collector state must not replace, imitate, write to, or duplicate Scout/Supervisor checkpoints, and must not be read by Scouts or the Supervisor as a cursor.
- The ledger lives only in the LocalStore (section 9). It is never written to a Health Book, issue, or repository.

## 2. Scope

The backfill covers exactly these seven repositories:

- `jannekbuengener/sample-brain`
- `jannekbuengener/sample-brain-analysis`
- `jannekbuengener/arvp`
- `jannekbuengener/traum_taenzer`
- `jannekbuengener/Claire_de_Binare`
- `jannekbuengener/agent-brain`
- `jannekbuengener/security-business`

Portfolio authority remains the live [`portfolio/REPOSITORIES.md`](../portfolio/REPOSITORIES.md). If live membership differs from the list above when the portfolio horizon is frozen (section 5), the collector stops with `BLOCKED_SCOPE_MISMATCH` and the owner decides; it never adds or drops a repository on its own. `jannekbuengener/gpt-mcp-server` is excluded.

## 3. Architecture boundary

Binding for this backfill:

```text
Claude Code (local) -> deterministic Python collector -> GitHub API -> LocalStore
```

Persistence is exclusively the local filesystem under `D:\Dev\Workspaces\AWH\history-backfill-v1` (the LocalStore).

Not part of the backfill, and not allowed as a data path or dependency: Claude Cloud runtime, Scheduled Tasks, Google Drive, W1, Google OAuth, n8n, service accounts, and any additional cloud storage.

No model is in the data path. Claude Code may start and observe the collector; collection, normalization, hashing, and gating are deterministic code.

## 4. Collect, do not think

The collector **may**: read; normalize deterministically; preserve source IDs; compute hashes; extract explicit references; apply the horizon; store; advance the ledger; verify completeness.

The collector **must not**: assess semantically; cluster; prioritize; determine root causes; recommend workforce roles; recommend automations; produce findings; summarize historical content.

The collector stores metadata and fingerprints. Bodies, comments, logs and similar raw content are retrieved only by a later, separately approved stage. Explicit references (for example GHSA/CVE identifiers, `owner/repo#n`, commit SHAs) may be extracted by pattern and recorded with the field of origin. Unclear data is recorded as unknown (section 5), never guessed.

## 5. Global horizon

- Exactly one portfolio-wide `portfolio_collection_horizon` (H) is frozen once for all seven repositories, with the owner's approval, before collection starts.
- Per repository, `horizon_sha` is recorded where it can be determined deterministically. A repository head that changes between the two freeze snapshots yields no `horizon_sha` for that repository until re-frozen under owner approval.
- Data created after H does not belong in the backfill.
- If the state at H cannot be reconstructed unambiguously from live data, the field is recorded as `UNKNOWN` with reason `AFTER_HORIZON_UNRECONSTRUCTABLE`. No state is reconstructed by inference or invented retroactively.
- Once frozen, H and the project configuration are immutable.

## 6. Scout cutover

`analysis_cutover` is separate from the horizon. It is derived per repository from the Health Book initial baselines as already defined for the Scouts; if it cannot be derived unambiguously the repository is `BLOCKED_CUTOVER_UNDETERMINED`.

Every record is marked `PRE_SCOUT_CUTOVER` or `POST_SCOUT_CUTOVER` (and as crossing the cutover where applicable). Records after the cutover up to H are collected, not dropped.

## 7. Identity and versioning

- Source IDs (node ID, native number/ID, URLs) are never lost.
- Every record has a stable `record_id` and a canonical `content_sha256`.
- Same ID and same hash: identical record.
- Same ID and different hash: a new version, recorded as `SOURCE_DRIFT`; the earlier version stays.
- Committed historical versions are never overwritten.
- Nothing is deleted. Information is filtered later by consumers, not discarded by the collector.

## 8. `READ_ONLY_FAIL_CLOSED`

This is a hard security invariant. The local GitHub credential has write rights (admin/push). Read-only behavior is therefore enforced technically, not by prompt discipline.

Allowed:

- REST `GET`
- GraphQL `POST` only to `/graphql` and only containing exactly one `query` operation

Forbidden:

- REST `POST`, `PUT`, `PATCH`, `DELETE`
- GraphQL `mutation` and `subscription`
- any repository mutation

A violation is `READ_ONLY_VIOLATION`, ends the run as BLOCKED with exit code 40, and occurs **before** a network request is built.

Requirements:

- All network access passes through one gateway that enforces the rules above; no other code path may open a network connection.
- Ambiguity is rejected (fail closed), for example a GraphQL document that cannot be classified as a single query.
- The credential is taken from the existing local GitHub authentication into process memory only. It is never printed, written to files, logs, reports, handoffs or ledger, never persisted as an environment variable, and error text is scrubbed of it.
- Tests must prove that each forbidden method and each mutation form is rejected without a network call. A backfill run requires those tests to pass.
- A narrower read-only credential is recommended but not required by this contract; it never replaces the gateway.

## 9. LocalStore

- Writes are atomic: temporary file, `fsync`, hash verification, then rename/replace.
- The hash is verified before the commit step.
- A committed file is never overwritten.
- Data files are JSONL, UTF-8, LF line endings, canonical serialization.
- An intent record is written before data is stored; a commit record is written only after verification.
- An open intent without a commit is resumed by repeating exactly the same range.
- There is no progress without a commit.

## 10. Sequence and concurrency

- Exactly one collector process.
- One repository is collected completely before the next starts.
- No parallel writers.
- The preservation sweep (section 13) is the only portfolio-wide exception to repository-sequential collection.
- A lock or lease file may guard against accidental double starts. It must not be described or relied on as an atomic distributed lock.

## 11. Required source domains

Each of the following has its own completeness domain with its own completeness evidence:

1. Scope/manifest
2. Dependabot alerts
3. Code Scanning alerts
4. Secret Scanning alerts, never storing secret content (`hide_secret=true`; the secret value is never requested or stored)
5. Workflows
6. Workflow runs and attempts
7. Jobs and steps
8. Run log and retention evidence
9. Artifact metadata
10. Check runs
11. Check annotations
12. Issue/PR number space (every number from 1 to the frozen maximum has exactly one recorded outcome)
13. Timeline
14. Reviews
15. PR commits
16. Commits
17. Discussions, or proven `NOT_ENABLED`
18. Labels
19. Milestones
20. Releases

A feature that is disabled for a repository counts as complete only when `NOT_ENABLED` is **reproducibly proven**: the exact request, the response status and message (or the GraphQL field such as `hasDiscussionsEnabled=false`), the time, and a fingerprint are stored, and a re-query yields the same classification. `NOT_ENABLED` is not a permission error. A missing permission is never recorded as `NOT_ENABLED`; it blocks the repository.

A zero-result response is not by itself proof of completeness; the domain's count check applies.

## 12. Completion

A repository may be marked complete only when every required domain is either collected and verified, or reproducibly proven `NOT_ENABLED`, and the repository gate passes. The gate checks at least: frozen scope and cutover evidence; gap-free number space against live totals; commit and run counts against live totals; child-record counts; ledger continuity and hash verification; link resolution; preservation coverage; and an independent verification step (schema check, recount with a different method, reproducible samples, scan of the output for secrets).

"Best effort" is never "complete". Failure is `REWORK` on the same repository identity and history, not a new order.

Portfolio completion exists only when all seven repository gates have passed.

## 13. Preservation sweep

Before the slow backfill, a single portfolio-wide pass may secure evidence that is demonstrably at risk of expiring (for example retention-limited logs of failed runs and retention-limited artifacts). It performs no analysis, mutates no repository, and does not bulk-store content blindly: every item is recorded with the reason it is considered at risk.

## 14. Reuse decision

Decision (reuse_before_build, see [`../docs/REUSE_BEFORE_BUILD.md`](../docs/REUSE_BEFORE_BUILD.md)): `BUILD_MINIMAL_CUSTOM`, standard library only.

- MeltanoLabs `tap-github` is `REUSE_COMPONENT` **only** as an endpoint and parent/child reference, a backoff and rate-limit design template, and an optional independent cross-check tool after separate approval.
- It is not a dependency of the collector data path.
- No code is adopted without a licence review.
- `github-to-sqlite` and Airbyte `source-github` were rejected.
- The bounded XERJ reference check returned `NO_RELEVANT_REFERENCE`.

## Out of scope

This contract does not authorize implementing the collector, freezing the horizon, running the preservation sweep, or starting the backfill. Each of those requires its own explicit owner approval.
