import csv
import json
import shutil
import time
import urllib.request
import urllib.error
from pathlib import Path
from collections import Counter

path = Path("results/tables/gnomad_api_frequencies.tsv")

with path.open(newline="") as f:
    reader = csv.DictReader(f, delimiter="\t")
    fields = reader.fieldnames
    rows = list(reader)

pending = [r for r in rows if r["STATUS"] == "REQUEST_ERROR"]
selected = pending[:10]

query = """
query($id: String!) {
  variant(variantId: $id, dataset: gnomad_r4) {
    genome { af }
    exome { af }
  }
}
"""

def save():
    shutil.copy2(path, str(path) + ".backup")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)

for i, row in enumerate(selected):
    vid = row["VARIANT_ID"]
    print("Checking:", row["GENE"], vid[:70], flush=True)

    req = urllib.request.Request(
        "https://gnomad.broadinstitute.org/api",
        data=json.dumps({
            "query": query,
            "variables": {"id": vid}
        }).encode(),
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.load(response)

        variant = (result.get("data") or {}).get("variant")

        if variant:
            genome = (variant.get("genome") or {}).get("af")
            exome = (variant.get("exome") or {}).get("af")

            row["GENOME_AF"] = genome if genome is not None else "."
            row["EXOME_AF"] = exome if exome is not None else "."
            row["STATUS"] = (
                "FOUND" if genome is not None or exome is not None
                else "NO_AF"
            )
        elif any(
            "Variant not found" in e.get("message", "")
            for e in result.get("errors", [])
        ):
            row["STATUS"] = "NOT_FOUND"
        else:
            print("API response needs review")
            break

        print("Result:", row["STATUS"], "Exome AF:", row["EXOME_AF"])
        save()

    except urllib.error.HTTPError as e:
        print("HTTP ERROR:", e.code)
        print("Retry-After:", e.headers.get("Retry-After", "Not provided"))
        break
    except Exception as e:
        print("ERROR:", str(e))
        break

    if i < len(selected) - 1:
        time.sleep(30)

print("Status counts:", dict(Counter(r["STATUS"] for r in rows)))
