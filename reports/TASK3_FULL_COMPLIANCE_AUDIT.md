# TASK 3 Full Compliance Audit

**Audit scope:** read-only inspection of `C:\Users\Asus\Desktop\DL_Project` against `C:\Users\Asus\Desktop\5eme ING\DL\Tâche3.pdf`.

**Official assignment:** 6 pages; `Tâche3.pdf`.

**Overall verdict:** **MOSTLY COMPLIANT**.

**Estimated grade after corrections:** **17.2 / 20** (see `TASK3_ESTIMATED_GRADING.md`).

## Executive findings

The project is substantially improved from a synthetic-fixture implementation. Real Kaggle and O*NET raw data are present, the old synthetic raw-generation function has been removed, DVC is initialized with a local remote, and the pipeline reports and alignment limitations are generally technically honest. The most important remaining gaps are:

1. GitHub Actions execution and external DVC remote access are not yet observed.
2. Corrected reports and source changes are not yet committed.
3. The existing `task3` tag points to the pre-correction commit.
4. No training/evaluation prototype or recorded demonstration is required for the mandatory report, but neither is present.

## Phase A - Structure and modularity

| Requirement ID | Official reference | Expected behavior | Evidence found | Status |
|---|---|---|---|---|
| A.1 | A.1 page 1 | Modular, reusable pipeline stages | Separate ingestion, validation, preprocessing, alignment and pipeline modules exist | PASS |
| A.2 | A.2 page 2 | Clear project structure | Required directories and `.github/workflows/ci.yml`, `dvc.yaml`, README and requirements exist | PASS |
| A.3 | A.2 page 2 | Central YAML configuration | `configs/params.yaml`, `src/common/config.py` | PASS |
| A.4 | A.2 page 2 | Refactored Task 2 scripts | Existing Task 2 ingestion scripts remain and are called/adapted | PASS |
| A.5 | A.2 page 2 | No hardcoded data paths/thresholds | The pipeline uses config for quality and paths, but ingestion modules derive hardcoded raw/interim/report paths from `__file__`; thresholds are mostly configured | PARTIAL |

Exact responsibilities:

- `src/pipeline/run_pipeline.py:main()` orchestrates five stage groups and refuses `--synthetic`.
- `src/ingestion/ingest_kaggle.py:main()` reads raw Kaggle CSV and writes only interim Kaggle CSV/report/log.
- `src/ingestion/ingest_onet.py:main()` validates and reports four O*NET raw files.
- `src/ingestion/validate_onet.py:main()` validates cross-file SOC consistency.
- `src/ingestion/prepare_onet.py:prepare_file()` writes trimmed/interim O*NET CSV copies.
- `src/preprocessing/text_preprocessing.py` writes processed text and structured summaries.
- `src/alignment/occupation_alignment.py` writes exploratory JSON/Markdown reports.
- `src/validation/data_quality.py` validates schemas and quality.

## Phase B - Data integrity and ingestion

Read-only measurements confirmed:

| Dataset | Actual dimensions | Missing cells | Exact duplicate rows | SHA-256 |
|---|---:|---:|---:|---|
| Kaggle | 2,484 x 4 | 0 | 0 | `816a7cd985a9a41e3ce8d1e83cb7e1beb1e854a89c1cf1fd0d75494faaa0559d` |
| occupation_data.csv | 1,016 x 3 | 0 | 0 | `a09eae1d6609686e44e05b7290993a1c8b523d8ca224bc0eedc194c855c3ee02` |
| software_skills.csv | 31,821 x 7 | 0 | 0 | `6aabb96b464288db849580e6510530efff3f80e25dde2bb23f1fc36bb526b016` |
| essential_skills.csv | 18,200 x 15 | 9,100 | 0 | `68c4d31d8c55077238395dca40cc4e6d32e6a608b5474bbe8264b1f98ae415bd7` |
| task_statements.csv | 18,838 x 8 | 1,005 | 0 | `4568e14d8db6f05551ad37e056e909b13ebaef7ea26bcb5ff915bb5f281d582c57` |

The Kaggle schema is correct and 24 categories were observed. One resume text is blank. Kaggle duplicate IDs are 0.

Code inspection found no remaining synthetic raw-file generator. `run_pipeline.py` suppresses `--synthetic` and rejects it. Synthetic files are under `tests/fixtures/`. Raw/interim/processed writes are explicit and do not overwrite raw source files. The DVC `.gitignore` patterns exclude raw/intermediate/processed data from Git, and DVC metadata is tracked.

| Requirement ID | Status | Explanation |
|---|---|---|
| B.1 real datasets | PASS | Raw dimensions and hashes match the supplied expectations |
| B.2 source provenance | PASS | Recovery report records source/destination and hashes |
| B.3 O*NET consistency | PASS | SOC reference and title checks report 0 unknown references/mismatches |
| B.4 synthetic isolation | PASS | No synthetic raw generator remains |
| B.5 missing raw-file behavior | PASS | Pipeline explicitly exits if raw files are missing |

## Phase C - DataOps principles

| Principle | Evidence | Status |
|---|---|---|
| Automation | `dvc.yaml`, Makefile and pipeline entry point exist; critical validation stop is implemented | PARTIAL |
| Modularity | Independent modules and explicit stage functions exist | PASS |
| Reproducibility | Seed 42 and YAML parameters exist; DVC lock/status are present | PARTIAL |
| Versioning | Git initialized, DVC initialized, raw .dvc outputs and local remote configured | PARTIAL |
| Continuous quality | pytest and critical status checks exist | PARTIAL |
| Observability | Log files and JSON/Markdown reports exist | PARTIAL |
| CI | GitHub Actions YAML exists for push and pull request | NOT VERIFIED |

