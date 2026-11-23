from __future__ import annotations

import json
import re
from difflib import SequenceMatcher
from pathlib import Path

import pandas as pd


def normalize_category_label(value: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", " ", str(value).lower()).strip()
    return " ".join(cleaned.split())


def build_category_to_occupation_mapping(kaggle_categories: list[str], occupation_titles: list[str], similarity_threshold: float = 0.30, max_candidates: int = 5) -> dict:
    """Generate a transparent, rule-based similarity mapping between Kaggle categories and O*NET occupation titles.

    This is not a verified ground-truth mapping. It is a proposal that can be reviewed manually before any ML task.
    """
    mappings: list[dict] = []
    for category in kaggle_categories:
        normalized_category = normalize_category_label(category)
        candidates = []
        for title in occupation_titles:
            score = SequenceMatcher(None, normalized_category, normalize_category_label(title)).ratio()
            candidates.append({"occupation_title": title, "similarity": round(float(score), 4)})
        ranked = sorted(candidates, key=lambda item: item["similarity"], reverse=True)[:max_candidates]
        best = ranked[0]["similarity"] if ranked else 0.0
        mapping = {
            "kaggle_category": category,
            "best_similarity": round(float(best), 4),
            "proposed_matches": ranked,
            "status": "exact" if best >= 0.75 else "probable" if best >= similarity_threshold else "unmatched",
            "threshold": similarity_threshold,
        }
        mappings.append(mapping)

    exact_count = sum(1 for item in mappings if item["status"] == "exact")
    probable_count = sum(1 for item in mappings if item["status"] == "probable")
    unmatched_count = sum(1 for item in mappings if item["status"] == "unmatched")

    return {
        "category_count": len(kaggle_categories),
        "occupation_count": len(occupation_titles),
        "proposed_mappings": exact_count + probable_count,
        "unmatched_categories": unmatched_count,
        "exact_mappings": exact_count,
        "probable_mappings": probable_count,
        "mappings": mappings,
    }


def generate_alignment_report(kaggle_csv_path: str | Path, onet_csv_path: str | Path, output_json: str | Path, output_md: str | Path, threshold: float = 0.30) -> dict:
    """Generate a multimodal alignment report.

    The report is intentionally non-authoritative: it highlights possible semantic relationships but does not assert a verified candidate-level alignment.
    """
    kaggle_df = pd.read_csv(kaggle_csv_path, encoding="utf-8-sig")
    onet_df = pd.read_csv(onet_csv_path, encoding="utf-8-sig")
    kaggle_categories = sorted(kaggle_df["Category"].dropna().astype(str).unique().tolist())
    occupation_titles = sorted(onet_df["Title"].dropna().astype(str).unique().tolist())

    mapping = build_category_to_occupation_mapping(kaggle_categories, occupation_titles, similarity_threshold=threshold, max_candidates=5)

    report = {
        "source": "Kaggle CV categories vs O*NET occupation titles",
        "methodology": "Rule-based text similarity using normalized strings and SequenceMatcher. No automatic candidate-level mapping is assumed or validated.",
        "threshold": threshold,
        "number_of_kaggle_categories": len(kaggle_categories),
        "number_of_onet_occupations": len(occupation_titles),
        "proposed_mappings": mapping["proposed_mappings"],
        "unmatched_categories": mapping["unmatched_categories"],
        "ambiguous_cases": [item for item in mapping["mappings"] if item["status"] in {"probable", "unmatched"}],
        "exact_mappings": mapping["exact_mappings"],
        "probable_mappings": mapping["probable_mappings"],
        "mapping_method": "SequenceMatcher over normalized labels",
        "limitations": [
            "The mapping is based on semantic similarity between category labels and occupation titles only.",
            "A CV is not automatically linked to a specific O*NET occupation without manual validation or a reliable candidate-level schema.",
            "Similarity does not imply ground truth or a causal relationship.",
        ],
        "recommendations": [
            "Keep Kaggle labels as-is and treat all O*NET links as exploratory only.",
            "If a later task creates a verified structured modality, re-run the mapping with candidacy-level evidence.",
            "Use this report as a starting point for human review, not as a source of labels.",
        ],
        "mappings": mapping["mappings"],
    }

    output_path = Path(output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, ensure_ascii=False)

    markdown_lines = [
        "# Rapport d'alignement multimodal",
        "",
        f"- Catégories Kaggle: {len(kaggle_categories)}",
        f"- Occupations O*NET: {len(occupation_titles)}",
        f"- Mappages proposés: {mapping['proposed_mappings']}",
        f"- Catégories non appariées: {mapping['unmatched_categories']}",
        "",
        "## Méthodologie",
        "",
        report["methodology"],
        "",
        "## Limites",
        "",
        *[f"- {limit}" for limit in report["limitations"]],
        "",
        "## Mappages les plus probables",
        "",
    ]

    for item in mapping["mappings"][:10]:
        markdown_lines.append(f"### {item['kaggle_category']}")
        markdown_lines.append(f"- Statut: {item['status']}")
        markdown_lines.append(f"- Meilleure similarité: {item['best_similarity']}")
        for candidate in item["proposed_matches"][:3]:
            markdown_lines.append(f"- {candidate['occupation_title']} ({candidate['similarity']})")
        markdown_lines.append("")

    Path(output_md).parent.mkdir(parents=True, exist_ok=True)
    with Path(output_md).open("w", encoding="utf-8") as handle:
        handle.write("\n".join(markdown_lines))

    return report


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    generate_alignment_report(
        root / "data" / "interim" / "kaggle" / "resumes.csv",
        root / "data" / "interim" / "onet" / "occupations.csv",
        root / "reports" / "multimodal_alignment_report.json",
        root / "reports" / "multimodal_alignment_report.md",
        threshold=0.30,
    )


if __name__ == "__main__":
    main()
