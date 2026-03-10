---
name: dillion-memo-qc
description: |
  Expose contradictions, evidence gaps, and arithmetic failures that manual review misses
  in FDD diligence memos. Produces ranked QC findings with severity, exact source citations,
  and minimal artifact requests. Use this skill whenever reviewing financial memos, comparing
  deal documents, checking memo consistency, reconciling figures, validating claims, or
  identifying contradictions across PDF submissions — even if the user just says "check this
  memo", "compare these two docs", "QC this file", or "find inconsistencies".

  MANDATORY TRIGGERS: memo QC, document QC, diligence review, compare memos, reconcile
  figures, check consistency, find contradictions, validate claims, cross-document check
allowed-tools: "Read Glob Grep Bash"
compatibility: Optimized for Claude Code/Cowork workflows. Falls back gracefully for Web/Desktop.
metadata:
  argument-hint: "[internal|cross] [focus-area]"
  user-invocable: true
---

# Dillion Memo QC

Run quality control for diligence memo PDFs. Two modes:

- **Internal QC:** One document — check internal consistency (arithmetic, dates, definitions, narrative-vs-numbers)
- **Cross QC:** Two documents — cross-source comparison with normalization and contradiction detection

## Mandatory First Step

Before any analysis, confirm the QC mode. Every run.

1. Count uploaded files.
2. Auto-detect recommendation:
   - 1 file -> recommend Internal QC
   - 2+ files -> recommend Cross QC
3. Ask user to confirm one mode.
4. Do not proceed until mode is confirmed.

If no files are present, request PDF upload first.

If user invoked with arguments (e.g., `/dillion-memo-qc cross legal-vs-financial`), treat as recommendation only — still confirm.

## Focus Areas

A focus area narrows the primary scope of analysis (e.g., "revenue recognition", "legal terms", "working capital", "purchase price"). When a user provides one:

- Prioritize findings in that area (check it first, report it first).
- Still report all material findings outside the focus area — contradictions and critical issues are never suppressed.
- Note the focus area in the QC Mode section of output.

## Operating Principles

- Treat missing evidence as a finding, not a footnote.
- Never invent values, definitions, or dates.
- Do not force tie-outs by rounding.
- Mark uncertainty explicitly using Status + Confidence (see `references/rubric.md`).
- Use precise source citations (file name, page, table/section) for every material claim.
- Normalize before comparing — see `references/normalization.md` for methodology.

## Internal QC Workflow (single PDF)

1. **Build claim inventory**
   - Extract all numeric and date claims.
   - Capture each claim with context, period/as-of date, units, and exact page citation.

2. **Run internal consistency checks**
   - Arithmetic and tie-outs: use `scripts/check_arithmetic.py` for systematic validation, or check manually for simpler cases.
   - Date/period coherence (FY vs YTD, quarter labels, as-of dates) — use `scripts/normalize_periods.py` to standardize labels.
   - Unit coherence (USD vs thousands, percent vs basis points).
   - Narrative-vs-number coherence ("profitable" while operating loss shown).
   - Definition coherence (bookings vs revenue, gross vs net).

3. **Classify findings**
   - Use severity thresholds and confidence grades in `references/rubric.md`.
   - Promote contradictions that impact deal interpretation.
   - Separate extraction-quality issues from true business/financial issues.

4. **Produce directive output**
   - Use the Required Output Format below.
   - End with minimal artifact requests that resolve highest-impact unknowns.

For a complete worked example, see `assets/example_internal_qc.md`.

## Cross QC Workflow (two PDFs)

1. **Build per-document claim inventory**
   - For each document, extract key claims with context, period, unit, and page citation.

2. **Normalize before comparing**
   - Follow the methodology in `references/normalization.md`:
     - Normalize metric labels (same concept, different wording — use the decision tree).
     - Normalize units/scales (USD vs $000, percent vs bps — apply conversion rules).
     - Normalize period definitions (LTM vs FY vs YTD — use `scripts/normalize_periods.py`).
   - For systematic comparison, use `scripts/build_comparison_table.py` to generate the alignment matrix.

3. **Align comparable claims**
   - Match only claims that refer to the same metric definition and period.
   - If definitions differ, record as a Definitional Mismatch first — do not flag as contradiction.

4. **Compare and classify**
   - Numeric differences: evaluate variance against severity thresholds in `references/rubric.md`.
   - Date differences: evaluate timeline conflict impact.
   - Legal-financial dependencies: treat purchase price, closing date, and valuation conflicts as high priority.
   - If data is incomplete, classify as Unverified instead of Contradictory.

5. **Resolve authority explicitly**
   - State which source is currently more reliable and why.
   - If no source can be preferred, mark unresolved and request the smallest resolving artifacts.

For a complete worked example, see `assets/example_cross_qc.md`.

## When to Stop and Request Clarification

