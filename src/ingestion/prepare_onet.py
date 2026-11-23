
import hashlib
import json
import logging
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

# --------------------------------------------------
# Configuration
# --------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw" / "onet"
INTERIM_DIR = ROOT / "data" / "interim" / "onet"
REPORT_DIR = ROOT / "reports"
LOG_DIR = ROOT / "logs"

INTERIM_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "prepare_onet.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
)

# Fichier source -> fichier intermédiaire
FILES = {
    "occupation_data.csv": "occupations.csv",
    "software_skills.csv": "software_skills.csv",
    "essential_skills.csv": "essential_skills.csv",
    "task_statements.csv": "task_statements.csv",
}

# --------------------------------------------------
# Fonctions utilitaires
# --------------------------------------------------

def read_csv_safely(path):
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return pd.read_csv(path, encoding=encoding)
        except UnicodeDecodeError:
            continue

    raise ValueError(f"Encodage non reconnu : {path.name}")


def sha256_file(path):
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def clean_text_columns(df):
    """Nettoie les espaces sans supprimer les lignes."""
    for column in df.select_dtypes(include=["object", "string"]).columns:
        df[column] = df[column].map(
            lambda value: value.strip()
            if isinstance(value, str)
            else value
        )

    return df


def prepare_file(source_name, output_name):
    source_path = RAW_DIR / source_name
    output_path = INTERIM_DIR / output_name

    if not source_path.exists():
        raise FileNotFoundError(
            f"Fichier source absent : {source_path}"
        )

    df = read_csv_safely(source_path)
    original_rows = len(df)

    # Contrôle des lignes sans code métier
    code_column = "O*NET-SOC Code"

    if code_column not in df.columns:
        raise ValueError(
            f"Colonne {code_column} absente de {source_name}"
        )

    missing_codes = int(df[code_column].isna().sum())

    # Copie de travail : le fichier brut n'est jamais modifié
    df = clean_text_columns(df.copy())

    # Conversion des colonnes numériques lorsqu'elles existent
    numeric_columns = [
        "Data Value",
        "N",
        "Standard Error",
        "Lower CI Bound",
        "Upper CI Bound",
        "Incumbents Responding",
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column], errors="coerce"
            )

    # Contrôle des doublons exacts, sans suppression automatique
    duplicate_rows = int(df.duplicated().sum())

    # Conservation de toutes les lignes : les anomalies sont signalées
    df.to_csv(
        output_path,
        index=False,
        encoding="utf-8-sig",
    )

    result = {
        "source_file": source_name,
        "source_sha256": sha256_file(source_path),
        "output_file": output_name,
        "output_sha256": sha256_file(output_path),
        "rows_before": int(original_rows),
        "rows_after": len(df),
        "columns": df.columns.tolist(),
        "missing_occupation_codes": missing_codes,
        "duplicate_rows": duplicate_rows,
        "rows_removed": int(original_rows - len(df)),
        "status": "success",
    }

    logging.info(
        "%s préparé : %s lignes",
        source_name,
        len(df),
    )

    return result


def main():
    logging.info("Début de la préparation O*NET")

    results = []
    errors = []

    for source_name, output_name in FILES.items():
        try:
            result = prepare_file(source_name, output_name)
            results.append(result)

            print(
                f"[OK] {source_name} -> {output_name} "
                f"({result['rows_after']} lignes)"
            )

        except (FileNotFoundError, ValueError, OSError) as exc:
            logging.exception(
                "Erreur de préparation : %s", source_name
            )
            errors.append({
                "source_file": source_name,
                "error": str(exc),
            })
            print(f"[ERREUR] {source_name} : {exc}")

    report = {
        "source": "O*NET Database",
        "generated_at_utc": datetime.now(
            UTC
        ).isoformat(),
        "output_directory": str(
            INTERIM_DIR.relative_to(ROOT)
        ),
        "files_successful": len(results),
        "files_failed": len(errors),
        "total_rows_prepared": sum(
            item["rows_after"] for item in results
        ),
        "results": results,
        "errors": errors,
    }

    report_path = REPORT_DIR / "onet_preparation_report.json"

    with report_path.open("w", encoding="utf-8") as file:
        json.dump(
            report,
            file,
            ensure_ascii=False,
            indent=2,
        )

    logging.info(
        "Préparation terminée : %s succès, %s erreurs",
        len(results),
        len(errors),
    )

    print("\n=== BILAN DE PRÉPARATION O*NET ===")
    print("Fichiers préparés :", len(results))
    print("Fichiers en erreur :", len(errors))
    print("Total des lignes :", report["total_rows_prepared"])
    print("Rapport :", report_path)

    if errors:
        raise SystemExit(
            "Préparation incomplète : consulte le rapport et les logs."
        )


if __name__ == "__main__":
    main()
