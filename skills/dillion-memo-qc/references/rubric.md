# Severity And Confidence Rubric

## Severity Levels

- Critical
  - Core transaction or financial interpretation may be wrong.
  - Numeric threshold: >10% variance on key metric, OR any legal-financial conflict (purchase price, valuation, closing date).
  - Examples: purchase price mismatch across authoritative docs, major tie-out failure, revenue bridge doesn't foot by >10%.
- High
  - Material metric inconsistency likely changes risk assessment.
  - Numeric threshold: 5-10% variance on key KPI, OR material period/definition mismatch.
  - Examples: revenue definition mismatch affecting growth rates, period mismatch on reported EBITDA.
- Medium
  - Important inconsistency or unsupported claim with moderate diligence impact.
  - Numeric threshold: 1-5% variance, OR definitional ambiguity on secondary metrics.
  - Examples: gross margin calculation uses different COGS definition, unit ambiguity ($000 vs $M) on mid-priority metric.
- Low
  - Minor discrepancy, formatting/label ambiguity, or non-material drift.
  - Numeric threshold: <1% variance, OR label inconsistency with no financial impact.
  - Examples: rounding differences, "Q1 2024" vs "1Q24" labeling, narrative slightly imprecise but tables are correct.

These thresholds are starting points. Adjust by deal context — a 3% variance on a $500M deal is more material than on a $5M deal. Metric sensitivity matters too (purchase price tolerance is near-zero; working capital may have wider tolerance per the mechanism).

## Status Definitions

- Verified
  - Claim is supported by at least two independent bases that align within tolerance.
  - "Within tolerance" means: after normalization (see `references/normalization.md`), variance is below the Low severity threshold for that metric type.
- Partially Verified
  - Claim has one supporting basis or second basis is weak/incomplete.
- Unverified
  - Insufficient support to test claim.
- Contradictory
  - Conflicting support exists for same definition and same period, after normalization.
  - Only use Contradictory when you've confirmed the metrics are truly comparable. If definitions differ, classify as Definitional Mismatch instead.

## Materiality Heuristics

Use judgment by context. Default heuristic:

- <= 1% numeric drift: usually non-material unless metric is highly sensitive (e.g., purchase price, closing conditions).
- > 1% and <= 5%: investigate definition/period alignment before escalating. Run normalization checks from `references/normalization.md`.
- > 5%: usually material unless clear explanatory adjustment is documented.
- Any legal-financial conflict on purchase price, valuation, or closing date: treat as High to Critical regardless of percentage.

## Confidence Grading

Report confidence alongside status in findings (e.g., "Status: Unverified, Confidence: C").

- A: Strong documentary support, high consistency, direct citations from authoritative sources.
- B: Good support with minor gaps (e.g., one source is a draft, or footnote is ambiguous).
- C: Partial support; multiple assumptions needed (e.g., inferred unit conversion, unclear period boundary).
- D: Sparse support; conclusion mostly provisional (e.g., narrative-only evidence, no tables/schedules).

Downgrade confidence when:

- Definitions differ across sources.
- Period boundaries are unclear.
- Units/scales need inferred conversion.
- Evidence is narrative-only without supporting tables/schedules.
