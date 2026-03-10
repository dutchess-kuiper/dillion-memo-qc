# Example: Internal QC Output

This is a fictitious but realistic example of Internal QC output. Use it as a reference for format and level of detail.

---

## QC Verdict
- The memo contains one critical arithmetic failure in the revenue bridge and two medium-severity definitional ambiguities. Three of eight key claims lack sufficient support.

## QC Mode
- Internal QC
- User confirmed single-document review
- Focus area: Revenue and profitability metrics

## Scope And Limitations
- File reviewed: Acme Corp CIM Draft v3.pdf (42 pages)
- What could not be validated: Forward projections (FY26-FY28) — no supporting schedules provided. Customer concentration data referenced on p. 31 but table missing.

## Ranked Findings

### Finding 1: Revenue Bridge Subtotal Failure
**Category:** Reconciliation
**Severity:** Critical
**Status:** Verified
**Issue:** FY24 revenue bridge on p. 14 does not foot — line items sum to $14.8M but stated total is $15.3M.
**Test:** Organic Growth ($2.1M) + Acquisitions ($3.7M) + Price Increases ($1.2M) + Base Revenue ($7.8M) = $14.8M
**Result:** Reported $15.3M vs computed $14.8M — variance of $500K (3.4%)
**Sources:** Acme Corp CIM Draft v3.pdf, p. 14, Table 3
**Impact:** Revenue overstated by $500K. Affects all downstream margin calculations and valuation multiples.
**Action:** Request updated revenue bridge schedule with reconciliation to audited financials.

### Finding 2: EBITDA Definition Inconsistency
**Category:** Metric
**Severity:** Medium
**Status:** Partially Verified
**Issue:** EBITDA on p. 8 ($4.2M) excludes stock-based compensation, but EBITDA on p. 22 ($3.9M) appears to include it.
**Test:** Compare definitions in Executive Summary (p. 8) vs Financial Detail (p. 22)
**Result:** $300K variance. P. 8 footnote says "excluding SBC" while p. 22 has no exclusion note.
**Sources:** Acme Corp CIM Draft v3.pdf, p. 8 and p. 22
**Impact:** Inconsistent EBITDA definition within same document undermines margin analysis.
**Action:** Confirm which EBITDA definition is authoritative and whether SBC adjustment is included.

### Finding 3: Period Label Ambiguity
**Category:** Narrative
**Severity:** Medium
**Status:** Unverified
**Issue:** "FY24" is used throughout but fiscal year end is never stated. If FY ends June 30, "FY24" means Jul 2023 - Jun 2024, not calendar 2024.
**Test:** Search for fiscal year end date declaration
**Result:** No fiscal year end date found in document
**Sources:** Acme Corp CIM Draft v3.pdf, throughout
**Impact:** All period comparisons may be misaligned if fiscal year differs from calendar year.
**Action:** Confirm fiscal year end date (December 31 or other).

### Finding 4: Gross Margin Narrative Contradiction
**Category:** Narrative
**Severity:** Low
**Status:** Verified
**Issue:** Executive summary (p. 3) states "gross margins have expanded consistently" but Table 5 (p. 18) shows Q3 2024 gross margin declining from 62% to 58%.
**Test:** Compare narrative claim to tabular data
**Result:** Q2 2024 GM = 62%, Q3 2024 GM = 58% — 4pp decline contradicts "consistent expansion"
**Sources:** Acme Corp CIM Draft v3.pdf, p. 3 and p. 18
**Impact:** Minor — one quarter's decline doesn't negate trend, but narrative is misleading.
**Action:** Suggest qualifying language: "gross margins have generally expanded, with a temporary dip in Q3 2024."

## Unresolved Items
| Item | Why Unresolved | What Resolves It |
|------|---------------|-----------------|
| Customer concentration | Table referenced on p. 31 but not present in PDF | Request customer concentration schedule |
| FY26-FY28 projections | No supporting model or assumptions provided | Request projection model and key assumptions |
| Working capital detail | Only summary line on p. 25 | Request WC schedule with AR/AP/inventory detail |

## Definitional Mismatches
| Metric | Definition on p. 8 | Definition on p. 22 | Why Non-Comparable |
|--------|--------------------|--------------------|-------------------|
| EBITDA | Excludes SBC | Not specified (appears to include SBC) | $300K gap. Need confirmation of authoritative definition |

## Minimal Artifact Requests
1. Updated revenue bridge schedule reconciled to audited FY24 financials (resolves Finding 1)
2. Confirmation of EBITDA definition — with or without SBC exclusion (resolves Finding 2)
3. Fiscal year end date confirmation (resolves Finding 3)
4. Customer concentration table referenced on p. 31 (resolves Unresolved Item 1)
