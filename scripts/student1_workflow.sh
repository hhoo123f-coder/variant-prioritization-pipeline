#!/usr/bin/env bash
# =============================================================================
# Student 1 Workflow — ClinVar Breast Cancer Panel Preparation
# =============================================================================
#
# Project  : A Reproducible Workflow for Prioritizing Cancer-Associated
#            Variants Using ClinVar and gnomAD
# Author   : Student 1
# Date     : 2026-09-27
# Genome   : GRCh38
# Genes    : BRCA1, BRCA2, PALB2, TP53
# Tools    : bcftools 1.24, htslib 1.24, tabix 1.24, Python 3.14.7
#
# Purpose:
#   This script performs the complete Student 1 workflow:
#     1. Download ClinVar GRCh38 VCF
#     2. Extract four target gene regions
#     3. Apply clinical filter (CLNSIG)
#     4. Create balanced teaching subset (120 variants)
#     5. Generate statistics and documentation
#     6. Create handoff archive for Student 2
#
# Usage:
#   bash scripts/student1_workflow.sh
#
# Requirements:
#   - bcftools, tabix installed in active Conda environment
#   - Internet connection (for ClinVar download)
#   - ~2 GB free disk space
#
# IMPORTANT: This is an educational workflow, not a clinical pipeline.
# =============================================================================

set -euo pipefail  # Exit on error, undefined variables, pipe failures

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

RAW_DIR="data/raw"
PROCESSED_DIR="data/processed"
REPORTS_DIR="results/reports"
DOCS_DIR="docs"
SCRIPTS_DIR="scripts"

CLINVAR_URL="https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz"
CLINVAR_TBI_URL="https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz.tbi"

# Gene regions (GRCh38, numeric chromosome names)
REGION_BRCA1="17:43044295-43170327"
REGION_BRCA2="13:32315474-32400266"
REGION_PALB2="16:23603165-23641310"
REGION_TP53="17:7668421-7687490"
ALL_REGIONS="${REGION_BRCA2},${REGION_PALB2},${REGION_TP53},${REGION_BRCA1}"

# -----------------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------------
log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

section() {
  echo ""
  echo "===================================================================="
  echo "  $*"
  echo "===================================================================="
}

check_tool() {
  if ! command -v "$1" &> /dev/null; then
    echo "ERROR: $1 not found. Activate the 'cancer-vcf' Conda environment."
    exit 1
  fi
}

# -----------------------------------------------------------------------------
# Pre-flight checks
# -----------------------------------------------------------------------------
section "Pre-flight checks"
check_tool bcftools
check_tool tabix
check_tool wget

log "bcftools version: $(bcftools --version | head -1)"
log "tabix version: $(tabix --version | head -1)"
log "Working directory: $PROJECT_ROOT"

# -----------------------------------------------------------------------------
# Step 1: Download ClinVar GRCh38 VCF
# -----------------------------------------------------------------------------
section "Step 1: Download ClinVar GRCh38 VCF"

mkdir -p "$RAW_DIR"

if [ -f "$RAW_DIR/clinvar.vcf.gz" ]; then
  log "clinvar.vcf.gz already exists — skipping download."
else
  log "Downloading ClinVar VCF..."
  wget -O "$RAW_DIR/clinvar.vcf.gz" "$CLINVAR_URL"
  log "Downloading ClinVar index..."
  wget -O "$RAW_DIR/clinvar.vcf.gz.tbi" "$CLINVAR_TBI_URL"
fi

ls -lh "$RAW_DIR"/clinvar.vcf.gz*

# -----------------------------------------------------------------------------
# Step 2: Extract target gene regions
# -----------------------------------------------------------------------------
section "Step 2: Extract target gene regions (BRCA1, BRCA2, PALB2, TP53)"

mkdir -p "$PROCESSED_DIR"

bcftools view \
  -r "$ALL_REGIONS" \
  "$RAW_DIR/clinvar.vcf.gz" \
  -Oz -o "$PROCESSED_DIR/breast_cancer_ClinVar_GRCh38.vcf.gz"

tabix -f -p vcf "$PROCESSED_DIR/breast_cancer_ClinVar_GRCh38.vcf.gz"

N_UNFILTERED=$(bcftools view -H "$PROCESSED_DIR/breast_cancer_ClinVar_GRCh38.vcf.gz" | wc -l)
log "Unfiltered records: $N_UNFILTERED"
log "Expected: 47,428"

# -----------------------------------------------------------------------------
# Step 3: Apply clinical filter (CLNSIG)
# -----------------------------------------------------------------------------
section "Step 3: Apply clinical filter (Pathogenic, Likely_pathogenic, VUS)"

bcftools view \
  -i 'INFO/CLNSIG="Pathogenic" || INFO/CLNSIG="Likely_pathogenic" || INFO/CLNSIG="Uncertain_significance"' \
  "$PROCESSED_DIR/breast_cancer_ClinVar_GRCh38.vcf.gz" \
  -Oz -o /tmp/breast_cancer_clinical_filtered.vcf.gz

N_FILTERED=$(bcftools view -H /tmp/breast_cancer_clinical_filtered.vcf.gz | wc -l)
log "After clinical filter: $N_FILTERED"
log "Expected: 21,799"

