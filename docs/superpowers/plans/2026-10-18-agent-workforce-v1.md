# Agent Workforce V1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Establish a minimal, low-cost cross-repository AI scout workforce with two advisory roles, one canonical private workforce repository, five repo-local Health Books, two scheduled ChatGPT scout tasks, and a controlled first baseline round.

**Architecture:** `agent-workforce` is the single versioned authority for cross-repository role contracts, workforce policy, portfolio membership, and templates. Each monitored product repository owns its own long-lived Repo Health Book issue; scheduled ChatGPT runs use GitHub live state plus those Health Books to select one repository for deep inspection per run. NotebookLM remains a derived read/retrieval surface only.

**Tech Stack:** Git/GitHub, Markdown with compact YAML front matter for role identity, GitHub Issues, ChatGPT scheduled tasks, GitHub connector / `gh` CLI, no database, no GitHub Actions required for V1.

**Spec:** `C:\Users\janne\Desktop\Agent-Workforce-V1-Design.md` (Task 1 commits the approved spec into `docs/superpowers/specs/2026-10-18-agent-workforce-v1-design.md` in `agent-workforce`).

## Global Constraints

- V1 has exactly two scout roles: Quality Scout and Process Scout.
- Initial portfolio: `sample-brain`, `sample-brain-analysis`, `arvp`, `traum_taenzer`, `Claire_de_Binare`.
- `gpt-mcp-server` is excluded from the initial active portfolio.
- Scouts are advisory only: read/analyze, append Health Book evidence, recommend follow-up work; no code repair, implementation PRs, governance changes, secret changes, specialist-agent creation, or automatic follow-up issue creation.
- One scheduled run may shallow-preflight all in-scope repositories but performs deep inspection of exactly one repository.
- Repo-local/live authority wins over generic assumptions; stale memory is never live truth.
- `SKIP_NO_DELTA` produces no Health Book comment.
- Routine unchanged conditions produce no repeated comments.
- Same root cause means same finding identity, even when observed by both scouts.
- Severity vocabulary: `INFO | LOW | MEDIUM | HIGH | CRITICAL`.
- Confidence vocabulary: `LOW | MEDIUM | HIGH`.
- No dedicated mutable scheduling database or committed `last_run` ledger in V1.
- NotebookLM is not an authority and is never an execution dependency.
- No heavy plugin/MCP build, no Hermes migration, no event-driven orchestration in V1.
- No hosted GitHub Actions are required for the private workforce repo; keep recurring cost near zero.
- No direct push to protected/default branches after repository initialization; implementation work goes through a feature branch and PR.

## Review Focus

1. **Duplicate Health Book already exists:** implementation must search each repo before creating anything and reuse an existing canonical Health Book if found.
2. **Mixed public/private portfolio access:** a scout blocked from one repo must emit `BLOCKED_NO_REPO_ACCESS`, never infer from another repo or stale memory.
3. **Bot/self-comment activity:** scout selection must not treat its own Health Book comments or generic bot noise as meaningful engineering activity that causes write loops.
4. **No-delta runs:** zero meaningful activity and no due finding must end without a GitHub comment.
5. **Finding identity drift:** repeated evidence for the same root cause must update/reference the same stable finding id instead of multiplying records.

---

## Planned File Structure

```text
agent-workforce/
├── README.md                         # human front door + authority map
├── AGENTS.md                         # agent operating boundary / truth order
├── agents/
│   ├── quality-scout.md              # Quality Scout role contract
│   └── process-scout.md              # Process Scout role contract
├── contracts/
│   └── FINDING_CONTRACT.md           # shared finding schema / vocab / identity rule
├── templates/
│   └── REPO_HEALTH_BOOK.md           # canonical issue body + comment shapes
├── portfolio/
│   └── REPOSITORIES.md               # monitored repo membership only
└── docs/
    ├── WORKFORCE_POLICY.md            # authority, scheduling, promotion, anti-noise
    ├── NOTEBOOKLM.md                  # derived knowledge-surface rules
    └── superpowers/
        ├── specs/
        │   └── 2026-10-18-agent-workforce-v1-design.md
        └── plans/
            └── 2026-10-18-agent-workforce-v1.md
```

No runtime state directory, database, workflow YAML, or generated dashboard is added in V1.

---

### Task 1: Bootstrap the private `agent-workforce` authority repository

**Files:**
- Create: `README.md`
- Create: `AGENTS.md`
- Create: `portfolio/REPOSITORIES.md`
- Create: `docs/WORKFORCE_POLICY.md`
- Create: `docs/NOTEBOOKLM.md`
- Create: `docs/superpowers/specs/2026-10-18-agent-workforce-v1-design.md`
- Create: `docs/superpowers/plans/2026-10-18-agent-workforce-v1.md`

