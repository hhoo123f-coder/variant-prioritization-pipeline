# Methods

**Module 1 — Dataset Preparation, VCF Inspection, Validation, Filtering, and Initial QC**

---

## 1. Study Design

The breast-cancer panel was selected, containing four genes: BRCA1, BRCA2, PALB2, TP53. All analysis steps used the GRCh38 genome assembly.

---

## 2. Data Sources

### 2.1 Primary Source — NCBI ClinVar

| Item | Value |
|------|-------|
| Source | NCBI ClinVar |
| URL | https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/ |
| Data type | Annotated VCF (GRCh38) |
| Download date | 2026-09-14 |
| Processing date | 2026-09-27 |

### 2.2 Population Source — gnomAD

| Item | Value |
|------|-------|
| Source | Genome Aggregation Database (gnomAD) |
| Release | v4.1 |
| Assembly | GRCh38 |
| Fields | AF, AC, AN |
| Use | Population-frequency evidence (Module 2) |

---

## 3. Software and Tools

The analysis was performed in Ubuntu/WSL2 using a Conda environment named cancer-vcf.

| Tool | Version | Purpose |
|------|---------|---------|
| bcftools | 1.24 | VCF manipulation |
| htslib | 1.24 | VCF/BCF I/O |
| tabix | 1.24 | VCF indexing |
| Python | 3.14.7 | Scripting |

---

## 4. Target Gene Regions

| Gene | Chromosome | GRCh38 Region |
|------|------------|---------------|
| BRCA1 | 17 | 17:43044295-43170327 |
| BRCA2 | 13 | 13:32315474-32400266 |
| PALB2 | 16 | 16:23603165-23641310 |
| TP53  | 17 | 17:7668421-7687490  |

Note: Chromosome names in the ClinVar VCF are numeric (13, 16, 17) without the chr prefix.

---

## 5. Workflow Steps

### Step 1 — Region Extraction

    bcftools view -r 13:32315474-32400266,16:23603165-23641310,17:7668421-7687490,17:43044295-43170327 \
      data/raw/clinvar.vcf.gz \
      -Oz -o data/processed/breast_cancer_ClinVar_GRCh38.vcf.gz

    tabix -p vcf data/processed/breast_cancer_ClinVar_GRCh38.vcf.gz

Result: 47,428 records.

### Step 2 — Clinical Filtering

    bcftools view \
      -i 'INFO/CLNSIG="Pathogenic" || INFO/CLNSIG="Likely_pathogenic" || INFO/CLNSIG="Uncertain_significance"' \
      data/processed/breast_cancer_ClinVar_GRCh38.vcf.gz \
      -Oz -o data/processed/breast_cancer_clinical_filtered.vcf.gz

Rationale: The regex operator did not reliably match compound CLNSIG values in bcftools 1.24. The explicit OR operator was used instead.

Result: 21,799 records.

### Step 3 — Balanced Teaching Subset

To create a small, reproducible teaching dataset, a stratified sample was drawn: 10 variants per gene per clinical class (4 genes x 3 classes x 10 = 120 variants).

    bcftools view -h clinical_filtered.vcf.gz > /tmp/small_panel.vcf

    for gene in BRCA1 BRCA2 PALB2 TP53; do
      for sig in "Pathogenic" "Likely_pathogenic" "Uncertain_significance"; do
        bcftools view -H -i "INFO/CLNSIG=\"$sig\"" -r "$REGION" \
          clinical_filtered.vcf.gz | shuf -n 10 >> /tmp/small_panel.vcf
      done
    done

    bcftools sort /tmp/small_panel.vcf -Oz -o breast_cancer_small_ClinVar_GRCh38.vcf.gz
    tabix -p vcf breast_cancer_small_ClinVar_GRCh38.vcf.gz

Note: bcftools sort is required before tabix because shuf randomizes record order.

Result: 120 records.

---

## 6. Final Distribution

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

### By Variant Type (from bcftools stats)

| Type | Count |
|------|-------|
| SNPs | 52 |
| Indels | 61 |
| MNPs | 2 |
| Others | 5 |

---

## 7. Quality Control

The following QC checks were performed:

1. Input VCF opened successfully with bcftools
2. Genome assembly confirmed as GRCh38
3. Chromosome names verified (numeric: 13, 16, 17)
4. INFO fields confirmed: CLNSIG, CLNREVSTAT, CLNDN, GENEINFO
5. Record counts verified: 47,428 to 21,799 to 120
6. Output compressed in BGZF format
7. Tabix index created successfully
8. Statistics generated with bcftools stats
9. Software versions recorded for reproducibility

---

## 8. Reproducibility

All steps are automated in scripts/student1_workflow.sh. The workflow is idempotent — safe to re-run.

To reproduce from scratch:

    bash scripts/student1_workflow.sh

---

## 9. Limitations

- ClinVar contains submitted assertions, not raw patient-level data.
- Record counts represent overlapping genomic intervals, not unique variants.
- Some records may contain multiple or conflicting classifications.
- GENEINFO may include overlapping gene annotations.
- The 120-variant subset is a representative teaching sample.
- gnomAD population-frequency information is not included at this stage.
- No variant normalization was applied — this is Module 2's task.

---

## 10. Educational Disclaimer

This is an educational bioinformatics workflow. The results are not intended for clinical interpretation, diagnosis, or patient care.

---

