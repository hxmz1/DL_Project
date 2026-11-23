# Plan de mise en œuvre Task 3

## Objectif

Mettre en place un pipeline DataOps reproductible, structuré, testé et documenté autour des données Kaggle et O*NET, puis préparer le cadre théorique et technique pour la fusion multimodale.

## Étapes

1. Créer la configuration centralisée `configs/params.yaml` et le chargeur associé.
2. Organiser le projet en modules `validation`, `preprocessing`, `alignment`, `fusion`, `pipeline`.
3. Préserver les scripts Task 2 existants et les utiliser dans le pipeline sans les écraser.
4. Ajouter des tests `pytest` sur les points de qualité de données.
5. Implémenter la préparation textuelle et les sorties `data/processed/`.
6. Créer l'alignement catégoriel Kaggle/O*NET avec score explicite et limites documentées.
7. Générer les rapports d'analyse et de recommandation sur la fusion multimodale.
8. Ajouter les fichiers DVC, la CI GitHub Actions et le Makefile de secours.
9. Exécuter le pipeline localement et vérifier les sorties.
10. Rédiger le rapport final `reports/TASK3_IMPLEMENTATION_REPORT.md`.

## Livrables attendus

- `configs/params.yaml`
- modules Python réutilisables dans `src/`
- `tests/` avec cas PASS et FAIL
- `reports/` avec audits, études et rapports
- `data/processed/` prêt pour des expériences futures
- `dvc.yaml`, `.dvcignore`, `.github/workflows/ci.yml`
- `Makefile` de secours si DVC est bloqué
- `reports/TASK3_IMPLEMENTATION_REPORT.md`

## Règles de mise en œuvre

- Ne pas modifier les fichiers bruts originaux.
- Conserver les sorties Task 2 existantes.
- Utiliser des chemins relatifs et des paramètres configurables.
- Documenter explicitement les limitations d'alignement et de fusion.
- Ne pas faire de promesse de vérité de terrain là où il n'y a pas de relation vérifiée.

## Critères de succès

- Les scripts existants continuent à fonctionner.
- Les nouveaux tests passent.
- Un pipeline orchestré fonctionne depuis la racine du dépôt.
- Les rapports générés correspondent aux exécutions réelles.
- Les limites méthodologiques sont clairement décrites.
