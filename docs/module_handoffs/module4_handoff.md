# Module 4 — Prioritization & Scoring

**Responsible Module:** Module 4 — Prioritization & Scoring
**Status:** Scoring results and documentation prepared for handoff
**Date:** 2026-10-26

---

## Input

### Annotated Variant Table

**Input file:** `input/final_annotation_with_VEP.tsv`

- Records: 120 variant records
- Contains ClinVar information, VEP annotations, and available population-frequency data.
- This is the input file used by the Module 4 scoring script.

---

## Tasks and Implementation

### 1. Define Prioritization Strategy

A rule-based scoring system was used to rank variants according to their available clinical significance, predicted impact, population frequency, and conflicting ClinVar evidence.

The scoring system supports educational prioritization and does not replace clinical interpretation.

### 2. Define Prioritization Criteria

The criteria implemented in the scoring script are:

- **Clinical significance:** ClinVar classification.
- **Impact:** VEP impact level.
- **Rarity:** Available genome and exome population-frequency values.
- **Conflicting evidence:** A penalty is applied when a conflict is identified.

### 3. Develop the Scoring System

Each criterion contributes to the total prioritization score according to the rules implemented in the script.

The scoring weights, frequency thresholds, conflict penalty, and priority-category cutoffs are documented in:

`docs/module4_scoring.md`

### 4. Apply the Score

The scoring script processes the annotated variant table and calculates a prioritization score for each variant.

### 5. Rank Variants

Variants are sorted by total score in descending order. Variants with equal scores share the same rank.

### 6. Identify High-Priority Variants

Variants are grouped into priority categories according to their total scores. These categories represent educational prioritization, not independent clinical classifications.

### 7. Prepare the Prioritization Table

The prepared main output contains the following columns:

`Rank, CHROM, POS, REF, ALT, GENE, Priority_Score, Priority_Category, Evidence_Summary`

---

## Output — Handoff to Module 5

### Main Output

`results/tables/prioritized_variants.tsv`

This is the main handoff table for Module 5.

### Supporting Outputs

- `results/tables/prioritized_variants_detailed.tsv` — detailed prioritization results.
- `results/tables/top5_prioritized_variants.tsv` — top five prioritized variants.
- `results/tables/top10_prioritized_variants.tsv` — top ten prioritized variants.

### Scoring Documentation

`docs/module4_scoring.md`

This document explains the scoring rules, thresholds, priority categories, ranking method, and interpretation limitations.

### Script

`scripts/prioritize_variants.py`

The script reads:

`input/final_annotation_with_VEP.tsv`

The script writes:

`results/tables/prioritized_variants.tsv`

**Note:** Running the script again may overwrite the existing main output. Review and back up the current results before rerunning it.

---

## Notes for Module 5

- Use `results/tables/prioritized_variants.tsv` as the main Module 4 handoff table.
- Refer to `docs/module4_scoring.md` for the scoring methodology.
- Use the detailed and top-variant tables as supporting outputs when needed.
- The prioritization score is project-specific and must not be interpreted as an independent ACMG/AMP classification or a clinical diagnosis.
