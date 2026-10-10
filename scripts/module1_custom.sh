#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

INPUT_VCF="${1:-data/raw/clinvar.vcf.gz}"
OUTPUT_DIR="${2:-data/processed/custom_$(date +%Y%m%d_%H%M%S)}"

REGIONS="13:32315474-32400266,16:23603165-23641310,17:7668421-7687490,17:43044295-43170327"

log() { echo "[$(date '+%H:%M:%S')] $*"; }

if ! command -v bcftools &> /dev/null; then
  echo "ERROR: bcftools not found. Run: conda activate cancer-vcf"
  exit 1
fi

if ! command -v tabix &> /dev/null; then
  echo "ERROR: tabix not found. Run: conda activate cancer-vcf"
  exit 1
fi

echo "============================================================"
echo "  Module 1 Custom Run"
echo "============================================================"
echo "  Input:  $INPUT_VCF"
echo "  Output: $OUTPUT_DIR"
echo "============================================================"
echo ""

if [ ! -f "$INPUT_VCF" ]; then
  echo "ERROR: File not found: $INPUT_VCF"
  exit 1
fi

if [ ! -s "$INPUT_VCF" ]; then
  echo "ERROR: File is empty: $INPUT_VCF"
  exit 1
fi

if ! bcftools view -h "$INPUT_VCF" > /dev/null 2>&1; then
  echo "ERROR: Cannot read VCF: $INPUT_VCF"
  exit 1
fi

log "Input file is valid"
mkdir -p "$OUTPUT_DIR"

log "Step 1: Extracting regions..."
bcftools view -r "$REGIONS" "$INPUT_VCF" -Oz -o "$OUTPUT_DIR/extracted.vcf.gz"
tabix -f -p vcf "$OUTPUT_DIR/extracted.vcf.gz"
N1=$(bcftools view -H "$OUTPUT_DIR/extracted.vcf.gz" | wc -l)
log "Extracted: $N1"

log "Step 2: Filtering CLNSIG..."
bcftools view -i 'INFO/CLNSIG="Pathogenic" || INFO/CLNSIG="Likely_pathogenic" || INFO/CLNSIG="Uncertain_significance"' "$OUTPUT_DIR/extracted.vcf.gz" -Oz -o "$OUTPUT_DIR/filtered.vcf.gz"
tabix -f -p vcf "$OUTPUT_DIR/filtered.vcf.gz"
N2=$(bcftools view -H "$OUTPUT_DIR/filtered.vcf.gz" | wc -l)
log "Filtered: $N2"

log "Step 3: Creating balanced subset..."
TMP_VCF="$OUTPUT_DIR/tmp.vcf"
bcftools view -h "$OUTPUT_DIR/filtered.vcf.gz" > "$TMP_VCF"

for gene in BRCA1 BRCA2 PALB2 TP53; do
  case "$gene" in
    BRCA1) REGION="17:43044295-43170327";;
    BRCA2) REGION="13:32315474-32400266";;
    PALB2) REGION="16:23603165-23641310";;
    TP53)  REGION="17:7668421-7687490";;
  esac
  for sig in "Pathogenic" "Likely_pathogenic" "Uncertain_significance"; do
    bcftools view -H -i "INFO/CLNSIG=\"$sig\"" -r "$REGION" "$OUTPUT_DIR/filtered.vcf.gz" | shuf -n 10 >> "$TMP_VCF" 2>/dev/null || true
  done
done

bcftools sort "$TMP_VCF" -Oz -o "$OUTPUT_DIR/small.vcf.gz"
tabix -f -p vcf "$OUTPUT_DIR/small.vcf.gz"
rm -f "$TMP_VCF"
N3=$(bcftools view -H "$OUTPUT_DIR/small.vcf.gz" | wc -l)
log "Final: $N3"

log "Step 4: Statistics..."
bcftools stats "$OUTPUT_DIR/small.vcf.gz" > "$OUTPUT_DIR/stats.txt"

echo ""
echo "============================================================"
echo "  Run Complete"
echo "============================================================"
echo "  Extracted: $N1"
echo "  Filtered:  $N2"
echo "  Final:     $N3"
echo ""
echo "  Output: $OUTPUT_DIR"
echo "============================================================"
