# Add SIFT and PolyPhen predictions to the new VEP file

import json
import pandas as pd
from urllib.request import Request, urlopen

# Define paths relative to the Module 4 folder
from pathlib import Path

MODULE4_DIR = Path(__file__).resolve().parent.parent
input_file = MODULE4_DIR / "input" / "final_annotation_with_VEP.tsv"
output_file = MODULE4_DIR / "input" / "final_annotation_with_VEP_SIFT_PolyPhen.tsv"

df = pd.read_csv(input_file, sep="\t")

# Create empty prediction columns
df["SIFT_PREDICTION"] = pd.NA
df["POLYPHEN_PREDICTION"] = pd.NA
df["PREDICTION_STATUS"] = pd.NA

# Select variants with a missense consequence
mask = df["VEP_MANE_CONSEQUENCE"].fillna("").str.contains(
    "missense_variant"
)

df.loc[mask, "PREDICTION_STATUS"] = "Not available"

# Prepare variant information for Ensembl
variant_rows = {}

for index, row in df[mask].iterrows():
    chrom = str(row["CHROM"]).replace("chr", "")
    pos = int(row["POS"])
    ref = str(row["REF"])
    alt = str(row["ALT"])

    variant = f"{chrom} {pos} {pos + len(ref) - 1} {ref}/{alt} 1"
    variant_rows.setdefault(variant, []).append(index)

variants = list(variant_rows.keys())
results = []

# Request predictions in small batches
for start in range(0, len(variants), 20):
    batch = variants[start:start + 20]

    url = "https://rest.ensembl.org/vep/human/region?mane=1"
    body = json.dumps({"variants": batch}).encode()

    request = Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    )

    # Get predictions from Ensembl
    with urlopen(request, timeout=60) as response:
        results.extend(json.load(response))

# Match predictions to the MANE transcript in our file
for item in results:
    variant = item.get("input")
    indexes = variant_rows.get(variant, [])

    for index in indexes:
        target_mane = df.at[index, "VEP_MANE_REFSEQ"]

        for transcript in item.get("transcript_consequences", []):
            mane = transcript.get("mane_select")

            if mane != target_mane:
                continue

            if "missense_variant" not in transcript.get(
                "consequence_terms", []
            ):
                continue

            sift = transcript.get("sift_prediction")
            polyphen = transcript.get("polyphen_prediction")

            df.at[index, "SIFT_PREDICTION"] = sift if sift else pd.NA
            df.at[index, "POLYPHEN_PREDICTION"] = (
                polyphen if polyphen else pd.NA
            )

            if sift or polyphen:
                df.at[index, "PREDICTION_STATUS"] = "Prediction available"

            break

# Save the new file without changing the original
df.to_csv(output_file, sep="\t", index=False)

# Show a simple summary
available = (df["PREDICTION_STATUS"] == "Prediction available").sum()
missing = (df["PREDICTION_STATUS"] == "Not available").sum()

print("Total variants:", len(df))
print("Missense variants:", int(mask.sum()))
print("Variants with predictions:", int(available))
print("Variants without predictions:", int(missing))
print("Saved file:", output_file)

# List missense variants without predictions
missing_rows = df[df["PREDICTION_STATUS"] == "Not available"]

if not missing_rows.empty:
    print("\nMissense variants without predictions:")
    print(
        missing_rows[["CHROM", "POS", "REF", "ALT"]]
        .to_string(index=False)
    )
