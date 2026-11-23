from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = PROJECT_ROOT / "configs" / "params.yaml"


def load_config(path: str | Path | None = None) -> dict[str, Any]:
    """Load the YAML configuration file from the project root."""
    config_file = Path(path) if path is not None else CONFIG_PATH
    if not config_file.exists():
        raise FileNotFoundError(f"Configuration not found: {config_file}")

    with config_file.open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle) or {}

    if not isinstance(payload, dict):
        raise ValueError(f"Configuration root must be a dictionary: {config_file}")

    return payload


def resolve_path(value: str | Path | None, *, root: Path | None = None) -> Path:
    """Resolve a project-relative path and keep it reproducible."""
    if value is None:
        return root if root is not None else PROJECT_ROOT

    candidate = Path(value)
    if candidate.is_absolute():
        return candidate

    base = root if root is not None else PROJECT_ROOT
    return base / candidate