**Interfaces:**
- Consumes: approved design at `C:\Users\janne\Desktop\Agent-Workforce-V1-Design.md` and this plan.
- Produces: private canonical repo `jannekbuengener/agent-workforce` with a stable main branch and feature branch `workforce/v1-bootstrap`.

- [ ] **Step 1: Verify repository does not already exist**

Run with GitHub/`gh`:
```powershell
gh repo view jannekbuengener/agent-workforce
```
Expected: not found. If it exists, stop and inspect before creating anything.

- [ ] **Step 2: Create the private repository with only an initial README commit**

From `D:\Dev\Workspaces\Repos`:
```powershell
gh repo create jannekbuengener/agent-workforce --private --add-readme --description "Canonical role and policy repository for Jannek's cross-repository AI engineering workforce." --clone
```
Expected: private repo created and cloned at `D:\Dev\Workspaces\Repos\agent-workforce`.

- [ ] **Step 3: Verify origin, visibility, default branch and clean state**

Run:
```powershell
cd D:\Dev\Workspaces\Repos\agent-workforce
git remote -v
git status --short --branch
gh repo view --json nameWithOwner,visibility,defaultBranchRef
```
Expected: `jannekbuengener/agent-workforce`, `PRIVATE`, default `main`, clean working tree.

- [ ] **Step 4: Create implementation branch**

Run:
```powershell
git switch -c workforce/v1-bootstrap
```
Expected: branch `workforce/v1-bootstrap`.

- [ ] **Step 5: Write the authority skeleton**

Required content decisions:
- `README.md`: purpose, truth order, repo map, no runtime state, links to roles/contracts/templates/policy.
- `AGENTS.md`: live truth first; repo-local truth for monitored repos; no private MCP requirement; advisory V1 authority; blocked states fail closed.
- `portfolio/REPOSITORIES.md`: exactly the five in-scope repos; separate section noting `gpt-mcp-server` is excluded from V1. Do not assign persisted activity classes here.
- `docs/WORKFORCE_POLICY.md`: scheduling priority, one-deep-repo rule, anti-noise, authority/state separation, promotion criteria.
- `docs/NOTEBOOKLM.md`: NotebookLM is derived; direct GitHub links or dated snapshots only; no write-back or sync service.
- copy approved design and this plan into the documented paths above.

- [ ] **Step 6: Run deterministic docs validation**

Run:
```powershell
$required = @(
  'README.md','AGENTS.md','portfolio/REPOSITORIES.md','docs/WORKFORCE_POLICY.md','docs/NOTEBOOKLM.md',
  'docs/superpowers/specs/2026-10-18-agent-workforce-v1-design.md',
  'docs/superpowers/plans/2026-10-18-agent-workforce-v1.md'
)
$missing = $required | Where-Object { -not (Test-Path $_) }
if ($missing) { throw "Missing: $($missing -join ', ')" }
if (Get-ChildItem -Recurse -File | Select-String -Pattern '\b(TBD|TODO|placeholder)\b' -CaseSensitive:$false) { throw 'Placeholder found' }
```
Expected: exit success, no missing files, no placeholders.

- [ ] **Step 7: Verify no recurring-cost automation was accidentally added**

Run:
```powershell
if (Test-Path .github\workflows) { Get-ChildItem .github\workflows -File }
```
Expected: no workflow files.

- [ ] **Step 8: Commit Task 1**

```powershell
git add README.md AGENTS.md portfolio docs
git commit -m "docs: bootstrap agent workforce authority"
```

---

### Task 2: Add the two role contracts and shared finding/Health Book contracts

**Files:**
- Create: `agents/quality-scout.md`
- Create: `agents/process-scout.md`
- Create: `contracts/FINDING_CONTRACT.md`
- Create: `templates/REPO_HEALTH_BOOK.md`

**Interfaces:**
- Consumes: `docs/WORKFORCE_POLICY.md` and portfolio membership.
- Produces: stable role ids, finding id format, output contract, and Health Book template used by scheduled tasks and repo issue creation.

- [ ] **Step 1: Define Quality Scout front matter and role contract**

Required front matter:
```yaml
---
agent_id: workforce.quality-scout.v1
display_name: Quality Scout
job_title: Engineering Quality Scout
manager_role: technical-operations-lead
authority_level: advisory-v1
---
```
Body must freeze mission, lenses, non-responsibilities, evidence standard, escalation rules, runtime outcomes, and the personality boundary: skeptical/precise/persistent without manufacturing findings.

