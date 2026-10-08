# Reproducibility Guide

**Project:** A Reproducible Workflow for Prioritizing Cancer-Associated Variants Using ClinVar and gnomAD
**Student 1:** Dataset Preparation, VCF Inspection, Validation, Filtering, and Initial QC
**Date:** 2026-09-27
**Genome:** GRCh38

---

## Goal

Enable any other student to fully reproduce the Student 1 workflow from scratch and obtain identical results.

---

## 1. System Requirements

| Requirement | Value |
|-------------|-------|
| Operating System | Ubuntu 20.04+ or WSL2 |
| Conda | Miniforge or Anaconda |
| Disk space | ~2 GB free |
| Internet | Required (ClinVar download) |

---

## 2. Software Versions

| Tool | Version |
|------|---------|
| bcftools | 1.24 |
| htslib | 1.24 |
| tabix | 1.24 |
| Python | 3.14.7 |

Recorded in docs/software_versions.txt.

---

## 3. Environment Setup

### 3.1 Create the Conda environment

    conda create -n cancer-vcf -c conda-forge -c bioconda \
      python=3.11 pandas pyyaml matplotlib seaborn \
      bcftools htslib tabix snakemake

### 3.2 Activate

    conda activate cancer-vcf

### 3.3 Verify

    bcftools --version
    tabix --version
    python3 --version

---

## 4. Data Sources

| Item | Value |
|------|-------|
| Primary source | NCBI ClinVar |
| URL | https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/ |
| Assembly | GRCh38 |
| Download date | 2026-09-14 |
| Processing date | 2026-09-27 |

| Population source | gnomAD v4.1 (used by Student 2) |

---

## 5. Reproducing the Workflow

### Option A - Run the full script (recommended)

    cd ~/cancer-vcf-project
    conda activate cancer-vcf
    bash scripts/student1_workflow.sh

This performs all steps automatically.

### Option B - Run step by step

See methods.md for full commands.

---

## 6. Expected Output

| File | Records |
|------|---------|
| data/processed/breast_cancer_ClinVar_GRCh38.vcf.gz | 47,428 |
| data/processed/breast_cancer_small_ClinVar_GRCh38.vcf.gz | 120 |
| data/processed/breast_cancer_small_ClinVar_GRCh38.vcf.gz.tbi | index |

### Distribution

By CLNSIG:

- Pathogenic: 40
- Likely_pathogenic: 40
- Uncertain_significance: 40

By gene:

- BRCA1: 30
- BRCA2: 30
- PALB2: 30
- TP53: 30

---

## 7. Verification Commands

    bcftools view -H data/processed/breast_cancer_small_ClinVar_GRCh38.vcf.gz | wc -l

    bcftools query -f '%INFO/CLNSIG\n' data/processed/breast_cancer_small_ClinVar_GRCh38.vcf.gz | sort | uniq -c

    bcftools query -f '%INFO/GENEINFO\n' data/processed/breast_cancer_small_ClinVar_GRCh38.vcf.gz | sort | uniq -c

---

## 8. Known Non-Determinism

Because shuf -n 10 randomly selects variants, the exact variant IDs may differ between runs. However, the following are guaranteed:

- Total records: 120
- Class distribution: 40 / 40 / 40
- Gene distribution: 30 per gene

To obtain identical variant IDs, use a random seed.

---

## 9. Data Handling Rules

- Do NOT commit VCF files to GitHub
- Do NOT use QUAL or DP filters (not present in ClinVar)
- Match gnomAD with CHROM + POS + REF + ALT (Student 2)

---

## 10. Troubleshooting

| Problem | Solution |
|---------|----------|
| tabix: command not found | Activate cancer-vcf environment |
| Unsorted positions error | Use bcftools sort before tabix |
| 0 records after filter | Use INFO/CLNSIG="..." not CLNSIG="..." |
| chr prefix mismatch | Use numeric names: 13, 16, 17 |

---

Educational project — not for clinical diagnosis.
