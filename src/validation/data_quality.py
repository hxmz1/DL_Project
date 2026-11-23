from __future__ import annotations

from typing import Any

import pandas as pd


def safe_missing_rate(frame: pd.DataFrame) -> float:
    """Return the share of missing values across the entire DataFrame."""
    if frame.empty:
        return 0.0
    return float(frame.isna().sum().sum() / (frame.shape[0] * frame.shape[1]))


def normalize_text_series(series: pd.Series) -> pd.Series:
    """Trim and normalize text values while preserving missing entries."""
    return series.map(lambda value: value.strip() if isinstance(value, str) else value)


def validate_required_columns(df: pd.DataFrame, required_columns: list[str], dataset_name: str) -> dict[str, Any]:
    missing = [column for column in required_columns if column not in df.columns]
    return {
        "dataset_name": dataset_name,
        "missing_columns": missing,
        "status": "pass" if not missing else "fail",
        "message": "All required columns are present." if not missing else f"Missing columns: {missing}",
    }


def validate_kaggle_dataframe(df: pd.DataFrame, config: dict[str, Any]) -> dict[str, Any]:
    """Validate Kaggle resume data and return a structured quality report."""
    required_columns = config.get("kaggle", {}).get("required_columns", [])
    check = validate_required_columns(df, required_columns, "kaggle")
    if check["status"] == "fail":
        return {
            "status": "fail",
            "errors": [check["message"]],
            "dataset_name": "kaggle",
            "summary": {},
        }

    if df.empty:
        return {
            "status": "fail",
            "errors": ["Kaggle dataset is empty."],
            "dataset_name": "kaggle",
            "summary": {},
        }

    resume_series = df["Resume_str"].astype("string")
    category_series = df["Category"].astype("string")
    blank_resume = int(resume_series.str.strip().fillna("").eq("").sum())
    blank_categories = int(category_series.str.strip().fillna("").eq("").sum())
    missing_ids = int(df["ID"].isna().sum())
    duplicate_ids = int(df["ID"].duplicated().sum())
    duplicate_rows = int(df.duplicated().sum())
    missing_rate = safe_missing_rate(df)

    warnings: list[str] = []
    errors: list[str] = []
    if list(df.columns) != required_columns:
        warnings.append("Kaggle column order differs from the configured schema.")
    if not pd.api.types.is_integer_dtype(df["ID"]) and not pd.api.types.is_numeric_dtype(df["ID"]):
        errors.append("Kaggle ID has an invalid data type; expected integer/numeric.")
    if not pd.api.types.is_object_dtype(df["Resume_str"]) and not pd.api.types.is_string_dtype(df["Resume_str"]):
        errors.append("Resume_str has an invalid data type; expected text.")
    if not pd.api.types.is_object_dtype(df["Resume_html"]) and not pd.api.types.is_string_dtype(df["Resume_html"]):
        errors.append("Resume_html has an invalid data type; expected text.")
    if not pd.api.types.is_object_dtype(df["Category"]) and not pd.api.types.is_string_dtype(df["Category"]):
        errors.append("Category has an invalid data type; expected text.")
    if blank_resume > 0:
        warnings.append(f"Found {blank_resume} blank resume texts.")
    if blank_categories > 0:
        errors.append(f"Found {blank_categories} empty categories.")
    if missing_ids > 0:
        errors.append(f"Found {missing_ids} missing IDs.")
    if duplicate_ids > 0:
        errors.append(f"Found {duplicate_ids} duplicate IDs.")
    if duplicate_rows > 0:
        warnings.append(f"Found {duplicate_rows} exact duplicate rows.")
    if missing_rate > config.get("validation", {}).get("critical_missing_value_rate", 0.20):
        errors.append("Missing-value rate exceeds the critical threshold.")
    elif missing_rate > config.get("validation", {}).get("warn_on_missing_value_rate", 0.02):
        warnings.append("Missing-value rate is above the warning threshold.")

    status = "pass" if not errors else "fail"
    return {
        "status": status,
        "warnings": warnings,
        "errors": errors,
        "dataset_name": "kaggle",
        "summary": {
            "rows": len(df),
            "columns": list(df.columns),
            "missing_value_rate": round(missing_rate, 6),
            "blank_resume_texts": blank_resume,
            "blank_categories": blank_categories,
            "missing_ids": missing_ids,
            "duplicate_ids": duplicate_ids,
            "duplicate_rows": duplicate_rows,
            "unique_categories": int(df["Category"].nunique(dropna=False)),
        },
    }


