# Runtime Tool Curation

Primary target is Claude Code/Cowork. Use fallback behavior for Web/Desktop.

## Claude Code / Cowork (Primary)

Invocation pattern:

- User should invoke directly with `/dillion-memo-qc`.
- Optional args are allowed, for example:
  - `/dillion-memo-qc internal`
  - `/dillion-memo-qc cross legal-vs-financial`
- Even with args, always confirm mode before analysis.

Preferred workflow:

1. Parse uploaded PDFs into claim inventories.
2. Build a normalized comparison table (metric, definition, period, value, source, page).
3. Run deterministic checks:
   - arithmetic/tie-out checks
   - unit and period normalization checks
   - narrative-vs-number contradiction checks
4. Emit ranked findings and minimal artifact requests.

Recommended tool behavior:

- Use file reading/extraction tools first.
- Use lightweight scripts for repeated normalization logic.
- Keep comparison tables compact and evidence-linked.
- Avoid broad web lookup unless user asks for external benchmarking.
- Prefer read-only tool usage for QC reliability. Only request write-capable tools if the user explicitly asks to generate an output artifact file.

## Claude Web / Desktop (Fallback)

When tool access is limited:

1. Ask user for:
   - key excerpts/tables from each PDF
   - period definitions
   - units/scales used
2. Build a manual claim ledger in the response.
3. Clearly separate:
   - directly evidenced statements
   - assumptions
   - unresolved requests

Prompting fallback pattern:

- "Paste the specific table or paragraph that supports this value."
- "Confirm whether values are in USD, USD thousands, or USD millions."
- "Confirm if this is FY, YTD, LTM, or quarterly."

## Tool Selection Rules

- Internal QC:
  - prioritize arithmetic and narrative consistency within one file
- Cross QC:
  - prioritize alignment table and contradiction detection across files
- If extraction quality is low:
  - reduce confidence
  - avoid definitive contradiction labels until definition and period are confirmed
- If user requests both Internal and Cross:
  - run one mode first, deliver output, then ask for confirmation before second pass
