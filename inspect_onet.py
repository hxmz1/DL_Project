
from pathlib import Path
import pandas as pd

DATA_DIR = Path("data/raw/onet")

files = [
    "occupation_data.csv",
    "software_skills.csv",
    "essential_skills.csv",
    "task_statements.csv",
]

for filename in files:
    path = DATA_DIR / filename

    print("\n" + "=" * 70)
    print(f"FICHIER : {filename}")
    print("=" * 70)

    if not path.exists():
        print("ERREUR : fichier introuvable :", path)
        continue

    try:
        df = pd.read_csv(path, encoding="utf-8-sig")
    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding="latin-1")

    print("Dimensions :", df.shape)
    print("Colonnes :", df.columns.tolist())
    print("\nAperçu :")
    print(df.head(3).to_string(index=False))
    print("\nValeurs manquantes :")
    print(df.isna().sum().to_string())
    print("\nLignes dupliquées :", df.duplicated().sum())
