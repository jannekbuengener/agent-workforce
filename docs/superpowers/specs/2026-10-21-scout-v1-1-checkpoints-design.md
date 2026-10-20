# Agent Workforce V1.1 — Scout Checkpoints, Finding Contract und Ausführungskette

Issue: #26

## 1. Ziel

V1.1 soll die vorhandene Workforce-Kette robuster machen, ohne neue Rollen, eine Runtime-Datenbank oder zusätzliche Scheduler-Hardcodierung einzuführen.

Der Slice löst drei konkrete Probleme:

1. stille Scout-Runs hinterlassen heute keinen dauerhaften Inspektions-Cursor;
2. der Supervisor kann bereits geprüfte Scout-Outputs erneut als neu behandeln;
3. `contracts/FINDING_CONTRACT.md` und `templates/REPO_HEALTH_BOOK.md` sind nicht vollständig deckungsgleich.

Zusätzlich wird die bereits vorhandene End-to-End-Kette an einer Stelle kompakt dokumentiert.

## 2. Nicht-Ziele

Dieser Slice führt **nicht** ein:

- neue Scouts, Manager oder Specialist-Rollen;
- höhere Produkt-/Repository-Mutation-Authority;
- neue Follow-up-Issue-Automation;
- event-driven Scheduling;
- eine Runtime-Datenbank;
- Agent Brain als Pflicht-Runtime-Abhängigkeit;
- neue Repo-spezifische Produktlogik;
- allgemeine CI-/Validator-Infrastruktur;
- Ruleset-/Branch-Protection-Änderungen;
- Änderung des aktuellen Scout-Takts.

## 3. Live-Evidence und Root Cause

### 3.1 Stille Runs und `least-recently-inspected`

Die Workforce-Policy wählt innerhalb einer Prioritätsklasse das am längsten nicht inspizierte Repository. Gleichzeitig erzeugen `SKIP_NO_DELTA` und routinemäßiges `NO_MATERIAL_CHANGE` absichtlich keinen Health-Book-Kommentar.

Damit ist aus der dauerhaften GitHub-Evidence nicht zuverlässig rekonstruierbar, dass ein Repo gerade eben inspiziert wurde. Historische Finding-/Baseline-Kommentare dürfen dafür nicht zweckentfremdet werden.

### 3.2 Supervisor-Dedup

Der Supervisor-Contract verlangt, bereits geprüfte Outputs nicht erneut zu reviewen. In der Live-Historie wurde der Finding `health:claire-de-binare:shared-base-image-security-exposure` jedoch in einem späteren Supervisor-Lauf erneut als neuer Output behandelt.

Das ist kein Scout-Qualitätsproblem, sondern ein Cursor-/State-Problem.

### 3.3 Finding-Schema-Drift

`FINDING_CONTRACT.md` fordert aktuell u. a.:

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

Das Health-Book-Template bildet nicht alle Felder im Finding-Delta ab. Zusätzlich besitzt `category` keine kontrollierte Vocabulary.

Root-Cause-/Finding-Identity-Unklarheit wird außerdem derzeit teilweise mit `BLOCKED_AUTHORITY_AMBIGUOUS` vermischt. Diese Zustände müssen semantisch getrennt werden.

## 4. Betrachtete Ansätze

### A. Mutable GitHub-Checkpoint-Kommentare — gewählt

Pro Scout und Health Book existiert genau ein stabiler Checkpoint-Kommentar, der bei jedem tatsächlichen Deep-Inspection-Run aktualisiert wird. Der Supervisor besitzt entsprechend genau einen Checkpoint in Meta-Issue #3.

Vorteile:

- GitHub bleibt dauerhafte operative Evidence-Fläche;
- stille Runs bleiben still, weil kein neuer normaler Kommentar entsteht;
- kein neues Datenbanksystem;
- Cursor ist repo-/scout-spezifisch und rekonstruierbar;
- Scheduler-Prompts bleiben unverändert.

Kosten:

