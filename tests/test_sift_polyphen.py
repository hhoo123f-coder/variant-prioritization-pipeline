# Test SIFT and PolyPhen for five missense variants

import json
import pandas as pd
from urllib.request import Request, urlopen

# Read the original VEP file
df = pd.read_csv("input/final_annotation_with_VEP.tsv", sep="\t")

# Select five missense variants
df = df[
    df["VEP_MANE_CONSEQUENCE"]
    .fillna("")
    .str.contains("missense_variant")
].head(5)

# Prepare the variants for Ensembl
variants = []
for _, row in df.iterrows():
    chrom = str(row["CHROM"]).replace("chr", "")
    pos = int(row["POS"])
    ref = row["REF"]
    alt = row["ALT"]
    variants.append(f"{chrom} {pos} {pos + len(ref) - 1} {ref}/{alt} 1")

# Request MANE predictions from Ensembl
url = "https://rest.ensembl.org/vep/human/region?mane=1"
body = json.dumps({"variants": variants}).encode()

request = Request(
    url,
    data=body,
    headers={
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
)

with urlopen(request, timeout=60) as response:
    results = json.load(response)

# Show predictions for MANE Select transcripts
for item in results:
    print("\nVariant:", item.get("input"))
    found = False

    for transcript in item.get("transcript_consequences", []):
        mane = transcript.get("mane_select")

        if mane and "missense_variant" in transcript.get("consequence_terms", []):
            print("MANE Select:", mane)
            print("SIFT:", transcript.get("sift_prediction", "Not available"))
            print("PolyPhen:", transcript.get("polyphen_prediction", "Not available"))
            found = True

    if not found:
        print("MANE predictions: Not available")
