from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.alignment.occupation_alignment import build_category_to_occupation_mapping
from src.preprocessing.data_split import create_candidate_split
from src.validation.data_quality import (
    validate_kaggle_dataframe,
    validate_onet_dataframe,
)

CONFIG = {
    "kaggle": {"required_columns": ["ID", "Resume_str", "Resume_html", "Category"]},
    "validation": {
        "warn_on_missing_value_rate": 0.02,
        "critical_missing_value_rate": 0.20,
    },
    "onet": {
        "required_columns": {
            "occupation_data.csv": ["O*NET-SOC Code", "Title", "Description"],
            "software_skills.csv": ["O*NET-SOC Code", "Title", "Workplace Example", "Element ID", "Element Name", "Hot Technology", "In Demand"],
            "essential_skills.csv": ["O*NET-SOC Code", "Title", "Element ID", "Element Name", "Scale ID", "Scale Name", "Data Value"],
            "task_statements.csv": ["O*NET-SOC Code", "Title", "Task ID", "Task"],
        },
        "quality": {
            "numeric_ranges": {
                "essential_skills": {"Data Value": [0.0, 5.0]},
                "task_statements": {"Incumbents Responding": [0.0, None]},
            },
        },
    },
}


def test_validate_kaggle_dataframe_pass():
    frame = pd.DataFrame(
        {
            "ID": [1, 2, 3],
            "Resume_str": ["Python developer", "Data engineer", "Machine learning engineer"],
            "Resume_html": ["<p>A</p>", "<p>B</p>", "<p>C</p>"],
            "Category": ["ENGINEERING", "DATA", "ENGINEERING"],
        }
    )
    result = validate_kaggle_dataframe(frame, CONFIG)
    assert result["status"] == "pass"
    assert result["summary"]["rows"] == 3


def test_validate_kaggle_dataframe_fails_on_empty_category():
    frame = pd.DataFrame(
        {
            "ID": [1, 2],
            "Resume_str": ["Python", "SQL"],
            "Resume_html": ["<p>1</p>", "<p>2</p>"],
            "Category": ["", "ENGINEERING"],
        }
    )
    result = validate_kaggle_dataframe(frame, CONFIG)
    assert result["status"] == "fail"
    assert result["errors"]


def test_validate_onet_dataframe_pass():
    frame = pd.DataFrame(
        {
            "O*NET-SOC Code": ["15-1252.00", "15-1253.00"],
            "Title": ["Software Developer", "Software Quality Assurance Analyst"],
            "Description": ["desc a", "desc b"],
        }
    )
    result = validate_onet_dataframe(frame, "occupation_data.csv", CONFIG)
    assert result["status"] == "pass"


def test_validate_onet_dataframe_fails_on_missing_columns():
    frame = pd.DataFrame({"O*NET-SOC Code": ["15-1252.00"]})
    result = validate_onet_dataframe(frame, "occupation_data.csv", CONFIG)
    assert result["status"] == "fail"
    assert result["errors"]


FIXTURE_DIR = Path(__file__).parent / "fixtures"


def test_fixture_kaggle_valid():
    frame = pd.read_csv(FIXTURE_DIR / "kaggle_valid.csv")
    result = validate_kaggle_dataframe(frame, CONFIG)
    assert result["status"] == "pass"


def test_fixture_kaggle_corrupted_fails():
    frame = pd.read_csv(FIXTURE_DIR / "kaggle_corrupted.csv")
    result = validate_kaggle_dataframe(frame, CONFIG)
    assert result["status"] == "fail"


def test_fixture_onet_valid():
    frame = pd.read_csv(FIXTURE_DIR / "onet_valid.csv")
    result = validate_onet_dataframe(frame, "occupation_data.csv", CONFIG)
    assert result["status"] == "pass"


def test_fixture_onet_corrupted_fails():
    frame = pd.read_csv(FIXTURE_DIR / "onet_corrupted.csv")
    result = validate_onet_dataframe(frame, "occupation_data.csv", CONFIG)
    assert result["status"] == "fail"


def test_kaggle_ids_are_unique_for_candidate_splits():
    frame = pd.read_csv(FIXTURE_DIR / "kaggle_valid.csv")
    assert frame["ID"].is_unique


def test_semantic_alignment_is_not_verified_ground_truth():
    mapping = build_category_to_occupation_mapping(
        ["DATA-SCIENCE"],
        ["Data Scientists"],
        similarity_threshold=0.30,
    )
    assert mapping["mappings"]
    assert set(mapping["mappings"][0]).issuperset({"kaggle_category", "proposed_matches", "status"})


def test_candidate_split_has_no_overlapping_ids():
    frame = pd.read_csv(FIXTURE_DIR / "split_valid.csv")
    train, validation, test, stats = create_candidate_split(
        frame, train_ratio=0.70, validation_ratio=0.15, test_ratio=0.15, seed=42
    )
    assert set(train["ID"]).isdisjoint(set(validation["ID"]))
    assert set(train["ID"]).isdisjoint(set(test["ID"]))
    assert set(validation["ID"]).isdisjoint(set(test["ID"]))
    assert stats["overlapping_candidate_ids"] == 0