- bestehende Authority muss explizit das Aktualisieren des eigenen Checkpoint-Kommentars erlauben;
- Parser/Contract müssen Checkpoint-Kommentare sicher von Baselines/Findings unterscheiden.

### B. Stateless Round-Robin

Repo-Auswahl könnte deterministisch aus Kalender-Slot und Portfolio-Position berechnet werden.

Abgelehnt, weil dies zwar Fairness verbessert, aber weder Activity-Cursor noch Supervisor-Output-Dedup zuverlässig löst.

### C. Runtime-Datenbank

Eine dedizierte State-Schicht könnte Run-/Review-Cursor vollständig verwalten.

Abgelehnt für V1.1: unnötige Betriebs-, Recovery- und Consistency-Komplexität bei sechs Repositories.

## 5. Scout-Checkpoint-Contract

### 5.1 Identität

Jeder aktive Scout besitzt pro kanonischem Repo Health Book genau einen Checkpoint-Kommentar.

Maschinenlesbarer Marker:

```text
<!-- agent-workforce:scout-checkpoint:v1 scout=workforce.quality-scout.v1 -->
```

bzw.

```text
<!-- agent-workforce:scout-checkpoint:v1 scout=workforce.process-scout.v1 -->
```

Der Marker ist die stabile Identität. Es darf pro Scout und Health Book höchstens einen aktiven Checkpoint mit diesem Marker geben.

### 5.2 Inhalt

Der Checkpoint enthält mindestens:

- `checkpoint_version: 1`
- `scout`
- `repo`
- `last_inspected_at`
- `last_repo_head`
- `last_runtime_outcome`
- `baseline_complete`
- `last_material_output_comment_id` oder `null`
- `last_material_output_at` oder `null`

Optional darf später ein expliziter Activity-Cursor ergänzt werden, falls `last_inspected_at + last_repo_head` für reale GitHub-Aktivität nicht ausreichen. V1.1 führt dafür noch keine zweite Event-Ledger-Struktur ein.

### 5.3 Update-Semantik

Bei jedem erfolgreichen Deep-Inspection-Run:

1. Scout liest den eigenen Checkpoint;
2. Scout führt die normale Inspection aus;
3. Initial Baseline oder Finding Delta wird nur nach bestehenden Evidence-Regeln geschrieben;
4. Scout aktualisiert **denselben** Checkpoint-Kommentar auf den aktuellen Lauf;
5. `NO_MATERIAL_CHANGE` und `SKIP_NO_DELTA` erzeugen weiterhin keinen neuen normalen Health-Book-Kommentar.

Der Checkpoint selbst ist operative Metadatenpflege und zählt nicht als Finding-/Baseline-Kommentar.

### 5.4 Lazy Migration

Bestehende Repositories werden nicht rückwirkend mit erfundenen historischen Cursorwerten befüllt.

Beim nächsten echten Lauf eines Scouts:

- existiert kein Checkpoint, wird genau einer mit den **aktuellen** Laufdaten angelegt;
- vorhandene Baseline-/Finding-Historie bleibt unverändert;
- `baseline_complete` wird nur dann `true`, wenn die Baseline für diesen Scout tatsächlich im Health Book nachweisbar existiert oder im aktuellen Lauf erzeugt wird.

### 5.5 Failure Mode

Kann der eigene Checkpoint nach einer Deep Inspection nicht sicher gelesen/erstellt/aktualisiert werden, darf der Run keine erfolgreiche Selection-State-Aktualisierung vortäuschen.

Neuer operativer Runtime Outcome:

`BLOCKED_CHECKPOINT_STATE_UNAVAILABLE`

Dieser Zustand ist kein Repository-Defekt.

## 6. Repo-Auswahl mit Checkpoints

Die Prioritätsklassen bleiben unverändert:

1. fehlende Baseline;
2. fälliger unresolved HIGH/CRITICAL Finding;
3. meaningful new activity;
4. periodic sweep.

Innerhalb einer Klasse wird `least-recently-inspected` aus `last_inspected_at` des passenden Scout-Checkpoints abgeleitet.

