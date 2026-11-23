from __future__ import annotations

import argparse
import hashlib
import json
import random
from collections import defaultdict
from pathlib import Path
from typing import Any

import pandas as pd

from src.common.config import PROJECT_ROOT, load_config


def _resume_key(value: object) -> str:
    if not isinstance(value, str):
        return ""
    normalized = " ".join(value.strip().lower().split())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def create_candidate_split(
    frame: pd.DataFrame,
    *,
    train_ratio: float,
    validation_ratio: float,
    test_ratio: float,
    seed: int,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    ratios = {"train": train_ratio, "validation": validation_ratio, "test": test_ratio}
    if any(ratio <= 0 for ratio in ratios.values()):
        raise ValueError("Train, validation and test ratios must be positive.")
    if abs(sum(ratios.values()) - 1.0) > 1e-9:
        raise ValueError("Train, validation and test ratios must sum to 1.0.")
    required = {"ID", "Resume_str", "Category"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"Missing required split columns: {sorted(missing)}")
    if frame.empty:
        raise ValueError("Cannot split an empty Kaggle dataset.")
    if frame["ID"].isna().any():
        raise ValueError("Candidate split contains missing IDs.")
    if not frame["ID"].is_unique:
        raise ValueError("Candidate IDs must be unique before splitting.")
    if frame["Category"].isna().any() or frame["Category"].astype("string").str.strip().eq("").any():
        raise ValueError("Candidate split contains missing or blank categories.")

    working = frame.copy()
    working["_resume_key"] = working["Resume_str"].map(_resume_key)

    text_groups: dict[str, list[int]] = defaultdict(list)
    for position, key in enumerate(working["_resume_key"]):
        text_groups[key].append(position)

    category_by_unit: dict[str, str] = {}
    for key, positions in text_groups.items():
        categories = working.iloc[positions]["Category"].astype("string").value_counts()
        category_by_unit[key] = str(categories.index[0])

    units_by_category: dict[str, list[str]] = defaultdict(list)
    for key, category in category_by_unit.items():
        units_by_category[category].append(key)

    rng = random.Random(seed)
    assignments: dict[str, list[str]] = {"train": [], "validation": [], "test": []}
    total_units = len(text_groups)
    rare_index = 0
    for category in sorted(units_by_category):
        units = units_by_category[category]
        rng.shuffle(units)
        count = len(units)
        if count == 1:
            assigned = ("train", "validation", "test")[rare_index % 3]
            rare_index += 1
            assignments[assigned].append(units[0])
        elif count == 2:
            assignments["train"].append(units[0])
            second_split = "validation" if rare_index % 2 == 0 else "test"
            rare_index += 1
            assignments[second_split].append(units[1])
        elif count == 3:
            assignments["train"].append(units[0])
            assignments["validation"].append(units[1])
            assignments["test"].append(units[2])
        else:
            train_count = max(1, round(count * train_ratio))
            validation_count = max(1, round(count * validation_ratio))
            test_count = max(1, count - train_count - validation_count)
            if train_count + validation_count + test_count > count:
                test_count = count - train_count - validation_count
            assignments["train"].extend(units[:train_count])
            assignments["validation"].extend(units[train_count:train_count + validation_count])
            assignments["test"].extend(units[train_count + validation_count:train_count + validation_count + test_count])

    # Ensure non-empty validation and test splits when the data is large enough.
    if not assignments["validation"] or not assignments["test"]:
        raise ValueError("A valid 70/15/15 split could not be produced with the available categories.")

    split_by_key = {}
    for split_name, keys in assignments.items():
        for key in keys:
            split_by_key[key] = split_name

    working["_split"] = working["_resume_key"].map(split_by_key)
    if working["_split"].isna().any():
        raise ValueError("One or more candidate text groups were not assigned.")

    trains = working[working["_split"] == "train"].drop(columns=["_resume_key", "_split"])
    validation = working[working["_split"] == "validation"].drop(columns=["_resume_key", "_split"])
    tests = working[working["_split"] == "test"].drop(columns=["_resume_key", "_split"])

    train_ids = set(trains["ID"])
    validation_ids = set(validation["ID"])
    test_ids = set(tests["ID"])
    if train_ids & validation_ids or train_ids & test_ids or validation_ids & test_ids:
        raise ValueError("Candidate ID overlap detected across splits.")

    for left_name, left in (("train", trains), ("validation", validation), ("test", tests)):
        for right_name, right in (("train", trains), ("validation", validation), ("test", tests)):
            if left_name >= right_name:
                continue
            left_text = set(left["Resume_str"].fillna("").map(_resume_key))
            right_text = set(right["Resume_str"].fillna("").map(_resume_key))
            if left_text & right_text:
                raise ValueError(f"Duplicate resume text detected between {left_name} and {right_name}.")

    def distribution(frame: pd.DataFrame) -> dict[str, int]:
        return {str(category): int(count) for category, count in frame["Category"].value_counts().items()}

    stats = {
        "seed": seed,
        "candidate_count": len(frame),
        "text_group_count": int(total_units),
        "ratios": ratios,
        "actual_row_counts": {
            "train": len(trains),
            "validation": len(validation),
            "test": len(tests),
        },
        "actual_row_rates": {
            "train": round(len(trains) / len(frame), 6),
            "validation": round(len(validation) / len(frame), 6),
            "test": round(len(tests) / len(frame), 6),
        },
        "category_distributions": {
            "train": distribution(trains),
            "validation": distribution(validation),
            "test": distribution(tests),
        },
        "overlapping_candidate_ids": 0,
        "duplicate_resume_text_across_splits": 0,
        "status": "pass",
    }
    return trains, validation, tests, stats


def split_from_config(config: dict[str, Any], source: Path, output_dir: Path) -> dict[str, Any]:
    frame = pd.read_csv(source, encoding="utf-8-sig")
    split_config = config["splits"]
    trains, validation, tests, stats = create_candidate_split(
        frame,
        train_ratio=float(split_config["train"]),
        validation_ratio=float(split_config["validation"]),
        test_ratio=float(split_config["test"]),
        seed=int(config["project"]["random_seed"]),
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    trains.to_csv(output_dir / "train.csv", index=False, encoding="utf-8-sig")
    validation.to_csv(output_dir / "validation.csv", index=False, encoding="utf-8-sig")
    tests.to_csv(output_dir / "test.csv", index=False, encoding="utf-8-sig")
    with (output_dir / "split_statistics.json").open("w", encoding="utf-8") as handle:
        json.dump(stats, handle, indent=2, ensure_ascii=False)
    return stats


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/params.yaml")
    parser.add_argument("--source", default=None)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()
    config = load_config(args.config)
    source = Path(args.source) if args.source else PROJECT_ROOT / config["paths"]["interim"]["kaggle_csv"]
    output = Path(args.output) if args.output else PROJECT_ROOT / "data" / "processed" / "splits"
    split_from_config(config, source, output)
    print(f"Candidate split completed: {output}")


if __name__ == "__main__":
    main()
