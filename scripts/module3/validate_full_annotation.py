# Validate final clinical, frequency, and VEP annotations

import csv
import json
from pathlib import Path
from collections import Counter

base = Path("results/tables")
original_path = base / "final_complete_annotation.tsv"
final_path = base / "final_annotation_with_VEP.tsv"

def read_table(path):
    with path.open(newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))

def key(row):
    return tuple(row[c] for c in ("CHROM", "POS", "REF", "ALT"))

# Check final tables
original = read_table(original_path)
final = read_table(final_path)

assert len(original) == len(final) == 120

old_map = {key(r): r for r in original}
final_map = {key(r): r for r in final}

assert len(old_map) == len(final_map) == 120
assert old_map.keys() == final_map.keys()

# Check original data were preserved
for k, row in old_map.items():
    for column, value in row.items():
        assert final_map[k][column] == value

print("Clinical and frequency data: PASSED")

# Check genes
genes = Counter(r["GENEINFO"].split(":")[0] for r in final)
assert genes == {
    "BRCA1": 30, "BRCA2": 30,
    "PALB2": 30, "TP53": 30
}

print("Gene counts:", dict(genes))

# Check population frequencies
status = Counter(r["GNOMAD_STATUS"] for r in final)

assert status == {"FOUND": 14, "NOT_FOUND": 106}

for row in final:
    values = [
        row["GNOMAD_GENOME_AF"],
        row["GNOMAD_EXOME_AF"]
    ]
    if row["GNOMAD_STATUS"] == "FOUND":
        assert any(v != "." for v in values)

    for value in values:
        if value != ".":
            assert 0 <= float(value) <= 1

print("gnomAD frequencies:", dict(status))
print("Population frequency: PASSED")

# Independently check all VEP MANE records
checked = set()

for batch in range(1, 13):
    path = Path(
        f"results/vep_mane/vep_mane_batch_{batch:02d}.json"
    )

    with path.open() as f:
        results = json.load(f)

    assert len(results) == 10

    for result in results:
        parts = result["input"].split()
        k = (parts[0], parts[1], parts[3], parts[4])

        assert k in final_map
        assert k not in checked
        assert result["assembly_name"] == "GRCh38"

        row = final_map[k]
        gene = row["GENEINFO"].split(":")[0]

        mane = [
            t for t in result.get("transcript_consequences", [])
            if t.get("gene_symbol") == gene
            and t.get("mane_select")
        ]

        assert len(mane) == 1
        t = mane[0]

        assert row["VEP_MANE_TRANSCRIPT"] == t["transcript_id"]
        assert row["VEP_MANE_IMPACT"] == t["impact"]
        assert row["VEP_MANE_REFSEQ"] == t["mane_select"]
        assert row["VEP_MANE_CONSEQUENCE"] == "&".join(
            t["consequence_terms"]
        )

        checked.add(k)

assert len(checked) == 120

print("VEP MANE annotations: PASSED (120)")
print("Duplicate variants: 0")
print("FINAL PROJECT VALIDATION PASSED")
