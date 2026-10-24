#!/usr/bin/env bash
set -euo pipefail

# Module 2 - VCF Normalization
# This script normalizes the filtered VCF file delivered by Student 1 (Hanouf)
# using bcftools norm with the GRCh38 reference genome.
# It verifies input files, runs normalization, indexes the output,
# and prints record counts before and after normalization.

# Input VCF (filtered file from Student 1)
INPUT_VCF="data/processed/breast_cancer_small_ClinVar_GRCh38.filtered.vcf.gz"

# Reference genome (GRCh38)
REF="data/processed/Homo_sapiens.GRCh38.dna.primary_assembly.fa"

# Output normalized VCF
OUT_VCF="data/processed/breast_cancer_small_ClinVar_GRCh38.norm.vcf.gz"

echo "Input VCF: $INPUT_VCF"
echo "Reference genome: $REF"
echo "Output VCF: $OUT_VCF"

# Check input VCF exists
if [ ! -f "$INPUT_VCF" ]; then
    echo "ERROR: Input VCF not found: $INPUT_VCF"
    exit 1
fi

# Check reference genome exists
if [ ! -f "$REF" ]; then
    echo "ERROR: Reference genome not found: $REF"
    exit 1
fi

# Run normalization
echo "Running bcftools norm..."
bcftools norm -f "$REF" -Oz -o "$OUT_VCF" "$INPUT_VCF"

# Index the normalized VCF
echo "Indexing output VCF..."
tabix -p vcf "$OUT_VCF"

# Count records before and after normalization
echo "Records in input VCF:"
bcftools view -H "$INPUT_VCF" | wc -l

echo "Records in output VCF:"
bcftools view -H "$OUT_VCF" | wc -l

echo "Normalization completed successfully."
