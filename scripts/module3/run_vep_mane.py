# Add MANE, Canonical, and HGVS annotations safely

import csv
import json
import time
import urllib.request
from pathlib import Path
from collections import Counter

source = Path("results/tables/final_complete_annotation.tsv")
folder = Path("results/vep_mane")

with source.open(newline="") as f:
    rows = list(csv.DictReader(f, delimiter="\t"))

assert len(rows) == 120, "Expected 120 variants"

folder.mkdir(parents=True, exist_ok=True)

def make_inputs(group):
    return [
        f'{r["CHROM"]} {r["POS"]} . {r["REF"]} {r["ALT"]} . . .'
        for r in group
    ]

for batch in range(1, 13):
    start = (batch - 1) * 10
    variants = make_inputs(rows[start:start + 10])
    output = folder / f"vep_mane_batch_{batch:02d}.json"

    if output.exists():
        with output.open() as f:
            results = json.load(f)
        print(f"Batch {batch:02d}: already saved", flush=True)
    else:
        request = urllib.request.Request(
            "https://rest.ensembl.org/vep/homo_sapiens/region"
            "?mane=1&canonical=1&hgvs=1",
            data=json.dumps({"variants": variants}).encode(),
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )

        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                results = json.load(response)
        except Exception as error:
            print(f"STOP at batch {batch:02d}: {error}", flush=True)
            break

    # Validate before proceeding
    assert len(results) == 10
    assert all(r.get("assembly_name") == "GRCh38" for r in results)

    assert Counter(
        tuple(r["input"].split()[:5]) for r in results
    ) == Counter(
        tuple(v.split()[:5]) for v in variants
    )

    if not output.exists():
        with output.open("x") as f:
            json.dump(results, f, indent=2)

    print(f"Batch {batch:02d}: PASSED", flush=True)
    time.sleep(5)

print("Finished available batches.", flush=True)