# -----------------------------------------------------------------------------
# Step 4: Create balanced teaching subset (120 variants)
# -----------------------------------------------------------------------------
section "Step 4: Create balanced teaching subset (10 per gene per class)"

TMP_VCF=/tmp/small_panel.vcf
rm -f "$TMP_VCF"

# Preserve header
bcftools view -h /tmp/breast_cancer_clinical_filtered.vcf.gz > "$TMP_VCF"

# Sample 10 variants per gene per class
for gene in BRCA1 BRCA2 PALB2 TP53; do
  case "$gene" in
    BRCA1) REGION="$REGION_BRCA1";;
    BRCA2) REGION="$REGION_BRCA2";;
    PALB2) REGION="$REGION_PALB2";;
    TP53)  REGION="$REGION_TP53";;
  esac
  for sig in "Pathogenic" "Likely_pathogenic" "Uncertain_significance"; do
    bcftools view -H \
      -i "INFO/CLNSIG=\"$sig\"" \
      -r "$REGION" \
      /tmp/breast_cancer_clinical_filtered.vcf.gz \
      | shuf -n 10 >> "$TMP_VCF"
  done
done

# Sort and compress (sort is required before tabix)
bcftools sort "$TMP_VCF" -Oz -o "$PROCESSED_DIR/breast_cancer_small_ClinVar_GRCh38.vcf.gz"
tabix -f -p vcf "$PROCESSED_DIR/breast_cancer_small_ClinVar_GRCh38.vcf.gz"

rm -f "$TMP_VCF" /tmp/breast_cancer_clinical_filtered.vcf.gz

N_FINAL=$(bcftools view -H "$PROCESSED_DIR/breast_cancer_small_ClinVar_GRCh38.vcf.gz" | wc -l)
log "Final balanced subset: $N_FINAL records"
log "Expected: 120"

# -----------------------------------------------------------------------------
# Step 5: Verify distribution
# -----------------------------------------------------------------------------
section "Step 5: Verify final distribution"

log "Distribution by clinical significance:"
bcftools query -f '%INFO/CLNSIG\n' \
  "$PROCESSED_DIR/breast_cancer_small_ClinVar_GRCh38.vcf.gz" \
  | sort | uniq -c

log "Distribution by gene:"
bcftools query -f '%INFO/GENEINFO\n' \
  "$PROCESSED_DIR/breast_cancer_small_ClinVar_GRCh38.vcf.gz" \
  | sort | uniq -c

log "Distribution by chromosome:"
bcftools query -f '%CHROM\n' \
  "$PROCESSED_DIR/breast_cancer_small_ClinVar_GRCh38.vcf.gz" \
  | sort | uniq -c

# -----------------------------------------------------------------------------
# Step 6: Generate statistics
# -----------------------------------------------------------------------------
section "Step 6: Generate VCF statistics"

mkdir -p "$REPORTS_DIR"

bcftools stats "$PROCESSED_DIR/breast_cancer_small_ClinVar_GRCh38.vcf.gz" \
  > "$REPORTS_DIR/vcf_stats_small.txt"

log "Statistics saved: $REPORTS_DIR/vcf_stats_small.txt"
log "SNP count: $(grep -m1 'number of SNPs:' "$REPORTS_DIR/vcf_stats_small.txt" | cut -f4)"
log "Indel count: $(grep -m1 'number of indels:' "$REPORTS_DIR/vcf_stats_small.txt" | cut -f4)"

# -----------------------------------------------------------------------------
# Step 7: Record software versions
# -----------------------------------------------------------------------------
section "Step 7: Record software versions"

mkdir -p "$DOCS_DIR"

{
  echo "Software versions recorded on: $(date '+%Y-%m-%d %H:%M:%S')"
  echo ""
  bcftools --version | head -2
  echo ""
  tabix --version | head -1
  echo ""
  python3 --version 2>&1
} > "$DOCS_DIR/software_versions.txt"

cat "$DOCS_DIR/software_versions.txt"

# -----------------------------------------------------------------------------
# Step 8: Create handoff archive
# -----------------------------------------------------------------------------
section "Step 8: Create handoff archive for Student 2"

tar -czvf student1_handoff.tar.gz \
  "$PROCESSED_DIR/breast_cancer_small_ClinVar_GRCh38.vcf.gz" \
  "$PROCESSED_DIR/breast_cancer_small_ClinVar_GRCh38.vcf.gz.tbi" \
  "$REPORTS_DIR/vcf_stats_small.txt" \
  "$DOCS_DIR/software_versions.txt" \
  data_description.txt \
  output_1.txt \
  HANDOFF_NOTES.md

log "Archive created: student1_handoff.tar.gz"
tar -tzvf student1_handoff.tar.gz

# -----------------------------------------------------------------------------
# Done
# -----------------------------------------------------------------------------
section "Student 1 workflow completed successfully"
log "End time: $(date '+%Y-%m-%d %H:%M:%S')"
log "Output directory: $PROCESSED_DIR"
log "Handoff archive: $PROJECT_ROOT/student1_handoff.tar.gz"

echo ""
echo "Next step for Student 2:"
echo "  - Normalize variants with bcftools norm"
echo "  - Match gnomAD using CHROM + POS + REF + ALT"
echo "  - Run prioritization scoring"
echo ""
echo "Educational project — not for clinical diagnosis."
