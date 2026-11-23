# Audit de l'intégrité des données après la mise en œuvre de Task 3

## 1. Objectif

Vérifier, en lecture seule, si les jeux de données réels de Task 2 sont toujours présents ou s'ils ont été remplacés par des fixtures synthétiques.

Ce document ne modifie ni n'écrit aucun fichier de données. Il se limite à l'inspection des fichiers existants et du code.

## 2. Dimensions attendues de Task 2

Les données réelles attendues selon le contexte historique de Task 2 étaient :

- Kaggle `Resume.csv`: 2,484 lignes, 4 colonnes
- O*NET `occupation_data.csv`: 1,016 lignes
- O*NET `software_skills.csv`: 31,821 lignes
- O*NET `essential_skills.csv`: 18,200 lignes
- O*NET `task_statements.csv`: 18,838 lignes

## 3. Dimensions actuelles des fichiers sous data/raw et data/interim

### 3.1 `data/raw/`

| Fichier | Lignes | Colonnes | Taille du fichier |
|---|---:|---:|---:|
| `data/raw/kaggle/extracted/Resume/Resume.csv` | 3 | 4 | 325 octets |
| `data/raw/onet/occupation_data.csv` | 2 | 3 | 159 octets |
| `data/raw/onet/software_skills.csv` | 2 | 7 | 227 octets |
| `data/raw/onet/essential_skills.csv` | 2 | 7 | 207 octets |
| `data/raw/onet/task_statements.csv` | 2 | 5 | 223 octets |

### 3.2 `data/interim/`

| Fichier | Lignes | Colonnes | Taille du fichier |
|---|---:|---:|---:|
| `data/interim/kaggle/resumes.csv` | 3 | 4 | 325 octets |
| `data/interim/onet/occupations.csv` | 2 | 3 | 159 octets |
| `data/interim/onet/software_skills.csv` | 2 | 7 | 227 octets |
| `data/interim/onet/essential_skills.csv` | 2 | 7 | 207 octets |
| `data/interim/onet/task_statements.csv` | 2 | 5 | 223 octets |

## 4. Contenu réel observé dans les CSV actuels

### Kaggle RAW actual

Le fichier `data/raw/kaggle/extracted/Resume/Resume.csv` contient exactement :

```csv
﻿ID,Resume_str,Resume_html,Category
1,Python developer with backend skills and data analysis experience.,<p>Python</p>,INFORMATION-TECHNOLOGY
2,Data engineer with ETL SQL pipelines and cloud deployment.,<p>Data</p>,BUSINESS-DEVELOPMENT
3,Project manager with leadership and stakeholder communication.,<p>Project</p>,HR
```

### O*NET RAW actual

Le fichier `data/raw/onet/occupation_data.csv` contient exactement :

```csv
﻿O*NET-SOC Code,Title,Description
15-1252.00,Software Developers,Design software systems.
11-9199.09,"Managers, All Other",Coordinate teams and projects.
```

Les autres fichiers O*NET raw ont la même logique : 2 lignes seulement, avec des valeurs minimales et artificielles.

## 5. Classification des datasets : réel vs synthétique

### 5.1 Données synthétiques confirmées

Les fichiers actuels sont clairement des fixtures synthétiques, car :

- `Resume.csv` contient seulement 3 CV.
- `occupation_data.csv` contient seulement 2 occupations.
- Chaque fichier O*NET contient seulement 2 lignes.
- Les données du `Kaggle` et du `O*NET` sont cohérentes avec des exemples de démonstration : champs très simples, très peu de lignes, pas les volumes historiques attendus.

### 5.2 Absence de preuves de conservation du dataset historique Task 2

Aucune copie des dimensions réelles de Task 2 n'est présente dans `data/raw/` ou `data/interim/`.

Les dossiers actuels ne montrent pas un dataset historique de 2,484 + 69,875 lignes. Les dimensions actuelles correspondent à des fixtures de test, pas aux données réelles précédemment validées.

## 6. Comparaison avec les dimensions attendues de Task 2

| Dataset | Attendu | Actuel | Écart |
|---|---:|---:|---:|
| Kaggle Resume | 2,484 | 3 | -2,481 |
| O*NET occupation_data | 1,016 | 2 | -1,014 |
| O*NET software_skills | 31,821 | 2 | -31,819 |
| O*NET essential_skills | 18,200 | 2 | -18,198 |
| O*NET task_statements | 18,838 | 2 | -18,836 |

## 7. Fichiers synthétiques présents et emplacements exacts

Les fichiers synthétiques sont présents aux emplacements suivants :

