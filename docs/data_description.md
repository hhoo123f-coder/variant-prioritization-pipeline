# Data Description

**Module 1 — Dataset Preparation and Initial QC**
**Date:** 2026-09-27

---

## 1. Overview

This document describes the ClinVar GRCh38 dataset prepared by Module 1 for the cancer variant prioritization project.

---

## 2. Source

| Item | Value |
|------|-------|
| Source | NCBI ClinVar |
| URL | https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/ |
| Data type | Annotated VCF (GRCh38) |
| Download date | 2026-09-14 |
| Processing date | 2026-09-27 |

---

## 3. Selected Genes and Regions

| Gene | Chromosome | GRCh38 Region |
|------|------------|---------------|
| BRCA1 | 17 | 17:43044295-43170327 |
| BRCA2 | 13 | 13:32315474-32400266 |
| PALB2 | 16 | 16:23603165-23641310 |
| TP53  | 17 | 17:7668421-7687490  |

**Note:** Chromosome names are numeric (13, 16, 17) — no chr prefix.

---

## 4. INFO Fields Available

| Field | Description |
|-------|-------------|
| CLNSIG | Clinical significance classification |
| CLNREVSTAT | Review status of the submission |
| CLNDN | Associated condition name(s) |
| GENEINFO | Gene annotation (may include overlapping genes) |

---

## 5. Record Counts Through the Pipeline

| Stage | Records |
|-------|---------|
| ClinVar full release | millions |
| After region extraction | 47,428 |
| After CLNSIG filter | 21,799 |
| After balanced sampling | 120 |

---

## 6. Final Distribution

### By Clinical Significance

| Category | Count |
|----------|-------|
| Pathogenic | 40 |
| Likely_pathogenic | 40 |
| Uncertain_significance | 40 |

### By Gene

| Gene | Count |
|------|-------|
| BRCA1 | 30 |
| BRCA2 | 30 |
| PALB2 | 30 |
| TP53 | 30 |

### By Variant Type

| Type | Count |
|------|-------|
| SNPs | 52 |
| Indels | 61 |
| MNPs | 2 |
| Others | 5 |

---

## 7. Files Produced

| File | Description |
|------|-------------|
| data/processed/breast_cancer_ClinVar_GRCh38.vcf.gz | Unfiltered panel |
| data/processed/breast_cancer_small_ClinVar_GRCh38.vcf.gz | Final balanced subset |
| data/processed/breast_cancer_small_ClinVar_GRCh38.vcf.gz.tbi | Tabix index |
| results/reports/vcf_stats_small.txt | VCF statistics |

---

## 8. Data Handling Rules Applied

- All files use GRCh38
- Chromosome names are numeric
- No QUAL or DP filters applied (not present in ClinVar)
- Large VCF files excluded from Git

---

## 9. Limitations

- Records overlap genomic intervals — not unique per gene
- Some records may have conflicting classifications
- GENEINFO may include overlapping gene annotations
- The 120-variant subset is a teaching sample, not a full panel

---

