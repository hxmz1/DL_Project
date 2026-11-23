from __future__ import annotations

from pathlib import Path

FUSION_APPROACHES = [
    {"name": "Early Fusion", "principle": "Concatenate raw or embedded features before prediction.", "advantages": "Simple and fast.", "limitations": "Sensitive to modality mismatch and scaling.", "use_case": "Small, aligned, structured datasets."},
    {"name": "Late Fusion", "principle": "Train separate models and combine their outputs.", "advantages": "Robust to missing modalities.", "limitations": "May ignore cross-modal interactions.", "use_case": "When modalities are independent and model-specific."},
    {"name": "Intermediate / Hybrid Fusion", "principle": "Fuse learned representations at a shared latent space.", "advantages": "Captures cross-modal interactions while preserving modality-specific signal.", "limitations": "More complex and harder to tune.", "use_case": "Best suited for multimodal text + structured metadata."},
]


def build_fusion_study_markdown(output_path: str | Path) -> str:
    lines = [
        "# Étude de la fusion multimodale",
        "",
        "## Approches classiques",
        "",
        "| Approche | Principe | Avantages | Limites | Cas d'usage |",
        "|---|---|---|---|---|",
    ]
    for approach in FUSION_APPROACHES:
        lines.append(f"| {approach['name']} | {approach['principle']} | {approach['advantages']} | {approach['limitations']} | {approach['use_case']} |")

    lines += [
        "",
        "## Recommandation pour ce projet",
        "",
        "Le projet contient un corpus textuel Kaggle (CV) et un référentiel métier O*NET. Les deux sources ne sont pas automatiquement alignées au niveau candidat, et O*NET est actuellement un référentiel professionnel, pas une source de vérité de terrain pour chaque CV. Dans ce contexte, la stratégie la plus prudente est une fusion intermédiaire ou hybride à partir de représentations apprises, avec un fallback robuste au cas où un sous-ensemble de modalités est absent.",
        "",
        "L'early fusion est utile comme baseline simple, mais il est plus sensible aux écarts de schéma et à la qualité de l'alignement. Le late fusion est plus robuste et interprétable, mais il est moins capable de capturer les interactions multimodales. L'intermediate fusion offre le meilleur compromis technique si un alignement fiable et un niveau candidat structuré deviennent disponibles.",
        "",
        "## Conclusion",
        "",
        "Pour l'instant, il faut considérer la fusion comme une architecture préparée pour des futures expérimentations, pas comme un modèle entraîné. La stratégie recommandée est une architecture de fusion hybride avec modèle de texte et branche structurée éventuellement ajoutée plus tard.",
    ]

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")
    return str(output)


def build_strategy_recommendation(output_path: str | Path) -> str:
    content = """# Recommandation de stratégie de fusion

## Contexte

- Kaggle : 2 484 CV, 24 catégories, texte libre.
- O*NET : 1 016 occupations, compétences, tâches et descriptions professionnelles.
- Les deux jeux ne partagent pas de relation candidate-level vérifiée.
- Le référentiel O*NET est utile pour l'analyse sémantique et le contexte métier, mais il ne remplace pas une vérité terrain sur le candidat.

## Recommandation

La stratégie recommandée est une fusion intermédiaire (hybrid fusion), avec:

1. un encodeur de texte pour les CV,
2. une branche structurée optionnelle lorsque des features candidate-level fiables existent,
3. une couche de projection commune,
4. un mécanisme de fusion par concaténation de représentations ou par attention simple,
5. une tête de classification multi-classes.

## Pourquoi pas les alternatives ?

- Early fusion : plus simple, mais sensible à la qualité de l'alignement et à la variabilité du texte.
- Late fusion : robuste aux modalités manquantes et facile à interpréter, mais moins capable d'apprendre des interactions multimodales.

## Limitation importante

Avant d'entraîner un vrai modèle multimodal, il faut créer une modalité structurée fiable au niveau candidat (par exemple, caractéristiques extraites du CV ou un schéma d'alignement métier vérifié). Sans cela, la fusion ne repose pas sur des données réellement alignées.
"""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")
    return str(output)


def build_architecture_proposal(output_path: str | Path) -> str:
    content = """# Proposition d'architecture de fusion

## 1. Architecture cible

La proposition la plus réaliste pour ce projet est une architecture de fusion hybride avec deux branches :

- branche textuelle : encodeur de texte transformant un CV en représentation latente,
- branche structurée : MLP sur des variables tabulaires si elles sont disponibles plus tard,
- couche de fusion : concaténation ou attention légère pour combiner les représentations,
- tête de classification : couche linéaire + softmax pour les 24 catégories Kaggle.

## 2. Encodage

- Texte : modèle de langue pré-entraîné (ex. distilBERT ou modèle de type transformer compact) sur des CV.
- Structuré : MLP sur variables dérivées, si un schéma candidat est disponible.

## 3. Forme mathématique

Soit h_text et h_struct les représentations latentes, alors :

z = [h_text ; h_struct]

ou, de manière plus expressive :

z = W_t h_text + W_s h_struct + b

p(y | x) = softmax(W_c z + b_c)

## 4. Pseudocode

```python
text_repr = text_encoder(cv_tokens)
struct_repr = mlp(structured_features)
combined = concat(text_repr, struct_repr)
logits = classifier(combined)
probs = softmax(logits)
loss = cross_entropy(probs, labels)
```

## 5. Baselines recommandés

- Text-only baseline.
- Structured-only baseline lorsque des features fiables existent.
- Early fusion baseline simple.
- Late fusion baseline robuste.

## 6. Métriques

- Accuracy
- Precision / Recall / F1
- Macro-F1
- Confusion matrix
- PR-AUC si classes déséquilibrées

## 7. Limites de cette architecture

Cette proposition n'est pas un modèle entraîné. Elle sert à préparer l'implémentation future et à justifier le design sans inventer de vérité terrain.
"""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")
    return str(output)
