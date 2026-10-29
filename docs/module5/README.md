# Cancer Variant Prioritization Workflow

## 1. Project Overview

This project develops a reproducible computational workflow for summarizing and reviewing cancer-associated genetic variants using ClinVar-related annotations, gnomAD status information, variant impact annotations, and educational prioritization scores.

The current workflow focuses on quality control, summary-table generation, and visualization of an existing variant-prioritization dataset. It does not independently perform every upstream analysis step.

## 2. Current Dataset

The current input dataset contains 120 variants across four genes:

- BRCA1: 30 variants
- BRCA2: 30 variants
- PALB2: 30 variants
- TP53: 30 variants

The main input files are:

- `data/prioritized_variants.tsv`
- `data/annotations_with_SIFT_PolyPhen.tsv`

These files contain the existing prioritization results and variant annotations used by the current workflow.

## 3. Workflow Components

The workflow is managed using Snakemake and contains the following rules:

### Quality Control

The `quality_control` rule runs `scripts/qc_results.py`.

It checks the input tables, required columns, duplicate variant keys, and consistency between priority scores and ranks. The report is written to:

`results/reports/qc_report.txt`

### Results Summary and Visualization

The `summarize_results` rule runs `scripts/summarize_results.py`.

It generates:

- `results/tables/results_summary.tsv`
- `results/reports/results_summary.txt`
- `results/figures/priority_categories.png`
- `results/figures/gnomad_status.png`

### Workflow Completion

The `all` rule requires the quality-control report, summary files, and both figures. This allows Snakemake to check whether all requested outputs have been generated.

## 4. Software and Environment

The workflow was tested in a Conda environment on an Apple Silicon Mac.

Recorded software versions include:

- Python 3.11.17
- Snakemake 9.27.0
- pandas 2.3.3
- Matplotlib 3.11.2

The scripts use Python's standard library for file processing and Matplotlib for plotting.

## 5. Running the Workflow

Activate the project environment first:

```bash
conda activate project4
```

Run a dry-run to inspect the planned jobs without executing them:

```bash
snakemake -n -p --forceall --snakefile "Deem_Results_Snakemake_05/Snakefile" --directory "Deem_Results_Snakemake_05"
```

Execute the workflow:

```bash
snakemake --cores 1 -p --forceall --snakefile "Deem_Results_Snakemake_05/Snakefile" --directory "Deem_Results_Snakemake_05"
```

The `--forceall` option forces all workflow jobs to run again.

## 6. Current Results

The current dataset contains 120 variants. The generated summary reports the following priority categories:

- High Priority: 63
- Intermediate Priority: 28
- Low Priority: 29

The recorded gnomAD statuses are:

- FOUND: 14
- MANUAL_REVIEW: 6
- NOT_FOUND: 100

The workflow completed all three Snakemake jobs successfully during the recorded test run.

## 7. SIFT and PolyPhen Prediction Summary

Among the 40 missense variants, SIFT classified 26 as deleterious and 13 as tolerated; one variant had no SIFT prediction available. PolyPhen classified 10 as probably damaging, 3 as possibly damaging, and 21 as benign; six variants had no PolyPhen prediction available.

Eleven missense variants had a SIFT deleterious prediction together with a PolyPhen possibly damaging or probably damaging prediction. Twelve had discordant predictions, with SIFT indicating deleterious and PolyPhen indicating benign.

These computational predictions provide supporting evidence for variant review but do not independently establish pathogenicity or clinical significance. Missing predictions and disagreements between tools should be documented and interpreted cautiously.

## 8. Interpretation and Limitations

The priority categories are educational computational rankings and must not be interpreted as independent clinical classifications.

A `NOT_FOUND` status does not establish that a variant is pathogenic or absent from all populations. API errors, unavailable data, and manual-review cases must be distinguished from confirmed absence.

The current workflow summarizes existing prioritization results; it does not independently validate every variant, reproduce all upstream annotation steps, or provide clinical recommendations.

The results depend on the supplied input files and the methods used to create them. Further validation, documentation of data provenance, and integration of the remaining project stages are required before describing the complete project as fully reproducible.

## 9. Reproducibility

The workflow uses a defined Snakefile, named input files, Python scripts, and explicit output paths. A dry-run and a successful execution were recorded.

For stronger reproducibility, the project should also retain input checksums, a complete software-version record, data-source references, and documentation of the upstream processing steps.
SHA256 checksums for the project inputs, scripts, workflow, documentation, and generated outputs are recorded in `docs/SHA256SUMS.txt`.

All 13 listed files passed checksum verification.
