# A Reproducible Workflow for Prioritizing Cancer-Associated Variants Using ClinVar and gnomAD

**Student 1 — Dataset Preparation, VCF Inspection, Validation, Filtering, and Initial QC**

---

## Overview

This repository contains a reproducible bioinformatics workflow for preparing, filtering, and documenting a ClinVar GRCh38 breast cancer variant panel. The project is part of a seven-week degree project using ClinVar, gnomAD, Python, Linux, and Snakemake.

**Genome assembly:** GRCh38
**Gene panel:** BRCA1, BRCA2, PALB2, TP53
**Data source:** NCBI ClinVar
**Population source (Student 2):** gnomAD v4.1

---

## Project Aim

Develop a reproducible workflow that:

1. Extracts clinically relevant variants from ClinVar
2. Filters by clinical significance (CLNSIG)
3. Creates a balanced teaching subset
4. Documents everything for reproducibility
5. Prepares a clean handoff for Student 2

---

## Quick Start

### Prerequisites

- Ubuntu / WSL2
- Conda environment named cancer-vcf
- Tools: bcftools, htslib, tabix, Python 3.11+, wget

### Activate the environment

    conda activate cancer-vcf

### Reproduce the entire Student 1 workflow

    bash scripts/student1_workflow.sh

This single command runs the full pipeline from downloading ClinVar to creating the handoff archive.

---

## Project Structure

    cancer-vcf-project/
    |-- README.md
    |-- methods.md
    |-- environment.yml
    |-- .gitignore
    |-- data_description.txt
    |-- output_1.txt
    |-- HANDOFF_NOTES.md
    |-- config/
    |-- workflow/
    |-- scripts/
    |   `-- student1_workflow.sh
    |-- data/
    |   |-- raw/
    |   `-- processed/
    |-- results/
    |   |-- tables/
    |   |-- figures/
    |   `-- reports/
    |-- docs/
    |   |-- software_versions.txt
    |   |-- reproducibility.md
    |   |-- final_checklist.md
    |   `-- command_history.txt
    `-- tests/

---

## Workflow Steps

### Step 1 — Download ClinVar GRCh38 VCF

Source: https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/

Download date: 2026-09-14

### Step 2 — Extract four target gene regions

| Gene | Chromosome | GRCh38 Region |
|------|------------|---------------|
| BRCA1 | 17 | 17:43044295-43170327 |
| BRCA2 | 13 | 13:32315474-32400266 |
| PALB2 | 16 | 16:23603165-23641310 |
| TP53  | 17 | 17:7668421-7687490  |

Result: 47,428 records

### Step 3 — Apply clinical filter

Keep only variants with:

- Pathogenic
- Likely_pathogenic
- Uncertain_significance

Result: 21,799 records

### Step 4 — Create balanced teaching subset

10 variants per gene per class (4 x 3 x 10 = 120).

Result: 120 variants

- Pathogenic: 40
- Likely_pathogenic: 40
- Uncertain_significance: 40
- 30 variants per gene

### Step 5 — Generate statistics and documentation

Output files:

- results/reports/vcf_stats_small.txt
- docs/software_versions.txt
- data_description.txt
- output_1.txt
- HANDOFF_NOTES.md

### Step 6 — Create handoff archive

student1_handoff.tar.gz contains all files needed by Student 2.

---

## Output Files

| File | Description | Records |
|------|-------------|---------|
| data/processed/breast_cancer_ClinVar_GRCh38.vcf.gz | Unfiltered panel | 47,428 |
| data/processed/breast_cancer_small_ClinVar_GRCh38.vcf.gz | Final balanced subset | 120 |
| data/processed/breast_cancer_small_ClinVar_GRCh38.vcf.gz.tbi | Tabix index | - |
| results/reports/vcf_stats_small.txt | VCF statistics | - |
| docs/software_versions.txt | Tool versions | - |
| student1_handoff.tar.gz | Complete handoff | - |

---

## Data Handling Rules

- All files use GRCh38
- Chromosome names are numeric (13, 16, 17) — no chr prefix
- gnomAD matching will use CHROM + POS + REF + ALT (not position alone)
- Do NOT commit large VCF files to GitHub
- Do NOT use QUAL or DP filters — not present in ClinVar
- Do NOT use the educational score as a clinical diagnosis

---

## Reproducibility

The project is reproducible when another student can:

1. Activate the Conda environment (conda activate cancer-vcf)
2. Run bash scripts/student1_workflow.sh
3. Obtain the same 120-variant subset
4. Verify the distribution matches (40/40/40 and 30 per gene)
5. Understand the scientific limitations

See docs/reproducibility.md for full details.

---

## Important Notes for Student 2

1. Use only breast_cancer_small_ClinVar_GRCh38.vcf.gz for analysis.
2. Do NOT apply QUAL or DP filters — ClinVar does not contain these fields.
3. Match gnomAD using CHROM + POS + REF + ALT.
4. Chromosome names are numeric (13, 16, 17) — no chr prefix.
5. CLNSIG syntax: use INFO/CLNSIG="Pathogenic" (with INFO/).
6. bcftools sort is required before tabix when using shuf.

See HANDOFF_NOTES.md for full instructions.

---

## Scientific Disclaimer

This project ranks variants using public ClinVar assertions, gnomAD population frequency, and available variant annotations. The ranking is an educational computational result. It does not establish pathogenicity, cancer risk, or a clinical diagnosis. Expert review and additional evidence are required for any medical interpretation.

---

## Authors

| Role | Responsibility |
|------|----------------|
| Student 1 | Dataset preparation, filtering, initial QC |
| Student 2 | Normalization, gnomAD matching, prioritization |
| Student 3 | Snakemake workflow, figures, reports |

---

## License

Educational project — not for clinical use.

---

Last updated: 2026-09-27