def test_candidate_split_has_no_duplicate_resume_text_across_splits():
    frame = pd.read_csv(FIXTURE_DIR / "split_valid.csv")
    train, validation, test, _ = create_candidate_split(
        frame, train_ratio=0.70, validation_ratio=0.15, test_ratio=0.15, seed=42
    )
    text_sets = [
        set(train["Resume_str"].fillna("").str.strip().str.lower()),
        set(validation["Resume_str"].fillna("").str.strip().str.lower()),
        set(test["Resume_str"].fillna("").str.strip().str.lower()),
    ]
    assert text_sets[0].isdisjoint(text_sets[1])
    assert text_sets[0].isdisjoint(text_sets[2])
    assert text_sets[1].isdisjoint(text_sets[2])


def test_candidate_split_reproducible_with_same_seed():
    frame = pd.read_csv(FIXTURE_DIR / "split_valid.csv")
    first = create_candidate_split(
        frame, train_ratio=0.70, validation_ratio=0.15, test_ratio=0.15, seed=42
    )
    second = create_candidate_split(
        frame, train_ratio=0.70, validation_ratio=0.15, test_ratio=0.15, seed=42
    )
    assert first[0].equals(second[0])
    assert first[1].equals(second[1])
    assert first[2].equals(second[2])


def test_duplicate_candidate_ids_raise():
    frame = pd.read_csv(FIXTURE_DIR / "split_invalid_duplicate_ids.csv")
    try:
        create_candidate_split(
            frame, train_ratio=0.70, validation_ratio=0.15, test_ratio=0.15, seed=42
        )
    except ValueError as exc:
        assert "unique" in str(exc)
    else:
        raise AssertionError("Duplicate candidate IDs must fail splitting.")


def test_empty_split_input_raises():
    frame = pd.DataFrame(columns=["ID", "Resume_str", "Category"])
    try:
        create_candidate_split(
            frame, train_ratio=0.70, validation_ratio=0.15, test_ratio=0.15, seed=42
        )
    except ValueError:
        pass
    else:
        raise AssertionError("Empty split input must fail.")


def test_candidate_split_changes_with_different_seed():
    frame = pd.read_csv(FIXTURE_DIR / "split_valid.csv")
    first = create_candidate_split(
        frame, train_ratio=0.70, validation_ratio=0.15, test_ratio=0.15, seed=42
    )
    second = create_candidate_split(
        frame, train_ratio=0.70, validation_ratio=0.15, test_ratio=0.15, seed=7
    )
    assert not first[0].equals(second[0]) or not first[1].equals(second[1]) or not first[2].equals(second[2])


def test_candidate_split_proportions_are_reasonable():
    frame = pd.read_csv(FIXTURE_DIR / "split_valid.csv")
    _, _, _, stats = create_candidate_split(
        frame, train_ratio=0.70, validation_ratio=0.15, test_ratio=0.15, seed=42
    )
    assert abs(stats["actual_row_rates"]["train"] - 0.70) < 0.20
    assert abs(stats["actual_row_rates"]["validation"] - 0.15) < 0.30
    assert abs(stats["actual_row_rates"]["test"] - 0.15) < 0.30


def test_rare_categories_do_not_cause_discarded_candidates():
    frame = pd.read_csv(FIXTURE_DIR / "split_rare_categories.csv")
    train, validation, test, stats = create_candidate_split(
        frame, train_ratio=0.70, validation_ratio=0.15, test_ratio=0.15, seed=42
    )
    assert len(train) + len(validation) + len(test) == len(frame)
    assert stats["candidate_count"] == len(frame)


def test_kaggle_fixture_uses_expected_text_and_id_types():
    frame = pd.read_csv(FIXTURE_DIR / "kaggle_valid.csv")
    result = validate_kaggle_dataframe(frame, CONFIG)
    assert result["status"] == "pass"
    assert pd.api.types.is_integer_dtype(frame["ID"])
    assert pd.api.types.is_string_dtype(frame["Resume_str"].astype("string"))


def test_onet_corrupted_soc_code_fails():
    frame = pd.read_csv(FIXTURE_DIR / "onet_corrupted.csv")
    result = validate_onet_dataframe(frame, "occupation_data.csv", CONFIG)
    assert result["status"] == "fail"
    assert any("occupation codes" in error for error in result["errors"])


def test_onet_data_value_range_warning_or_error_is_configurable():
    frame = pd.DataFrame(
        {
            "O*NET-SOC Code": ["15-1252.00"],
            "Title": ["Software Developer"],
            "Element ID": ["1"],
            "Element Name": ["Programming"],
            "Scale ID": ["IM"],
            "Scale Name": ["Importance"],
            "Data Value": [9.0],
        }
    )
    result = validate_onet_dataframe(frame, "essential_skills.csv", CONFIG)
    assert result["status"] == "pass"
    assert any("exceed 5.0" in warning for warning in result["warnings"])
