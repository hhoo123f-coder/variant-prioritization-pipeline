# Final Quality Control Checklist

**Student 1 — Dataset Preparation and Initial QC**
**Date:** 2026-09-27

---

## 1. Data Integrity

- [x] Input ClinVar VCF downloaded successfully
- [x] Input VCF is readable with bcftools
- [x] Input VCF index (.tbi) is present
- [x] Output VCF (unfiltered) is readable
- [x] Output VCF (unfiltered) is indexed
- [x] Output VCF (filtered) is readable
- [x] Output VCF (filtered) is indexed

## 2. Genome Assembly

- [x] Genome assembly confirmed as GRCh38
- [x] No mixing of GRCh37 and GRCh38 coordinates
- [x] Chromosome names verified: numeric (13, 16, 17) — no chr prefix

## 3. Record Counts

- [x] Unfiltered records: 47,428
- [x] After clinical filter: 21,799
- [x] Final balanced subset: 120

## 4. Distribution Verification

### By Clinical Significance

- [x] Pathogenic: 40
- [x] Likely_pathogenic: 40
- [x] Uncertain_significance: 40

### By Gene

- [x] BRCA1: 30
- [x] BRCA2: 30
- [x] PALB2: 30
- [x] TP53: 30

## 5. INFO Fields

- [x] CLNSIG present
- [x] CLNREVSTAT present
- [x] CLNDN present
- [x] GENEINFO present

## 6. Documentation

- [x] data_description.txt created
- [x] output_1.txt created
- [x] HANDOFF_NOTES.md created
- [x] docs/software_versions.txt created
- [x] README.md created
- [x] methods.md created
- [x] docs/reproducibility.md created
- [x] docs/final_checklist.md created

## 7. Handoff Archive

- [x] student1_handoff.tar.gz created
- [x] Archive contains VCF + index
- [x] Archive contains statistics
- [x] Archive contains software versions
- [x] Archive contains documentation

## 8. GitHub Readiness

- [x] .gitignore created
- [x] Large VCF files excluded from commit
- [x] .tar.gz archives excluded from commit
- [x] No patient-level data included

## 9. Scientific Correctness

- [x] CLNSIG filter uses explicit OR (not regex)
- [x] bcftools sort applied before tabix
- [x] Numeric chromosome names used
- [x] Educational disclaimer included

## 10. Handoff to Student 2

- [x] HANDOFF_NOTES.md contains clear instructions
- [x] Known pitfalls documented (QUAL, DP, chr prefix)
- [x] File names and paths specified
- [x] Verification commands provided

---

## Sign-off

| Role | Name | Date |
|------|------|------|
| Student 1 | Alhanouf | 2026-09-27 |

---

Educational project — not for clinical diagnosis.
