# Breast Cancer Variant Analysis

## Project Overview
Bioinformatics analysis of 120 genetic variants across:
- BRCA1: 30 variants
- BRCA2: 30 variants
- PALB2: 30 variants
- TP53: 30 variants

Reference genome: GRCh38

## Main Final Output
results/tables/final_annotation_with_VEP.tsv

This table contains:
- ClinVar clinical annotations
- Population frequencies from gnomAD and ExAC
- Ensembl VEP consequences
- MANE Select transcripts
- Predicted impact and HGVS annotations

## Methods
1. Clinical annotation: ClinVar and bcftools
2. Population frequency: gnomAD r4 API
3. Variant effect prediction: Ensembl VEP REST API
4. Transcript selection: MANE Select
5. Quality control: Python validation scripts

## Results
Total variants: 120
Variants with gnomAD AF: 14
Variants not found in queried gnomAD dataset: 106
Variants with ExAC AF: 3
VEP annotated variants: 120
Duplicate variants: 0

VEP impact:
HIGH: 66
MODERATE: 49
LOW: 4
MODIFIER: 1

## Validation
Run from the project root:

python scripts/validate_full_annotation.py

Expected:
FINAL PROJECT VALIDATION PASSED

## Important Files
- results/tables/final_annotation_with_VEP.tsv
- results/tables/population_frequencies_final.tsv
- results/tables/gnomad_api_frequencies.tsv
- results/reports/final_annotation_summary.txt
- results/vep_mane/
- scripts/validate_full_annotation.py

## Important Notes
- Use final_annotation_with_VEP.tsv for downstream analysis.
- Missing AF values are not equivalent to zero.
- NOT_FOUND does not prove that a variant is absent from all gnomAD datasets.
- VEP impact is not a clinical pathogenicity classification.
- VEP annotations were obtained through the Ensembl REST API.
- The original final_annotation.sh generates earlier clinical-only tables.
- Existing results are protected against accidental overwriting.
