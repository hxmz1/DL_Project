from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.preprocessing.data_split import create_candidate_split
from src.validation.data_quality import validate_kaggle_dataframe

CONFIG = {
    "kaggle": {"required_columns": ["ID", "Resume_str", "Resume_html", "Category"]},
    "onet": {"required_columns": {}},
    "validation": {
        "warn_on_missing_value_rate": 0.02,
        "critical_missing_value_rate": 0.20,
    },
}


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    fixture = root / "tests" / "fixtures" / "split_valid.csv"
    frame = pd.read_csv(fixture, encoding="utf-8-sig")
    quality = validate_kaggle_dataframe(frame, CONFIG)
    if quality["status"] != "pass":
        raise SystemExit("Fixture quality validation failed.")

    with tempfile.TemporaryDirectory(prefix="task3_ci_") as temporary:
        output = Path(temporary)
        train, validation, test, statistics = create_candidate_split(
            frame,
            train_ratio=0.70,
            validation_ratio=0.15,
            test_ratio=0.15,
            seed=42,
        )
        train.to_csv(output / "train.csv", index=False)
        validation.to_csv(output / "validation.csv", index=False)
        test.to_csv(output / "test.csv", index=False)
        if set(train["ID"]) & set(validation["ID"]):
            raise SystemExit("Candidate leakage detected.")
        if set(train["ID"]) & set(test["ID"]):
            raise SystemExit("Candidate leakage detected.")
        if set(validation["ID"]) & set(test["ID"]):
            raise SystemExit("Candidate leakage detected.")
        print(f"Fixture pipeline OK: {statistics['actual_row_counts']}")


if __name__ == "__main__":
    main()
