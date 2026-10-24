# Module 3 Handoff — Annotation & Data Extraction

**Responsible Module:** Module 3 — Annotation & Data Extraction  
**Status:** Outputs prepared for team review; JSON-upload decision pending  
**Date:** 24 October 2026

---

## Input from Module 2

### Filtered and normalized VCF

The team's template names the expected Module 2 input as:
`data/processed/breast_cancer_filtered_normalized.vcf.gz`

**Input used for Module 3 annotation:**
`data/processed/breast_cancer_small_correct.vcf.gz`

The Module 3 analysis package includes this VCF file and its `.tbi` index.

## Tasks Completed

1. **Clinical annotation:** Extracted ClinVar gene information, variant identifiers, clinical significance (`CLNSIG`), review status (`CLNREVSTAT`), and other available fields with `bcftools`.
2. **Population-frequency enrichment:** Queried gnomAD r4 and retained other frequency fields present in the input annotations, including ExAC where available.
3. **Variant effect prediction:** Used the Ensembl VEP REST API (GRCh38) to obtain consequences, predicted molecular impact, HGVS annotations, and MANE Select transcript details.
4. **Annotation QC:** Checked 120 variant records, expected gene counts, duplicate variant keys, preservation of clinical/frequency values, and the VEP/MANE response-to-table match.
5. **Structured extraction:** Delivered a tab-separated table for downstream Module 4 analysis.

## Output — Handoff to Module 4

**Primary deliverable:** `results/tables/final_annotation_with_VEP.tsv`

This is the most complete supplied result table: **120 rows × 26 columns**. It includes:
- `CHROM`, `POS`, `ID`, `REF`, `ALT`, `GENEINFO`
- `CLNSIG`, `CLNREVSTAT`, `CLNDN`, `MC`
- Frequency fields, including `AF_EXAC`, `GNOMAD_GENOME_AF`, `GNOMAD_EXOME_AF`, and `GNOMAD_STATUS`
- `VEP_MANE_TRANSCRIPT`, `VEP_MANE_CONSEQUENCE`, `VEP_MANE_IMPACT`, `VEP_MANE_HGVSc`, `VEP_MANE_HGVSp`, and other VEP/MANE fields

The original team template proposed `results/tables/annotated_variants.tsv`. **That filename is not the delivered Module 3 table.** Module 4 should use `final_annotation_with_VEP.tsv`, or the team should explicitly agree on a named copy/updated input path.

**Do not use `results/tables/variants_for_prioritization.tsv` as a substitute for the final integrated table.** It is an earlier intermediate extract whose `AF`, `AC`, and `AN` fields are placeholders (`NA`). Missing values must never be interpreted as zeros.

## Dataset and Results Summary

| Gene | Variant records |
|---|---:|
| BRCA1 | 30 |
| BRCA2 | 30 |
| PALB2 | 30 |
| TP53 | 30 |
| **Total** | **120** |

- Genome assembly: **GRCh38**
- Duplicate variant keys: **0**
- gnomAD API status: **14 FOUND**, **106 NOT_FOUND** for the queried dataset
- ExAC allele-frequency entries available: **3**
- VEP consequence annotation: **120 variant records**
- VEP predicted impact: **HIGH 66**, **MODERATE 49**, **LOW 4**, **MODIFIER 1**

## Annotation QC Documentation

Local validation previously reported `FINAL PROJECT VALIDATION PASSED` for the supplied output and raw VEP MANE batches. Run from the repository root:

```bash
python scripts/module3/validate_full_annotation.py
```

**Prerequisite:** This validator reads `results/vep_mane/vep_mane_batch_01.json` through `vep_mane_batch_12.json`. These original JSON files are currently kept in the local analysis package pending supervisor guidance and are **not yet part of the planned GitHub upload**. Consequently, the full validation cannot run from a GitHub checkout that omits them. Do not report a fresh verification on GitHub unless the required inputs are available.

## Commands and Scripts

The existing team placeholder is `scripts/module3_annotate_extract.py`. The analysis code supplied for Module 3 is currently organized separately under `scripts/module3/`:

- `final_annotation.sh` — early ClinVar extraction; expects `data/processed/breast_cancer_small_correct.vcf.gz`
- `retry_gnomad_api.py` — gnomAD query retries
- `run_remaining_vep.py` — VEP REST API batch requests
- `run_vep_mane.py` — MANE/HGVS VEP requests
- `validate_full_annotation.py` — final consistency checks against original JSON outputs

The initial extraction script does **not** regenerate the integrated final VEP table alone. The complete merge/build procedure is not yet available as one end-to-end reproducible script. The workflow and dependencies must be documented before claiming full from-scratch reproducibility.

Environment specifications are in `docs/module3/environment.yml` and `docs/module3/environment_vep.yml`. Additional notes belong in `docs/module3/README.md`.

## Additional Output Files

- `results/tables/clinvar_annotations.tsv`
- `results/tables/final_annotated_variants.tsv`
- `results/tables/final_complete_annotation.tsv`
- `results/tables/population_frequencies_final.tsv`
- `results/tables/gnomad_api_frequencies.tsv`
- `results/tables/variants_for_prioritization.tsv` (intermediate, **not** the recommended Module 4 input)
- `results/reports/final_annotation_summary.txt`

## Interpretation and Pending Decisions

- VEP predicted impact is **not** an ACMG/AMP clinical pathogenicity classification.
- `NOT_FOUND` refers only to the queried gnomAD dataset; it does not prove complete population absence.
- The currently supplied `final_annotation_with_VEP.tsv` **does not contain separate SIFT or PolyPhen columns**. If a newer table is used to include available predictions, confirm its provenance and mark missing scores as missing rather than negative.
- The supervisor indicated that final annotated tables and scripts are generally sufficient for GitHub unless the detailed VEP/VEP MANE JSON files are specifically required. Keep the originals safely, and document their location or regeneration procedure before declaring the checkout fully reproducible.
- Confirm the output filename expected by Module 4 and any changes to the project README before finalizing the pull request.