Automation caveat: DVC stages are isolated into ingestion, validation, preprocessing, candidate splitting and alignment entry points. The pipeline is reproducible locally.

Reproducibility caveat: dependencies should be pinned exactly before final publication. A deterministic candidate-ID split is implemented with seed 42.

Observability caveat: structured row, missing and duplicate values are present in several reports, but start/end timestamps, rejected-record counts and a consolidated stage pipeline report are incomplete or manually assembled.

## Phase D - Data quality tests

The test suite contains 21 tests and passed under pytest with cache disabled and a basetemp outside the repository.

Coverage:

- Kaggle required columns and empty category checks.
- Kaggle unique-ID fixture.
- O*NET required columns.
- O*NET SOC validity.
- Passing and corrupted fixtures for Kaggle/O*NET.
- Exploratory alignment-not-ground-truth shape check.

Missing or weak coverage:

- No explicit Kaggle dtype assertion.
- No production O*NET schema test for all actual 15/8-column schemas.
- No cross-file referential integrity test in pytest; it exists in `validate_onet.py`.
- No missing/duplicate threshold test using both passing and failing cases beyond basic examples.
- Configurable numerical range checks cover meaningful O*NET numeric fields.
- Candidate-ID separation and duplicate resume-text checks are implemented.
- Rare-category, reproducibility and invalid-input split cases are covered.
- No explicit no-candidate-level-join test; the implementation's alignment report limitation is clear, but no dedicated test asserts that relationship.

## Phase E - DVC and pipeline orchestration

- DVC 3.67.1 is installed.
- DVC is initialized.
- `dvc.lock` records dependencies and outputs.
- Kaggle raw CSV and O*NET directory have `.dvc` files.
- A local remote named `local` points to `../dvc-storage`.
- `dvc status` reports all data and pipelines up to date.
- `dvc list . --dvc-only` lists `data`, `logs`, and `reports`.
- DVC local cache and remote exist.
- External remote was not configured or tested.
- `dvc pull` was not executed by this audit.
- Normal `dvc repro` was not executed by this audit because it may have side effects.

Status: **PARTIAL**.

## Phase F - Continuous integration

The workflow has push and pull-request triggers, Python 3.11 setup, dependency installation, pytest and Ruff. It does not execute `dvc repro`, `make pipeline`, or a real reduced pipeline command. It only reruns fixture quality tests. Therefore the workflow is syntactically present and fixture tests are verified locally, but GitHub Actions syntax/operation and success are not verified.

Status: **NOT VERIFIED**.

## Phase G - Data card and traceability

`reports/data_card.md` includes sources, dimensions, schemas, preprocessing, biases, limitations, provenance, intended use and misuse. It does not invent a license and explains that license terms need provider verification. This is strong evidence.

Machine-readable `pipeline_report.json`, `data_quality_report.json`, and alignment JSON exist. Several claim to be execution reports, and pipeline/DVC evidence exists, but logs lack a single structured schema and report start/end timestamps are incomplete.

## Phase H - Fusion literature

`reports/multimodal_fusion_study.md` and `TASK3_REPORT.md` cover early, late and intermediate/hybrid fusion; concatenation; weighted sum/product; GMU; FiLM; TFN/LMF; MCB/MFB; cross-attention; multimodal transformers; bottlenecks; CLIP; graph fusion; and all requested challenges.

The comparative table contains approach, principle, advantage, limitation, conditions and references. The study includes identifiable `[1]`-`[10]` citations from the official assignment.

Status: **PASS**.

## Phase I - Project-specific choice

The project correctly treats Kaggle as a resume corpus and O*NET as an occupational knowledge base, explicitly rejects candidate-level pseudo-pairs, and limits fusion to a future experiment. It discusses granularity, alignment, missing modalities, data volume and interpretability. It does not discuss measured GPU memory or hardware in detail, and no real candidate-level structured features exist.

Status: **PARTIAL/PASS**: scientifically defensible in limitation handling, with a strong need for real reference citations and measured hardware conditions.

## Phase J - Architecture

The precise report provides:

- Text, optional structured and optional O*NET context branches.
- Latent dimensions.
- Projection layers.
- Concatenation and gating equations.
- Prediction head.
- Cross-entropy loss.
- Optional auxiliary contrastive loss.
- Missing-modality masks/text fallback.
- Text-only, structured-only, late-fusion and concatenation baselines.
- Macro-F1 and calibration-oriented evaluation.
- Ablations and integration plan.

The text branch specifies a compact pretrained transformer, 512-token handling and frozen/fine-tuned strategy. The O*NET branch specifies normalized document retrieval and projection. Missing modalities, modality dropout and class balance are described. No prototype or model metrics are claimed.

Status: **PARTIAL**.

## Phase K - Deliverables

- Git repository: PASS.
- Tag `task3`: PASS, targeted to commit `ecec1c6`.
- README installation/recovery/pipeline: PASS.
- PDF: PASS for existence and 15-page length.
- PDF references: PASS.
- Demo plan: PASS, but no recorded 5-10 minute demonstration: NOT VERIFIED.
