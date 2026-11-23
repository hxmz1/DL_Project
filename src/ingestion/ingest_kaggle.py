
import hashlib
import json
import logging
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

# ==================================================
# 1. CONFIGURATION
# ==================================================

ROOT = Path(__file__).resolve().parents[2]

RAW_FILE = (
    ROOT / "data" / "raw" / "kaggle"
    / "extracted" / "Resume" / "Resume.csv"
)

INTERIM_DIR = ROOT / "data" / "interim" / "kaggle"
REPORT_DIR = ROOT / "reports"
LOG_DIR = ROOT / "logs"

OUTPUT_FILE = INTERIM_DIR / "resumes.csv"
REPORT_FILE = REPORT_DIR / "kaggle_ingestion_report.json"

for directory in (INTERIM_DIR, REPORT_DIR, LOG_DIR):
    directory.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "ingestion_kaggle.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
)

REQUIRED_COLUMNS = [
    "ID",
    "Resume_str",
    "Resume_html",
    "Category",
]


# ==================================================
# 2. UTILITAIRES
# ==================================================

def sha256_file(path):
    """Calcule l'empreinte SHA-256 d'un fichier."""
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def load_csv(path):
    """Lit le CSV en essayant plusieurs encodages."""
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return pd.read_csv(path, encoding=encoding)
        except UnicodeDecodeError:
            continue

    raise ValueError("Impossible de déterminer l'encodage du CSV.")


# ==================================================
# 3. INGESTION ET VALIDATION
# ==================================================

def main():
    logging.info("Début de l'ingestion Kaggle")

    if not RAW_FILE.exists():
        raise FileNotFoundError(
            f"Dataset introuvable : {RAW_FILE}"
        )

    source_hash = sha256_file(RAW_FILE)
    df = load_csv(RAW_FILE)

    # Vérification du schéma
    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Colonnes obligatoires absentes : {missing_columns}"
        )

    rows_before = len(df)

    # Contrôles de qualité sans supprimer de lignes
    blank_text = (
        df["Resume_str"].isna()
        | df["Resume_str"].astype("string").str.strip().eq("").fillna(True)
    )

    blank_category = (
        df["Category"].isna()
        | df["Category"].astype("string").str.strip().eq("").fillna(True)
    )

    missing_ids = (
        df["ID"].isna()
        | df["ID"].astype("string").str.strip().eq("").fillna(True)
    )

    duplicate_ids = int(
        df["ID"].duplicated(keep=False).sum()
    )

    duplicate_rows = int(df.duplicated().sum())

    # Profil des catégories
    category_counts = {
        str(category): int(count)
        for category, count in
        df["Category"].value_counts(dropna=False).items()
    }

    # Longueur du texte des CV
    text_lengths = df["Resume_str"].fillna("").astype(str).str.len()

    # Copie de travail : suppression des espaces superflus
    # aux extrémités des champs textuels, sans retirer de lignes.
    prepared = df.copy()

    for column in ["Resume_str", "Resume_html", "Category"]:
        prepared[column] = prepared[column].map(
            lambda value: value.strip()
            if isinstance(value, str)
            else value
        )

    prepared.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8-sig",
    )

    # Rapport d'ingestion
    report = {
        "source": "Kaggle Resume Dataset",
        "source_file": str(RAW_FILE.relative_to(ROOT)),
        "source_sha256": source_hash,
        "generated_at_utc": datetime.now(
            UTC
        ).isoformat(),
        "rows_before": int(rows_before),
        "rows_after": len(prepared),
        "columns": df.columns.tolist(),
        "missing_values_by_column": {
            column: int(count)
            for column, count in df.isna().sum().items()
        },
        "blank_resume_texts": int(blank_text.sum()),
        "blank_categories": int(blank_category.sum()),
        "missing_ids": int(missing_ids.sum()),
        "duplicate_ids": duplicate_ids,
        "exact_duplicate_rows": duplicate_rows,
        "unique_ids": int(df["ID"].nunique()),
        "unique_categories": int(df["Category"].nunique()),
        "category_distribution": category_counts,
        "resume_text_length": {
            "min": int(text_lengths.min()),
            "median": float(text_lengths.median()),
            "mean": round(float(text_lengths.mean()), 2),
            "max": int(text_lengths.max()),
        },
        "rows_removed": int(rows_before - len(prepared)),
        "output_file": str(OUTPUT_FILE.relative_to(ROOT)),
        "output_sha256": sha256_file(OUTPUT_FILE),
        "status": "success",
    }

    with REPORT_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            report,
            file,
            ensure_ascii=False,
            indent=2,
        )

    logging.info(
        "Ingestion terminée : %s lignes, %s catégories",
        len(prepared),
        df["Category"].nunique(),
    )

    print("\n=== RAPPORT D'INGESTION KAGGLE ===")
    print("Fichier source :", RAW_FILE)
    print("Dimensions :", df.shape)
    print("Catégories :", df["Category"].nunique())
    print("CV avec texte vide :", int(blank_text.sum()))
    print("Catégories vides :", int(blank_category.sum()))
    print("Identifiants manquants :", int(missing_ids.sum()))
    print("Identifiants présents dans plusieurs lignes :", duplicate_ids)
    print("Lignes exactement dupliquées :", duplicate_rows)
    print("Lignes conservées :", len(prepared))
    print("Fichier intermédiaire :", OUTPUT_FILE)
    print("Rapport JSON :", REPORT_FILE)

    print("\nRépartition par catégorie :")
    for category, count in category_counts.items():
        print(f"  {category}: {count}")

    print("\n[OK] Ingestion terminée.")


if __name__ == "__main__":
    try:
        main()
    except (FileNotFoundError, ValueError, OSError) as exc:
        logging.exception("Échec de l'ingestion Kaggle")
        print(f"[ERREUR] {exc}")
        raise SystemExit(1)
