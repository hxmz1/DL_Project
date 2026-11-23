from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter
from typing import Any


def stage_observation(
    stage_name: str,
    *,
    inputs: list[str],
    outputs: list[str],
    input_rows: int | None = None,
    output_rows: int | None = None,
    missing_values: int | None = None,
    duplicate_rows: int | None = None,
    rejected_records: int = 0,
    warnings: list[str] | None = None,
    errors: list[str] | None = None,
    status: str = "success",
) -> dict[str, Any]:
    return {
        "stage": stage_name,
        "start_timestamp": datetime.now(UTC).isoformat(),
        "end_timestamp": datetime.now(UTC).isoformat(),
        "duration_seconds": 0.0,
        "inputs": inputs,
        "outputs": outputs,
        "input_rows": input_rows,
        "output_rows": output_rows,
        "missing_values": missing_values,
        "duplicate_rows": duplicate_rows,
        "rejected_records": rejected_records,
        "warnings": warnings or [],
        "errors": errors or [],
        "status": status,
    }


class StageRecorder:
    def __init__(
        self,
        stage_name: str,
        *,
        inputs: list[str],
        outputs: list[str],
    ) -> None:
        self.stage_name = stage_name
        self.inputs = inputs
        self.outputs = outputs
        self.started_at = datetime.now(UTC)
        self.started_perf = perf_counter()

    def finish(
        self,
        *,
        input_rows: int | None = None,
        output_rows: int | None = None,
        missing_values: int | None = None,
        duplicate_rows: int | None = None,
        rejected_records: int = 0,
        warnings: list[str] | None = None,
        errors: list[str] | None = None,
        status: str = "success",
    ) -> dict[str, Any]:
        ended_at = datetime.now(UTC)
        return {
            "stage": self.stage_name,
            "start_timestamp": self.started_at.isoformat(),
            "end_timestamp": ended_at.isoformat(),
            "duration_seconds": round(perf_counter() - self.started_perf, 6),
            "inputs": self.inputs,
            "outputs": self.outputs,
            "input_rows": input_rows,
            "output_rows": output_rows,
            "missing_values": missing_values,
            "duplicate_rows": duplicate_rows,
            "rejected_records": rejected_records,
            "warnings": warnings or [],
            "errors": errors or [],
            "status": status,
        }


def write_stage_report(output_path: str | Path, report: dict[str, Any]) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, ensure_ascii=False)