Für Repositories ohne Checkpoint gilt bis zur Lazy-Initialisierung `never inspected in checkpoint model` und damit höchste Fairness-Priorität innerhalb der passenden Klasse, ohne historische Kommentare künstlich umzuschreiben.

Meaningful activity wird gegen den letzten Scout-Checkpoint bewertet, nicht gegen den letzten beliebigen Health-Book-Kommentar.

## 7. Supervisor-Checkpoint-Contract

Meta-Issue #3 erhält genau einen stabilen Supervisor-Checkpoint-Kommentar.

Marker:

```text
<!-- agent-workforce:supervisor-checkpoint:v1 -->
```

Mindestens gespeicherte Felder:

- `checkpoint_version: 1`
- `last_supervisor_run_at`
- pro Health Book: `last_reviewed_output_comment_id`

Der Supervisor betrachtet nur Kommentare als reviewbare Scout-Outputs, die dem Baseline-/Finding-Format entsprechen. Scout-Checkpoint-Kommentare werden explizit ignoriert.

Nach erfolgreicher Review neuer Scout-Outputs wird derselbe Supervisor-Checkpoint aktualisiert.

Wenn kein neuer reviewbarer Scout-Output vorhanden ist, bleibt die bestehende Silence-Regel bestehen: kein neuer Meta-Issue-Kommentar. Der Checkpoint darf trotzdem auf den aktuellen Supervisor-Lauf aktualisiert werden, falls dies für den Review-Cursor erforderlich ist.

Kann der Review-Cursor nicht sicher gelesen oder aktualisiert werden, lautet der operative Zustand:

`BLOCKED_CHECKPOINT_STATE_UNAVAILABLE`.

## 8. Finding Contract V1.1

### 8.1 Pflichtfelder

`FINDING_CONTRACT.md` und das `FINDING DELTA`-Template müssen exakt dieselben Pflichtfelder verwenden:

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
- `lifecycle`
- `suggested_action`
- `suggested_owner`
- `disposition`

### 8.2 Category Vocabulary

V1.1 verwendet genau eine primäre Kategorie pro Finding:

- `CORRECTNESS`
- `VALIDATION`
- `CI`
- `SECURITY`
- `DEPENDENCY`
- `ARCHITECTURE`
- `OWNERSHIP`
- `DOCUMENTATION`
- `PROCESS`
- `AUTOMATION`
- `OTHER`

Die Kategorie klassifiziert den Root Cause bzw. die primäre Arbeits-/Risikoklasse, nicht den Scout. Quality und Process dürfen denselben Finding weiterhin mit derselben ID beobachten.

### 8.3 Zeitsemantik

- `first_seen` bleibt beim ersten stabilen Finding unverändert;
- `last_seen` wird nur bei materiell neuer bestätigender Evidence aktualisiert;
- `recurrence` steigt nur bei materiell neuer Evidence;
- ein stiller Checkpoint-Run verändert `first_seen`, `last_seen` oder `recurrence` nicht.

### 8.4 Finding-Identity vs Authority

`BLOCKED_AUTHORITY_AMBIGUOUS` bleibt ausschließlich für unklare Zuständigkeit/Authority.

Wenn eine materielle Abweichung beobachtet wird, aber die stabile Root-Cause-/Finding-Identität nicht sicher bestimmt werden kann, darf keine ID erfunden werden.

Neuer operativer Outcome:

`BLOCKED_FINDING_IDENTITY_AMBIGUOUS`

Dieser Outcome ist ebenfalls kein Repository-Defekt.

## 9. Authority

V1.1 erweitert keine Produkt- oder Governance-Authority.

Explizit erlaubt wird nur:

- einen eigenen Scout-Checkpoint im kanonischen Health Book erstellen/aktualisieren;
- den Supervisor-Checkpoint in Meta-Issue #3 erstellen/aktualisieren.

Nicht erlaubt bleiben insbesondere:

- Produktcode-Mutation;
- Implementierungs-PRs durch Scouts;
- automatische Follow-up-Issues;
- Secret-/Governance-Änderungen;
- Erzeugung neuer Rollen.

