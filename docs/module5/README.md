# Cancer Variant Prioritization Workflow — Module 5

## 1. Project Overview

Module 5 summarizes an existing cancer variant-prioritization dataset, performs structural quality-control checks, and generates summary tables, figures, and a Snakemake HTML report.

This module does not independently reproduce every upstream variant-processing or annotation step.

## 2. Input Data

Input files:

- `data/module5/prioritized_variants.tsv`
- `data/module5/annotations_with_SIFT_PolyPhen.tsv`

The dataset contains 120 variants across four genes:

- BRCA1: 30 variants
- BRCA2: 30 variants
- PALB2: 30 variants
- TP53: 30 variants

## 3. Workflow Components

The workflow is defined in `workflow/Snakefile.module5`.

### Quality Control

The `quality_control` rule runs `scripts/module5/qc_results.py`.

It checks required columns, duplicate variant keys, row counts, and consistency between priority scores and ranks.

Output: `results/module5/reports/qc_report.txt`

Log: `logs/module5/qc.log`

### Results Summary and Visualization

The `summarize_results` rule runs `scripts/module5/summarize_results.py`.

It generates:

- `results/module5/tables/results_summary.tsv`
- `results/module5/reports/results_summary.txt`
- `results/module5/figures/priority_categories.png`
- `results/module5/figures/gnomad_status.png`
- `results/module5/figures/variant_counts_by_gene.png`

Log: `logs/module5/summarize_results.log`

The `all` rule requires the QC report, summary table, text report, and all three figures.

## 4. Software and Environment

The workflow was tested in a Conda environment on an Apple Silicon Mac.

- Python: 3.11.17
- Snakemake: 9.27.0
- pandas: 2.3.3
- Matplotlib: 3.11.2
- Platform: macOS Apple Silicon (arm64)
- Conda environment: `project4`

See `docs/module5/environment_versions.txt` for the recorded versions.

## 5. Running the Workflow

Run commands from the repository root.

Activate the environment:

    conda activate project4

Preview the planned jobs without executing them:

    snakemake -n -p --snakefile workflow/Snakefile.module5 --cores 2

Execute all workflow jobs with two cores and print the commands:

    snakemake -p --forceall --snakefile workflow/Snakefile.module5 --cores 2

The `--forceall` option forces all workflow jobs to run again.

Generate the Snakemake HTML report:

    snakemake --snakefile workflow/Snakefile.module5 --report results/module5/reports/snakemake_report.html

## 6. Current Results

The dataset contains 120 variants.

Educational priority categories:

- High educational priority: 63
- Intermediate educational priority: 28
- Low or uncertain educational priority: 29

Recorded gnomAD statuses:

- FOUND: 14
- MANUAL_REVIEW: 6
- NOT_FOUND: 100

Gene counts:

- BRCA1: 30
- BRCA2: 30
- PALB2: 30
- TP53: 30

The recorded workflow execution completed all three Snakemake jobs successfully, and structural QC checks passed for the current input tables.

## 7. Interpretation and Limitations

Priority categories are educational computational rankings, not independent clinical classifications.

A `NOT_FOUND` status does not establish that a variant is pathogenic or absent from all populations. Data-source errors, unavailable results, and cases requiring manual review must not be treated as confirmed biological absence.

Structural QC checks do not establish clinical validity or biological correctness.

This module summarizes existing prioritization results. It does not independently reproduce every upstream processing step, validate every variant, or provide clinical recommendations. Results depend on the supplied input files and the methods used to create them.

## 8. Reproducibility and Data Provenance

The workflow uses a dedicated Snakefile, named input files, Python scripts, explicit output paths, and recorded software versions. A dry-run and a successful execution were performed.

Input checksums should be regenerated and verified whenever files change. Data-source references, release dates, and upstream processing details should be documented where available.

Generated outputs should be regenerated and checked after relevant changes to input data or code.
