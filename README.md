# Candidate Screening AI - DataOps and Multimodal Fusion Preparation

## Project overview

This project prepares a reproducible DataOps pipeline for 2,484 Kaggle resumes and 69,875 O*NET records. It implements ingestion, validation, preprocessing, exploratory alignment, reporting, DVC versioning, pytest coverage, and a proposed future fusion architecture.

Kaggle and O*NET do not provide a verified candidate-to-occupation relationship. Semantic alignment is exploratory only and is never represented as ground truth.

## Prerequisites

- Windows 10/11
- Python 3.11
- Git
- DVC Python package

## Environment setup

```powershell
cd C:\Users\Asus\Desktop\DL_Project
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Dataset recovery

The independent source directory is the read-only source of truth:

- Kaggle: `C:\Users\Asus\Desktop\data-dl\kaggle\archive (4).zip`
- O*NET: `C:\Users\Asus\Desktop\data-dl\onet\`

Do not modify, replace, or synthesize data in `C:\Users\Asus\Desktop\data-dl`. Recover:

- `Resume/Resume.csv` from the Kaggle ZIP to `data/raw/kaggle/extracted/Resume/Resume.csv`
- `occupation_data.csv`
- `software_skills.csv`
- `essential_skills.csv`
- `task_statements.csv`

into `data/raw/onet/`.

Synthetic fixtures must exist only under `tests/fixtures/`. The pipeline never creates synthetic raw data.

## Run the pipeline

```powershell
python -m src.pipeline.run_pipeline
make pipeline
```

DVC reproduction:

```powershell
dvc repro
dvc status
dvc push
dvc pull
```

To reproduce with Google Drive after the repository owner has configured credentials:

```powershell
dvc remote add -d gdrive gdrive://GOOGLE_DRIVE_FOLDER_ID
dvc remote modify gdrive gdrive_acknowledge_abuse true
dvc push
dvc pull
```

Do not place OAuth tokens or Google credentials in the repository. The first `dvc pull` or
`dvc push` may open a secure browser authentication flow.

The DVC pipeline stages are isolated: Kaggle/O*NET ingestion, O*NET consistency validation,
quality validation, preprocessing, candidate-ID splitting, and semantic alignment. A
candidate split writes only to `data/processed/splits/`.

The repository uses a local DVC remote named `dvc-storage`. For an external remote:

```powershell
dvc remote add -d storage s3://your-bucket/candidate-screening
dvc remote add -d storage gdrive://your-folder-id
```

No external remote is claimed until configured and tested.

## Tests and lint

```powershell
python -m pytest -q
ruff check src tests --ignore LOG015,TRY004
make test
make lint
```

## CI

`.github/workflows/ci.yml` installs dependencies, runs linting and pytest, and performs fixture-only quality checks. A workflow file does not prove that GitHub Actions passed; GitHub execution must be verified in the repository Actions page.
CI also executes `scripts/run_fixture_pipeline.py`, which creates split artifacts only in a temporary directory and must not access production raw data.

## Data layout

```text
data/raw/       recovered source data, DVC-tracked
data/interim/   intermediate CSV files
data/processed/ prepared text and structured summaries
reports/        machine-readable and human-readable reports
logs/           pipeline and ingestion logs
tests/fixtures/ passing and deliberately corrupted synthetic fixtures
```

## Architecture

```text
raw data -> ingestion -> validation -> preprocessing -> exploratory alignment -> reports
```

The fusion package documents future intermediate/hybrid fusion. No multimodal model is trained or evaluated; no candidate-level ground truth is fabricated.

## Main reports

- `reports/TASK3_PRE_IMPLEMENTATION_AUDIT.md`
- `reports/TASK3_DATA_RECOVERY_REPORT.md`
- `reports/multimodal_alignment_report.json`
- `reports/data_card.md`
- `reports/multimodal_fusion_study.md`
- `reports/fusion_strategy_recommendation.md`
- `reports/fusion_architecture_proposal.md`
- `reports/TASK3_IMPLEMENTATION_REPORT.md`
- `reports/TASK3_FINAL_VALIDATION_REPORT.md`

## Known limitations

- There is no verified candidate-level Kaggle/O*NET join.
- SequenceMatcher-based alignment is exploratory and not ground truth.
- O*NET is an occupational knowledge base, not a candidate-level feature table.
- Missing modalities and validated structured candidate features are unresolved prerequisites for supervised fusion.
