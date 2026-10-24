# Continue VEP analysis safely without overwriting previous batches

import csv
import json
import time
import urllib.request
import urllib.error
from pathlib import Path
from collections import Counter

source = Path("results/tables/final_complete_annotation.tsv")
folder = Path("results/vep")
folder.mkdir(parents=True, exist_ok=True)

with source.open(newline="") as f:
    rows = list(csv.DictReader(f, delimiter="\t"))

assert len(rows) == 120, "Expected 120 variants"

def expected_inputs(batch):
    start = (batch - 1) * 10
    return [
        f'{r["CHROM"]} {r["POS"]} . {r["REF"]} {r["ALT"]} . . .'
        for r in rows[start:start + 10]
    ]

def validate(results, variants):
    assert isinstance(results, list)
    assert len(results) == len(variants)
    assert all(r.get("assembly_name") == "GRCh38" for r in results)
    assert Counter(
        tuple(r["input"].split()[:5]) for r in results
    ) == Counter(
        tuple(v.split()[:5]) for v in variants
    )

# Verify previously completed batches
for batch in (1, 2):
    path = folder / f"vep_batch_{batch:02d}.json"
    with path.open() as f:
        validate(json.load(f), expected_inputs(batch))

print("Previous batches verified: 20 variants", flush=True)

# Process remaining batches
for batch in range(3, 13):
    output = folder / f"vep_batch_{batch:02d}.json"
    variants = expected_inputs(batch)

    if output.exists():
        with output.open() as f:
            validate(json.load(f), variants)
        print(f"Batch {batch:02d}: already verified", flush=True)
        continue

    request = urllib.request.Request(
        "https://rest.ensembl.org/vep/homo_sapiens/region",
        data=json.dumps({"variants": variants}).encode(),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    )

    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            results = json.load(response)

        validate(results, variants)

        # Create a new file; never overwrite an existing result
        with output.open("x") as f:
            json.dump(results, f, indent=2)

        print(f"Batch {batch:02d}: PASSED (10 variants)", flush=True)
        time.sleep(5)

    except Exception as error:
        print(f"STOP at batch {batch:02d}: {error}", flush=True)
        print("Saved batches remain unchanged.", flush=True)
        break

print("Finished available batches.", flush=True)
