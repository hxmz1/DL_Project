# TASK 3 Requirements Checklist

Statuses: PASS, PARTIAL, FAIL, NOT VERIFIED, NOT APPLICABLE.

| Requirement ID | Official reference | Requirement | Evidence | Status |
|---|---|---|---|---|
| ST-01 | B-A.2, page 2 | Clear project structure | Directories and modules exist | PASS |
| ST-02 | B-A.2, page 2 | Independent data modules | `src/ingestion`, `src/validation`, `src/preprocessing`, `src/alignment` | PASS |
| ST-03 | B-A.2, page 2 | External configuration | `configs/params.yaml`, `src/common/config.py` | PASS |
| ST-04 | B-A.2, page 2 | No hardcoded paths/thresholds | Modules have derived hardcoded project-relative paths and pipeline stage names; thresholds partly config-driven | PARTIAL |
| DI-01 | B-A.2, page 2 | Kaggle real ingestion | Raw Kaggle 2,484 x 4, hash verified | PASS |
| DI-02 | B-A.2, page 2 | O*NET real ingestion | Four raw files total 69,875 rows | PASS |
| DI-03 | C1, page 1 | One-command rebuild | `dvc.yaml`, Makefile and run pipeline exist | PARTIAL |
| DI-04 | C6, pages 1-2 | Critical validation stops pipeline | Validation stop after dataframe status fails | PASS |
| DI-05 | C4, page 2 | Data versioning | DVC `.dvc` files and lock/cache/remote | PARTIAL |
| DI-06 | C4, page 2 | Raw/prepared data retrieval docs | README documents DVC/pull and local remote, external remote remains unconfigured | PARTIAL |
| DQ-01 | A.2.5, page 2 | Schema tests | Required-column tests exist | PARTIAL |
| DQ-02 | A.2.5, page 2 | Text/data types | Blank text and text encoding coverage; no complete dtype matrix | PARTIAL |
| DQ-03 | A.2.5, page 2 | Missing/duplicate thresholds | Config and basic implementation exist | PARTIAL |
| DQ-04 | A.2.5, page 2 | Outlier checks | Configurable numerical range checks include essential-skill and task numeric fields | PARTIAL |
| DQ-05 | A.2.5, page 2 | Cross-modal consistency | O*NET internal integrity implemented; no candidate-level join | PASS/NOT APPLICABLE for invented join |
| DQ-06 | A.2.5, page 2 | Leakage prevention | Candidate split module and overlap/resume-text/reproducibility tests exist | PASS |
| DQ-07 | A.2.5, page 2 | Positive and negative tests | Passing/corrupted fixtures exist | PASS |
| CI-01 | A.2.6, page 2 | CI workflow | `.github/workflows/ci.yml` exists | PASS |
| CI-02 | A.2.6, page 2 | Lint/unit/tests | Workflow installs Ruff and pytest | PASS |
| CI-03 | A.2.6, page 2 | Reduced pipeline | Fixture-only pipeline entry point added; GitHub execution remains unverified | PARTIAL |
| CI-04 | A.2.6, page 2 | GitHub execution | No GitHub Actions run evidence | NOT VERIFIED |
| OB-01 | C6, page 2 | Stage logs | Ingestion/consistency/preparation logs exist | PARTIAL |
| OB-02 | C6, page 2 | Row/statistics reports | Kaggle/O*NET/pipeline JSON reports exist | PARTIAL |
| OB-03 | C6, page 2 | Rejected records | Rejected-record counts are not tracked explicitly | FAIL |
| OB-04 | C6, page 2 | Data card | `reports/data_card.md` exists with sources/schemas/biases | PASS |
| OB-05 | C6, page 2 | Automatic reports | Pipeline scripts generate reports | PASS |
| TR-01 | C4, page 1 | Code in Git | Git repository and commit exist | PASS |
| TR-02 | C4, page 1 | Tag `task3` | Tag exists and targets `ecec1c6`, but final correction commit is not yet created | PARTIAL |
| TR-03 | C4, page 1 | Raw DVC tracking | Kaggle and O*NET `.dvc` outputs exist | PASS |
| TR-04 | C4, page 1 | External remote | No external remote credentials/configure/test | FAIL |
| TR-05 | C4, page 1 | DVC pull | Not tested in audit | NOT VERIFIED |
| FU-01 | B.1, pages 3-4 | Classical fusion levels | Early/late/intermediate covered | PASS |
| FU-02 | B.1, pages 3-4 | Mechanisms | All required mechanisms covered | PASS |
| FU-03 | B.1, pages 3-4 | Challenges | Heterogeneity, alignment, missing, imbalance, cost, interpretability covered | PASS |
| FU-04 | B.1, pages 3-4 | Comparative table | Table exists with a reference column | PASS |
| FU-05 | B.1, page 6 | References | Formal `[1]`-`[10]` bibliography and mechanism citations added | PASS |
| FS-01 | B.2, page 4 | Justification by actual data | Kaggle/O*NET characteristics and pairing limitation covered | PASS |
| FS-02 | B.2, page 4 | Granularity/alignment/interactions | Discussed explicitly | PARTIAL |
| FS-03 | B.2, page 4 | Missing modalities | Text fallback and modality masks proposed | PASS |
| FS-04 | B.2, page 4 | Hardware/volume | Volume discussed; GPU constraints not measured | PARTIAL |
| AR-01 | B.3, pages 4-5 | Architecture diagram | Text diagram exists | PASS |
| AR-02 | B.3, pages 4-5 | Encoder/dimensions/projections/head | DistilBERT/compact transformer, dimensions and branches documented | PASS |
| AR-03 | B.3, pages 4-5 | Formal equations/pseudocode | Equations and pseudocode exist | PASS |
| AR-04 | B.3, pages 4-5 | Loss/auxiliary loss | Cross entropy and optional contrastive loss | PASS |
| AR-05 | B.3, pages 4-5 | Missing/imbalance | Missing fallback, modality masks, modality dropout and class balance described | PASS |
| AR-06 | B.3, pages 4-5 | Baselines | Text, structured, late and concatenation baselines proposed | PASS |
| AR-07 | B.3, pages 4-5 | Evaluation/ablation | Metrics and ablations proposed | PASS |
| AR-08 | B.3, pages 4-5 | Pipeline integration | Integration plan described | PASS |
| AR-09 | Bonus page 5 | Prototype | No implementation/prototype/test | NOT APPLICABLE, bonus |
| DL-01 | Livrable page 5 | Git repository/tag | Git and tag exist | PASS |
| DL-02 | Livrable page 5 | README | Installation, recovery and execution documented | PASS |
| DL-03 | Livrable page 5 | PDF 10-15 pages | Project PDF is 15 pages | PASS |
| DL-04 | Livrable page 5 | PDF content | DataOps, fusion and architecture sections exist | PARTIAL |
| DL-05 | Livrable page 5 | References | Generic statement, no completed bibliography | FAIL |
| DL-06 | Livrable page 5 | Demo 5-10 minutes | Demo script exists, no recording evidence | NOT VERIFIED |
