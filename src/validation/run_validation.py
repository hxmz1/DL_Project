from __future__ import annotations

import json

import pandas as pd

from src.common.config import PROJECT_ROOT, load_config
from src.common.observability import StageRecorder, write_stage_report
from src.validation.data_quality import (
    validate_kaggle_dataframe,
    validate_onet_dataframe,
)


def main() -> None:
    config = load_config()
    kaggle_path = PROJECT_ROOT / config["paths"]["interim"]["kaggle_csv"]
    onet_dir = PROJECT_ROOT / config["paths"]["interim"]["onet_dir"]
    outputs = [str(PROJECT_ROOT / "reports" / "data_quality_report.json")]
    recorder = StageRecorder(
        "data_validation",
        inputs=[str(kaggle_path), str(onet_dir)],
        outputs=outputs,
    )

    kaggle = pd.read_csv(kaggle_path, encoding="utf-8-sig")
    kaggle_report = validate_kaggle_dataframe(kaggle, config)

    onet_reports: dict[str, dict] = {}
    onet_missing = 0
    onet_duplicates = 0
    for name, filename in {
        "occupation_data.csv": "occupations.csv",
        "software_skills.csv": "software_skills.csv",
        "essential_skills.csv": "essential_skills.csv",
        "task_statements.csv": "task_statements.csv",
    }.items():
        frame = pd.read_csv(onet_dir / filename, encoding="utf-8-sig")
        report = validate_onet_dataframe(frame, name, config)
        onet_reports[name] = report
        onet_missing += int(frame.isna().sum().sum())
        onet_duplicates += int(frame.duplicated().sum())

    failed = kaggle_report["status"] == "fail" or any(
        report["status"] == "fail" for report in onet_reports.values()
    )
    report = {
        "status": "fail" if failed else "pass",
        "kaggle": kaggle_report,
        "onet": onet_reports,
        "totals": {
            "kaggle_missing_values": int(kaggle.isna().sum().sum()),
            "kaggle_duplicate_rows": int(kaggle.duplicated().sum()),
            "onet_missing_values": onet_missing,
            "onet_duplicate_rows": onet_duplicates,
        },
    }
    quality_path = PROJECT_ROOT / "reports" / "data_quality_report.json"
    quality_path.parent.mkdir(parents=True, exist_ok=True)
    with quality_path.open("w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, ensure_ascii=False)

    stage_report = recorder.finish(
        input_rows=len(kaggle),
        output_rows=len(kaggle),
        missing_values=int(kaggle.isna().sum().sum()) + onet_missing,
        duplicate_rows=int(kaggle.duplicated().sum()) + onet_duplicates,
        warnings=[
            warning
            for report in [kaggle_report, *onet_reports.values()]
            for warning in report.get("warnings", [])
        ],
        errors=[
            error
            for report in [kaggle_report, *onet_reports.values()]
            for error in report.get("errors", [])
        ],
        status="failed" if failed else "success",
    )
    write_stage_report(PROJECT_ROOT / "reports" / "stage_validation_report.json", stage_report)
    if failed:
        raise SystemExit("Critical data validation failure.")


if __name__ == "__main__":
    main()
