#!/usr/bin/env python3
"""
Build a normalized comparison table from two claim inventories.

Usage:
    python scripts/build_comparison_table.py --doc-a claims_a.json --doc-b claims_b.json
    echo '{"doc_a": [...], "doc_b": [...]}' | python scripts/build_comparison_table.py --stdin

Input format: Each document is a JSON array of claim objects:
{
  "metric": "Revenue",
  "definition": "Net revenue after returns",  (optional)
  "period": "FY 2024",
  "value": 15000,
  "unit": "$000",
  "source": "Memo A",
  "page": "p. 12"
}

Output: Aligned comparison table with variance analysis.
"""

import argparse
import json
import sys
from typing import Optional

# Import normalize_period if available (same directory)
try:
    from normalize_periods import normalize_period
except ImportError:
    def normalize_period(label):
        return {"original": label, "standard": label, "type": "unknown"}


UNIT_MULTIPLIERS = {
    "$": 1,
    "usd": 1,
    "$000": 1000,
    "$000s": 1000,
    "thousands": 1000,
    "$m": 1_000_000,
    "$mm": 1_000_000,
    "millions": 1_000_000,
    "$b": 1_000_000_000,
    "billions": 1_000_000_000,
    "%": 1,
    "percent": 1,
    "bps": 0.01,  # convert bps to percent
}


def normalize_unit_value(value: float, unit: str) -> tuple:
    """Normalize a value to base units. Returns (normalized_value, base_unit)."""
    unit_lower = unit.lower().strip().strip("()")

    # Percentage family
    if unit_lower in ("bps", "basis points"):
        return value * 0.01, "%"
    if unit_lower in ("%", "percent", "pct"):
        return value, "%"

    # Currency family - normalize to actual USD
    multiplier = UNIT_MULTIPLIERS.get(unit_lower, 1)
    if unit_lower in ("$", "usd", "$000", "$000s", "thousands", "$m", "$mm", "millions", "$b", "billions"):
        return value * multiplier, "USD"

    # Ratios
    if unit_lower in ("x", "turns", "multiple"):
        return value, "x"

    return value, unit


def match_metrics(claims_a: list, claims_b: list) -> list:
    """Match claims across documents by metric + period."""
    # Index doc B claims by (metric_lower, period_standard)
    b_index = {}
    for claim in claims_b:
        metric = claim.get("metric", "").strip().lower()
        period = claim.get("period", "")
        period_norm = normalize_period(period)["standard"]
        key = (metric, period_norm)
        b_index.setdefault(key, []).append(claim)

    matched = []
    unmatched_a = []
    matched_b_keys = set()

    for claim_a in claims_a:
        metric_a = claim_a.get("metric", "").strip().lower()
        period_a = claim_a.get("period", "")
        period_norm_a = normalize_period(period_a)["standard"]
        key = (metric_a, period_norm_a)

        if key in b_index and b_index[key]:
            claim_b = b_index[key][0]  # take first match
            matched.append({"doc_a": claim_a, "doc_b": claim_b})
            matched_b_keys.add(key)
        else:
            unmatched_a.append(claim_a)

    # Find unmatched B claims
    unmatched_b = []
    for claim in claims_b:
        metric = claim.get("metric", "").strip().lower()
        period = claim.get("period", "")
        period_norm = normalize_period(period)["standard"]
        key = (metric, period_norm)
        if key not in matched_b_keys:
            unmatched_b.append(claim)

    return matched, unmatched_a, unmatched_b


def compute_variance(pair: dict) -> dict:
    """Compute variance between matched claims."""
    a = pair["doc_a"]
    b = pair["doc_b"]

    val_a = a.get("value")
    val_b = b.get("value")
    unit_a = a.get("unit", "")
    unit_b = b.get("unit", "")

    result = {
        "metric": a.get("metric", b.get("metric", "")),
        "period": normalize_period(a.get("period", ""))["standard"],
        "doc_a_value": val_a,
        "doc_a_unit": unit_a,
        "doc_a_source": f"{a.get('source', '')} {a.get('page', '')}".strip(),
        "doc_b_value": val_b,
        "doc_b_unit": unit_b,
        "doc_b_source": f"{b.get('source', '')} {b.get('page', '')}".strip(),
    }

    # Check definition alignment
    def_a = a.get("definition", "")
    def_b = b.get("definition", "")
    if def_a and def_b and def_a.lower() != def_b.lower():
        result["definition_mismatch"] = True
        result["def_a"] = def_a
        result["def_b"] = def_b
        result["status"] = "DEFINITIONAL_MISMATCH"
        return result

    if val_a is None or val_b is None:
        result["status"] = "INCOMPLETE"
        return result

    # Normalize units
    norm_a, base_unit_a = normalize_unit_value(float(val_a), unit_a)
    norm_b, base_unit_b = normalize_unit_value(float(val_b), unit_b)

    if base_unit_a != base_unit_b:
        result["status"] = "UNIT_MISMATCH"
        result["base_unit_a"] = base_unit_a
        result["base_unit_b"] = base_unit_b
        return result

    result["normalized_a"] = round(norm_a, 4)
    result["normalized_b"] = round(norm_b, 4)
    result["base_unit"] = base_unit_a

    diff = abs(norm_a - norm_b)
    base = max(abs(norm_a), abs(norm_b), 1)
    pct_diff = diff / base

    result["variance"] = round(diff, 4)
    result["variance_pct"] = round(pct_diff * 100, 4)

    if pct_diff <= 0.001:
        result["status"] = "MATCH"
    elif pct_diff <= 0.01:
        result["status"] = "MINOR_VARIANCE"
        result["severity"] = "Low"
    elif pct_diff <= 0.05:
        result["status"] = "MODERATE_VARIANCE"
        result["severity"] = "Medium"
    elif pct_diff <= 0.10:
        result["status"] = "MATERIAL_VARIANCE"
        result["severity"] = "High"
    else:
        result["status"] = "CRITICAL_VARIANCE"
        result["severity"] = "Critical"

    return result


def main():
    parser = argparse.ArgumentParser(description="Build comparison table")
    parser.add_argument("--doc-a", help="JSON file with doc A claims")
    parser.add_argument("--doc-b", help="JSON file with doc B claims")
    parser.add_argument("--stdin", action="store_true", help="Read from stdin")
    args = parser.parse_args()

    if args.stdin:
        data = json.load(sys.stdin)
        claims_a = data["doc_a"]
        claims_b = data["doc_b"]
    elif args.doc_a and args.doc_b:
        with open(args.doc_a) as f:
            claims_a = json.load(f)
        with open(args.doc_b) as f:
            claims_b = json.load(f)
    else:
        print("Usage: --doc-a file --doc-b file OR --stdin", file=sys.stderr)
        sys.exit(1)

    matched, unmatched_a, unmatched_b = match_metrics(claims_a, claims_b)
    comparisons = [compute_variance(pair) for pair in matched]

    # Categorize results
    matches = [c for c in comparisons if c["status"] == "MATCH"]
    findings = [c for c in comparisons if c["status"] not in ("MATCH", "INCOMPLETE")]
    incomplete = [c for c in comparisons if c["status"] == "INCOMPLETE"]

    output = {
        "summary": {
            "total_claims_a": len(claims_a),
            "total_claims_b": len(claims_b),
            "matched": len(matched),
            "exact_matches": len(matches),
            "findings": len(findings),
            "incomplete": len(incomplete),
            "unmatched_a": len(unmatched_a),
            "unmatched_b": len(unmatched_b),
        },
        "comparisons": comparisons,
        "unmatched_doc_a": unmatched_a,
        "unmatched_doc_b": unmatched_b,
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