- [ ] **Step 2: Define Process Scout front matter and role contract**

Required front matter:
```yaml
---
agent_id: workforce.process-scout.v1
display_name: Process Scout
job_title: Engineering Process Scout
manager_role: technical-operations-lead
authority_level: advisory-v1
---
```
Body must freeze mission, lenses, non-responsibilities, evidence standard, escalation rules, runtime outcomes, and the personality boundary: curious/systems-oriented/impatient with repeated manual work without automating merely because repetition exists.

- [ ] **Step 3: Define shared finding identity and lifecycle**

`contracts/FINDING_CONTRACT.md` must require:
- id format: `health:<repo-slug>:<root-cause-slug>` using lowercase kebab-case components;
- same root cause across scouts reuses the same id;
- fields from the approved spec;
- severity/confidence vocabularies from Global Constraints;
- lifecycle: `NEW | RECURRING | WORSENED | IMPROVED | RESOLVED | NO_MATERIAL_CHANGE`;
- disposition: `OBSERVE | FOLLOW_UP_RECOMMENDED | OWNER_DECISION_REQUIRED | ACCEPTED_RISK | RESOLVED`;
- recurrence changes only on materially new confirming evidence.

- [ ] **Step 4: Define Health Book issue/comment templates**

`templates/REPO_HEALTH_BOOK.md` must include:
- exact issue title: `[OPS][HEALTH] Repo Health Book — continuous quality & process evidence`;
- issue purpose and rules;
- Initial Baseline comment template including `Scout`, `Observed at`, repo state, activity level, quality mechanisms, process mechanisms, strengths, deviations, unknowns, observation focus;
- Finding Delta template with `Finding ID`, lifecycle, evidence, severity, confidence, recurrence, suggested action/owner, disposition;
- explicit rule that `SKIP_NO_DELTA` and unchanged `NO_MATERIAL_CHANGE` create no comment.

- [ ] **Step 5: Validate role ids, finding vocabulary and anti-noise text**

Run:
```powershell
python -c "from pathlib import Path; q=Path('agents/quality-scout.md').read_text(); p=Path('agents/process-scout.md').read_text(); f=Path('contracts/FINDING_CONTRACT.md').read_text(); h=Path('templates/REPO_HEALTH_BOOK.md').read_text(); assert 'workforce.quality-scout.v1' in q; assert 'workforce.process-scout.v1' in p; assert 'health:<repo-slug>:<root-cause-slug>' in f; assert all(x in f for x in ['INFO','LOW','MEDIUM','HIGH','CRITICAL']); assert 'SKIP_NO_DELTA' in h; assert 'no comment' in h.lower()"
```
Expected: exit 0.

- [ ] **Step 6: Commit Task 2**

```powershell
git add agents contracts templates
git commit -m "docs: define scout role and evidence contracts"
```

---

### Task 3: Review and merge the canonical workforce bootstrap

**Files:**
- Review only; no new required files unless review finds an in-scope defect.

**Interfaces:**
- Consumes: Tasks 1–2 branch.
- Produces: merged canonical `main` before any monitored repo links to it.

- [ ] **Step 1: Run local closeout checks**

Run:
```powershell
git diff main...HEAD --check
git status --short
```
Expected: no whitespace errors; working tree clean.

- [ ] **Step 2: Inspect the complete diff against the approved design**

Run:
```powershell
git diff --stat main...HEAD
git diff main...HEAD
```
Check specifically: no runtime state, no workflow YAML, no extra repos, no autonomous mutation authority, no NotebookLM authority drift.

- [ ] **Step 3: Push only the feature branch and open a PR**

```powershell
git push -u origin workforce/v1-bootstrap
gh pr create --base main --head workforce/v1-bootstrap --title "docs: bootstrap Agent Workforce V1" --body "Implements the approved Agent Workforce V1 design: canonical workforce policy, two role contracts, shared finding contract, Health Book template, portfolio membership, and NotebookLM derived-surface guidance. No runtime database, hosted Actions, autonomous code repair, or Hermes migration."
```

- [ ] **Step 4: Perform one whole-branch review**

Review focus: authority ambiguity, duplicate state, hidden recurring cost, missing fail-closed outcome, identity/schema inconsistency.
Expected: either PASS or focused repair on same branch followed by re-validation.

- [ ] **Step 5: Merge only after review passes**

Use GitHub/`gh` normal merge path; no bypass and no force operations.

- [ ] **Step 6: Verify live `main`**

