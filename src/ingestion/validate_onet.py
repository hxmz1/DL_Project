
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
REPORT_DIR = ROOT / "reports"
LOG_DIR = ROOT / "logs"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "onet_consistency.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
)

FILES = {
    "occupations": "occupation_data.csv",
    "software": "software_skills.csv",
    "essential": "essential_skills.csv",
    "tasks": "task_statements.csv",
}


def load_csv(filename):
    path = RAW_DIR / filename

    if not path.exists():
        raise FileNotFoundError(f"Fichier absent : {path}")

    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return pd.read_csv(path, encoding=encoding)
        except UnicodeDecodeError:
            continue

    raise ValueError(f"Encodage impossible à déterminer : {filename}")


def normalized(series):
    """Normalise les chaînes pour comparer les identifiants et titres."""
    return series.astype("string").str.strip()


def main():
    logging.info("Début de la validation de cohérence O*NET")

    occupations = load_csv(FILES["occupations"])
    software = load_csv(FILES["software"])
    essential = load_csv(FILES["essential"])
    tasks = load_csv(FILES["tasks"])

    code_col = "O*NET-SOC Code"
    title_col = "Title"

    # Normalisation en mémoire uniquement : aucun CSV brut modifié.
    for df in (occupations, software, essential, tasks):
        df[code_col] = normalized(df[code_col])
        df[title_col] = normalized(df[title_col])

    # --------------------------------------------------
    # 1. Référentiel des métiers
    # --------------------------------------------------

    occupation_codes = set(occupations[code_col].dropna())

    duplicate_occupation_codes = int(
        occupations.duplicated(subset=[code_col]).sum()
    )

    missing_codes = {}
    unknown_codes = {}
    title_mismatches = {}

    related_files = {
        "software_skills": software,
        "essential_skills": essential,
        "task_statements": tasks,
    }

    occupation_titles = (
        occupations.dropna(subset=[code_col])
        .drop_duplicates(subset=[code_col])
        .set_index(code_col)[title_col]
    )

    for name, df in related_files.items():
        missing_codes[name] = int(df[code_col].isna().sum())

        codes_in_file = set(df[code_col].dropna())
        unknown = sorted(codes_in_file - occupation_codes)

        unknown_codes[name] = {
            "count": len(unknown),
            "examples": unknown[:20],
        }

        # Un même code métier doit normalement avoir un titre cohérent.
        comparison = df[[code_col, title_col]].dropna().copy()
        comparison["reference_title"] = (
            comparison[code_col].map(occupation_titles)
        )

        mismatches = comparison[
            comparison["reference_title"].notna()
            & (
                comparison[title_col]
                != comparison["reference_title"]
            )
        ]

        title_mismatches[name] = {
            "rows": len(mismatches),
            "examples": mismatches.head(10).to_dict(
                orient="records"
            ),
        }

    # --------------------------------------------------
    # 2. Doublons sur des clés métier pertinentes
    # --------------------------------------------------

    duplicate_keys = {
        "occupations_by_code": duplicate_occupation_codes,
        "software_by_code_element_example": int(
            software.duplicated(
                subset=[
                    code_col,
                    "Element ID",
                    "Workplace Example",
                ]
            ).sum()
        ),
        "essential_by_code_element_scale": int(
            essential.duplicated(
                subset=[code_col, "Element ID", "Scale ID"]
            ).sum()
        ),
        "tasks_by_task_id": int(
            tasks.duplicated(subset=["Task ID"]).sum()
        ),
        "tasks_by_code_task_text": int(
            tasks.duplicated(subset=[code_col, "Task"]).sum()
        ),
    }

    # --------------------------------------------------
    # 3. Statistiques complémentaires
    # --------------------------------------------------

    report = {
        "source": "O*NET Database",
        "generated_at_utc": datetime.now(
            UTC
        ).isoformat(),
        "occupation_count": len(occupations),
        "unique_occupation_codes": int(
            occupations[code_col].nunique()
        ),
        "files": {
            name: len(df)
            for name, df in {
                "occupations": occupations,
                **related_files,
            }.items()
        },
        "missing_occupation_codes": missing_codes,
        "unknown_occupation_codes": unknown_codes,
        "title_mismatches": title_mismatches,
        "duplicate_keys": duplicate_keys,
        "essential_scale_distribution": {
            str(key): int(value)
            for key, value in essential[
                "Scale ID"
            ].value_counts(dropna=False).items()
        },
        "status": "completed",
    }

    output = REPORT_DIR / "onet_consistency_report.json"

    with output.open("w", encoding="utf-8") as file:
        json.dump(
            report,
            file,
            ensure_ascii=False,
            indent=2,
        )

    logging.info("Rapport généré : %s", output)

    print("\n=== VALIDATION DE COHÉRENCE O*NET ===")
    print("Codes métiers uniques :", report["unique_occupation_codes"])

    print("\nCodes métiers inconnus :")
    for name, result in unknown_codes.items():
        print(f"  {name}: {result['count']}")

    print("\nIncohérences de titres :")
    for name, result in title_mismatches.items():
        print(f"  {name}: {result['rows']}")

    print("\nDoublons sur clés métier :")
    for name, count in duplicate_keys.items():
        print(f"  {name}: {count}")

    print("\nRapport enregistré :", output)


if __name__ == "__main__":
    try:
        main()
    except (FileNotFoundError, ValueError, KeyError) as exc:
        logging.exception("Échec de la validation")
        print(f"Erreur : {exc}")
        raise SystemExit(1)
