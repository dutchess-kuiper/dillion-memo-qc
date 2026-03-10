# Normalization Guide

Cross-document QC fails without normalization. Two documents may report the same underlying fact using different labels, units, or period definitions. Normalize before comparing — never flag a contradiction that's actually a labeling difference.

## Metric Normalization

### When metrics are comparable

Same underlying economic event, different labels:

| Doc A Label | Doc B Label | Comparable? | Why |
|-------------|-------------|-------------|-----|
| Revenue | Total Revenue | Yes | Same concept, one is more explicit |
| Revenue | Net Revenue | Maybe | Check if "Net" excludes returns/allowances |
| Revenue | Bookings | No | Bookings = contracted, Revenue = recognized |
| Gross Profit | Gross Margin | Maybe | Profit is absolute, Margin is %. Check context |
| EBITDA | Adjusted EBITDA | No | Adjustments change the number materially |
| ARR | MRR x 12 | Yes | Equivalent if MRR is current-month |
| Purchase Price | Enterprise Value | No | EV includes debt/cash adjustments |

### Decision tree

1. **Labels match exactly** -> Comparable. Proceed to period/unit check.
2. **Labels differ but definition is stated in both docs** -> Compare definitions. If they describe the same calculation, treat as comparable.
3. **Labels differ and definition is missing from one doc** -> Record as Definitional Mismatch. Request clarification before comparing.
4. **Labels clearly refer to different concepts** (e.g., Bookings vs Revenue) -> Not comparable. Do not compute variance. Report as separate metrics.

## Period Normalization

### Common period representations

| Representation | Standard Form | Meaning |
|----------------|--------------|---------|
| FY24A | FY 2024 Actual | Full fiscal year 2024, actual results |
| FY 2024 Actual | FY 2024 Actual | Same |
| Jan-Dec 2024 | FY 2024 Actual | Same (if fiscal year = calendar year) |
| CY2024 | FY 2024 Actual | Calendar year = fiscal year unless stated |
| 1Q24 | Q1 2024 | First quarter 2024 |
| Q1 2024 | Q1 2024 | Same |
| Quarter ending 3/31/24 | Q1 2024 | Same (calendar year) |
| LTM 6/30/24 | LTM Jun 2024 | Last twelve months ending June 2024 |
| TTM Q2 2024 | LTM Jun 2024 | Trailing twelve months = LTM |
| YTD Sep 2024 | YTD Sep 2024 | Year-to-date through September |
| 9M 2024 | YTD Sep 2024 | Nine months = YTD Sep (if FY starts Jan) |

### Fiscal year warning

If one document uses a non-calendar fiscal year (e.g., FY ends June 30), "FY2024" means Jul 2023 - Jun 2024, not Jan-Dec 2024. Always check for fiscal year end date before assuming calendar alignment.

### Period comparison rules

1. **Exact match** (both say "FY 2024 Actual") -> Comparable.
2. **Same period, different label** (e.g., "1Q24" vs "Q1 2024") -> Comparable.
3. **Overlapping but different** (e.g., "LTM Jun 2024" vs "FY 2024") -> Not directly comparable. Note the overlap and compute only if user confirms.
4. **Different periods entirely** -> Not comparable. Do not flag as contradiction.

## Unit Normalization

### Detection heuristics

Look for these signals in headers, footnotes, and table titles:

| Signal | Unit |
|--------|------|
| "($000s)", "(in thousands)", "$000" | USD Thousands |
| "($M)", "(in millions)", "$mm" | USD Millions |
| "$", "USD" (no qualifier) | USD Actual |
| "%", "percent", "pct" | Percentage |
| "bps", "basis points" | Basis points (1 bps = 0.01%) |
| "x", "turns" | Multiple / ratio |

### Conversion rules

| From | To | Operation |
|------|----|-----------|
| $000 -> $M | Divide by 1,000 |
| $M -> $000 | Multiply by 1,000 |
| % -> bps | Multiply by 100 |
| bps -> % | Divide by 100 |
| % -> decimal | Divide by 100 |

### Rounding tolerance

After unit conversion, apply rounding tolerance before flagging variance:
- **Absolute amounts:** tolerance = max(0.5 unit, 0.1% of value). E.g., if comparing $000 values, a difference of $0.5K or less is rounding.
- **Percentages:** tolerance = 0.05 percentage points (5 bps).
- **Ratios:** tolerance = 0.01x.

If variance is within tolerance after conversion, do not flag as a finding. If variance exceeds tolerance, flag and compute the percentage difference.
