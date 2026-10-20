# External References

> Canonical repo-local manifest of external technical references that are relevant to this repository.
>
> Source semantics: `jannekbuengener/agent-workforce/contracts/EXTERNAL_REFERENCE_CONTRACT.md`.
>
> This file records **reference relevance**, not repository truth. GitHub/repo live state, local canon, source/config/CI and dependency manifests remain authoritative for what this repository actually uses.

## Usage rules

- Keep only references justified by current repository evidence or an explicitly parked future/pattern scope.
- `P0` / `P1` require a concrete current `Repo signal`.
- `P2` is parked/reference-only and must not imply active implementation scope.
- Priority expresses repository relevance, not source authority.
- Prefer official/upstream sources over community/example sources for consequential factual claims.
- Load only references relevant to the current task; do not dump this entire manifest into every agent context.
- Do not commit workstation-specific absolute paths, credentials, private endpoints, secrets or transient local installation state.

## Priority legend

| Priority | Meaning |
|---|---|
| `P0` | Active/core reference for a current core tool, service, runtime, direct dependency or operational path. |
| `P1` | Relevant secondary reference for an area that is actively maintained, debugged, tested or operated. |
| `P2` | Parked/reference-only; use only when concrete scope activates it. |

## Source authority legend

Highest applicable external authority first:

1. `OFFICIAL_SPEC`
2. `OFFICIAL_DOCS`
3. `UPSTREAM_PROJECT_DOCS`
4. `UPSTREAM_ISSUES_RELEASES`
5. `ESTABLISHED_TECHNICAL_KNOWLEDGE`
6. `COMMUNITY`
7. `EXAMPLE_DISCOVERY`

This hierarchy is still below target-repository live truth/canon for claims about this repository.

## Active references

Use one row per `P0` / `P1` reference.

| Category | Name | Priority | Source type | Authority | Purpose | Repo signal | When to use | Canonical URL / portable identity |
|---|---|---|---|---|---|---|---|---|
| `<category>` | `<name>` | `P0` | `official_docs` | `OFFICIAL_DOCS` | `<what question this source answers>` | `<current file/dependency/config/workflow/service/contract signal>` | `<task/scope trigger>` | `<public canonical URL or upstream identity>` |
| `<category>` | `<name>` | `P1` | `upstream_project_docs` | `UPSTREAM_PROJECT_DOCS` | `<purpose>` | `<current repo evidence>` | `<when relevant>` | `<URL or identity>` |

## Parked references

Use this section only when retaining the reference has a concrete future/pattern/discovery purpose. Otherwise omit the entry.

| Category | Name | Priority | Source type | Authority | Purpose | Repo signal / parked reason | When to use | Canonical URL / portable identity |
|---|---|---|---|---|---|---|---|---|
| `<category>` | `<name>` | `P2` | `example_discovery` | `EXAMPLE_DISCOVERY` | `<future/pattern/discovery purpose>` | `<no active path; explain why intentionally retained>` | `<scope that would activate it>` | `<URL or identity>` |

## Inclusion check

Before adding a reference, at least one should be true:

- it belongs to an active tool, service, agent, runtime or operational path;
- it documents a direct repository dependency;
- it is needed for onboarding, implementation, debugging, testing, CI, security or runtime operation;
- it is intentionally retained as an example/pattern/discovery source and is explicitly marked as such.

If none apply, omit it.

## Maintenance notes

- Remove or demote entries when the supporting repo signal disappears.
- Promote `P2` only when real scope activates it and current repo evidence justifies the new priority.
- A source appearing in the Agent Workforce shared catalog does not automatically belong here.
- Community/example references can suggest approaches; verify consequential claims against stronger current sources before implementation decisions.
