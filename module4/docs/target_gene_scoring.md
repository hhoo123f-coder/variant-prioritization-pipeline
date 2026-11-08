# Target Gene Prioritization Analysis Report

## Overview
This analysis compares the variant prioritization results across four target genes: BRCA1, BRCA2, PALB2, and TP53. The aim was to calculate an average prioritization score for each gene and compare their educational priority categories.

## Input Data
The analysis used the corrected prioritization results file:
`prioritized_variants_CORRECTED.tsv`

The dataset contained 120 variants, with 30 variants assigned to each target gene.

## Method
Python and Pandas were used to group variants by gene and calculate the total and average prioritization scores.

**Average Gene Score** = Total Prioritization Scores / Number of Variants

The existing variant-level prioritization scores were used. No new clinical classification system was introduced.

## Results Summary

| Gene | Number of Variants | Total Score | Average Gene Score |
|------|-------------------|-------------|--------------------|
| PALB2 | 30 | 192 | 6.40 |
| TP53 | 30 | 190 | 6.33 |
| BRCA1 | 30 | 188 | 6.27 |
| BRCA2 | 30 | 180 | 6.00 |

PALB2 showed the highest average score (6.40), followed by TP53 (6.33), BRCA1 (6.27), and BRCA2 (6.00).

## Priority Category Distribution

| Gene | High | Intermediate | Low or Uncertain |
|------|------|--------------|------------------|
| BRCA1 | 16 | 6 | 8 |
| BRCA2 | 15 | 7 | 8 |
| PALB2 | 19 | 3 | 8 |
| TP53 | 13 | 12 | 5 |

## Visualizations
- **Figure 5:** Average Target Gene Prioritization Score.
- **Figure 6:** Variant Priority Categories by Target Gene.

## Output Files
- `target_gene_scoring_summary.tsv`
- `Figure5_target_gene_scoring.png`
- `Figure6_target_gene_priority_categories.png`
- The Python notebook containing the analysis code is saved as: `Target_Gene_Scoring_Analysis.ipynb`

## Important Note
The average gene score is a project-derived educational measure based on the prioritization scores of the variants in each gene. It is not an independent clinical classification, does not establish gene pathogenicity, and should not be interpreted as a measure of cancer risk.
