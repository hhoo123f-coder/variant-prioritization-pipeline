# Module 3 Handoff — Annotation & Data Extraction

**Responsible Module:** Module 3 — Annotation & Data Extraction
**Status:** Pending completion
**Date:** [To be filled]

---

## Input from Module 2

### Filtered + Normalized VCF
`data/processed/breast_cancer_filtered_normalized.vcf.gz`
- Records: [To be filled]
- Filters applied: [To be filled]
- Normalization: [To be filled]

---

## Tasks

1. **Annotation**
   - Add gene information
   - Add clinical significance (CLNSIG)
   - Add review status (CLNREVSTAT)
   - Add variant identifier information
   - Add frequency information (if available)

2. **Annotation QC**
   - Verify annotation correctness
   - Check required fields exist
   - Ensure no information lost

3. **Data Extraction**
   - Extract important fields from annotated VCF

4. **Structured Table**
   - Create a clear TSV table with columns:
     - CHROM, POS, REF, ALT
     - GENE
     - CLNSIG, CLNREVSTAT
     - FREQUENCY

---

## Output (to be delivered to Module 4)

- `results/tables/annotated_variants.tsv`
- Annotation QC documentation

---

## Commands/Script

See `scripts/module3_annotate_extract.py`

---

*Educational project — not for clinical diagnosis.*
