# TASK 3 - DataOps Pipeline and Multimodal Fusion Study

## 1. Introduction

The project is a DataOps preparation study for Candidate Screening AI. It uses Kaggle resume text (2,484 records, 24 labels) and the O*NET occupational database (69,875 records across four files). No candidate-level Kaggle/O*NET pairing is available.

## 2. Data sources and recovery

The Kaggle archive and O*NET CSV files were validated from `C:\Users\Asus\Desktop\data-dl`, a read-only source. The Kaggle member `Resume/Resume.csv` is 2,484 x 4 and has 24 categories. The O*NET file dimensions are 1,016; 31,821; 18,200; and 18,838 rows. Destination hashes match source hashes. Synthetic raw fixtures discovered by the audit were backed up before replacement.

## 3. DataOps architecture

Raw data is ingested without modification, copied to interim datasets, validated, preprocessed, aligned in an explicitly exploratory stage, and exported to reports and prepared datasets. DVC stages make the sequence reproducible. A critical validation failure stops the pipeline.

```text
Read-only source -> raw recovery -> ingestion -> validation -> preprocessing -> alignment -> reports
```

## 4. Tools and justification

Python 3.11, pandas, PyYAML, pytest, DVC, Ruff, and ReportLab were used. Pandas is appropriate for these tabular datasets; PyYAML centralizes configuration; pytest provides fixture tests; DVC provides artifact versioning; Ruff supplies linting; ReportLab exports the report.

## 5. Quality tests and CI

The pipeline verified Kaggle unique IDs, schema, missing values, duplicate rows, and 24 categories. O*NET validation verified schemas, SOC patterns, referential integrity, occupation titles, and duplicate keys. Passing and corrupt fixtures cover both expected outcomes. CI is fixture-only and does not claim GitHub execution.

The candidate split uses fixed seed 42, candidate IDs and normalized resume text as non-overlap units. It writes train, validation and test CSV files plus a statistics JSON under `data/processed/splits/`. Rare categories are explicitly handled; duplicate IDs or duplicate text across splits cause validation failure.

## 6. Fusion literature review

Early fusion concatenates or combines features before the model. It is simple but sensitive to missing modalities and scaling. Late fusion combines unimodal predictions and is robust to missing modalities but weak at cross-modal interactions. Intermediate/hybrid fusion learns modality representations and fuses them in latent space.

Concatenation is simple and interpretable. Weighted sums/products are efficient but assume comparable probability or representation scales. GMU gates modalities; FiLM conditions one representation on another. TFN and LMF capture high-order interactions with different computational costs. MCB/MFB provide compact bilinear pooling. Cross-attention and multimodal transformers support rich token-level interactions. Attention bottlenecks and CLIP-like contrastive alignment improve controlled cross-modal exchange or shared embeddings. Graph fusion represents entities and relations but adds labeling and graph-construction risk.

## 7. Comparative table

| Approach | Principle | Advantages | Limitations | Conditions | References |
|---|---|---|---|---|---|
| Early fusion | Concatenate/merge features | Simple, low latency | Alignment, scaling, missing modalities | Aligned low-volume data | [1] |
| Late fusion | Combine unimodal outputs | Robust, interpretable | Weak cross-modal interaction | Independent modalities | [1] |
| Intermediate | Fuse latent representations | Rich interactions | Higher tuning cost | Defensible paired samples | [1] |
| GMU/FiLM | Gating or conditioning | Adaptive information flow | Potential overfitting | Sufficient paired data | [4], [5] |
| TFN/LMF/MCB/MFB | Bilinear/compact tensors | Expressive interaction | Tensor cost or approximation | Moderate hardware/data | [2], [3], [1] |
| Cross-attention/Transformers | Cross-modal token attention | Strong interaction | Data/hardware intensive | Large paired corpora | [6] |
| Bottlenecks/CLIP | Limited exchange or contrastive shared space | Efficient or aligned | Requires suitable pairing | Retrieval/alignment studies | [7], [8] |
| Graph fusion | Relational graph | Explicit occupational structure | Complex construction | Verified entities/relations | [1] |

