# Recommandation de stratégie de fusion

## Contexte du projet

- Kaggle : 2 484 CV, 24 catégories, texte libre et labels de catégorie.
- O*NET : 1 016 occupations, compétences, tâches et descriptions.
- Les deux datasets ne se chevauchent pas nécessairement au niveau candidat.
- Le référentiel O*NET est un contexte métier précieux mais pas une source de vérité de terrain pour chaque CV.

## Recommandation

La meilleure stratégie est une fusion intermédiaire (hybrid fusion) avec :

1. branche texte sur les CV,
2. branche structurée si une modalité candidate-level fiable est créée,
3. projection latente commune,
4. fusion légère par concaténation ou attention simple,
5. tête de classification multi-classes.

## Pourquoi elle est la meilleure ici

- Elle permet de conserver l'information textuelle sans dépendre trop de l'alignement brut des modalités.
- Elle offre un plan d'extension clair pour des features tabulaires plus tard.
- Elle reste plus réaliste que des architectures plus lourdes quand les données candidate-level sont absentes.

## Alternatives

- Early fusion : simple, mais sensible aux différences de distribution et d'alignement.
- Late fusion : robuste et interprétable, mais moins efficace pour apprendre des interactions entre modalités.

## Limitation méthodologique importante

Une vraie fusion multimodale de qualité exige un niveau de données candidat alignées, ou un schéma explicite de mapping validé. À ce stade, O*NET sert de référence métier, pas de vérité terrain pour chaque CV.
