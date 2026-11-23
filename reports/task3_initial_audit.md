# Audit initial de la tâche 3

## 1. Structure existante

Le dépôt contient actuellement :

- `README.md`
- `requirements.txt`
- `inspect_onet.py`
- `src/ingestion/` avec les scripts Task 2
- `data/raw/` contenant les jeux de données bruts Kaggle et O*NET
- `data/interim/` contenant les versions préparées
- `logs/` et `reports/` déjà alimentés
- un dossier virtuel `.venv/` local

## 2. Scripts existants

- `src/ingestion/ingest_kaggle.py` : ingestion du CSV Kaggle, vérification schéma, calcul de l'empreinte SHA256, génération d'un rapport JSON.
- `src/ingestion/ingest_onet.py` : contrôle d'intégrité de chaque fichier O*NET.
- `src/ingestion/validate_onet.py` : cohérence métier entre occupations, compétences et tâches.
- `src/ingestion/prepare_onet.py` : préparation des CSV O*NET sans suppression des lignes, uniquement nettoyage et normalisation.

## 3. Fichiers de données disponibles

### Kaggle
- `data/raw/kaggle/extracted/Resume/Resume.csv`
- 2 484 lignes, 4 colonnes, 24 catégories.
- Données déjà validées et reportées.
- `data/interim/kaggle/resumes.csv` est présent.

### O*NET
- `data/raw/onet/occupation_data.csv`
- `data/raw/onet/software_skills.csv`
- `data/raw/onet/essential_skills.csv`
- `data/raw/onet/task_statements.csv`
- `data/interim/onet/` contient les 4 CSV préparés.

## 4. Dépendances et environnement

- Python 3.11 détecté.
- `requirements.txt` ne contient actuellement que `pandas>=2.2,<3.0`.
- `PyYAML` et `pytest` ne sont pas installés dans l'environnement actuel.
- `dvc` n'est pas installé dans ce poste.
- Le dépôt n'est pas un dépôt Git initialisé (`git rev-parse --show-toplevel` a échoué).

## 5. Travaux Task 2 déjà accomplis

Les étapes de validation et préparation O*NET ont déjà été exécutées avec succès :

- 4 fichiers O*NET validés.
- 0 codes métiers inconnus.
- 0 incohérences de titres.
- 0 doublons sur les clés métier retenues.
- 69 875 lignes conservées.
- Ingestion Kaggle validée : 2 484 lignes, 24 catégories, 0 identifiants dupliqués.

## 6. Écarts par rapport à la tâche 3

Les éléments manquants ou incomplets sont :

- structure modulaire projet (ingestion / validation / preprocessing / alignment / fusion / pipeline)
- configuration centralisée dans `configs/params.yaml`
- tests automatisés `pytest`
- pipeline DVC / orchestration reproductible
- validation des données généralisée avec seuils configurables
- module d'alignement entre catégories Kaggle et occupations O*NET
- préparation des données traitées dans `data/processed/`
- rapport de Data Card, fusion study et stratégie de fusion
- CI GitHub Actions
- rapport final `reports/TASK3_IMPLEMENTATION_REPORT.md`

## 7. Risques et incohérences constatés

- Le dépôt n'est pas un dépôt Git ; la gestion de version doit être signalée comme non initialisée.
- DVC n'est pas disponible dans l'environnement actuel ; il faudra soit l'installer, soit documenter le blocage et utiliser un Makefile de secours.
- Les scripts Task 2 sont encore dans un seul sous-package `src/ingestion` et ne sont pas organisés par étapes fonctionnelles.
- Il n'existe pas aujourd'hui de validation explicite des erreurs critiques vs warnings.
- Il n'existe pas de module d'alignement multimodal vérifiable entre les catégories Kaggle et l'ontologie O*NET.
- Le suivi de données volumineuses et la CI doivent être ajoutés sans modifier les données brutes originales.

## 8. Conclusion

Le socle technique de Task 2 est fonctionnel et les données brutes / intermédiaires sont déjà présentes. La prochaine étape consiste à organiser le projet en modules réutilisables, externaliser la configuration, ajouter des tests, automatiser le pipeline et documenter le point de vue multimodal avec des limites explicites.
