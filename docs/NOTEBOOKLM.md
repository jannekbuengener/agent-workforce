# NotebookLM Knowledge Surface

NotebookLM is an optional derived knowledge surface for Jannek and compatible agent hosts. It is useful for reading, querying, summarizing, and navigating workforce documentation. It is not a source of truth.

## Authority

- Git/GitHub remains canonical for role contracts, workforce policy, portfolio membership, and versioned employee documentation.
- Repo Health Books remain canonical repo-local evidence in their owning repositories.
- NotebookLM consumes canonical sources by direct GitHub link where practical, or by explicitly dated uploaded snapshots when a static copy is more useful.
- Notes or edits created in NotebookLM are proposals until written back through normal repo governance.
- NotebookLM availability is never a V1 execution dependency or blocker.

## V1 source set

After bootstrap, useful NotebookLM sources are:

- `README.md`
- `agents/quality-scout.md`
- `agents/process-scout.md`
- `docs/WORKFORCE_POLICY.md`
- `contracts/FINDING_CONTRACT.md`
- `portfolio/REPOSITORIES.md`

Later, evidence-backed employee-development notes or management maps may be added as canonical repo documents and linked from NotebookLM.

## Explicit non-goals

V1 has no NotebookLM sync service, importer, write-back automation, or runtime dependency. The NotebookLM MCP may be used by an execution host that already has it configured, but no worker may require private MCP access to perform its job.
