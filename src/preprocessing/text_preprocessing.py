from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def normalize_whitespace(value: object) -> object:
    if isinstance(value, str):
        return " ".join(value.strip().split())
    return value


def prepare_kaggle_text_dataset(source_path: str | Path, output_dir: str | Path) -> dict:
    """Prepare a text-only Kaggle dataset without altering the raw or interim sources."""
    source = Path(source_path)
    output_root = Path(output_dir)
    output_root.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(source, encoding="utf-8-sig")
    prepared = df.copy()
    prepared["Resume_str"] = prepared["Resume_str"].map(normalize_whitespace)
    prepared["Resume_html"] = prepared["Resume_html"].map(normalize_whitespace)
    prepared["Category"] = prepared["Category"].map(lambda value: value.strip() if isinstance(value, str) else value)

    text_csv = output_root / "kaggle_text_preprocessed.csv"
    prepared.to_csv(text_csv, index=False, encoding="utf-8-sig")

    summary = {
        "source_file": str(source),
        "output_file": str(text_csv),
        "rows": len(prepared),
        "columns": list(prepared.columns),
        "blank_resume_texts": int(prepared["Resume_str"].fillna("").astype(str).str.strip().eq("").sum()),
        "category_count": int(prepared["Category"].nunique(dropna=False)),
    }

    summary_path = output_root / "kaggle_text_summary.json"
    with summary_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, ensure_ascii=False)

    return summary


def prepare_onet_structured_dataset(source_path: str | Path, output_dir: str | Path) -> dict:
    """Create a structured summary for O*NET data that keeps the original files unchanged."""
    source = Path(source_path)
    output_root = Path(output_dir)
    output_root.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(source, encoding="utf-8-sig")
    summary = {
        "source_file": str(source),
        "rows": len(df),
        "columns": list(df.columns),
        "missing_values": {col: int(value) for col, value in df.isna().sum().items()},
        "duplicate_rows": int(df.duplicated().sum()),
    }

    summary_path = output_root / f"{source.stem}_structured_summary.json"
    with summary_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, ensure_ascii=False)

    return summary


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    kaggle_input = root / "data" / "interim" / "kaggle" / "resumes.csv"
    processed_text = root / "data" / "processed" / "text"
    prepare_kaggle_text_dataset(kaggle_input, processed_text)

    onet_input = root / "data" / "interim" / "onet"
    structured_output = root / "data" / "processed" / "structured"
    for filename in [
        "occupations.csv",
        "software_skills.csv",
        "essential_skills.csv",
        "task_statements.csv",
    ]:
        prepare_onet_structured_dataset(onet_input / filename, structured_output)


if __name__ == "__main__":
    main()
