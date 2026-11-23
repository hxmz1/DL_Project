# Task 3 Data Recovery Search Audit

Date: 2026-11-08
Scope: Read-only forensic search for original Task 2 datasets on this Windows machine.

## 1. Search locations

The following locations were inspected without modifying any files or executing the pipeline:

- Project directory: `C:\Users\Asus\Desktop\DL_Project`
- Parent directory: `C:\Users\Asus\Desktop`
- User Documents: `C:\Users\Asus\Documents`
- User Downloads: `C:\Users\Asus\Downloads`
- Candidate archive folders under Downloads
- Exact CSV lookups for:
  - `Resume.csv`
  - `occupation_data.csv`
  - `software_skills.csv`
  - `essential_skills.csv`
  - `task_statements.csv`
- ZIP archive inspection for filenames and embedded dataset names

## 2. Expected original Task 2 dataset dimensions

These are the expected source dimensions from the original Task 2 specification:

- Kaggle Resume.csv: 2,484 rows, 4 columns
- O*NET occupation_data.csv: 1,016 rows
- O*NET software_skills.csv: 31,821 rows
- O*NET essential_skills.csv: 18,200 rows
- O*NET task_statements.csv: 18,838 rows

## 3. Current project data under data/raw and data/interim

The current project files are synthetic fixtures and do not match the original Task 2 dimensions.

| File path | File size | Rows | Columns | Classification |
|---|---:|---:|---:|---|
| `C:\Users\Asus\Desktop\DL_Project\data\raw\kaggle\extracted\Resume\Resume.csv` | 325 bytes | 3 | 4 | Synthetic fixture |
| `C:\Users\Asus\Desktop\DL_Project\data\raw\onet\occupation_data.csv` | 159 bytes | 2 | 3 | Synthetic fixture |
| `C:\Users\Asus\Desktop\DL_Project\data\raw\onet\software_skills.csv` | 227 bytes | 2 | 7 | Synthetic fixture |
| `C:\Users\Asus\Desktop\DL_Project\data\raw\onet\essential_skills.csv` | 207 bytes | 2 | 7 | Synthetic fixture |
| `C:\Users\Asus\Desktop\DL_Project\data\raw\onet\task_statements.csv` | 223 bytes | 2 | 5 | Synthetic fixture |
| `C:\Users\Asus\Desktop\DL_Project\data\interim\kaggle\resumes.csv` | 325 bytes | 3 | 4 | Synthetic fixture |
| `C:\Users\Asus\Desktop\DL_Project\data\interim\onet\software_skills.csv` | 227 bytes | 2 | 7 | Synthetic fixture |
| `C:\Users\Asus\Desktop\DL_Project\data\interim\onet\essential_skills.csv` | 207 bytes | 2 | 7 | Synthetic fixture |
| `C:\Users\Asus\Desktop\DL_Project\data\interim\onet\task_statements.csv` | 223 bytes | 2 | 5 | Synthetic fixture |

## 4. Files discovered outside the project

### 4.1 Candidate original Kaggle copy

I found a likely original Kaggle Resume dataset in the Downloads area:

- File: `C:\Users\Asus\Downloads\archive (3)\Resume\Resume.csv`
- Size: 56,273,235 bytes (~53.6 MB)
- Rows: 2,484
- Columns: 4
- Header: `ID, Resume_str, Resume_html, Category`
- Match to expected Task 2 Kaggle dataset: Exact row count and column count match.
- Confidence: High
- Classification: Likely original dataset copy

I also inspected the corresponding archive without extraction:

- File: `C:\Users\Asus\Downloads\archive (3).zip`
- Contains `Resume/Resume.csv`
- The zip file itself has the same dataset dimensions: 2,484 rows, 4 columns
- Confidence: High
- Classification: Likely original dataset archive copy

### 4.2 O*NET original copies

Searches for exact filenames and zip contents did not locate any accessible original O*NET CSVs in the user folders, desktop, documents, downloads, or archive bundles.

- Searched for exact files:
  - `occupation_data.csv`
  - `software_skills.csv`
  - `essential_skills.csv`
  - `task_statements.csv`
