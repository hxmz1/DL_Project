# Multimodal Fusion Literature Review

## Classical fusion levels

Early fusion combines raw or low-level features before one model. It can capture interactions but is sensitive to heterogeneous scales and missing modalities.

Late fusion trains unimodal models and combines predictions. It is robust and interpretable but can miss feature-level interactions.

Intermediate/hybrid fusion aligns learned representations in latent space and adds a fusion head. It is the most defensible candidate for a future paired experiment.

## Mechanisms

| Mechanism | Principle | Advantage | Limitation |
|---|---|---|---|
| Concatenation | Join representations | Simple | Ignores learned interaction structure | [1] |
| Weighted sum/product | Combine logits or representations | Low cost | Requires calibrated scales | [1] |
| GMU | Learns modality gates | Missing-modality adaptation | Can overfit | [4] |
| FiLM | One representation conditions another | Explicit feature modulation | Pairing required | [5] |
| TFN | Cartesian product of representations | Captures high-order interactions | High parameters/cost | [2] |
| LMF | Low-rank TFN approximation | Lower cost than TFN | Approximation loss | [3] |
| MCB/MFB | Bilinear pooling with compact projections | Expressive compact interactions | Tuning and implementation complexity | [1] |
| Cross-attention | Attend modality tokens to each other | Rich token interaction | Compute-heavy | [6] |
| Multimodal Transformers | Joint token sequence | Strong contextual fusion | Large data/hardware | [6] |
| Attention Bottlenecks | Restrict cross-modal exchange through bottleneck tokens | Control over cost | Can discard information | [7] |
| CLIP-like contrastive | Align shared representation spaces | Strong retrieval/alignment | Needs aligned pairs | [8] |
| Graph fusion | Fuse entities/relations | Explicit structure | Graph construction uncertainty | [1] |

## Challenges

- Heterogeneous text and occupational representations
- Semantic rather than verified alignment
- Missing modalities
- Modality imbalance
- Compute cost
- Interpretability
- Candidate-level leakage and invalid pseudo-pairs

## Project-specific conclusion

There is no valid candidate-level ground truth. The first design should be a text-only baseline plus O*NET retrieval context. Intermediate/hybrid fusion becomes appropriate only after verified paired candidate data is available.

## References

[1] T. Baltrušaitis, C. Ahuja, and L.-P. Morency, "Multimodal Machine Learning: A Survey and Taxonomy," IEEE Transactions on Pattern Analysis and Machine Intelligence, 2019.

[2] A. Zadeh, P. P. Liang, S. Poria, E. Cambria, and L.-P. Morency, "Tensor Fusion Network for Multimodal Sentiment Analysis," 2017.

[3] Z. Liu, Y. Shen, V. B. Lakshminarasimhan, P. P. Liang, A. Zadeh, and L.-P. Morency, "Efficient Low-Rank Multimodal Fusion with Modality-Specific Factors," 2018.

[4] J. Arevalo, T. Solorio, M. Montes-y-Gomez, and F. A. Gonzalez, "Gated Multimodal Units for Information Fusion," ICLR Workshop, 2017.

[5] E. Perez, F. Strub, H. de Vries, V. Dumoulin, and A. Courville, "FiLM: Visual Reasoning with a General Conditioning Layer," 2018.

[6] Y.-H. H. Tsai, S. Bai, P. P. Liang, J. Z. Kolter, L.-P. Morency, and R. Salakhutdinov, "Multimodal Transformer for Unaligned Multimodal Language Sequences," 2019.

[7] A. Nagrani, S. Yang, A. Arnab, A. Jansen, C. Schmid, and C. Sun, "Attention Bottlenecks for Multimodal Fusion," 2021.

[8] A. Radford, J. W. Kim, C. Hallacy, A. Ramesh, G. Goh, S. Agarwal, G. Sastry, A. Askell, P. Mishkin, J. Clark, G. Krueger, and I. Sutskever, "Learning Transferable Visual Models from Natural Language Supervision," 2021.

[9] D. Kreuzberger, N. Kühl, and S. Hirschl, "Machine Learning Operations (MLOps): Overview, Definition, and Architecture," IEEE Access, 2023.

[10] Official documentation: DVC (`dvc.org`), Great Expectations, and GitHub Actions.
