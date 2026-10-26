#!/usr/bin/env python3
"""Prioritize annotated variants using the project-defined scoring rules."""

from pathlib import Path

import pandas as pd


# Define the project input and output paths.
PROJECT_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_DIR / "input" / "final_annotation_with_VEP.tsv"
OUTPUT_DIR = PROJECT_DIR / "results" / "tables"
OUTPUT_FILE = OUTPUT_DIR / "prioritized_variants.tsv"


# Define the scoring weights specified in the project rubric.
CLINVAR_SCORES = {
    "pathogenic": 5,
    "likely_pathogenic": 4,
    "benign": -4,
    "likely_benign": -4,
}

IMPACT_SCORES = {
    "HIGH": 4,
    "MODERATE": 2,
}

RARE_AF_THRESHOLD = 0.001
LOW_AF_THRESHOLD = 0.01


def is_missing(value):
    """Identify missing values and unavailable frequency records."""
    if pd.isna(value):
        return True

    return str(value).strip().upper() in {
        "", ".", "NA", "N/A", "NOT_FOUND"
    }


def normalize_text(value):
    """Normalize text values for consistent matching."""
    if is_missing(value):
        return ""

    return str(value).strip().lower().replace(" ", "_")


def get_clinvar_score(clnsig):
    """Score only an unambiguous ClinVar classification."""
    significance = normalize_text(clnsig)

    # Do not score conflicting clinical interpretations.
    if "conflicting" in significance:
        return 0

    # Match the complete normalized classification to avoid substring collisions.
    if significance in CLINVAR_SCORES:
        return CLINVAR_SCORES[significance]

    return 0


def get_impact_score(impact):
    """Return the score associated with the VEP impact."""
    if is_missing(impact):
        return 0

    return IMPACT_SCORES.get(str(impact).strip().upper(), 0)


def get_allele_frequency(row):
    """Return the highest available gnomAD allele frequency."""
    available_frequencies = []

    # Inspect genome and exome allele-frequency columns.
    for column in ("GNOMAD_GENOME_AF", "GNOMAD_EXOME_AF"):
        if column not in row.index or is_missing(row[column]):
            continue

        try:
            frequency = float(row[column])
        except (TypeError, ValueError):
            continue

        # Accept only valid allele frequencies.
        if 0 <= frequency <= 1:
            available_frequencies.append(frequency)

    # Missing frequency information must not be interpreted as zero.
    if not available_frequencies:
        return None

    # Use the highest observed frequency to avoid overstating rarity.
    return max(available_frequencies)


def get_frequency_score(frequency):
    """Calculate the rarity score when a usable frequency is available."""
    if frequency is None:
        return pd.NA

    if frequency < RARE_AF_THRESHOLD:
        return 2

    if frequency <= LOW_AF_THRESHOLD:
        return 1

    return 0


def has_conflicting_interpretations(row):
    """Detect explicit conflicts without matching no_conflicts."""
    for column in ("CLNSIG", "CLNREVSTAT"):
        value = normalize_text(row.get(column, ""))

        # A no-conflicts statement must not trigger a penalty.
        if "no_conflicts" in value or "no_conflict" in value:
            continue

        if "conflicting" in value:
            return True

    return False


def get_priority_category(score):
    """Assign an educational priority category using project thresholds."""
    if score >= 8:
        return "High educational priority"
    if score >= 4:
        return "Intermediate educational priority"
    if score >= 0:
        return "Low or uncertain educational priority"
    return "Likely low educational priority"


def build_evidence_summary(row):
    """Summarize available annotations without inventing evidence."""
    items = []

    for column, label in (
        ("CLNSIG", "ClinVar"),
        ("CLNREVSTAT", "ClinVar review status"),
        ("VEP_MANE_IMPACT", "VEP impact"),
        ("VEP_MANE_CONSEQUENCE", "Consequence"),
    ):
        value = row.get(column, "")
        if not is_missing(value):
            items.append(f"{label}: {str(value).strip()}")

    frequency = row.get("gnomAD_AF_Used", pd.NA)
    if is_missing(frequency):
        items.append("gnomAD AF unavailable")
    else:
        items.append(f"gnomAD AF used: {frequency}")

    return "; ".join(items) if items else "No evidence fields available"


def score_variant(row):
    """Calculate transparent educational prioritization-score components."""
    clinvar_score = get_clinvar_score(row.get("CLNSIG", ""))
    impact_score = get_impact_score(row.get("VEP_MANE_IMPACT", ""))
    frequency = get_allele_frequency(row)
    frequency_score = get_frequency_score(frequency)

    # Apply the project-defined penalty for explicit conflicting interpretations.
    conflict_penalty = (
        -2 if has_conflicting_interpretations(row) else 0
    )

    # Sum the project-defined scoring components.
    frequency_points = 0 if pd.isna(frequency_score) else frequency_score
    total_score = (
        clinvar_score
        + impact_score
        + frequency_points
        + conflict_penalty
    )

    # Return individual components so the score can be audited.
    return pd.Series({
        "ClinVar_Score": clinvar_score,
        "Impact_Score": impact_score,
        "Frequency_Score": frequency_score,
        "Conflict_Penalty": conflict_penalty,
        "Prioritization_Score": total_score,
        "gnomAD_AF_Used": (
            frequency if frequency is not None else pd.NA
        ),
        "ACMG_AMP_Review_Status": "NOT_INDEPENDENTLY_CLASSIFIED",
    })


def main():
    """Read annotations, score variants, and save ranked results."""

    # Verify that the expected input file exists.
    if not INPUT_FILE.is_file():
        raise FileNotFoundError(
            f"Input file not found: {INPUT_FILE}"
        )

    # Read the tab-separated annotation table.
    data = pd.read_csv(INPUT_FILE, sep="\t", dtype=str)

    # Check that all required scoring columns are available.
    required_columns = [
        "CLNSIG",
        "CLNREVSTAT",
        "VEP_MANE_IMPACT",
        "GNOMAD_GENOME_AF",
        "GNOMAD_EXOME_AF",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            "Required columns are missing: "
            + ", ".join(missing_columns)
        )

    # Calculate scores for every variant.
    score_columns = data.apply(score_variant, axis=1)

    # Combine the original annotations and calculated scores.
    results = pd.concat([data, score_columns], axis=1)

    # Sort variants from highest to lowest prioritization score.
    results = results.sort_values(
        by="Prioritization_Score",
        ascending=False,
        kind="stable",
    ).reset_index(drop=True)

    # Assign ranks while preserving tied scores.
    results.insert(
        0,
        "Priority_Rank",
        results["Prioritization_Score"].rank(
            method="min",
            ascending=False,
        ).astype(int),
    )

    # Add the reporting fields required for the project.
    results["Rank"] = results["Priority_Rank"]
    results["Priority_Score"] = results["Prioritization_Score"]
    results["Priority_Category"] = results["Prioritization_Score"].apply(
        get_priority_category
    )
    results["Evidence_Summary"] = results.apply(
        build_evidence_summary,
        axis=1,
    )

    # Save results without modifying the original annotation file.
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results.to_csv(
        OUTPUT_FILE,
        sep="\t",
        index=False,
        na_rep="NA",
    )

    # Print a summary for reproducibility and initial quality control.
    print(f"Input variants: {len(data)}")
    print(f"Output file: {OUTPUT_FILE}")
    print("ACMG/AMP classification was not independently performed.")
    print("Prioritization scores are educational, not clinical diagnoses.")


if __name__ == "__main__":
    main()