- Result: no matches outside the project, and no accessible O*NET dataset archive was found.
- Confidence: High for "not found in accessible locations"
- Classification: Not found / no original copy available in this environment

## 5. Candidate classification summary

| Candidate file | Path | Dimensions | Expected match? | Likely status | Confidence |
|---|---|---|---|---|---|
| Kaggle Resume original candidate | `C:\Users\Asus\Downloads\archive (3)\Resume\Resume.csv` | 2,484 x 4 | Yes | Original copy | High |
| Kaggle archive bundle | `C:\Users\Asus\Downloads\archive (3).zip` | 2,484 x 4 in `Resume/Resume.csv` | Yes | Original archive copy | High |
| Project raw Kaggle file | `C:\Users\Asus\Desktop\DL_Project\data\raw\kaggle\extracted\Resume\Resume.csv` | 3 x 4 | No | Synthetic fixture | High |
| Project O*NET files | `C:\Users\Asus\Desktop\DL_Project\data\raw\onet\*.csv` | 2 rows each | No | Synthetic fixture | High |
| O*NET original copies in accessible system folders | None found | — | — | Not found | High |

## 6. Search results by location

### Project directory and parent

- `C:\Users\Asus\Desktop\DL_Project` contains the synthetic raw/interim fixture files only.
- `C:\Users\Asus\Desktop` does not contain a relevant original Resume/O*NET dataset copy by exact filename matching.

### Downloads

- `C:\Users\Asus\Downloads\archive (3)\Resume\Resume.csv` was found and matches the historical Kaggle dataset dimensions exactly.
- No exact O*NET CSV filenames were found in Downloads.
- No zip archive in Downloads had obvious O*NET dataset names or embedded O*NET CSVs.

### Documents

- No relevant dataset files found.

## 7. Code evidence regarding synthetic generation and overwrite risk

The synthetic generation logic is in the pipeline orchestration file:

- `C:\Users\Asus\Desktop\DL_Project\src\pipeline\run_pipeline.py`

The relevant logic is:

- `ensure_synthetic_data_if_needed(force: bool = False)` creates a minimal 3-row Kaggle file and 2-row O*NET CSV fixtures in `data/raw` when raw data is missing.
- The CLI flag `--synthetic` calls this function via:
  `if args.synthetic: ensure_synthetic_data_if_needed(force=True)`

This means the synthetic path intentionally writes raw CSVs to the project’s `data/raw` folders and therefore represents an overwrite risk if the pipeline is run against a populated real-data project.

## 8. Recovery status

### Found
- Kaggle Resume original dataset candidate: yes

### Not found
- O*NET occupation_data.csv original copy
- O*NET software_skills.csv original copy
- O*NET essential_skills.csv original copy
- O*NET task_statements.csv original copy

## 9. Files that could not be accessed or were not found

- No additional original O*NET dataset archives were discovered in Downloads/Desktop/Documents.
- No exact O*NET CSVs were found in other accessible user directories.
- No zip files with names matching `O*NET`, `Occupational Information Network`, or `occupation_data` were found in the inspected locations.

## 10. Recommended recovery source

The best available recovery source in this environment is the extracted Kaggle Resume dataset found here:

- `C:\Users\Asus\Downloads\archive (3)\Resume\Resume.csv`

For the O*NET datasets, the recommended recovery source would be an original upstream archive from the project’s original data source (for example, a trusted Kaggle/O*NET download bundle or a backup from the prior Task 2 environment), because no original O*NET files were found in the machine’s accessible folders.

## 11. Final verdict

PARTIAL RECOVERY: Some original datasets were found.

Rationale:
- The Kaggle Resume dataset was found and matches the expected original dimensions exactly.
- The O*NET original datasets were not found anywhere in the accessible Windows user folders, Downloads, Desktop, Documents, or archive scans.
- The project’s current `data/raw` and `data/interim` files are synthetic and should not be treated as the original Task 2 data.

## 12. Summary

The evidence shows that the original Kaggle resume dataset still exists on this machine in a Downloads archive, while the original O*NET datasets are not present in the accessible workspace or user directories. The project’s current raw files are synthetic fixtures created by the pipeline, and the synthetic generator explicitly writes to those raw paths under `data/raw`.
