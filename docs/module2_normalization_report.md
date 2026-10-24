# Module 2 — Filtering and Normalization Report

## Overview
This report describes the filtering checks and normalization performed on the ClinVar GRCh38 breast cancer dataset (120 variants).  
The goal of this step is to ensure that all variants are clean, consistent, and aligned to the GRCh38 reference genome before annotation.

---

## Input
- File: `breast_cancer_small_ClinVar_GRCh38.vcf.gz`
- Variants: 120
- Genome build: GRCh38

---

## Filtering Checks
- Verified chromosome names (13, 16, 17, no “chr” prefix)
- Confirmed REF and ALT fields are valid
- Checked CLINSIG groups (Pathogenic, Likely Pathogenic, VUS)
- Ensured no missing POS or INFO fields
- Confirmed file integrity and tabix index

---

## Normalization
Command used:

bcftools norm -f GRCh38.fa breast_cancer_small_ClinVar_GRCh38.vcf.gz -Oz -o breast_cancer_small_ClinVar_GRCh38.norm.vcf.gz
tabix -p vcf breast_cancer_small_ClinVar_GRCh38.norm.vcf.gz


### Normalization Results
- Variants before normalization: 120  
- Variants after normalization: 120  
- No multiallelic variants found  
- REF/ALT alignment successful  
- Output compressed and indexed

---

## Output Files
- `data/processed/breast_cancer_small_ClinVar_GRCh38.norm.vcf.gz`
- `data/processed/breast_cancer_small_ClinVar_GRCh38.norm.vcf.gz.tbi`
- `results/reports/module2_normalization_stats.txt`

---

## Conclusion
The dataset is fully normalized and ready for Module 3 annotation.  
No issues were detected during normalization.
