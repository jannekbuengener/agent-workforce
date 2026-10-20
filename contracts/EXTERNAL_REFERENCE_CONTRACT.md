# External Reference Contract

## Purpose

This contract defines how Agent Workforce discovers and uses external technical references without turning external documentation into a second repository truth store.

It separates two concerns:

1. **shared discovery/reference anchors** known across repositories;
2. **repository-local relevance** owned by each target repository.

External references support engineering work. They do not override GitHub live state, target-repository canon, source code, dependency manifests, CI configuration, or repository-local authority.

## Authority order

Use external references only after current target-repository authority is established.

1. GitHub / repository live state;
2. target-repository local authority (`AGENTS.md`, README/front door, canon, architecture, contracts, source/config/CI as applicable);
3. this external-reference contract;
4. repo-local external-reference manifest;
5. external source authority hierarchy defined below.

A repo-local manifest records what references are relevant to the repository. It does not make those external sources authoritative over the repository itself.

## Ownership model

### Shared catalog — workforce-owned

[`references/CATALOG.yml`](../references/CATALOG.yml) contains a deliberately small set of reusable cross-repository reference/discovery anchors.

The shared catalog owns only:

- portable source identity / canonical public URL;
- source type;
- external-source authority class;
- broad purpose/category;
- `when_to_use` discovery triggers.

Catalog membership means **known reusable source**, not **used by this repository**.

The shared catalog must not become:

- a central inventory of every technology used by every repository;
- a dependency lockfile;
- a copy of target-repository architecture or runtime state;
- a reason to load every listed source into every agent context.

### Repo-local manifest — target-repository-owned

Each target repository may own one canonical external-reference manifest, normally:

```text
docs/external-docs/index.md
```

If that repository already has an equivalent canonical docs surface, local authority may use it instead. Uniform ownership/semantics matter more than forcing a path rename.

The repo-local manifest owns repository-specific relevance:

- what external references matter to this repository;
- why they matter;
- what current repo evidence supports that relevance;
- when the reference should be consulted;
- whether it is active (`P0`/`P1`) or parked (`P2`).

## Priority: repository relevance

Priority is independent from source authority.

### `P0`

Active/core reference.

Use when the reference supports a current core tool, service, agent, runtime, direct dependency, CI/security path, or operational surface that maintainers/agents need to understand correctly.

A `P0` entry belongs in the repo-local canonical manifest while that current repo signal exists.

### `P1`

Relevant secondary reference.

Use when the referenced area is actively maintained, debugged, tested, integrated, operated, or likely to require recurring engineering attention, but is not a core always-needed path.

### `P2`

Parked/reference-only.

Use for intentionally retained future-scope, example, pattern or discovery references that are not active implementation assumptions.

`P2` entries must not be loaded or treated as active technology/dependency evidence until a concrete task/scope activates them. If a parked reference has no useful future purpose, omit it rather than growing the manifest indefinitely.

## External source authority

Priority (`P0`/`P1`/`P2`) does **not** express truth authority.

When external sources conflict, prefer the highest applicable class:

1. `OFFICIAL_SPEC` — standards/specifications published by the owning standards/project authority;
2. `OFFICIAL_DOCS` — official product/language/platform documentation;
3. `UPSTREAM_PROJECT_DOCS` — upstream repository/project documentation maintained with the implementation;
4. `UPSTREAM_ISSUES_RELEASES` — upstream issues, changelogs, releases and maintainer evidence;
5. `ESTABLISHED_TECHNICAL_KNOWLEDGE` — durable technical references with established engineering value;
6. `COMMUNITY` — community experience such as Stack Overflow;
7. `EXAMPLE_DISCOVERY` — examples, curated lists, awesome lists and inspiration/discovery sources.

Even `OFFICIAL_SPEC`/`OFFICIAL_DOCS` remain below current target-repository truth for claims about what the target repository actually uses, configures, supports or requires.

## Source types

Repo-local manifests and the shared catalog should use precise source types when practical. Recommended values:

- `official_spec`
- `official_docs`
- `upstream_project_docs`
- `upstream_issues_releases`
- `established_technical_knowledge`
- `community`
- `example_discovery`

A source type describes the source. It does not determine `P0`/`P1`/`P2` priority.

## Canonical inclusion rule

A reference normally belongs in a repo-local manifest only when at least one is true:

1. it belongs to an active tool, service, agent, runtime or operational path;
2. it documents a direct repository dependency;
3. it is needed for onboarding, implementation, debugging, testing, CI, security or runtime operation;
4. it is intentionally retained as an example/pattern/discovery source and explicitly marked as such.

Otherwise:

- keep it `P2` / parked if there is a concrete reason to retain it; or
- omit it.

A shared-catalog entry alone is never sufficient inclusion evidence.

## Required repo-local fields

Every repo-local reference entry should provide enough information for an agent to decide whether to load it without guessing.

Required fields:

- `name` — human-readable source/project name;
- `url` or portable upstream identity — public canonical location;
- `priority` — `P0 | P1 | P2`;
- `source_type`;
- `authority` — one of the authority classes above;
- `category` — repository-relevant grouping;
- `purpose` — what technical question the source helps answer;
- `repo_signal` — concrete repository evidence/relevance justification;
- `when_to_use` — task/scope trigger.

For `P0` and `P1`, `repo_signal` must identify current evidence such as a dependency declaration, source path, workflow/config file, runtime/service surface, architecture contract, test surface or other live repo artifact.

For `P2`, `repo_signal` may explicitly say that no active path exists and why the reference is intentionally parked.

## Relevance-gated loading

Do not load a whole manifest or the whole shared catalog merely because it exists.

After target-repository authority handoff:

1. identify the current technical question and scope;
2. inspect the repo-local manifest when present;
3. select only entries whose category / `when_to_use` / repo signal match the task;
4. consult the shared catalog only when a matching reusable reference/discovery anchor is useful;
5. use higher-authority external sources first for factual/compatibility claims;
6. use community/example sources for experience, edge cases or discovery leads, then verify consequential claims against stronger evidence.

No relevant match means no external-reference loading requirement.

## Relationship to reuse-before-build

[`docs/REUSE_BEFORE_BUILD.md`](../docs/REUSE_BEFORE_BUILD.md) defines the engineering decision procedure for build-vs-reuse choices.

This contract can supply external evidence for that discovery, but it does not change the reuse decision order:

- existing repo code and accepted dependencies still come first;
- shared catalog entries are discovery anchors, not automatic adoption recommendations;
- dependency/tool adoption still requires target-repository authority and normal validation.

## Portability and privacy

Committed shared catalogs, templates and repo-local manifests must not contain:

- workstation-specific absolute installation or checkout paths;
- credentials, tokens, secrets or private endpoints;
- internal hostnames that are not intentionally public project identifiers;
- mutable connection/install state;
- private sample/data paths;
- copied local environment inventories that are not repository canon.

Use public canonical URLs and portable upstream identities.

Execution hosts may resolve local checkouts/installations at runtime, but that host-local path remains operational state and is not committed as reference canon.

## Mutation boundary

References provide knowledge/evidence only. They do not authorize:

- dependency installation;
- vendoring/copying third-party code;
- enabling external/cloud services;
- configuration or governance changes;
- license exceptions;
- security exceptions;
- target-repository mutations outside normal authority/review rules.

## Template

Use [`templates/EXTERNAL_REFERENCE_INDEX.md`](../templates/EXTERNAL_REFERENCE_INDEX.md) when creating or normalizing a repo-local manifest unless local repository canon defines an equivalent compatible surface.

Issue #13 owns repository-by-repository rollout. This contract does not itself require a target repository mutation.
