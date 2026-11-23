from __future__ import annotations

import argparse
import json
from typing import Any

import pandas as pd

from src.alignment.occupation_alignment import generate_alignment_report
from src.common.config import PROJECT_ROOT, load_config
from src.preprocessing.text_preprocessing import (
    prepare_kaggle_text_dataset,
    prepare_onet_structured_dataset,
)
from src.validation.data_quality import (
    validate_kaggle_dataframe,
    validate_onet_dataframe,
)


def run_kaggle_ingestion(config: dict[str, Any]) -> dict[str, Any]:
    """Run the Kaggle ingestion stage using the existing script."""
    from src.ingestion.ingest_kaggle import main as kaggle_main

    kaggle_main()
    kaggle_path = PROJECT_ROOT / config["paths"]["interim"]["kaggle_csv"]
    return {"status": "success", "output": str(kaggle_path)}


def run_onet_stages(config: dict[str, Any]) -> dict[str, Any]:
    """Run O*NET ingestion, validation and preparation using the existing scripts."""
    from src.ingestion.ingest_onet import main as onet_ingest_main
    from src.ingestion.prepare_onet import main as onet_prepare_main
    from src.ingestion.validate_onet import main as onet_validate_main

    onet_ingest_main()
    onet_validate_main()
    onet_prepare_main()
    return {"status": "success", "outputs": [
        str(PROJECT_ROOT / "reports" / "onet_ingestion_report.json"),
        str(PROJECT_ROOT / "reports" / "onet_consistency_report.json"),
        str(PROJECT_ROOT / "reports" / "onet_preparation_report.json"),
    ]}


def run_quality_validation(config: dict[str, Any]) -> dict[str, Any]:
    kaggle_path = PROJECT_ROOT / config["paths"]["interim"]["kaggle_csv"]
    onet_dir = PROJECT_ROOT / config["paths"]["interim"]["onet_dir"]

    kaggle_df = pd.read_csv(kaggle_path, encoding="utf-8-sig")
    kaggle_report = validate_kaggle_dataframe(kaggle_df, config)

    onet_reports = {}
    for name, fn in {
        "occupation_data.csv": onet_dir / "occupations.csv",
        "software_skills.csv": onet_dir / "software_skills.csv",
        "essential_skills.csv": onet_dir / "essential_skills.csv",
        "task_statements.csv": onet_dir / "task_statements.csv",
    }.items():
        onet_df = pd.read_csv(fn, encoding="utf-8-sig")
        onet_reports[name] = validate_onet_dataframe(onet_df, name, config)

    return {"status": "success", "kaggle": kaggle_report, "onet": onet_reports}


def run_preprocessing(config: dict[str, Any]) -> dict[str, Any]:
    kaggle_input = PROJECT_ROOT / config["paths"]["interim"]["kaggle_csv"]
    processed_dir = PROJECT_ROOT / config["paths"]["processed"]["text_dir"]
    kaggle_summary = prepare_kaggle_text_dataset(kaggle_input, processed_dir)

    onet_dir = PROJECT_ROOT / config["paths"]["interim"]["onet_dir"]
    structured_dir = PROJECT_ROOT / config["paths"]["processed"]["structured_dir"]
    onet_summaries = {}
    for file_name in ["occupations.csv", "software_skills.csv", "essential_skills.csv", "task_statements.csv"]:
        onet_summaries[file_name] = prepare_onet_structured_dataset(onet_dir / file_name, structured_dir)

    return {"status": "success", "kaggle": kaggle_summary, "onet": onet_summaries}


def run_alignment(config: dict[str, Any]) -> dict[str, Any]:
    kaggle_path = PROJECT_ROOT / config["paths"]["interim"]["kaggle_csv"]
    onet_path = PROJECT_ROOT / config["paths"]["interim"]["onet_dir"] / "occupations.csv"
    report_path = PROJECT_ROOT / config["alignment"]["report_path"]
    markdown_path = PROJECT_ROOT / config["alignment"]["markdown_path"]
    report = generate_alignment_report(kaggle_path, onet_path, report_path, markdown_path, threshold=config["alignment"].get("similarity_threshold", 0.30))
    return {"status": "success", "report": report}


def build_summary_report(results: dict[str, Any]) -> dict[str, Any]:
    summary = {"pipeline": "candidate_screening", "stages": results}
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the DataOps pipeline for the multimodal candidate-screening project.")
    parser.add_argument("--config", type=str, default="configs/params.yaml", help="Project configuration YAML file")
    parser.add_argument("--quick", action="store_true", help="Run pipeline with reduced validation scope.")
    parser.add_argument("--synthetic", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()

    if args.synthetic:
        raise SystemExit("Synthetic raw-data generation is prohibited. Use tests/fixtures/ only.")

    config = load_config(args.config)
    if args.quick:
        config["pipeline"]["quick_mode"] = True

    required_raw = [
        PROJECT_ROOT / config["paths"]["raw"]["kaggle_csv"],
        *[
            PROJECT_ROOT / value
            for value in config["onet"]["raw_files"].values()
        ],
    ]
    missing_raw = [str(path.relative_to(PROJECT_ROOT)) for path in required_raw if not path.is_file()]
    if missing_raw:
        raise SystemExit("Critical error: required raw files are missing: " + ", ".join(missing_raw))

    stages = {
        "kaggle_ingestion": lambda: run_kaggle_ingestion(config),
        "onet": lambda: run_onet_stages(config),
        "validation": lambda: run_quality_validation(config),
        "preprocessing": lambda: run_preprocessing(config),
        "alignment": lambda: run_alignment(config),
    }

    results: dict[str, Any] = {}
    for stage_name, stage_runner in stages.items():
        results[stage_name] = stage_runner()
        if stage_name == "validation":
            validation = results[stage_name]
            failed = validation["kaggle"]["status"] == "fail"
            failed = failed or any(report["status"] == "fail" for report in validation["onet"].values())
            if failed:
                raise SystemExit("Critical data validation failure; pipeline stopped. See validation reports and logs.")

    summary = build_summary_report(results)
    report_path = PROJECT_ROOT / "reports" / "pipeline_summary.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with report_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, ensure_ascii=False)

    print("\n=== PIPELINE DATAOPS OK ===")
    print(f"Rapport global: {report_path}")
    print("Command: python -m src.pipeline.run_pipeline")


if __name__ == "__main__":
    main()