## 10. End-to-End Execution Flow

Der README-Frontdoor erhält einen kompakten kanonischen Überblick:

```text
Scheduler / Execution Host
        ↓
WORKFORCE_BOOTSTRAP.md
        ↓
Workforce Canon + Role/Policy Contracts
        ↓
Live Portfolio + Target Repository
        ↓
Target Repo Local Authority
        ↓
Conditional Capability / Reference Routing
        ↓
Quality Scout oder Process Scout
        ↓
Repo Health Book
  ├─ Initial Baseline / Finding Delta
  └─ mutable Scout Checkpoint
        ↓
Workforce Supervisor
        ↓
Meta Issue #3
  ├─ material supervisor review comments
  └─ mutable Supervisor Checkpoint
        ↓
Owner Escalation nur bei echtem Interventionsbedarf
```

Diese Darstellung ist Orientierung, keine zweite Detail-Spezifikation. Detailregeln bleiben in Bootstrap, Policy, Rollen, Finding Contract und Health-Book-Template.

## 11. Betroffene kanonische Flächen

Voraussichtlich:

- `README.md`
- `WORKFORCE_BOOTSTRAP.md`
- `docs/WORKFORCE_POLICY.md`
- `agents/quality-scout.md`
- `agents/process-scout.md`
- `contracts/FINDING_CONTRACT.md`
- `templates/REPO_HEALTH_BOOK.md`
- optional ein eigenes kleines Checkpoint-Contract-Dokument, falls die Implementierung sonst zu viel Semantik in Policy/Bootstrap duplizieren würde.

Scheduler-Prompts bleiben unverändert und bootstrappen weiterhin ausschließlich aus live `main`.

## 12. Validation / Golden Cases

Der Implementierungsslice muss mindestens diese Fälle durchspielen:

1. **Missing baseline** — neuer Portfolio-Eintrag ohne Scout-Checkpoint wird korrekt priorisiert.
2. **Silent run** — `NO_MATERIAL_CHANGE` erzeugt keinen neuen Evidence-Kommentar, aktualisiert aber den existierenden Scout-Checkpoint.
3. **No-delta run** — `SKIP_NO_DELTA` erzeugt keinen neuen Evidence-Kommentar und erhält korrekten Inspection-Cursor.
4. **Material finding** — Finding Delta und Checkpoint werden getrennt aktualisiert; Finding-Zeitsemantik bleibt korrekt.
5. **Supervisor dedup** — ein bereits reviewter Finding-Kommentar wird im Folgelauf nicht erneut als neu behandelt.
6. **Checkpoint filtering** — Scout-/Supervisor-Checkpoint-Kommentare werden niemals als Baseline/Finding interpretiert.
7. **Finding schema** — Template und Contract besitzen exakt dieselben Pflichtfelder und erlaubten Kategorien.
8. **Identity ambiguity** — Finding-Identity-Unklarheit erzeugt keine erfundene ID und wird nicht als Authority-Ambiguität bezeichnet.
9. **Authority** — Checkpoint-Mutation gewährt keine weitere Repo-/Produkt-Write-Authority.
10. **Execution flow** — README-Übersicht verweist auf bestehende Canon-Flächen statt Regeln zu duplizieren.

## 13. Exit-Kriterien

Der Design-Slice ist implementierungsbereit, wenn:

- Checkpoint-Identität und Felder eindeutig sind;
- Lazy-Migration ohne historische Erfindung definiert ist;
- Selection- und Supervisor-Dedup-Semantik deterministisch aus GitHub-State rekonstruierbar sind;
- Finding Contract und Template ein gemeinsames Schema besitzen;
- neue Runtime-Outcomes klar von Repository-Findings getrennt sind;
- End-to-End-Kette kompakt dokumentiert werden kann, ohne eine zweite Source of Truth zu erzeugen;
- Scope weiterhin ohne neue Datenbank, Rollen oder Scheduler-Duplikation auskommt.
