# Handoff Notes — Module 1 to Module 2

## Delivered Files

| File | Description |
|------|-------------|
| data/processed/breast_cancer_small_ClinVar_GRCh38.vcf.gz | Ready-to-analyze file (120 variants) |
| data/processed/breast_cancer_small_ClinVar_GRCh38.vcf.gz.tbi | Tabix index |
| results/reports/vcf_stats_small.txt | Statistics of the filtered file |
| software_versions.txt | Tool versions |
| data_description.txt | Dataset description |
| output_1.txt | Handoff summary |

## Work Completed

1. Downloaded ClinVar GRCh38 VCF (2026-09-14)
2. Extracted regions for BRCA1, BRCA2, PALB2, TP53
3. Compressed and indexed the file (47,428 records)
4. Applied CLNSIG filter to keep only:
   - Pathogenic
   - Likely_pathogenic
   - Uncertain_significance
5. Selected a balanced sample: 10 variants per gene per class = 120 variants
6. Sorted the file and indexed it with tabix
7. Validated the file and generated statistics

## Final Distribution

### By Clinical Significance

| Category | Count |
|----------|-------|
| Pathogenic | 40 |
| Likely_pathogenic | 40 |
| Uncertain_significance | 40 |
| Total | 120 |

### By Gene

| Gene | Count |
|------|-------|
| BRCA1 | 30 |
| BRCA2 | 30 |
| PALB2 | 30 |
| TP53 | 30 |

## Important Notes for Module 2

### DO NOT use:
- QUAL filter — not present in ClinVar
- DP filter — not present in ClinVar
- Position-only matching — use CHROM+POS+REF+ALT

### DO use:
- File: breast_cancer_small_ClinVar_GRCh38.vcf.gz
- Four-field matching: CHROM, POS, REF, ALT
- CLNSIG filter if additional filtering is needed

### Technical Notes:
1. Chromosome names are numeric: 13, 16, 17 (no chr prefix)
2. CLNSIG syntax: use INFO/CLNSIG="Pathogenic" NOT CLNSIG="Pathogenic"
3. GENEINFO may contain overlapping genes: e.g., BRCA1:672|LOC126862571:126862571

## Commands to Verify the File

bcftools view -H data/processed/breast_cancer_small_ClinVar_GRCh38.vcf.gz | wc -l

bcftools query -f '%INFO/CLNSIG\n' data/processed/breast_cancer_small_ClinVar_GRCh38.vcf.gz | sort | uniq -c

bcftools query -f '%INFO/GENEINFO\n' data/processed/breast_cancer_small_ClinVar_GRCh38.vcf.gz | sort | uniq -c

bcftools query -f '%CHROM\t%POS\t%REF\t%ALT\t%INFO/GENEINFO\t%INFO/CLNSIG\n' data/processed/breast_cancer_small_ClinVar_GRCh38.vcf.gz | head -5

## If You Get Zero Results

Send me the exact command you ran, and I will help.

## Reminder

This is an educational analysis, not a clinical diagnosis. Educational scores do not mean a variant is truly pathogenic.

Good luck!
