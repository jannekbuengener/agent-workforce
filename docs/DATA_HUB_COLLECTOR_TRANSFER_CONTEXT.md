# Data Hub — Collector-Transfer- und Scout-Kontext

## Zweck

Dieses Dokument hält den cross-repository Kontext zwischen Agent Workforce, dem AWH History Backfill Collector, Security Business und `jannekbuengener/data-hub` fest.

Es ist **kein** Data-Hub-Produktkanon. Produktwahrheit bleibt im Ziel-Repository `jannekbuengener/data-hub`. Dieses Dokument existiert, damit Workforce-Routing und Scouts den aktuellen Zusammenhang nicht aus Chat-Historie rekonstruieren müssen.

## Aktueller Stand

### Data Hub

`jannekbuengener/data-hub` ist ein eigenständiges Produkt-Repository im Incubator-Status.

Produktziel in Kurzform:

`eigene Daten -> Evidence -> Tendenzen -> Potenzial -> bessere nächste Entscheidung`

Der erste Produktfokus liegt auf user-owned / first-party Daten, zunächst insbesondere:

- LinkedIn;
- Meta / Instagram;
- Meta / Facebook;
- CSV / JSON als Fallback-Import.

Data Hub ist **nicht** primär ein rückwärtsgewandtes "Außenwirkungs-Dashboard". Der Kern ist, aus eigenen historischen Content- und Performance-Daten belastbare Tendenzen, Potenzial, Warnungen und spätere Handlungsempfehlungen abzuleiten, bevor die nächste Entscheidung oder Veröffentlichung erfolgt.

Produktkanon und aktuelle Details liegen im Data-Hub-Repository, insbesondere:

- `README.md`;
- `docs/PRODUCT_VISION.md`;
- `docs/CURRENT_STATE_AND_TRANSFER.md`;
- `docs/ARCHITECTURE_DIRECTION.md`;
- `docs/ANALYSIS_LIFECYCLE.md`;
- `docs/MVP_V1.md`.

### Aktueller Collector-Proving-Ground

Der heute existierende Collector-Proving-Ground liegt **noch in `jannekbuengener/agent-workforce`** als AWH History Backfill Collector unter:

`tools/history_collector/`

Sein ursprünglicher Auftrag ist die vollständige, neutrale historische Erfassung von GitHub-/Workforce-Evidence. Er trennt Sammlung bewusst von Interpretation und Analyse.

Die aktuelle AWH-Architektur ist lokal und deterministisch:

`Claude Code lokal -> Python Collector -> GitHub API -> LocalStore`

Der AWH-Collector ist **nicht** bereits der Data-Hub-Collector und darf nicht als solcher behandelt werden.

### Geplanter Transfer

Der Produktisierungspfad ist bewusst zweistufig:

1. AWH beweist robuste Collector-Mechaniken im realen History-Backfill-Szenario.
2. Erst danach werden nachweislich generische Mechaniken isoliert und in `data-hub` übertragen.

Der geparkte Transfer ist derzeit in `jannekbuengener/security-business#32` dokumentiert.

Erwartbar generische Kandidaten sind unter anderem:

- sichere read-only Source-Zugriffe;
- Pagination;
- Retry / Rate-Limit-Behandlung;
- resumierbare Sammlung / Ledger-Prinzipien;
- deterministische Normalisierung;
- Source Identity / Provenance;
- Duplicate-/Conflict-Behandlung;
- lokale Persistenz- und Verifikationsmuster.

Nicht automatisch generisch sind AWH-spezifische Semantiken wie:

- Scout-Cutover;
- GitHub Issue/PR-Nummernraum;
- Actions-Preservation;
- GitHub Security-Alert-Domänen;
- AWH-spezifische Completion Gates;
- Workforce-spezifische Horizon-/Backfill-Semantik.

Es gilt ausdrücklich: **kein Wholesale-Copy eines unfertigen AWH-Collectors nach Data Hub.**

## Historische, supersedete AWH-Infrastruktur

Folgende frühere AWH-Experimente sind historische Evidence und **keine Data-Hub-Vorgabe**:

