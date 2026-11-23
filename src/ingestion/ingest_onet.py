
import json
import logging
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

# --------------------------------------------------
# 1. Configuration du projet
# --------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw" / "onet"
REPORT_DIR = ROOT / "reports"
LOG_DIR = ROOT / "logs"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "ingestion_onet.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
)

FILES = {
    "occupation_data.csv": [
        "O*NET-SOC Code", "Title", "Description"
    ],
    "software_skills.csv": [
        "O*NET-SOC Code", "Title", "Workplace Example",
        "Element ID", "Element Name", "Hot Technology",
        "In Demand"
    ],
    "essential_skills.csv": [
        "O*NET-SOC Code", "Title", "Element ID",
        "Element Name", "Scale ID", "Scale Name",
        "Data Value"
    ],
    "task_statements.csv": [
        "O*NET-SOC Code", "Title", "Task ID", "Task", "Task Type"
    ],
}


def read_csv_safely(path):
    """Lit un CSV en essayant plusieurs encodages."""
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return pd.read_csv(path, encoding=encoding)
        except UnicodeDecodeError:
            continue

    raise ValueError(f"Encodage non reconnu : {path.name}")


def inspect_file(filename, required_columns):
    """Vérifie la présence et la qualité d'un fichier."""
    path = RAW_DIR / filename

    if not path.exists():
        raise FileNotFoundError(
            f"Fichier introuvable : {path}"
        )

    df = read_csv_safely(path)

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"{filename} : colonnes absentes : {missing_columns}"
        )

    # Contrôle des identifiants métier
    code_col = "O*NET-SOC Code"
    invalid_codes = (
        df[code_col].isna()
        | df[code_col].astype(str).str.strip().eq("")
    )

    report = {
        "file": filename,
        "size_bytes": path.stat().st_size,
        "rows": len(df),
        "columns_count": len(df.columns),
        "columns": df.columns.tolist(),
        "missing_values_by_column": {
            col: int(count)
            for col, count in df.isna().sum().items()
        },
        "total_missing_values": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "invalid_occupation_codes": int(invalid_codes.sum()),
        "required_columns_present": True,
        "status": "success",
    }

    # Contrôles spécifiques
    if filename == "essential_skills.csv":
        report["scale_distribution"] = {
            str(key): int(value)
            for key, value in
            df["Scale ID"].value_counts(dropna=False).items()
        }

    if filename == "software_skills.csv":
        report["hot_technology_values"] = {
            str(key): int(value)
            for key, value in
            df["Hot Technology"].value_counts(
                dropna=False
            ).items()
        }

    if filename == "task_statements.csv" and "Task Type" in df.columns:
        report["task_type_distribution"] = {
            str(key): int(value)
            for key, value in
            df["Task Type"].value_counts(
                dropna=False
            ).items()
        }
    elif filename == "task_statements.csv":
        report["task_type_distribution"] = {}

    return report


def main():
    logging.info("Début de l'ingestion O*NET")

    results = []
    errors = []

    for filename, required_columns in FILES.items():
        try:
            result = inspect_file(
                filename, required_columns
            )
            results.append(result)

            logging.info(
                "%s : %s lignes, %s doublons",
                filename,
                result["rows"],
                result["duplicate_rows"],
            )

            print(
                f"[OK] {filename} : "
                f"{result['rows']} lignes"
            )

        except (FileNotFoundError, ValueError, OSError) as exc:
            errors.append({
                "file": filename,
                "error": str(exc),
            })
            logging.exception(
                "Échec de vérification de %s",
                filename,
            )
            print(f"[ERREUR] {filename} : {exc}")

    report = {
        "source": "O*NET Database",
        "collection_method": "CSV download",
        "generated_at_utc": datetime.now(
            UTC
        ).isoformat(),
        "files_checked": len(FILES),
        "files_successful": len(results),
        "files_failed": len(errors),
        "total_rows": sum(
            item["rows"] for item in results
        ),
        "results": results,
        "errors": errors,
    }

    report_path = REPORT_DIR / "onet_ingestion_report.json"

    with report_path.open("w", encoding="utf-8") as file:
        json.dump(
            report,
            file,
            indent=2,
            ensure_ascii=False,
        )

    logging.info(
        "Fin de l'ingestion : %s fichiers OK, %s erreurs",
        len(results),
        len(errors),
    )

    print("\nRésumé")
    print("-" * 40)
    print("Fichiers validés :", len(results))
    print("Fichiers en erreur :", len(errors))
    print(
        "Total des lignes :",
        report["total_rows"],
    )
    print("Rapport :", report_path)

    if errors:
        raise SystemExit(
            "Ingestion incomplète : consulter les erreurs."
        )


if __name__ == "__main__":
    main()
