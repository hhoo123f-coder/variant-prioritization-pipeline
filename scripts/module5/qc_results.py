import csv
from collections import Counter
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "module5"
RESULTS_DIR = BASE_DIR / "results" / "module5"
REPORT_DIR = RESULTS_DIR / "reports"

PRIORITY_FILE = DATA_DIR / "prioritized_variants.tsv"
ANNOTATION_FILE = DATA_DIR / "annotations_with_SIFT_PolyPhen.tsv"
REPORT_FILE = REPORT_DIR / "qc_report.txt"


def read_tsv(path):
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        rows = list(reader)
        return reader.fieldnames or [], rows


def main():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    issues = []
    report = []

    priority_headers, priority_rows = read_tsv(PRIORITY_FILE)
    annotation_headers, annotation_rows = read_tsv(ANNOTATION_FILE)

    report.append("QUALITY CONTROL REPORT")
    report.append("=" * 60)
    report.append(f"Priority table rows: {len(priority_rows)}")
    report.append(f"Priority table columns: {len(priority_headers)}")
    report.append(f"Annotation table rows: {len(annotation_rows)}")
    report.append(f"Annotation table columns: {len(annotation_headers)}")

    required_priority = {
        "CHROM", "POS", "REF", "ALT", "GENEINFO", "CLNSIG",
        "GNOMAD_STATUS", "VEP_MANE_IMPACT", "Priority_Rank",
        "Prioritization_Score", "Priority_Score", "Priority_Category",
        "ACMG_AMP_Review_Status",
    }
    required_annotation = {
        "CHROM", "POS", "REF", "ALT", "SIFT_PREDICTION",
        "POLYPHEN_PREDICTION", "PREDICTION_STATUS",
    }

    missing_priority = sorted(required_priority - set(priority_headers))
    missing_annotation = sorted(required_annotation - set(annotation_headers))

    report.append(f"Missing required priority columns: {missing_priority}")
    report.append(f"Missing required annotation columns: {missing_annotation}")

    if missing_priority:
        issues.append("Priority table is missing required columns.")
    if missing_annotation:
        issues.append("Annotation table is missing required columns.")

    report.append("\nPriority categories:")
    report.extend(
        f"  {key}: {value}"
        for key, value in sorted(
            Counter(row.get("Priority_Category", "") for row in priority_rows).items()
        )
    )

    report.append("\ngnomAD status counts:")
    report.extend(
        f"  {key or 'EMPTY'}: {value}"
        for key, value in sorted(
            Counter(row.get("GNOMAD_STATUS", "").strip() for row in priority_rows).items()
        )
    )

    report.append("\nACMG/AMP review status counts:")
    report.extend(
        f"  {key or 'EMPTY'}: {value}"
        for key, value in sorted(
            Counter(row.get("ACMG_AMP_Review_Status", "").strip() for row in priority_rows).items()
        )
    )

    report.append("\nPrediction status counts:")
    report.extend(
        f"  {key or 'EMPTY'}: {value}"
        for key, value in sorted(
            Counter(row.get("PREDICTION_STATUS", "").strip() for row in annotation_rows).items()
        )
    )

    priority_keys = [
        (
            row.get("CHROM", "").strip(),
            row.get("POS", "").strip(),
            row.get("REF", "").strip(),
            row.get("ALT", "").strip(),
        )
        for row in priority_rows
    ]
    annotation_keys = [
        (
            row.get("CHROM", "").strip(),
            row.get("POS", "").strip(),
            row.get("REF", "").strip(),
            row.get("ALT", "").strip(),
        )
        for row in annotation_rows
    ]

    report.append("\nVariant key checks:")
    report.append(f"  Unique priority keys: {len(set(priority_keys))}")
    report.append(f"  Unique annotation keys: {len(set(annotation_keys))}")
    report.append(f"  Duplicate priority keys: {len(priority_keys) - len(set(priority_keys))}")
    report.append(f"  Duplicate annotation keys: {len(annotation_keys) - len(set(annotation_keys))}")

    if len(priority_keys) != len(set(priority_keys)):
        issues.append("Duplicate variant keys found in priority table.")
    if len(annotation_keys) != len(set(annotation_keys)):
        issues.append("Duplicate variant keys found in annotation table.")

    if len(priority_rows) != 120:
        issues.append(f"Expected 120 priority rows, found {len(priority_rows)}.")
    if len(annotation_rows) != 120:
        issues.append(f"Expected 120 annotation rows, found {len(annotation_rows)}.")

    score_errors = 0
    for row in priority_rows:
        try:
            score = float(row["Prioritization_Score"])
            priority_score = float(row["Priority_Score"])
            rank = int(row["Priority_Rank"])
            rank_alias = int(row["Rank"])
            if score != priority_score or rank != rank_alias:
                score_errors += 1
        except (ValueError, KeyError, TypeError):
            score_errors += 1

    report.append("\nScore and rank checks:")
    report.append(f"  Score/rank inconsistencies: {score_errors}")
    if score_errors:
        issues.append(f"{score_errors} score/rank inconsistencies found.")

    report.append("\nFinal QC status:")
    if issues:
        report.append("QC NEEDS REVIEW")
        report.extend(f"  - {issue}" for issue in issues)
    else:
        report.append("QC STRUCTURAL CHECKS PASSED")
        report.append(
            "Note: Structural checks do not establish clinical validity or biological correctness."
        )

    REPORT_FILE.write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))

    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