def validate_onet_dataframe(df: pd.DataFrame, file_name: str, config: dict[str, Any]) -> dict[str, Any]:
    """Validate an individual O*NET CSV file."""
    required_columns = config.get("onet", {}).get("required_columns", {}).get(file_name, [])
    check = validate_required_columns(df, required_columns, file_name)
    if check["status"] == "fail":
        return {
            "dataset_name": file_name,
            "status": "fail",
            "errors": [check["message"]],
            "summary": {},
        }

    if df.empty:
        return {
            "dataset_name": file_name,
            "status": "fail",
            "errors": [f"{file_name} is empty."],
            "summary": {},
        }

    code_column = "O*NET-SOC Code"
    code_series = df[code_column].astype("string").str.strip()
    invalid_codes = int((~code_series.str.fullmatch(r"\d{2}-\d{4}\.\d{2}", na=False)).sum())
    duplicate_rows = int(df.duplicated().sum())
    missing_rate = safe_missing_rate(df)
    warnings: list[str] = []
    errors: list[str] = []
    if list(df.columns) != required_columns:
        warnings.append(f"{file_name} column order differs from the configured schema.")

    if invalid_codes > 0:
        errors.append(f"Found {invalid_codes} invalid or empty occupation codes.")
    if duplicate_rows > 0:
        warnings.append(f"Found {duplicate_rows} duplicate rows.")
    if missing_rate > config.get("validation", {}).get("critical_missing_value_rate", 0.20):
        errors.append("Missing-value rate exceeds the critical threshold.")
    elif missing_rate > config.get("validation", {}).get("warn_on_missing_value_rate", 0.02):
        warnings.append("Missing-value rate is above the warning threshold.")

    duplicate_threshold = config.get("onet", {}).get("quality", {}).get("max_duplicate_rate", 0.01)
    duplicate_rate = float(duplicate_rows / len(df)) if len(df) else 0.0
    if duplicate_rate > duplicate_threshold:
        warnings.append(f"Duplicate-row rate {duplicate_rate:.4f} exceeds the configured warning threshold.")

    numeric_ranges = (
        config.get("onet", {})
        .get("quality", {})
        .get("numeric_ranges", {})
    )
    file_ranges = numeric_ranges.get(
        "essential_skills" if file_name == "essential_skills.csv" else
        "task_statements" if file_name == "task_statements.csv" else "",
        {},
    )
    for column, (minimum, maximum) in file_ranges.items():
        if column not in df.columns:
            continue
        numeric = pd.to_numeric(df[column], errors="coerce")
        if minimum is not None:
            below = int((numeric.dropna() < float(minimum)).sum())
            if below:
                warnings.append(f"{below} values in {column} are below {minimum}.")
        if maximum is not None:
            above = int((numeric.dropna() > float(maximum)).sum())
            if above:
                warnings.append(f"{above} values in {column} exceed {maximum}.")

    return {
        "dataset_name": file_name,
        "status": "pass" if not errors else "fail",
        "warnings": warnings,
        "errors": errors,
        "summary": {
            "rows": len(df),
            "columns": list(df.columns),
            "invalid_occupation_codes": invalid_codes,
            "duplicate_rows": duplicate_rows,
            "missing_value_rate": round(missing_rate, 6),
        },
    }
