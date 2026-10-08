# Module 4 Handoff — Prioritization & Scoring

**Responsible Module:** Module 4 — Prioritization & Scoring
**Status:** Pending completion
**Date:** [To be filled]

---

## Input from Module 3

### Annotated TSV Table
`results/tables/annotated_variants.tsv`
- Columns: CHROM, POS, REF, ALT, GENE, CLNSIG, CLNREVSTAT, FREQUENCY
- Records: [To be filled]

---

## Tasks

1. **Define Prioritization Strategy**
2. **Define Prioritization Criteria**
   - Impact
   - Clinical significance
   - Rarity
   - Consequence

3. **Develop Scoring System**
   - Criterion → Score/Weight → Total Score

4. **Apply the Score**
5. **Rank Variants**
6. **Identify High-Priority Variants**
7. **Prepare Prioritization Table**

---

## Output (to be delivered to Module 5)

- `results/tables/prioritized_variants.tsv`
- Columns: Rank, CHROM, POS, REF, ALT, GENE, Priority_Score, Priority_Category, Evidence_Summary
- Scoring documentation

---

## Commands/Script

See `scripts/module4_prioritize.py`

---

*Educational project — not for clinical diagnosis.*
