# Manual Review Notes — Variant Prioritization

## Purpose
Six variants remain marked MANUAL_REVIEW because their original representations
were not confirmed as exact matches in the gnomAD lookup. These variants are
not independently classified by this review.

## Variants reviewed

| Gene | Position (GRCh38) | REF length | ALT length | Priority score |
|---|---|---:|---:|---:|
| BRCA1 | chr17:43057049 | 129 | 1 | 9 |
| BRCA2 | chr13:32356499 | 293 | 1 | 8 |
| BRCA2 | chr13:32344741 | 1 | 7352 | 5 |
| BRCA1 | chr17:43051060 | 59 | 1 | 4 |
| TP53 | chr17:7675149 | 3 | 3 | 2 |
| TP53 | chr17:7676118 | 2 | 2 | 2 |

## Review findings

- BRCA1, chr17:43057049: The regional export did not confirm an exact
  match for the target large deletion. A nearby SNV was not an exact match.
- BRCA2, chr13:32356499: An overlapping duplication was observed in the
  regional export, but it was not the target deletion.
- BRCA2, chr13:32344741: Nearby structural variants were reviewed, but
  an exact match for the target insertion was not confirmed.
- BRCA1, chr17:43051060: The reviewed regional structural variants did
  not confirm the target 59-bp deletion.
- TP53, chr17:7675149: The compound variant TGC>ATG was not confirmed
  as an exact match. One component substitution was reported as not found;
  the other components were not confirmed by the reviewed results.
- TP53, chr17:7676118: The compound variant GC>TT was not confirmed as
  an exact match. Its component substitutions were found individually in
  gnomAD, but their frequencies must not be assigned to the original
  compound variant.

## Interpretation and limitations

- Keep all six original variants marked MANUAL_REVIEW.
- Do not transfer component-variant allele frequencies to a compound variant.
- A missing exact match does not prove that a variant is absent from all
  population datasets or alternative representations.
- These notes document variant prioritization and database lookup only.
  They do not constitute an ACMG/AMP classification.
