# Precise Future Fusion Architecture Proposal

## Status

This is an architecture proposal only. It is not implemented, trained, or evaluated.

## Diagram

```text
CV text -> Text encoder -> h_t -> W_t -> z_t
Optional structured candidate features -> MLP -> h_s -> W_s -> z_s
z_t, z_s -> gated/concatenation fusion -> classifier -> class probabilities
O*NET retrieval context -> auxiliary encoder/context -> optional text conditioning
```

## Dimensions

- Text encoder output: `h_t ∈ R^768`
- Projected text: `z_t ∈ R^256`
- Structured vector: `x_s ∈ R^d_s`
- Projected structured: `z_s ∈ R^128`
- Concatenated vector: `z ∈ R^(384)`
- Gated vector: `z ∈ R^256`
- Kaggle outputs: 24 classes

## Concrete text branch

- Encoder: `distilbert-base-uncased` or a compact multilingual transformer only if French/English coverage is measured.
- Tokenization: WordPiece/SentencePiece from the selected pretrained tokenizer.
- Maximum sequence length: 512 tokens; overflow is chunked and mean-pooled.
- Strategy: freeze the encoder for a first baseline, then fine-tune the final transformer block and projection with a lower learning rate.
- Text representation: `[CLS]` or masked mean pooling; projected from 768 dimensions to 256 dimensions.

## O*NET knowledge branch

O*NET descriptions, software skills, essential skills and tasks are normalized and grouped by SOC code. For a future CV/O*NET study, the encoder is used to embed these normalized occupational documents. Retrieval is lexical TF-IDF plus dense cosine ranking. Retrieved contexts are labeled exploratory unless manual or verified candidate-level evidence exists.

The context vector is the weighted mean of the top-k O*NET document embeddings (or attention-pooling), then projected to 128 dimensions. It is never treated as a candidate label or a supervised candidate feature.

## Retrieval semantics

For each CV, encode the preprocessed text and rank O*NET occupations. The result is context for retrieval, interpretability or an auxiliary contrastive study. It does not create candidate-to-occupation ground truth. Supervised paired fusion requires an external verified mapping or an employer-reviewed label.

## Equations

`h_t = TextEncoder(x_t)`

`z_t = W_t h_t + b_t`

`h_s = MLP(x_s)`

`z_s = W_s h_s + b_s`

Concatenation:

`z = [z_t || z_s]`

Gated:

`g = sigmoid(W_g [z_t || z_s] + b_g)`

`z = g ⊙ z_t + (1-g) ⊙ z_s`

Prediction:

`p(y|x_t,x_s) = softmax(W_c z+b_c)`

## Pseudocode

```text
text_repr = text_encoder(cv_text)
text_latent = text_projection(text_repr)
if structured_features_available:
    struct_latent = mlp(structured_features)
    fused = concat(text_latent, struct_latent)
else:
    fused = text_latent
logits = classifier(fused)
return softmax(logits)
```

## Training

Use cross-entropy, AdamW, seed 42, candidate-ID group splits, early stopping, macro-F1 model selection, and class weighting only after measuring distribution. A verified O*NET contrastive auxiliary loss may be added for aligned pairs.

## Missing modalities

Use modality masks and text-only fallback. Never fill a missing candidate feature with a fabricated O*NET assignment.

## Modality balance

If paired data becomes available, modality dropout removes the O*NET context with probability 0.2. The gate is trained with both modalities while remaining usable on text-only batches. A class-balanced loss may be used only after measuring the supported split distribution. Modality contribution is measured by gate activation, ablation, and unimodal/fusion performance deltas.

## Baselines and ablations

- Text-only model
- Structured-only model
- Late-fusion model
- Simple concatenation baseline
- Gated intermediate baseline
- Ablations removing O*NET context and structured branches

## Evaluation

Use candidate-ID holdout splits; accuracy, macro-F1, per-class precision/recall, calibration, confusion matrices, leakage checks, and runtime/memory records.
