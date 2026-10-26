
# Clinical Interpretation and Classification of Human Genetic Variants

A reproducible bioinformatics pipeline for prioritizing genetic variants using clinical annotations (ClinVar) and population frequency (gnomAD).

- **Genome assembly:** GRCh38
- **Gene panel:** BRCA1, BRCA2, PALB2, TP53
- **Data source:** NCBI ClinVar
- **Population source:** gnomAD v4.1

---

## Project Status: COMPLETED

The pipeline has been fully implemented, executed, and validated. The final results include:

- **Total variants analyzed:** 120 (30 per gene).
- **Priority Categories:** 63 High, 28 Intermediate, 29 Low/Uncertain.
- **Quality Control:** 0 duplicate variants, 120 validated records, and all structural checks passed.
- **Automation:** Fully automated using `workflow/Snakefile.module5`.

---

## Project Aim

Develop a reproducible workflow that:
1. Extracts clinically relevant variants from ClinVar.
2. Filters and normalizes variants.
3. Annotates with clinical (ClinVar) and population (gnomAD) evidence.
4. Prioritizes variants using educational scoring.
5. Automates everything with Snakemake.
6. Produces reproducible tables, figures, and reports.

---

## Team Division (5 Modules)

| Module | Responsibility | Output |
| :--- | :--- | :--- |
| **Module 1** | Dataset preparation, VCF inspection, initial QC | Validated VCF + documentation |
| **Module 2** | Filtering + Normalization | Filtered + normalized VCF |
| **Module 3** | Annotation + Data extraction | Annotated TSV table |
| **Module 4** | Variant prioritization + Scoring | Ranked + scored table |
| **Module 5** | Results + Snakemake automation | Final pipeline + report |

---

## Quick Start

### 1. Clone the repository
git clone https://github.com/hhoo123f-coder/variant-prioritization-pipeline.git
cd variant-prioritization-pipeline

### 2. Create the Conda environment
conda env create -f environment_simple.yml
conda activate cancer-vcf

### 3. Run the full workflow (Module 5)
snakemake -s workflow/Snakefile.module5 --cores 2

### 4. View the generated reports and figures
- **HTML Report:** results/module5/reports/snakemake_report.html
- **Figures:** results/module5/figures/

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
|   `-- module_handoffs/
|
|-- scripts/
|   |-- module1_data_prep.sh
|   |-- module2_filter_normalize.sh
|   |-- module3/
|   |-- module4/
|   `-- module5/
|
|-- workflow/
|   `-- Snakefile.module5
|
|-- data/
|   |-- raw/
|   |-- processed/
|   `-- module5/
|
|-- results/
|   |-- tables/
|   |-- figures/
|   |-- reports/
|   `-- module5/
|
`-- tests/

---

## Final Results Summary

| Category | Count |
| :--- | :--- |
| Total Variants | 120 |
| High Priority | 63 |
| Intermediate Priority | 28 |
| Low/Uncertain Priority | 29 |
| gnomAD FOUND | 14 |
| gnomAD NOT_FOUND | 100 |
| gnomAD MANUAL_REVIEW | 6 |

---

## Data Handling Rules

- All files use GRCh38.
- Chromosome names are numeric (13, 16, 17) — no chr prefix.
- gnomAD matching uses CHROM + POS + REF + ALT.
- Do NOT commit large VCF files to GitHub.
- Do NOT use QUAL or DP filters — not present in ClinVar.
- Do NOT use the educational score as a clinical diagnosis.

---

## Scientific Disclaimer

This project ranks variants using public ClinVar assertions, gnomAD population frequency, and available variant annotations. The ranking is an educational computational result. It does not establish pathogenicity, cancer risk, or a clinical diagnosis.