Confirm the merged commit is the current `main` head and all required files are fetchable through GitHub.

---

### Task 4: Create or reconcile one Repo Health Book per monitored repository

**Files:**
- No repository file changes.
- GitHub issues in five existing repos.

**Interfaces:**
- Consumes: merged `templates/REPO_HEALTH_BOOK.md` on `agent-workforce/main`.
- Produces: exactly one canonical open Health Book issue per monitored repo.

Repositories:
1. `jannekbuengener/sample-brain`
2. `jannekbuengener/sample-brain-analysis`
3. `jannekbuengener/arvp`
4. `jannekbuengener/traum_taenzer`
5. `jannekbuengener/Claire_de_Binare`

- [ ] **Step 1: Search each repo for an existing Health Book before creating one**

Search title terms `Repo Health Book` and `[OPS][HEALTH]` in open and closed issues.
Expected: reuse an existing canonical issue if semantically equivalent; do not create duplicates.

- [ ] **Step 2: Create missing Health Books with the canonical template**

Use the exact title from Task 2. The issue body must link to:
- `agent-workforce/README.md`
- `agents/quality-scout.md`
- `agents/process-scout.md`
- `contracts/FINDING_CONTRACT.md`
- `templates/REPO_HEALTH_BOOK.md`

Do not add an Initial Baseline yet; first scout visit owns that comment.

- [ ] **Step 3: Verify exactly one canonical open Health Book per repo**

Search each repo again. If a historical duplicate exists, do not delete it; mark or close only after confirming which issue is canonical and linking the successor.

- [ ] **Step 4: Record the five issue URLs in `agent-workforce/portfolio/REPOSITORIES.md`**

Create a branch in `agent-workforce`, add only the Health Book URLs to the corresponding repo rows, validate, PR, review, and merge.

---

### Task 5: Create the two scheduled ChatGPT scout tasks

**Files:**
- No repo file changes unless a prompt defect is found and the role contract must be repaired through normal PR flow.

**Interfaces:**
- Consumes: merged role contracts, portfolio membership, and five live Health Books.
- Produces: two enabled recurring ChatGPT tasks.

**Schedule:**
- Quality Scout: Monday + Thursday morning, flexible schedule, approximately 09:00 local time.
- Process Scout: Tuesday + Friday morning, flexible schedule, approximately 09:00 local time.

- [ ] **Step 1: Create Quality Scout task**

Task title: `Quality Scout`

Prompt contract:
```text
Act as the Quality Scout defined by the live canonical role contract at jannekbuengener/agent-workforce/agents/quality-scout.md. Fetch the live workforce policy, finding contract, portfolio membership, and Repo Health Book template before acting. Use GitHub live state; never infer current repo state from memory.

Shallow-preflight every in-scope repo, then select exactly one repo for deep inspection using the canonical priority order: missing Quality Scout baseline; due unresolved HIGH/CRITICAL finding; meaningful new commit/PR/issue/CI activity since the last material scout observation; otherwise longest without inspection. Ignore generic bot noise and the scouts' own Health Book comments as activity triggers.

Deep-inspect only the selected repo for correctness/regression risk, test quality, CI/check drift, dependency/security/repository hygiene, architecture/ownership drift, documentation/canon drift, repeated defects/review findings, and stale/misleading technical surfaces. Apply repo-local authority before generic engineering assumptions.

Before writing, read the repo's canonical Health Book and deduplicate by root cause and stable finding id. If this is the scout's first visit, append an INITIAL BASELINE. Otherwise append only a material NEW/RECURRING/WORSENED/IMPROVED/RESOLVED delta. SKIP_NO_DELTA and unchanged NO_MATERIAL_CHANGE produce no GitHub comment. Do not create follow-up issues, code changes, PRs, governance changes, or new agents. If access/tool/authority is blocked, classify the blocked outcome separately from repo quality.

Return a compact run receipt naming selected repo, outcome, and any finding ids touched. Notify Jannek only for material findings, blocked runs, or initial baseline completion.
```

- [ ] **Step 2: Create Process Scout task**

Task title: `Process Scout`

Prompt uses the same selection/dedup/noise rules but fetches `agents/process-scout.md` and deep-inspects for repeated manual work, repeated agent tasks, recurring handoffs, duplicated effort, decision bottlenecks, missing ownership/context, deterministic-automation candidates, and recurring task clusters that may justify future roles. It may recommend follow-up work but must not create it.

- [ ] **Step 3: Verify task definitions**

Use private automation inspection to confirm both tasks are enabled, schedules are non-overlapping as specified, and prompts reference the canonical workforce repo rather than chat memory.

