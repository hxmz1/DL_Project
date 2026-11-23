# Data Card

## Intended use

The datasets support transparent DataOps preparation, exploratory occupation alignment, text preprocessing, and future evaluation of resume classification or retrieval. They are not sufficient for verified candidate-level supervised multimodal training.

## Sources

- Kaggle Resume Dataset: `C:\Users\Asus\Desktop\data-dl\kaggle\archive (4).zip`, CSV member `Resume/Resume.csv`
- O*NET occupation and skills: `C:\Users\Asus\Desktop\data-dl\onet\`
- Recovered Kaggle CSV SHA-256: `816A7CD985A9A41E3CE8D1E83CB7E1BEB1E854A89C1CF1FD0D75494FAAA0559`

## Dataset dimensions

| Dataset | Rows | Columns |
|---|---:|---:|
| Kaggle resume | 2,484 | 4 |
| O*NET occupation | 1,016 | 3 |
| O*NET software skills | 31,821 | 7 |
| O*NET essential skills | 18,200 | 15 |
| O*NET task statements | 18,838 | 8 |

## Kaggle schema

`ID`, `Resume_str`, `Resume_html`, `Category`; 24 unique categories. There are no missing values, duplicate IDs, or exact duplicate rows. One resume text is blank.

## O*NET schemas

The four source files preserve their original O*NET schemas. Essential skills contain 9,100 missing cells and task statements contain 1,005 missing cells. Exact duplicate rows and unknown SOC references are 0.

## Preprocessing

- Raw files are preserved unchanged.
- Kaggle text whitespace is normalized in the prepared text dataset.
- O*NET text columns are trimmed in interim copies; row counts are preserved.
- Category and O*NET SOC codes are retained for traceability.
- Candidate-ID and resume-text duplicate-aware train/validation/test assignments are exported separately to `data/processed/splits/`.

## Known biases and limitations

- Kaggle categories are dataset labels, not necessarily objective occupation classifications.
- Resume text and HTML quality may vary; one blank Resume_str is present.
- Kaggle is a resume corpus and O*NET is an occupational knowledge base.
- No verified candidate-level relationship connects Kaggle resumes to O*NET occupations.
- SequenceMatcher alignment is lexical/rule-based and can produce false or ambiguous matches.

## License and usage constraints

License terms were not supplied with the project snapshot and must not be inferred. Users must verify Kaggle and O*NET usage constraints with the original providers before redistribution or external publication.

## Provenance

Real datasets were recovered from `C:\Users\Asus\Desktop\data-dl` after backup of the synthetic raw files. Destination/source hash comparisons passed. Synthetic files used only for tests remain under `tests/fixtures/`.

## Potential misuse

- Do not use the exploratory alignment as hiring ground truth.
- Do not infer protected attributes or make autonomous screening decisions.
- Do not claim a trained or evaluated fusion model.
- Do not use O*NET alone as a candidate-level label source.
