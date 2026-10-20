# Checkpoint Contract V1.1

## Purpose

Agent Workforce uses exactly one durable operational checkpoint mechanism for Scout inspection state and Supervisor review state.

A checkpoint is mutable GitHub issue-comment metadata. It is not repository truth, not a Finding, not a Baseline, not a runtime database, and not recurrence evidence.

## Core rule

```text
Scout: read checkpoint -> inspect -> write normal evidence only when material -> update same checkpoint
Supervisor: read cursor -> review newer Scout outputs -> update same cursor
```

No parallel state mechanism is introduced.

## Scout checkpoint

Each active Scout has exactly one checkpoint comment in each canonical Repo Health Book.

Stable marker:

```text
<!-- agent-workforce:scout-checkpoint:v1 scout=<agent_id> -->
```

Required fields:

- `checkpoint_version`
- `scout`
- `repo`
- `last_inspected_at`
- `last_repo_head`
- `last_runtime_outcome`
- `baseline_complete`
- `last_material_output_comment_id`
- `last_material_output_at`

Example serialization:

```yaml
checkpoint_version: 1
scout: workforce.quality-scout.v1
repo: owner/repository
last_inspected_at: 2026-10-21T12:00:00+02:00
last_repo_head: abcdef123456
last_runtime_outcome: NO_MATERIAL_CHANGE
baseline_complete: true
last_material_output_comment_id: 1234567890
last_material_output_at: 2026-10-20T10:00:00+02:00
```

### Update semantics

After every completed deep inspection, the acting Scout updates the same checkpoint comment with the current run state.

`INITIAL BASELINE` and `FINDING DELTA` comments remain governed by their own evidence rules. `NO_MATERIAL_CHANGE` and `SKIP_NO_DELTA` do not create normal evidence comments; they still advance the Scout checkpoint because an inspection occurred.

Checkpoint-only updates do not change Finding lifecycle, `last_seen`, recurrence, severity, confidence, or disposition.

### Lazy initialization

Existing Health Books are not rewritten to invent historical inspection timestamps.

If no Scout checkpoint exists, the next real Scout inspection creates one from the current run. `last_inspected_at` and `last_repo_head` are never backfilled from historical comments.

`baseline_complete` may be set to `true` only when that Scout's Initial Baseline is visibly present in the Health Book or is created in the current run.

`last_material_output_comment_id` and `last_material_output_at` may be initialized from an existing Baseline or Finding comment only when attribution to the acting Scout is unambiguous; otherwise they remain `null` until the next material output.

## Supervisor checkpoint

Meta issue `#3` contains exactly one Supervisor checkpoint comment.

Stable marker:

```text
<!-- agent-workforce:supervisor-checkpoint:v1 -->
```

Required state:

- `checkpoint_version`
- `last_supervisor_run_at`
- one `last_reviewed_output_comment_id` per canonical Repo Health Book

Example serialization:

```yaml
checkpoint_version: 1
last_supervisor_run_at: 2026-10-21T12:00:00+02:00
health_books:
  owner/repository#123:
    last_reviewed_output_comment_id: 1234567890
```

The Supervisor treats only `INITIAL BASELINE` and `FINDING DELTA` comments as reviewable Scout outputs. Scout checkpoint comments and the Supervisor checkpoint itself are ignored as evidence outputs.

After reviewing all newer Scout outputs for a Health Book, the Supervisor advances that Health Book's cursor to the highest successfully reviewed output comment id.

## V1.1 Supervisor cutover

The Supervisor checkpoint must not start with guessed or blanket-null review cursors.

For each current Health Book, initialize `last_reviewed_output_comment_id` only from inspectable evidence:

1. identify Baseline/Finding comments in the Health Book;
2. read existing Workforce Supervisor comments in meta issue `#3`;
3. determine the highest Scout output comment that is unambiguously already reviewed;
4. write that comment id as the initial cursor.

If this cannot be determined safely for any Health Book, do not guess. The cutover for that Health Book remains blocked.

Historical duplicate Supervisor reviews may be accepted as historical facts. They do not create new Scout evidence or recurrence.

## Duplicate markers

There must be at most one active matching checkpoint marker for the same identity.

If more than one matching Scout checkpoint or more than one Supervisor checkpoint exists, fail closed with:

`BLOCKED_CHECKPOINT_STATE_UNAVAILABLE`

Never choose one duplicate arbitrarily.

## Failure semantics

If a required checkpoint cannot be read, created, updated, or verified safely, the run must not claim successful state advancement.

Runtime outcome:

`BLOCKED_CHECKPOINT_STATE_UNAVAILABLE`

This is an operational state, not a repository defect.

## Authority

This contract adds only the minimum write permission required for checkpoint maintenance:

- a Scout may create or update its own checkpoint comment in the canonical Repo Health Book;
- the Supervisor may create or update the Supervisor checkpoint in meta issue `#3`.

It grants no permission to modify product code, create implementation PRs, create follow-up issues automatically, change secrets/governance, or create new workforce roles.
