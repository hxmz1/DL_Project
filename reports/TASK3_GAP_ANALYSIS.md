# TASK 3 Gap Analysis

**Correction status:** This gap analysis now records original gaps and their post-correction status.

## Corrected gaps

- G1/G6: DVC stages are now independent and `dvc repro` passes locally.
- G3: candidate splitting and leakage tests are implemented.
- G4: the official `[1]`-`[10]` bibliography and reference column were added.
- G7: schema/type/range and split tests were added.
- G10: concrete text encoder, O*NET retrieval and modality-balancing specifications were added.

## Critical gaps

### G1 - CI does not execute the pipeline

**Evidence:** `.github/workflows/ci.yml` runs pytest and Ruff only. It does not run `dvc repro` or `make pipeline`.

**Impact:** The CI criterion cannot receive full credit even though a workflow file exists.

**Required fix:** In CI, use fixture or reduced real data stages and execute `dvc repro` or a safe Makefile target. Verify DVC/pytest exit codes and upload logs.

### G2 - External DVC remote not operational

**Evidence:** `.dvc/config` sets `../dvc-storage`; no external remote is configured. `dvc status` is up to date; no pull or external push was verified.

**Impact:** Another user cannot currently retrieve all data from an external service.

**Required fix:** Configure and test a credential-scoped remote (S3/Google Drive/shared storage), execute push/pull, and document exact retrieval commands.

### G3 - Data splitting and leakage prevention missing

**Evidence:** `configs/params.yaml` defines 70/15/15 ratios, but no Python split function or leakage tests exist. Searches found no `train_test_split`, split module or stratified group split implementation.

**Impact:** The assignment's leakage criterion is not satisfied operationally.

**Required fix:** Implement candidate-ID split, duplicate-CV test and a stratified test. Export split assignments only after verified ID separation.

### G4 - Official literature references missing

**Evidence:** `TASK3_REPORT.md` section 13 does not cite `[1]`-`[10]`; it states that bibliography entries should be inserted later.

**Impact:** The comparative table and report lose substantial academic rigor and points.

**Required fix:** Add a real numbered bibliography using the official assignment references and use citations in the comparative table and report.

### G5 - GitHub Actions execution not proven

**Evidence:** Workflow exists, but no GitHub run, job URL or action log was available in the project.

**Impact:** Workflow status is configuration-only.

**Required fix:** Push explicitly only with authorization, trigger CI, and record a successful Actions run.

## High gaps

### G6 - Stage orchestration duplicates pipeline work

**Evidence:** DVC validation/preprocessing/alignment stages execute `src.pipeline.run_pipeline --quick`, which itself reruns ingestion and other stages.

**Impact:** DVC stage isolation is weaker, dependencies are coarse and incremental execution is less precise.

**Required fix:** Move stage commands to dedicated modules/functions with minimal inputs and outputs and one final pipeline wrapper.

### G7 - Quality tests incomplete

Missing:

- Complete Kaggle dtype assertions.
- Complete O*NET per-file dtype and schema matrix.
- Outlier tests.
- Production-style threshold tests.
- Cross-modal/candidate-level limitation test.
- Real split leakage tests.

### G8 - Observability incomplete

There are logs and reports, but no consistent machine-readable stage record containing start/end time, input/output paths, row/column counts, missing/duplicate rates, rejected rows, warnings/errors and status.

### G9 - Training/evaluation package absent

No `src/training/` or `src/evaluation/` exists. The assignment makes these future extensions rather than mandatory, but page 2 asks to anticipate them.

**Required fix:** Add extension interfaces or package placeholders plus experiment-tracking configuration, not fabricated metrics.

### G10 - Encoder and modality-imbalance details weak

The architecture report does not choose a concrete pretrained text encoder or frozen/fine-tuned policy. It does not define modality weighting or modality-dropout beyond a textual missing fallback.

## Medium gaps

- The `.gitignore` and DVC `.dvcignore` configuration is duplicated and should be simplified.
- DVC pipeline commands do not use the central YAML configuration consistently.
- `TASK3_FINAL_VALIDATION_REPORT.md` now reports 21 tests and 15 PDF pages and remains to be committed.
- PDF tools and references need stronger academic formatting.
- `TASK3_IMPLEMENTATION_REPORT.md` and JSON reports should be regenerated from a common machine-readable execution record.
- ReportLab PDF is 15 pages and contains the corrected bibliography.

## Low gaps

- Add Docker/HTML report bonus only if time permits.
- Add drift detection and scheduled collection only if required by the project.
- Record an actual 5-10 minute demo, if deliverable requirements demand evidence rather than a script.
