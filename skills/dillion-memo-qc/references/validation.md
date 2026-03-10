# Validation Scenarios And Acceptance Checks

Use these scenarios to test skill behavior before relying on it.

## Scenario 1: Single-File Internal Tie-Out Failure

Input:

- One memo PDF with a subtotal that does not equal line items.

Expected:

- Mode prompt asks user to confirm Internal QC.
- Finding category includes Reconciliation.
- Severity is High or Critical based on impact.
- Clear formula shown in Test and exact source citation included.

## Scenario 2: Two-File Numeric Drift Near Threshold

Input:

- Two memo PDFs reporting same metric and period with small variance.

Expected:

- Mode prompt asks and user confirms Cross QC.
- Skill checks definition/unit/period alignment before contradiction.
- Output labels as low/medium discrepancy or unresolved if context is incomplete.

## Scenario 3: Legal-Financial Contradiction

Input:

- Memo A references purchase price that differs from legal summary in Memo B.

Expected:

- Legal dependency finding appears near top.
- Severity escalates to High/Critical.
- Action requests exact resolving artifacts (signed agreement schedule, final term sheet pages).

## Scenario 4: Sparse Evidence Single File

Input:

- One narrative-heavy memo with few tables and no clear schedules.

Expected:

- Missing evidence explicitly flagged.
- Multiple claims marked Unverified, not Contradictory.
- Minimal artifact requests are specific and short.

## Acceptance Checklist

- Skill always asks user to choose QC mode before analysis.
- Every material finding has explicit source citation.
- Verified status is never assigned without sufficient support.
- Contradictory status is only used for true conflicts, not missing data.
- Definitional mismatches are isolated as non-comparable until normalized.
- Final output includes ranked findings and minimal artifact requests.
