# Module 2 — Handoff Summary (Normalization)
Student: Kholud  
Date: 11 October 2026  
Module: 2 — Variant Normalization  
Next Module: 3 — Variant Annotation (Raghad)

---

## 1. Overview

This handoff summarizes the output of Module 2 (VCF normalization).  
The filtered ClinVar GRCh38 breast cancer dataset was normalized using bcftools and aligned to the GRCh38 reference genome.  
The output is ready for Module 3 annotation.

---

## 2. Input Provided by Module 1 (Hanouf)

- Filtered VCF file:  
  `data/processed/breast_cancer_small_ClinVar_GRCh38.filtered.vcf.gz`

- Genome assembly: GRCh38

---

## 3. Processing Performed in Module 2

- Normalization using `bcftools norm`
- Reference genome used:  
  `data/processed/Homo_sapiens.GRCh38.dna.primary_assembly.fa`
- Output compressed with bgzip
- Output indexed with tabix
- QC checks performed (header, reference match, record count, index generation)

---

## 4. Output Files for Module 3

These files must be used by the next student (Raghad):

### **Normalized VCF**
data/processed/breast_cancer_small_ClinVar_GRCh38.norm.vcf.gz


### **Index File**

data/processed/breast_cancer_small_ClinVar_GRCh38.norm.vcf.gz.tbi


### **Record Count**
- Number of variants: **120**

---

## 5. Notes for Module 3 (Raghad)

- The VCF is fully normalized and indexed.
- No multiallelic variants required splitting.
- No realignment or corrections were needed.
- The file is ready for annotation using VEP, ANNOVAR, or bcftools query.
- No errors or warnings were encountered during processing.

---

## 6. Reproducibility

### Command used:
bcftools norm -f data/processed/Homo_sapiens.GRCh38.dna.primary_assembly.fa \
-Oz -o data/processed/breast_cancer_small_ClinVar_GRCh38.norm.vcf.gz \
data/processed/breast_cancer_small_ClinVar_GRCh38.filtered.vcf.gz


### Software versions:
- bcftools 1.17  
- htslib 1.17  
- tabix 1.17  

---

## 7. Completion Status

Module 2 is **fully completed**.  
Output is ready for Module 3.

