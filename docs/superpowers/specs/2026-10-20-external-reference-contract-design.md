# External Reference Contract Design

## Goal

Define a portable, relevance-gated external-reference architecture for Agent Workforce that separates globally reusable discovery/reference sources from repository-owned external-documentation manifests.

## Source basis

This design implements issue #12 and generalizes the owner-provided `CDB Externe Docsliste` / `Gute Links` pattern without copying Claire de Binare's technology inventory into workforce canon.

The source pattern establishes:

- repository relevance classes `P0`, `P1`, `P2`;
- concrete repo-signal evidence for included references;
- explicit parked/inactive references;
- a canonical-inclusion rule tied to active tools, direct dependencies, onboarding/debugging/CI/security/runtime needs, or intentionally retained pattern sources;
- community/example sources as useful references, not repository truth.

## Architecture

### Shared catalog

`references/CATALOG.yml` is a small cross-repository catalog of reusable reference/discovery anchors. It owns portable source identity, source type, authority class, purpose, and relevance triggers.

It does not prove that a source is relevant to a particular target repository and must never be treated as a dependency or technology inventory.

### Repo-local manifest

Each target repository may own a canonical external-reference manifest, normally `docs/external-docs/index.md` unless local canon provides an equivalent established surface.

That manifest owns repository-specific relevance only. Every active `P0`/`P1` entry requires concrete current repo evidence (`repo_signal`). `P2` entries are parked/reference-only and do not imply active implementation scope.

### Generic contract/template

`contracts/EXTERNAL_REFERENCE_CONTRACT.md` defines precedence, inclusion, relevance gating, privacy/path boundaries, and loading behavior.

`templates/EXTERNAL_REFERENCE_INDEX.md` is the reusable human-readable schema for repository manifests.

## Priority semantics

- `P0`: active/core reference; must be represented when it supports a current core tool, service, runtime, direct dependency or operational path.
- `P1`: relevant secondary reference; include when the area is actively maintained, debugged, tested or operated.
- `P2`: parked/reference-only; load only when concrete scope activates it, otherwise omit.

Priority expresses repository relevance, not truth authority.

## Source authority

External evidence precedence:

1. `OFFICIAL_SPEC`
2. `OFFICIAL_DOCS`
3. `UPSTREAM_PROJECT_DOCS`
4. `UPSTREAM_ISSUES_RELEASES`
5. `ESTABLISHED_TECHNICAL_KNOWLEDGE`
6. `COMMUNITY`
7. `EXAMPLE_DISCOVERY`

Repository/GitHub live truth and target-repository canon remain above this external-source hierarchy.

## Canonical inclusion rule

A repo-local reference normally belongs in the active manifest only when at least one is true:

1. it belongs to an active tool, service, agent, runtime or operational path;
2. it documents a direct repository dependency;
3. it is needed for onboarding, debugging, CI, security, testing or runtime operation;
4. it is intentionally retained as an example/pattern/discovery source and explicitly marked as such.

Otherwise keep it `P2`/parked or omit it.

## Relevance-gated loading

Agents do not bulk-load the shared catalog or every manifest entry.

After target-repository authority handoff:

1. determine the current technical question/scope;
2. use the target repo's manifest when one exists;
3. select only entries whose `when_to_use`/category/repo signal match the current work;
4. consult the shared catalog only for applicable cross-repository discovery/reference anchors;
5. prefer higher-authority sources when claims conflict.

## Shared catalog V1 seed

Seed only sources directly supported by the approved working material and broadly reusable across engineering repositories:

- GitHub Docs;
- GitHub CLI manual;
- Python documentation;
- Stack Overflow;
- Awesome Python;
- Awesome System Design.

The seed is deliberately small. Catalog membership does not imply target-repo relevance.

## Safety and portability

Committed reference files must not contain:

- workstation-specific absolute installation or checkout paths;
- credentials, tokens, private endpoints, internal hostnames or secrets;
- transient installation/connection state;
- copied repository truth that belongs in source/config/CI/live GitHub.

Use public canonical URLs or portable upstream identities.

## Scope boundary

This issue creates the generic contract, shared catalog, template and workforce/front-door discovery rules only.

Issue #13 owns repository-by-repository rollout and normalization. No target repository manifests are created in this slice.