Some findings are serious enough that proceeding without clarification produces unreliable output. Pause and ask the user when:

- **Purchase price or valuation contradictions** — request signed term sheet or LOI before ranking downstream findings, because all multiples depend on this number.
- **Period definition conflicts** — if "FY2024" might mean different date ranges in different docs, request fiscal year confirmation before computing variances.
- **Extraction quality too low** — if PDF extraction is garbled or tables aren't parseable, reduce all confidence grades to C/D, flag as a scope limitation, and request cleaner source files.
- **Scope ambiguity** — if user provided 3+ files and it's unclear which to compare, ask before proceeding.

After clarification, resume analysis with the new information.

## Required Output Format

Use this structure exactly:

```markdown
## QC Verdict
- One sentence verdict.

## QC Mode
- Internal QC or Cross QC
- Why this mode was chosen (user-confirmed)
- Focus area (if user provided one)

## Scope And Limitations
- Files reviewed
- What could not be validated

## Ranked Findings
### Finding [ID]: [Title]
**Category:** Reconciliation | Metric | Controls | Narrative | Legal Dependency | Cross-Doc
**Severity:** Critical | High | Medium | Low
**Status:** Verified | Partially Verified | Unverified | Contradictory
**Confidence:** A | B | C | D
**Issue:** [One sentence]
**Test:** [Formula/check applied OR "insufficient evidence"]
**Result:** [Numbers + variance OR "insufficient evidence"]
**Sources:** [File names + page refs]
**Impact:** [What this changes for diligence confidence]
**Action:** [Concrete next step]

## Unresolved Items
- Item | Why unresolved | What resolves it

## Definitional Mismatches
- Metric | Definition in Source A | Definition in Source B | Why non-comparable yet

## Minimal Artifact Requests
- Target 3-5 specific requests, each tied to a top unresolved finding.
- Good: "Signed Term Sheet Exhibit A showing final purchase price and structure"
- Bad: "Any other supporting documents"
- Each request should name the exact document/table and what it resolves.
```

Rank findings by severity (Critical first), then by confidence (higher confidence findings first within same severity).

## Utility Scripts

The `scripts/` directory provides automation helpers. These are optional — use them when they save time, fall back to manual analysis when needed.

| Script | When to Use |
|--------|------------|
| `scripts/normalize_periods.py` | Standardize period labels before comparing across documents |
| `scripts/check_arithmetic.py` | Validate tie-outs systematically (subtotals, roll-forwards) |
| `scripts/build_comparison_table.py` | Generate aligned metric comparison matrix for Cross QC |

## Parallel Execution

For larger documents (>10 pages), use the Agent tool to parallelize independent work. This significantly reduces QC time without sacrificing quality.

### Cross QC — Parallel extraction (biggest win)

Step 1 extracts claims from each document independently. Spawn 2 agents in the same turn:

```
Agent 1: Extract all numeric/date claims from Doc A.
         For each claim: metric, definition (if stated), period, value, unit, source file, page.
         Return as JSON array.

Agent 2: Extract all numeric/date claims from Doc B.
         Same format as Agent 1.
```

After both return, the coordinator runs normalization + comparison (steps 2-5) sequentially, since comparison needs both inventories.

### Internal QC — Parallel consistency checks

After building the claim inventory (step 1, must be sequential), the consistency checks in step 2 are independent:

```
Agent 1: Arithmetic/tie-out checks — run scripts/check_arithmetic.py on claim inventory
Agent 2: Date/period + unit coherence — run scripts/normalize_periods.py, flag mismatches
Agent 3: Narrative-vs-number + definition coherence — compare prose claims against tables
```

Coordinator collects findings from all agents, deduplicates, ranks by severity, and produces the final output.

### Coordinator pattern

1. Mode confirmation (sequential — must happen first)
2. Spawn extraction agents (parallel for Cross QC, or build inventory yourself for Internal QC)
3. Collect claim inventories
4. Spawn check/comparison agents (parallel)
5. Collect findings, deduplicate, rank by severity
6. Run validation gate (`references/validation.md`)
7. Produce final output

### When NOT to parallelize

- **Small documents** (<10 pages) — sequential is faster due to agent overhead
- **Uncertain extraction quality** — run sequentially so you can escalate early if PDFs are garbled
- **Web/Desktop mode** — Agent tool not available, fall back to sequential

## Runtime Guidance

Use runtime-specific tool guidance in `references/runtime-tooling.md`.

- Prefer Claude Code/Cowork behavior first.
- Apply Web/Desktop fallback behavior when tools are limited.

## Validation

Before finalizing output, self-check against the Acceptance Checklist in `references/validation.md`. This catches common errors like marking claims as Verified without support, or labeling definitional mismatches as contradictions.

For scenario-based self-checks, use the test scenarios in the same file.
