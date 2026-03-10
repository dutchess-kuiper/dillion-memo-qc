# Example: Cross QC Output

This is a fictitious but realistic example of Cross QC output comparing a financial memo against a legal summary. Use it as a reference for format and level of detail.

---

## QC Verdict
- Two critical contradictions found between the financial memo and legal summary, including a $2M purchase price discrepancy. Three metrics cannot be compared due to definitional mismatches.

## QC Mode
- Cross QC
- User confirmed two-document comparison
- Focus area: Purchase price and key financial terms

## Scope And Limitations
- Files reviewed:
  - Doc A: Acme Corp Financial Memo v2.pdf (38 pages)
  - Doc B: Acme Corp Legal Summary - Draft.pdf (15 pages)
- What could not be validated: Earn-out structure (referenced in Doc B p. 8 but no financial modeling in Doc A). Net debt calculation methodology differs and could not be reconciled without balance sheet schedules.

## Ranked Findings

### Finding 1: Purchase Price Contradiction
**Category:** Legal Dependency
**Severity:** Critical
**Status:** Contradictory
**Issue:** Purchase price stated as $45M in financial memo but $47M in legal summary.
**Test:** Direct comparison of stated purchase price
**Result:** Doc A states "$45M enterprise value" (p. 4). Doc B states "aggregate purchase price of $47,000,000" (p. 2, Section 2.1).
**Sources:** Doc A p. 4; Doc B p. 2 Section 2.1
**Impact:** $2M discrepancy (4.4%) on the core transaction value. All valuation multiples in the financial memo may be understated.
**Action:** Request signed term sheet or LOI with final purchase price. Determine whether $45M is equity value and $47M is enterprise value, or if this is a true conflict.

### Finding 2: Closing Date Conflict
**Category:** Legal Dependency
**Severity:** Critical
**Status:** Contradictory
**Issue:** Financial memo projects closing in Q1 2025; legal summary states closing condition is "no later than March 15, 2025" but also references a 60-day extension option.
**Test:** Compare closing timeline references
**Result:** Doc A p. 6: "Expected close Q1 2025." Doc B p. 5 Section 4.2: "Closing no later than March 15, 2025, subject to 60-day extension at Buyer's option."
**Sources:** Doc A p. 6; Doc B p. 5 Section 4.2
**Impact:** If extension is exercised, closing could be May 2025 (Q2), which affects working capital peg date and financial projections.
**Action:** Confirm whether Q1 2025 projection in financial memo accounts for extension option. Request working capital peg date.

### Finding 3: Revenue Variance Near Threshold
**Category:** Cross-Doc
**Severity:** High
**Status:** Partially Verified
**Issue:** FY24 revenue reported as $15.3M in financial memo but $14.9M in legal summary's financial overview.
**Test:** Normalize units (both in USD actual) and period (both FY 2024). Compare.
**Result:** Variance of $400K (2.7%). Both claim "FY 2024 Actual" but definitions may differ.
**Sources:** Doc A p. 14 Table 3; Doc B p. 7 Exhibit A
**Impact:** 2.7% revenue variance propagates to all revenue-based multiples and growth rates.
**Action:** Determine if difference is timing (audit adjustments) or definitional (gross vs net). Request audited financials.

### Finding 4: EBITDA Not Comparable
**Category:** Cross-Doc
**Severity:** Medium
**Status:** Unverified
**Issue:** Cannot compare EBITDA across documents — Doc A reports "Adjusted EBITDA" ($4.2M) while Doc B references "EBITDA" ($3.8M) without adjustment detail.
**Test:** Definition comparison
**Result:** "Adjusted" vs unadjusted EBITDA — $400K gap likely reflects add-backs but cannot be verified without adjustment schedule.
**Sources:** Doc A p. 8; Doc B p. 7
**Impact:** If Doc B's $3.8M is used for covenant calculations while Doc A's $4.2M drives valuation, there's a structural gap.
**Action:** Request EBITDA-to-Adjusted-EBITDA bridge showing all add-backs.

## Unresolved Items
| Item | Why Unresolved | What Resolves It |
|------|---------------|-----------------|
| Earn-out structure | Doc B references earn-out (p. 8) but Doc A has no financial modeling | Request earn-out terms and financial impact modeling |
| Net debt calculation | Doc A shows net debt $8M, Doc B shows $9.2M — methodology not stated | Request net debt bridge from both parties |
| Working capital peg | Neither doc specifies the WC target or peg date | Request WC mechanism from purchase agreement |

## Definitional Mismatches
| Metric | Definition in Doc A | Definition in Doc B | Why Non-Comparable |
|--------|--------------------|--------------------|-------------------|
| EBITDA | "Adjusted EBITDA" — includes unspecified add-backs | "EBITDA" — no adjustments mentioned | $400K gap. Need add-back schedule |
| Net Debt | Not defined, stated as $8M | Not defined, stated as $9.2M | $1.2M gap. Different inclusion of items likely |
| Revenue | "Total Revenue" | "Net Revenue" | May differ by returns/allowances. Need definitions |

## Minimal Artifact Requests
1. Signed term sheet or LOI with final purchase price and structure (resolves Finding 1)
2. Working capital mechanism and peg date from purchase agreement (resolves Finding 2 + Unresolved Item 3)
3. Audited FY24 financial statements (resolves Finding 3)
4. EBITDA-to-Adjusted-EBITDA bridge with all add-backs (resolves Finding 4)
5. Net debt bridge showing components included by each party (resolves Unresolved Item 2)
