# Module 4: Variant Prioritization and Scoring

## 1. Purpose

Module 4 ranks genetic variants using a rule-based scoring system.
The score uses ClinVar classification, VEP impact, population frequency,
and conflicting ClinVar evidence.

The output supports educational variant prioritization. It is not a
clinical diagnosis and does not replace expert review or ACMG/AMP
variant classification.

## 2. Input and Output

**Input file**

`input/final_annotation_with_VEP.tsv`

The input contains variant annotations, including ClinVar information,
VEP consequence and impact, and available population-frequency fields.

**Script**

`scripts/prioritize_variants.py`

**Output file**

`results/tables/prioritized_variants.tsv`

The output contains the priority rank, variant information, score,
priority category, and evidence summary.

## 3. Scoring Rules

### 3.1 ClinVar classification

| ClinVar classification | Score |
|---|---:|
| Pathogenic | +5 |
| Likely pathogenic | +4 |
| Benign | -4 |
| Likely benign | -4 |
| Conflicting classification | 0 |

The script applies a penalty of -2 when a conflict is identified in
the ClinVar classification or review-status information. The
`no_conflicts` label is not treated as a conflict.

### 3.2 VEP impact

| VEP impact | Score |
|---|---:|
| HIGH | +4 |
| MODERATE | +2 |
| Other impact levels | 0 |

### 3.3 Population frequency

The script uses the highest available valid frequency from the
genome and exome frequency fields.

| Frequency | Score |
|---|---:|
| Less than 0.001 | +2 |
| From 0.001 to 0.01, inclusive | +1 |
| Greater than 0.01 | 0 |
| Missing or invalid frequency | No frequency points |

A missing frequency is not treated as a frequency of zero. If the
frequency is missing or invalid, the frequency component contributes
no points to the total score.

### 3.4 Total score

The total prioritization score is calculated by combining the
ClinVar score, VEP impact score, frequency score, and conflict penalty.

A higher score indicates higher priority under this project's
educational scoring rules.

## 4. Priority Categories

| Total score | Priority category |
|---|---|
| 8 or higher | High educational priority |
| 4 to less than 8 | Intermediate educational priority |
| 0 to less than 4 | Low or uncertain educational priority |
| Below 0 | Likely low educational priority |

These categories describe the project's scoring output. They are not
clinical classifications.

## 5. Ranking

Variants are sorted by total score in descending order. Variants with
the same score share the same rank. The script uses the minimum rank
for tied scores.

## 6. Evidence Summary and Review Status

The output includes an evidence summary based on available variant
annotations. The script also sets `ACMG_AMP_Review_Status` to
`NOT_INDEPENDENTLY_CLASSIFIED`.

This means the prioritization score should not be interpreted as an
independent ACMG/AMP classification. A high score does not by itself
prove that a variant is pathogenic.

## 7. Reproducibility Notes

- The script reads `input/final_annotation_with_VEP.tsv`.
- The script writes `results/tables/prioritized_variants.tsv`.
- Running the script again may overwrite the existing output file.
  Check and back up the current results before rerunning it.
- Missing frequency data do not automatically receive rare-frequency
  points.
- This documentation describes the rules implemented in the script;
  it does not independently validate the biological interpretation
  of each variant.

## 8. SIFT and PolyPhen Functional Predictions

SIFT and PolyPhen predictions were included as additional functional
information to support variant review. According to the final report,
these predictions were not included in the prioritization scoring
formula and did not change the existing scores, priority categories,
or ranks.

The additional predictions are available in:

`input/final_annotation_with_VEP_SIFT_PolyPhen.tsv`

The prioritization scoring script uses:

`input/final_annotation_with_VEP.tsv`

Missing SIFT or PolyPhen predictions are not interpreted as benign
results. These predictions provide supporting information only and
do not replace independent ACMG/AMP classification
.
## 9. Additional Functional Prediction Scripts

The project includes separate scripts for obtaining and testing SIFT
and PolyPhen functional predictions.

- `scripts/add_sift_polyphen.py`: retrieves SIFT and PolyPhen predictions
  from Ensembl VEP for eligible missense variants and saves an additional
  annotated input table.
- `tests/test_sift_polyphen.py`: performs a small test request using up
  to five missense variants and prints the available MANE, SIFT, and
  PolyPhen information.

The additional predictions support variant review only. They are not
included in the prioritization scoring formula and do not replace
independent ACMG/AMP classification.

Both scripts require access to the Ensembl REST API and the expected
input file, `input/final_annotation_with_VEP.tsv`.