- `data/raw/kaggle/extracted/Resume/Resume.csv`
- `data/raw/onet/occupation_data.csv`
- `data/raw/onet/software_skills.csv`
- `data/raw/onet/essential_skills.csv`
- `data/raw/onet/task_statements.csv`
- `data/interim/kaggle/resumes.csv`
- `data/interim/onet/occupations.csv`
- `data/interim/onet/software_skills.csv`
- `data/interim/onet/essential_skills.csv`
- `data/interim/onet/task_statements.csv`

Aucune autre copie des datasets historiques Task 2 n'a été trouvée dans les dossiers `data/raw/` et `data/interim/` que nous avons inspectés.

## 8. Vérification du code responsable des fixtures synthétiques

Le code responsable de la génération des fixtures synthétiques se trouve dans :

- [src/pipeline/run_pipeline.py](../src/pipeline/run_pipeline.py)

Les zones clé sont :

1. `ensure_synthetic_data_if_needed(force: bool = False)`
   - Cette fonction crée explicitement des DataFrames de petite taille et les écrit dans `data/raw/...`.
   - Elle remplace les fichiers CSV de raw lorsque `--synthetic` est utilisé.

2. `main()`
   - Le paramètre `--synthetic` active la création des fixtures.
   - Le code exécute :

```python
if args.synthetic:
    ensure_synthetic_data_if_needed(force=True)
```

3. Les fichiers de sortie des DataFrames synthétiques sont écrits avec `to_csv(..., index=False, encoding="utf-8-sig")` dans :
   - `data/raw/kaggle/extracted/Resume/Resume.csv`
   - `data/raw/onet/occupation_data.csv`
   - `data/raw/onet/software_skills.csv`
   - `data/raw/onet/essential_skills.csv`
   - `data/raw/onet/task_statements.csv`

Le code montre que les fixtures synthétiques sont bien conçues pour remplacer les CSV de raw dans le mode `--synthetic`.

## 9. Le pipeline normal remplace-t-il les raw data ?

### Réponse courte : non, pas dans le code de `ingest_kaggle.py` et `prepare_onet.py`

Les scripts de Task 2 lisent les fichiers raw et écrivent dans `data/interim/...`, sans écraser les raw files.

Le code de pipeline `run_pipeline.py` ne provoque pas automatiquement l'écriture sur raw lors d'un run normal sans `--synthetic`.

En revanche, le mode `--synthetic` est explicitement conçu pour créer des données de test dans `data/raw` et donc pour remplacer la source réelle si l'utilisateur l'exécute.

## 10. Risque de perte de données / écrasement accidentel

Oui, il existe un risque réel de perte de données si le mode `--synthetic` est exécuté sur un dépôt qui contenait encore les vraies données :

- la fonction `ensure_synthetic_data_if_needed(force=True)` écrit directement dans les fichiers raw CSV,
- l'option `--synthetic` est activable depuis la ligne de commande,
- il n'y a pas de garde-fou explicite qui exige une confirmation avant écrasement.

Cela constitue un risque d'écrasement accidentel des données si l'on exécute la commande suivante :

```powershell
python -m src.pipeline.run_pipeline --synthetic --quick
```

## 11. Conclusion: l'état des données réelles

Les données historiques Task 2 ne sont pas intactes dans l'état actuel du dépôt observable. Les fichiers `data/raw` et `data/interim` contiennent des fixtures synthétiques de petite taille, et la dimension actuelle ne correspond pas du tout aux valeurs précédemment documentées.

## 12. Recommandations

1. Sauvegarder immédiatement toute copie originale connue hors du dépôt.
2. Vérifier si les datasets réels existent ailleurs dans le système, indépendamment de ce projet.
3. Ne jamais exécuter `--synthetic` sur une copie qui peut contenir des données réelles.
4. Introduire une protection explicite dans le code :
   - refuser la génération synthétique si les raw files réels existent déjà,
   - exiger une confirmation explicite avant écrasement,
   - séparer les fixtures de test dans un dossier dédié comme `tests/fixtures/`.
5. Si la vraie donnée doit être restaurée, la réimporter à partir d'une source de vérité indépendante et non à partir de `data/interim/` tant que les raw originaux sont absents.

## 13. Verdict

FAIL: Original datasets were replaced or modified.

Les preuves disponibles sont suffisantes pour conclure que les jeux de données historiques Task 2 n'ont pas été conservés dans leur état original dans le dépôt actuel. Les fichiers `data/raw` et `data/interim` contiennent des données synthétiques au lieu des datasets réels attendus.