- Claude Cloud als Collector-Host;
- Google Drive als Collector-Store;
- W1 / Google OAuth als notwendiger Datenpfad;
- Scheduled Claude Tasks als produktive Collector-Runtime;
- n8n als verpflichtende Collector-Runtime.

Wenn Data Hub später eine dieser Technologien auswählt, braucht es eine neue Data-Hub-spezifische Begründung. Alte AWH-Experimente erzeugen keine implizite Produktanforderung.

## Erwartete Data-Hub-Analyse-Richtung

Die langfristige Produktidee umfasst einen nativen Analyse-Workflow, grob:

`Business-Kontext -> eigene Datenquellen -> neutrale Evidence -> deterministische Strukturierung -> begrenzte Small-Model-Aufgaben -> Deep Reasoning -> Tendenzen/Potenzial/Warnungen -> Evidence Report`

Wichtig:

- AI transportiert nicht einfach Source-Bytes;
- deterministische Schritte bleiben deterministisch, wo sie besser geeignet sind;
- kleinere Modelle dürfen klar begrenzte Extraktions-/Strukturierungsaufgaben übernehmen;
- große Reasoning-Modelle dürfen dort eingesetzt werden, wo Synthese, Mustererkennung und schwierige Bewertung echten Mehrwert bringen;
- Claims und Empfehlungen müssen auf Evidence zurückführbar bleiben;
- Korrelation darf nicht als Kausalität dargestellt werden;
- fehlende oder widersprüchliche Evidence bleibt sichtbar.

## Workforce-/Scout-Bedeutung

Sobald `data-hub` im kanonischen Portfolio steht, behandeln Quality Scout und Process Scout das Repository wie jedes andere überwachte Repository:

- repo-lokale Autorität zuerst lesen;
- initiale Baseline je Scout erstellen;
- danach nur material neue Quality-/Process-Evidence als Findings schreiben;
- keine Produktentscheidung aus diesem Workforce-Dokument ableiten, wenn Data-Hub-Canon etwas anderes sagt.

Besondere Beobachtungspunkte für die ersten Baselines:

### Quality Scout

- Drift zwischen README, Product Vision, MVP, Architecture und Transferstatus;
- versehentliche Vermischung von AWH-spezifischer Logik mit generischem Data-Hub-Core;
- fehlende Evidence-/Provenance-Grenzen;
- unklare AI-vs-deterministic Verantwortung;
- privacy/credential/data-boundary drift.

### Process Scout

- wiederholte manuelle Connector-/Collector-Arbeit, die in einen generischen Core gehört;
- doppelte Implementierung zwischen AWH und Data Hub;
- wiederholte Kontextverluste zwischen Research, Produktcanon und Umsetzung;
- unnötige Agent-Arbeit, die deterministisch automatisierbar wäre;
- wiederkehrende Übergaben, die eine stabile Produkt-/Connector-Schnittstelle rechtfertigen.

## Agent Brain

`jannekbuengener/agent-brain` ist bereits Teil der Agent-Workforce-Metaebene und des überwachten Portfolios.

Seine Rolle bleibt shared context/evidence infrastructure. Es ist **keine implizite Data-Hub-Runtime-Abhängigkeit**.

Wenn Data Hub später Shared Context, provenance-aware Evidence, Memory/Retrieval oder strukturierte Ingestion aus Agent Brain nutzen soll, muss das unter Data-Hub-Produktkanon und Workforce-Capability-Routing ausdrücklich entschieden werden. Die bloße Existenz von Agent Brain ist kein Adoption-Beweis.

## Autoritätsgrenze

- Agent Workforce besitzt Workforce-/Scout-Routing und das AWH-Proving-Ground.
- `data-hub` besitzt Data-Hub-Produktwahrheit und die spätere produktseitige Collector-/Evidence-/Analysearchitektur.
- `security-business#32` hält aktuell den geparkten Transferpfad fest; dadurch erhält Security Business keine Data-Hub-Produktautorität.
- Agent Brain bleibt optionales Shared-Context/Evidence-Metatool unter eigener Autorität.
