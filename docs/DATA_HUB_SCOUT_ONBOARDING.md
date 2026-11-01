# Data Hub — Scout Onboarding Note

## Purpose

This note records the intended Workforce onboarding of `jannekbuengener/data-hub`.

The repository should be monitored by the existing Quality Scout and Process Scout under the normal Agent Workforce V1.1 rules. No new Scout role, scheduler prompt, checkpoint mechanism or special runtime is required.

## Canonical mechanism

The canonical trigger is portfolio membership in `portfolio/REPOSITORIES.md` plus a repo-local canonical Repo Health Book.

Once added:

- Quality Scout owes one `INITIAL BASELINE` for `data-hub`;
- Process Scout owes one `INITIAL BASELINE` for `data-hub`;
- missing baselines are the highest normal selection priority under Workforce Policy;
- later inspections use the same material-delta and silence rules as every other monitored repository.

Do not special-case `data-hub` in scheduler prompts.

## Initial observation focus

### Quality Scout

Pay particular attention to:

- drift between Data Hub product vision, MVP, architecture and actual implementation;
- accidental adoption of superseded AWH infrastructure as current Data Hub architecture;
- accidental coupling of Data Hub to AWH-specific GitHub/Workforce semantics;
- provenance/evidence gaps;
- privacy/credential boundaries;
- AI outputs that are not traceable to evidence;
- correlation/causality or certainty overclaiming.

### Process Scout

Pay particular attention to:

- duplicate collector implementations between Agent Workforce and Data Hub;
- repeated manual connector/normalization work that should become a generic primitive;
- repeated context-loss/reconstruction across research, canon and implementation;
- recurring agent work that would be cheaper/more reliable as deterministic automation;
- transfer/handoff friction around the generic collector-core extraction.

## Cross-repository context

Read `docs/DATA_HUB_COLLECTOR_TRANSFER_CONTEXT.md` when the AWH/Data-Hub transfer relationship materially affects an inspection.

Target-repository truth still wins: after selecting `data-hub`, enter its local authority and read its current `AGENTS.md`, README and relevant product canon before applying these observation hints.

## Agent Brain

Agent Brain is already a registered shared context/evidence capability and a monitored portfolio repository. Its availability does not make it an implicit dependency of Data Hub. Use it only through the normal relevance-gated capability routing rules.
