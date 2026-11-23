# GitHub and DVC Publication Report

**Date:** 2026-11-23

## GitHub

- Repository: [hxmz1/DL_Project](https://github.com/hxmz1/DL_Project)
- Visibility: private
- Published branch: `main`
- Initial sanitized snapshot commit: `c25ce92d63304ed2dd68456d8811f433dd49772d`
- The publication uses a fresh Git history so the original local history was not rewritten.
- Raw Kaggle/O*NET inputs and 2,484 resume PDFs were excluded. DVC pointer files remain.
- The original local `task3` tag was not moved or pushed.

## GitHub Actions

- Workflow: [ci.yml](../.github/workflows/ci.yml)
- Run: [CI run 45277559205](https://github.com/hxmz1/DL_Project/actions/runs/45277559205)
- Result: **PASS** on the initial published snapshot.
- Unit tests, Ruff, fixture validation, and the fixture-only pipeline all passed.

## Local validation

- pytest: 21 passed, using an external temporary pytest directory.
- Ruff: passed with the workflow command `ruff check src tests --ignore LOG015,TRY004`.
- Fixture pipeline: passed (`train=5`, `validation=4`, `test=1`).
- Full local `dvc repro`: completed with all stages already up to date.
- Local `dvc push`: completed; the configured local remote was already up to date.

## DVC remote status

- The source workspace has only a machine-local `dvc-storage` remote.
- Its local `.dvc/config` and data store were not published.
- No shared DVC remote is configured; no external DVC data push or pull was performed.
- A Google Drive folder ID and OAuth authorization are still needed to configure a shared remote.

## Remaining work

Configure and verify a shared DVC remote before expecting a new clone to retrieve the real datasets. Do not add OAuth credentials to Git.
