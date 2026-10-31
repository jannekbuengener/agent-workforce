# Head of Knowledge — Weekly Owner Report

## Status

```text
CONTRACT_STUB_FOR_CAPABILITY_ID
full_body_owned_by: agent-workforce#73
capability_id: knowledge_owner_report
```

This stub exists so Capability ID `knowledge_owner_report` can be registered
under least-privilege authority (#70) without inventing a productive report
format early.

Until #73 completes this contract:

- do **not** treat this document as a finished reporting schema;
- productive Owner-report generation must fail closed rather than invent KPIs
  or section semantics;
- required report sections planned in the employee record remain authoritative
  intent only.

## Planned required sections (from employee record; finalized in #73)

1. What happened?
2. What is critical?
3. What was decided?
4. Current data-quality situation
5. Relevant uncertainties
6. Concrete action recommendations from trends / recurring patterns

## Planned data-quality rule

No percentage without a reproducible method. Until a method exists:

```text
Datenqualität: nicht belastbar quantifizierbar
```

## Exit token (issue #73)

`HEAD_OF_KNOWLEDGE_OWNER_REPORT_DEFINED`