- [ ] **Step 4: Verify no extra scheduling state was created in Git**

Confirm `agent-workforce` contains no `last_run`, scheduler database, mutable task ledger, or generated execution history.

---

### Task 6: Execute two canary baseline runs before trusting the recurring loop

**Files:**
- GitHub Health Book comments only.

**Interfaces:**
- Consumes: final role contracts + Health Books.
- Produces: one Quality baseline and one Process baseline for review before the scheduled system accumulates more evidence.

- [ ] **Step 1: Run Quality Scout canary on `sample-brain`**

Use live GitHub/repo evidence. Append exactly one Initial Baseline comment to the `sample-brain` Health Book, with any concrete findings deduplicated under stable finding ids.

- [ ] **Step 2: Validate Quality canary output**

Check:
- evidence supports every deviation;
- repo-local canon was consulted;
- no finding was manufactured to fill categories;
- infrastructure/tool state is not mislabeled as repo defect;
- no implementation issue/PR was created.

- [ ] **Step 3: Run Process Scout canary on `sample-brain-analysis`**

Append exactly one Initial Baseline comment to that repo's Health Book, focused on process/work-pattern evidence rather than code quality duplication.

- [ ] **Step 4: Validate Process canary output**

Check:
- repeated work claims have actual evidence;
- deterministic automation is preferred before proposing an agent role;
- no department/manager is invented from one observation;
- no duplicated Quality finding identity exists for the same root cause.

- [ ] **Step 5: Repair role contracts only if canaries expose a real failure mode**

If either canary is noisy, ambiguous, or overreaches, update only the responsible role/policy/contract via branch + PR. Do not compensate by adding a new subsystem.

---

### Task 7: Begin the controlled ten-baseline evidence round and close implementation

**Files:**
- No required new files.
- Health Book comments accumulate through normal scout runs.

**Interfaces:**
- Consumes: two validated canaries and enabled schedules.
- Produces: operational V1 with a measurable completion condition.

- [ ] **Step 1: Treat the canaries as baseline run 1/5 for their respective scouts**

Do not re-run them just to satisfy a counter.

- [ ] **Step 2: Let scheduled selection prioritize the remaining missing scout/repo baselines**

Quality Scout must eventually baseline the remaining four repos; Process Scout must eventually baseline the remaining four repos. Do not manually accelerate unless there is a concrete reason.

- [ ] **Step 3: After all ten baseline combinations exist, review V1 evidence quality**

Evaluate false positives, duplicate findings, noise, blocked-access frequency, and whether activity-based selection behaved fairly.

- [ ] **Step 4: Record V1 closeout in `agent-workforce`**

Add a short reviewed closeout section to `README.md` or a single `docs/V1_CLOSEOUT.md` only if there is real evidence worth preserving. Do not create a KPI dashboard.

- [ ] **Step 5: Do not promote authority automatically**

Repo Manager, specialist agents, event-driven triggers, plugins, Hermes, mutable runtime state, or automatic follow-up issue creation require separate evidence-backed design decisions.

---

## Self-Review Result

- **Spec coverage:** all 19 design sections map to Tasks 1–7; no spec requirement intentionally omitted.
- **Step scan:** setup is folded into the deliverable that needs it; no task introduces an unrelated subsystem.
- **Type/identity consistency:** role ids are `workforce.quality-scout.v1` and `workforce.process-scout.v1`; finding ids are `health:<repo-slug>:<root-cause-slug>`; vocabularies match the approved design.
- **Review Focus coverage:** duplicate issue handling is Task 4; private-access failure is Tasks 5–6; bot/self-loop prevention is Tasks 2 and 5; no-delta silence is Tasks 2 and 5; root-cause dedup is Tasks 2, 4, 5, and 6.
- **Proportion:** implementation is documentation/issue/task orchestration rather than product code, so verification uses live GitHub checks and deterministic content checks instead of adding a test framework or CI merely for the plan.

## Intended Completion State

`AGENT_WORKFORCE_V1_OPERATIONAL` means:
- `agent-workforce` exists privately and its V1 bootstrap is merged;
- two role contracts and shared evidence contracts are canonical;
- five repos each have one canonical open Health Book;
- two scheduled scout tasks are enabled;
- two canaries passed review;
- the remaining baseline round is progressing through scheduled runs without duplicate/noise behavior.

`AGENT_WORKFORCE_V1_BASELINED` is a later operational milestone reached only after both scouts have completed one baseline for all five repos and that evidence has been reviewed for quality.
