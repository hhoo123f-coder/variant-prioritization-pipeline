# Variant Prioritization Pipeline

A reproducible bioinformatics pipeline for prioritizing genetic variants using clinical annotations (ClinVar) and population frequency (gnomAD).

**Genome assembly:** GRCh38
**Gene panel:** BRCA1, BRCA2, PALB2, TP53
**Data source:** NCBI ClinVar
**Population source:** gnomAD v4.1

---

## Project Aim

Develop a reproducible workflow that:

1. Extracts clinically relevant variants from ClinVar
2. Filters and normalizes variants
3. Annotates with clinical and population evidence
4. Prioritizes variants using educational scoring
5. Automates everything with Snakemake
6. Produces reproducible tables, figures, and reports

---

## Team Division (5 Modules)

| Module | Responsibility | Output |
|---------|----------------|--------|
| **Module 1** | Dataset preparation, VCF inspection, initial QC | Validated VCF + documentation |
| **Module 2** | Filtering + Normalization | Filtered + normalized VCF |
| **Module 3** | Annotation + Data extraction | Annotated TSV table |
| **Module 4** | Variant prioritization + Scoring | Ranked + scored table |
| **Module 5** | Results + Snakemake automation | Final pipeline + report |

---

## Quick Start

### 1. Clone the repository

    git clone https://github.com/hhoo123f-coder/variant-prioritization-pipeline.git
    cd cancer-vcf-project

### 2. Create the Conda environment

    conda env create -f environment_simple.yml
    conda activate cancer-vcf

### 3. Run the full workflow (once Module 5 completes the Snakefile)

    snakemake -s workflow/Snakefile --cores 2

### 4. Generate the HTML report

    snakemake -s workflow/Snakefile --report results/reports/snakemake_report.html

---

## Project Structure

    cancer-vcf-project/
    |-- README.md
    |-- methods.md
    |-- environment.yml
    |-- environment_simple.yml
    |-- .gitignore
    |
    |-- docs/
    |   |-- software_versions.txt
    |   |-- data_description.md
    |   |-- reproducibility.md
    |   |-- final_checklist.md
    |   `-- student_handoffs/
    |       |-- student1_handoff.md
    |       |-- student2_handoff.md
    |       |-- student3_handoff.md
    |       |-- student4_handoff.md
    |       `-- student5_handoff.md
    |
    |-- scripts/
    |   |-- student1_workflow.sh
    |   |-- student2_filter_normalize.sh
    |   |-- student3_annotate_extract.py
    |   |-- student4_prioritize.py
    |   `-- student5_snakemake.sh
    |
    |-- workflow/
    |   `-- Snakefile
    |
    |-- config/
    |   `-- config.yaml
    |
    |-- data/
    |   |-- raw/
    |   `-- processed/
    |
    |-- results/
    |   |-- tables/
    |   |-- figures/
    |   `-- reports/
    |
    `-- tests/

---

## Workflow Overview

    ClinVar GRCh38 VCF
         |
         v
    [Module 1] Dataset Preparation + Initial QC
         |
         v
    [Module 2] Filtering + Normalization
         |
         v
    [Module 3] Annotation + Data Extraction
         |
         v
    [Module 4] Prioritization + Scoring
         |
         v
    [Module 5] Snakemake Automation + Reports
         |
         v
    Final Deliverables

---

## What Module 1 Did (Complete)

- Downloaded ClinVar GRCh38 VCF from NCBI (2026-09-14)
- Extracted 4 gene regions: BRCA1, BRCA2, PALB2, TP53
- Validated VCF and confirmed GRCh38
- Compressed and indexed with bgzip + tabix
- Generated statistics: 47,428 records
- Applied CLNSIG filter: 21,799 records
- Created balanced teaching subset: 120 variants
- Documented everything for reproducibility

### Module 1 Output Files

| File | Description | Records |
|------|-------------|---------|
| `data/processed/breast_cancer_ClinVar_GRCh38.vcf.gz` | Unfiltered panel | 47,428 |
| `data/processed/breast_cancer_small_ClinVar_GRCh38.vcf.gz` | Final balanced subset | 120 |
| `data/processed/breast_cancer_small_ClinVar_GRCh38.vcf.gz.tbi` | Tabix index | — |
| `results/reports/vcf_stats_small.txt` | VCF statistics | — |
| `docs/software_versions.txt` | Tool versions | — |

---

## What Modules 2–5 Will Do

### Module 2 — Filtering + Normalization
- Define filtering criteria
- Apply filters
- Normalize variants with GRCh38 reference
- Left-align indels
- Split multiallelic variants

### Module 3 — Annotation + Data Extraction
- Annotate variants with gene, CLNSIG, review status
- Add frequency information
- Perform annotation QC
- Extract important fields to TSV table

### Module 4 — Prioritization + Scoring
- Define prioritization strategy
- Build transparent scoring system
- Apply scores to all variants
- Rank variants
- Identify high-priority variants

### Module 5 — Results + Snakemake
- Combine all results
- Create Snakemake workflow
- Generate figures and reports
- Produce HTML report
- Final submission

---

## Data Handling Rules

- ✅ All files use **GRCh38**
- ✅ Chromosome names are **numeric** (13, 16, 17) — no chr prefix
- ✅ gnomAD matching uses **CHROM + POS + REF + ALT**
- ❌ Do **NOT** commit large VCF files to GitHub
- ❌ Do **NOT** use `QUAL` or `DP` filters — not present in ClinVar
- ❌ Do **NOT** use the educational score as a clinical diagnosis

---

## Important Notes for All Modules

1. **Only Module 1** has the raw ClinVar data (large files are not on GitHub).
2. Each student's handoff file is in `docs/student_handoffs/`.
3. Each student's script is in `scripts/studentN_*.sh` or `.py`.
4. **Module 5** connects all scripts into the Snakemake workflow.
5. All students must document their work.
6. Create a branch for your work: `studentN-work`.

---

## Git Workflow for Team

Each student should:

    # 1. Clone the repository
    git clone https://github.com/hhoo123f-coder/variant-prioritization-pipeline.git
    cd cancer-vcf-project

    # 2. Create your branch
    git checkout -b student2-work

    # 3. Do your work
    # ...

    # 4. Commit and push
    git add .
    git commit -m "Module 2: filtering and normalization"
    git push origin student2-work

    # 5. Open a Pull Request on GitHub

---

## Scientific Disclaimer

This project ranks variants using public ClinVar assertions, gnomAD population frequency, and available variant annotations. The ranking is an **educational computational result**. It does **not** establish pathogenicity, cancer risk, or a clinical diagnosis.

---

