# TASK 3 - Pre-Implementation Forensic Audit

**Audit date:** 2026-11-21

## 1. Current project status

- The repository is not currently a Git repository (`git status` reports that `.git` is absent).
- DVC is not installed or not available on `PATH`; `dvc version` could not run.
- The independent source directory `C:\Users\Asus\Desktop\data-dl` exists and contains the Kaggle ZIP and four O*NET CSV files.
- The source directory and files were only read; no source artifact was modified.
- The project already contains ingestion, validation, preprocessing, alignment, pipeline, report, and test modules.
- A prior implementation has already produced Task 2-style interim and report artifacts.

## 2. Verified source datasets

| Source | Verified dimensions/schema | Hash |
|---|---|---|
| Kaggle ZIP `archive (4).zip` | ZIP member `Resume/Resume.csv`; extracted CSV 2,484 rows x 4 columns; columns `ID`, `Resume_str`, `Resume_html`, `Category`; 24 categories; no missing values; 0 duplicate IDs; 0 exact duplicate rows | `B12C4AB34DF707AD2CC64312C016509CAD9B6C93B0BAED7A6A2C7CBD6B2B7AA4` (ZIP) |
| O*NET `occupation_data.csv` | 1,016 x 3; `O*NET-SOC Code`, `Title`, `Description`; 0 missing cells; 0 exact duplicate rows | `A09EAE1D6609686E44E05B7290993A1C8B523D8CA224BC0EEDC194C855C3EE02` |
| O*NET `software_skills.csv` | 31,821 x 7; 7 expected columns; 0 missing cells; 0 exact duplicate rows | `6AABB96B464288DB849580E6510530EFFF3F80E25DDE2BB23F1FC36BB526B016` |
| O*NET `essential_skills.csv` | 18,200 x 15; 15 expected columns; 9,100 missing cells; 0 exact duplicate rows | `68C4D31D8C55077238395DCA40CC4E6D32E6A608B5474BB8264B1F98AE415BD7` |
| O*NET `task_statements.csv` | 18,838 x 8; 8 expected columns; 1,005 missing cells; 0 exact duplicate rows | `4568E14D8DB6F05551AD37E056E909B13EBAE4A26BCB5FF915BB5F281D582C57` |

O*NET source records total 69,875 rows across the four files.

## 3. Existing components

- `src/ingestion/ingest_kaggle.py`: reads the raw Kaggle CSV and writes a Kaggle interim copy.
- `src/ingestion/ingest_onet.py`: validates and reports the four O*NET files.
- `src/ingestion/validate_onet.py`: O*NET consistency checks.
- `src/ingestion/prepare_onet.py`: prepares O*NET interim CSVs.
- `src/preprocessing/text_preprocessing.py`: Kaggle text and O*NET structured preprocessing.
- `src/alignment/occupation_alignment.py`: exploratory category-to-occupation similarity alignment.
- `src/validation/data_quality.py`: structured quality validation.
- `src/pipeline/run_pipeline.py`: stage orchestrator.
- `src/fusion/fusion_study.py`: existing fusion literature/proposal support.
- `tests/test_data_quality.py`: limited unit tests for Kaggle and O*NET validation.
- `dvc.yaml`: stage-oriented draft, but DVC was not installed and stage orchestration requires repair.
- `.github/workflows/ci.yml`: CI draft runs pytest and invokes synthetic mode.
- `Makefile`: pipeline and quick-pipeline fallback exists.

## 4. Data integrity findings

- The current production raw files are small synthetic fixtures, not the real datasets:
  - Kaggle raw: 325 bytes, SHA-256 `D8242DD0A28704F5BEA8320A8C5FFCD9ED01FC12E364B982F98D83C0A885F52C`
  - O*NET occupation: 159 bytes
  - O*NET software: 227 bytes
  - O*NET essential: 207 bytes
  - O*NET task: 223 bytes
- `ensure_synthetic_data_if_needed()` in `src/pipeline/run_pipeline.py` writes synthetic CSV records directly into `data/raw`.
- `--synthetic` forces this behavior with `force=True`.
- The CI workflow currently invokes `--synthetic`, making it capable of producing synthetic production data.
- The Makefile quick-pipeline fallback invokes synthetic mode.
- The existing draft DVC stages do not fully enforce the safe ingestion and reporting requirements.
- Several required fixtures, unit/integration folders, structured logging/report consolidation, Git metadata, and DVC remote setup are not complete.

## 5. Missing requirements

- A real `TASK3_PRE_IMPLEMENTATION_AUDIT.md` did not previously exist; older audit/report files are present but do not replace this pre-change audit.
- No real Kaggle/O*NET recovery report.
- No initialized Git repository or `task3` tag.
- No operating DVC installation, local remote, or verified `dvc repro`.
- Synthetic fixtures are not organized in `tests/fixtures/`.
- Test coverage is limited and does not cover all Kaggle/O*NET/cross-modal requirements.
- Centralized pipeline observability and consolidated quality/pipeline reports are incomplete.
- The README describes synthetic quick mode and does not fully document verified recovery and DVC usage.
- PDF report and demo script are not verified deliverables.

## 6. Potential destructive operations

Do not execute:

- `python -m src.pipeline.run_pipeline --synthetic`
- `make quick-pipeline`
- Any old ingestion or fixture code that calls `to_csv()` under `data/raw/`
- Any `force=True` raw-dataset overwrite path

The source directory `C:\Users\Asus\Desktop\data-dl` must remain read-only. Existing synthetic raw files must be backed up before replacement and the source CSV bytes must be copied, not transformed or overwritten.

## 7. Implementation plan

1. Back up each synthetic raw file and record its path and hash.
2. Inspect and validate the Kaggle ZIP entry and all O*NET source CSVs.
3. Copy real files byte-for-byte into `data/raw/` only after validation.
4. Remove destructive synthetic raw-data generation from normal pipeline code and reroute fixture behavior exclusively to `tests/fixtures/`.
5. Repair configuration, modular validation, preprocessing, alignment, logging, reports, and critical-failure behavior.
6. Add passing and deliberately failing fixture-based tests.
7. Add DVC, initialize a local repository/remote, and repair `dvc.yaml`.
8. Repair CI so production raw data is never synthesized or downloaded in unit tests.
9. Update documentation, literature/fusion reports, data card, and the implementation report.
10. Verify datasets, pipeline, tests, DVC, Git, tag, and PDF deliverables and document actual evidence.

## 8. No-go conditions

Proceed to recovery is conditioned on:

- The independent source directory remaining available.
- Kaggle CSV dimensions and schema matching the assignment.
- O*NET dimensions and schemas matching the assignment.
- Hashes and source bytes remaining unchanged.
- Any destination replacement being preceded by a backup and hash record.
