import csv
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parents[2]
MODULE_DIR = BASE_DIR / "results" / "module5"
DATA_FILE = BASE_DIR / "data" / "module5" / "prioritized_variants.tsv"
TABLES_DIR = MODULE_DIR / "tables"
FIGURES_DIR = MODULE_DIR / "figures"
REPORTS_DIR = MODULE_DIR / "reports"


def main():
    for directory in (TABLES_DIR, FIGURES_DIR, REPORTS_DIR):
        directory.mkdir(parents=True, exist_ok=True)

    with DATA_FILE.open(
        newline="", encoding="utf-8-sig"
    ) as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        required = {
            "Priority_Category",
            "GNOMAD_STATUS",
            "GENEINFO",
            "CLNSIG",
        }
        missing = required - set(reader.fieldnames or [])

        if missing:
            raise ValueError(
                f"Missing required columns: {sorted(missing)}"
            )

        rows = list(reader)

    if not rows:
        raise ValueError("The priority table contains no rows.")

    category_counts = Counter(
        (row["Priority_Category"].strip() or "EMPTY")
        for row in rows
    )
    gnomad_counts = Counter(
        (row["GNOMAD_STATUS"].strip() or "EMPTY")
        for row in rows
    )
    gene_counts = Counter(
        (row["GENEINFO"].strip() or "EMPTY").split(":")[0]
        for row in rows
    )
    clinical_counts = Counter(
        (row["CLNSIG"].strip() or "EMPTY")
        for row in rows
    )

    summary_file = TABLES_DIR / "results_summary.tsv"
    with summary_file.open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(["Section", "Category", "Count"])

        for section, counts in (
            ("Priority_Category", category_counts),
            ("GNOMAD_STATUS", gnomad_counts),
            ("GENEINFO", gene_counts),
            ("CLNSIG", clinical_counts),
        ):
            for category, count in sorted(counts.items()):
                writer.writerow([section, category, count])

    def make_bar_chart(counts, title, xlabel, output_name):
        labels = list(counts.keys())
        values = list(counts.values())

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(labels, values)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel("Number of variants")
        ax.tick_params(axis="x", labelrotation=25)
        fig.tight_layout()
        fig.savefig(FIGURES_DIR / output_name, dpi=300)
        plt.close(fig)

    make_bar_chart(
        category_counts,
        "Distribution of Educational Priority Categories",
        "Priority category",
        "priority_categories.png",
    )

    make_bar_chart(
        gnomad_counts,
        "gnomAD Status Distribution",
        "gnomAD status",
        "gnomad_status.png",
    )

    make_bar_chart(
        gene_counts,
        "Variant Counts by Gene",
        "Gene",
        "variant_counts_by_gene.png",
    )

    report_file = REPORTS_DIR / "results_summary.txt"
    with report_file.open("w", encoding="utf-8") as handle:
        handle.write("RESULTS SUMMARY\n")
        handle.write("==============================\n")
        handle.write(f"Total variants: {len(rows)}\n\n")

        handle.write("Priority categories:\n")
        for category, count in sorted(category_counts.items()):
            handle.write(f"  {category}: {count}\n")

        handle.write("\ngnomAD statuses:\n")
        for status, count in sorted(gnomad_counts.items()):
            handle.write(f"  {status}: {count}\n")

        handle.write("\nGene counts:\n")
        for gene, count in sorted(gene_counts.items()):
            handle.write(f"  {gene}: {count}\n")

        handle.write(
            "\nInterpretation note:\n"
            "Priority categories are educational rankings, "
            "not independent clinical classifications.\n"
            "NOT_FOUND does not establish that a variant is "
            "pathogenic or absent from all populations.\n"
        )

    print("RESULTS SUMMARY COMPLETED")
    print(f"Variants summarized: {len(rows)}")
    print(f"Summary table: {summary_file}")
    print(f"Text report: {report_file}")
    print(f"Priority chart: {FIGURES_DIR / 'priority_categories.png'}")
    print(f"gnomAD chart: {FIGURES_DIR / 'gnomad_status.png'}")


if __name__ == "__main__":
    main()