## 8. Project-specific fusion choice

The Kaggle dataset provides rich text and 2,484 labels. O*NET provides occupational descriptions, skills, and tasks but is not candidate-specific. Therefore, O*NET should be an auxiliary knowledge/retrieval source, not a direct second candidate feature table, until verified candidate-level alignment exists.

The project-specific recommendation is not a large transformer fusion system. Use a text-only baseline, a retrieval-augmented O*NET context experiment, and late/intermediate fusion only after a validated structured candidate modality is available.

## 9. Proposed architecture

Candidate text is encoded as `h_t = TextEncoder(x_t)`, projected to `z_t = W_t h_t + b_t`. Optional structured features are encoded as `h_s = MLP(x_s)`, projected to `z_s = W_s h_s + b_s`. The fusion baseline computes `z = [z_t; z_s]` or a gated combination `z = g⊙z_t +(1-g)⊙z_s`. The classifier produces `p(y|x)=softmax(W_c z+b_c)`.

The text branch uses a compact pretrained transformer such as DistilBERT, with 512-token truncation or chunked pooling. A frozen encoder is used for the first experiment, and the final transformer block plus projection may be fine-tuned with a lower learning rate.

The O*NET branch normalizes descriptions, skills and tasks by SOC code and embeds them through TF-IDF for a transparent baseline or a dense sentence encoder for retrieval. A CV retrieves top-k occupations; retrieved text is auxiliary context and is not candidate ground truth.

Cross-entropy is the primary supervised loss. Auxiliary losses may include contrastive candidate/context alignment and graph regularization, but only with verified pairs. Missing modalities use modality masks and a text-only fallback. Evaluate against text-only and late-fusion baselines, not headline fusion metrics alone.

## 10. Evaluation protocol

Candidate IDs must never cross train/validation/test splits. A 70/15/15 split with random seed 42 and stratification is specified. Metrics include accuracy, macro-F1, per-class precision/recall, confusion matrices, and calibration. Ablations remove the O*NET context, structured branch, and fusion gate. No model metrics are reported here because no model was trained.

## 11. Integration plan

The future model package should accept a preprocessed candidate table and a retrieved O*NET context table. It should return probabilities and retrieval evidence, log data provenance, and preserve missing-modality masks. Experiment tracking should record seed, split, encoder, fusion mechanism, hardware, metrics, and ablations.

## 12. Implementation evidence

The normal pipeline, DVC reproduction, DVC local push, and pytest suite were executed successfully. The DVC local remote stored 23 files. Ruff fixes and linting were applied. Git is initialized locally, but GitHub push and GitHub Actions execution are blocked on authorization and remote setup.

## 13. References

## References

[1] T. Baltrušaitis, C. Ahuja, and L.-P. Morency, "Multimodal Machine Learning: A Survey and Taxonomy," IEEE TPAMI, 2019.

[2] A. Zadeh et al., "Tensor Fusion Network for Multimodal Sentiment Analysis," EMNLP, 2017.

[3] Z. Liu et al., "Efficient Low-Rank Multimodal Fusion with Modality-Specific Factors," ACL, 2018.

[4] J. Arevalo et al., "Gated Multimodal Units for Information Fusion," ICLR Workshop, 2017.

[5] E. Perez et al., "FiLM: Visual Reasoning with a General Conditioning Layer," AAAI, 2018.

[6] Y.-H. H. Tsai et al., "Multimodal Transformer for Unaligned Multimodal Language Sequences," ACL, 2019.

[7] A. Nagrani et al., "Attention Bottlenecks for Multimodal Fusion," NeurIPS, 2021.

[8] A. Radford et al., "Learning Transferable Visual Models from Natural Language Supervision," ICML, 2021.

[9] D. Kreuzberger, N. Kühl, and S. Hirschl, "Machine Learning Operations (MLOps): Overview, Definition, and Architecture," IEEE Access, 2023.

[10] Official documentation: DVC (`dvc.org`), Great Expectations, and GitHub Actions.
