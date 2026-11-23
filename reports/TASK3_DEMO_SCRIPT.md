# TASK 3 - 5 to 10 Minute Demo

1. Show `configs/params.yaml` and explain centralized paths and quality thresholds.
2. Show `data/raw/` and state that it contains recovered real data; show the recovery report and hashes.
3. Run `python -m src.pipeline.run_pipeline`.
4. Show successful Kaggle and O*NET ingestion counts and pipeline report.
5. Run `pytest -q tests/test_data_quality.py`.
6. Show `tests/fixtures/kaggle_corrupted.csv`, then run the corresponding deliberately failing test with `pytest -q tests/test_data_quality.py -k corrupted`.
7. Explain that pytest validates corrupt fixtures and does not overwrite raw data.
8. Run `dvc repro` and `dvc status`.
9. Show the exploratory alignment report and state that it is not candidate-level ground truth.
10. Show the fusion architecture proposal and distinguish architecture proposed from model trained and model evaluated.
