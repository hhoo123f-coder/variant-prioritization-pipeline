# Module 2 Handoff — Filtering & Normalization

**Responsible Module:** Module 2 — Filtering & Normalization
**Status:** Pending completion
**Date:** [To be filled]

---

## Input from Module 1

### Primary file
`data/processed/breast_cancer_ClinVar_GRCh38.vcf.gz`
- 47,428 records
- Genes: BRCA1, BRCA2, PALB2, TP53
- No clinical filtering applied
- Chromosome names: numeric (13, 16, 17)

### Optional pre-filtered subset
`data/processed/breast_cancer_small_ClinVar_GRCh38.vcf.gz`
- 120 records
- Pathogenic + Likely_pathogenic + VUS
- Balanced: 30 per gene, 40 per class

---

## Tasks

1. **Filtering**
   - Define filtering criteria
   - Apply filters
   - Record before → after counts
   - Justify each filter

2. **Normalization**
   - Use GRCh38 reference genome
   - Left-align indels
   - Split multiallelic variants
   - Verify output

---

## Output (to be delivered to Module 3)

- Filtered + Normalized VCF
- `data/processed/breast_cancer_filtered_normalized.vcf.gz`
- `.tbi` index
- Documentation of filtering criteria

---

## Commands/Script

See `scripts/module2_filter_normalize.sh`

---

*Educational project — not for clinical diagnosis.*
