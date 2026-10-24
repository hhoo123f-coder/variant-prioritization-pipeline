#!/bin/bash
set -euo pipefail

# Step 1: Define input and output paths
INPUT="data/processed/breast_cancer_small_correct.vcf.gz"
OUTPUT="${OUTPUT_DIR:-results/tables}"
mkdir -p "$OUTPUT"

# Safety: Never overwrite existing result tables
for name in clinvar_annotations.tsv final_annotated_variants.tsv variants_for_prioritization.tsv; do
    if [[ -e "$OUTPUT/$name" ]]; then
        echo "STOP: Existing result file: $OUTPUT/$name"
        echo "Use a new OUTPUT_DIR to run the script safely."
        exit 1
    fi
done

# Step 2: Extract clinical annotations from ClinVar
# Create a table with variant information
printf 'CHROM\tPOS\tID\tREF\tALT\tGENEINFO\tCLNSIG\tCLNREVSTAT\tCLNDN\tMC\n' > "$OUTPUT/clinvar_annotations.tsv"

bcftools query \
-f '%CHROM\t%POS\t%ID\t%REF\t%ALT\t%INFO/GENEINFO\t%INFO/CLNSIG\t%INFO/CLNREVSTAT\t%INFO/CLNDN\t%INFO/MC\n' \
"$INPUT" >> "$OUTPUT/clinvar_annotations.tsv"

# Step 3: Add population frequency columns
# NA means frequency values are not yet confirmed
awk 'BEGIN {FS=OFS="\t"}
NR==1 {print $0,"AF","AC","AN"; next}
{print $0,"NA","NA","NA"}' \
"$OUTPUT/clinvar_annotations.tsv" \
> "$OUTPUT/final_annotated_variants.tsv"

# Step 4: Prepare the table for prioritization
cp "$OUTPUT/final_annotated_variants.tsv" \
"$OUTPUT/variants_for_prioritization.tsv"

# Step 5: Count total variants
echo "Total variants:"
awk 'END {print NR-1}' \
"$OUTPUT/final_annotated_variants.tsv"

# Step 6: Count variants per gene
echo "Variants per gene:"
awk -F '\t' 'NR>1 {
split($6,g,":")
count[g[1]]++
}
END {
for (gene in count) print gene,count[gene]
}' "$OUTPUT/final_annotated_variants.tsv"

# Step 7: Check duplicate variants
echo "Duplicate variants:"
awk -F '\t' 'NR>1 {
key=$1 FS $2 FS $4 FS $5
count[key]++
}
END {
for (key in count)
if (count[key]>1) duplicates++
print duplicates+0
}' "$OUTPUT/final_annotated_variants.tsv"

# Step 8: Check missing core annotations
echo "Missing core annotation values:"
awk -F '\t' 'NR>1 {
for (i=1;i<=10;i++)
if ($i=="" || $i=="." || $i=="NA") missing++
}
END {print missing+0}' \
"$OUTPUT/final_annotated_variants.tsv"

# Step 9: Count unavailable frequency values
echo "Missing AF values:"
awk -F '\t' 'NR>1 && $11=="NA" {n++}
END {print n+0}' \
"$OUTPUT/final_annotated_variants.tsv"

echo "Annotation workflow completed."

