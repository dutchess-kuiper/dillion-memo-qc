#!/usr/bin/env python3
"""
Validate arithmetic tie-outs: check that subtotals equal sums of line items.

Usage:
    python scripts/check_arithmetic.py --json '[
      {"label": "Revenue", "value": 100},
      {"label": "COGS", "value": 40},
      {"label": "Gross Profit", "value": 55, "expected_formula": "Revenue - COGS"}
    ]'

    echo '<json>' | python scripts/check_arithmetic.py --stdin

Input format: JSON array of claim objects with at least "label" and "value".
Objects with "expected_formula" are tested. Formula syntax:
  - "A + B + C"        (sum)
  - "A - B"            (difference)
  - "A / B"            (ratio — result compared as decimal)
  - "SUM(A, B, C)"     (explicit sum)

Tolerance: configurable via --tolerance (default 0.005 = 0.5%)
"""

import argparse
import json
import re
import sys


def parse_claims(claims: list[dict]) -> dict:
    """Index claims by label for formula resolution."""
    index = {}
    for c in claims:
        label = c.get("label", "").strip()
        if label:
            index[label] = c.get("value")
            # Also index lowercase for case-insensitive matching
            index[label.lower()] = c.get("value")
    return index


def resolve_formula(formula: str, index: dict) -> tuple:
    """Resolve a formula string to a computed value.
    Returns (computed_value, explanation, missing_refs)."""

    # SUM(A, B, C)
    sum_match = re.match(r'SUM\((.+)\)', formula, re.IGNORECASE)
    if sum_match:
        refs = [r.strip() for r in sum_match.group(1).split(",")]
        values = []
        missing = []
        for ref in refs:
            val = index.get(ref) or index.get(ref.lower())
            if val is None:
                missing.append(ref)
            else:
                values.append(float(val))
        if missing:
            return None, f"Missing: {', '.join(missing)}", missing
        computed = sum(values)
        explanation = " + ".join(f"{r}={index.get(r) or index.get(r.lower())}" for r in refs)
        return computed, explanation, []

    # A + B + C or A - B or A / B
    # Split by operators, preserving them
    tokens = re.split(r'\s*([+\-/])\s*', formula.strip())
    if len(tokens) < 3:
        return None, f"Cannot parse formula: {formula}", []

    refs = tokens[0::2]  # operands
    ops = tokens[1::2]   # operators

    values = []
    missing = []
    for ref in refs:
        ref = ref.strip()
        val = index.get(ref) or index.get(ref.lower())
        if val is None:
            missing.append(ref)
        else:
            values.append(float(val))

    if missing:
        return None, f"Missing: {', '.join(missing)}", missing

    # Compute left to right
    result = values[0]
    explanation_parts = [f"{refs[0]}={values[0]}"]
    for i, op in enumerate(ops):
        val = values[i + 1]
        explanation_parts.append(f"{op} {refs[i+1]}={val}")
        if op == "+":
            result += val
        elif op == "-":
            result -= val
        elif op == "/":
            if val == 0:
                return None, "Division by zero", []
            result /= val

    return result, " ".join(explanation_parts), []


def check_tieouts(claims: list[dict], tolerance: float = 0.005) -> list[dict]:
    """Check all claims with expected_formula against computed values."""
    index = parse_claims(claims)
    findings = []

    for claim in claims:
        formula = claim.get("expected_formula")
        if not formula:
            continue

        label = claim.get("label", "unknown")
        reported = claim.get("value")
        source = claim.get("source", "")
        page = claim.get("page", "")

        computed, explanation, missing = resolve_formula(formula, index)

        finding = {
            "label": label,
            "formula": formula,
            "reported_value": reported,
            "computed_value": computed,
            "explanation": explanation,
        }

        if missing:
            finding["status"] = "UNRESOLVED"
            finding["reason"] = f"Missing references: {', '.join(missing)}"
            finding["severity"] = "Medium"
        elif reported is None:
            finding["status"] = "UNRESOLVED"
            finding["reason"] = "No reported value to compare"
            finding["severity"] = "Medium"
        else:
            reported_f = float(reported)
            diff = abs(computed - reported_f)
            base = max(abs(reported_f), abs(computed), 1)
            pct_diff = diff / base

            if pct_diff <= tolerance:
                finding["status"] = "PASS"
                finding["variance"] = round(diff, 4)
                finding["variance_pct"] = round(pct_diff * 100, 4)
            else:
                finding["status"] = "FAIL"
                finding["variance"] = round(diff, 4)
                finding["variance_pct"] = round(pct_diff * 100, 4)
                if pct_diff > 0.10:
                    finding["severity"] = "Critical"
                elif pct_diff > 0.05:
                    finding["severity"] = "High"
                elif pct_diff > 0.01:
                    finding["severity"] = "Medium"
                else:
                    finding["severity"] = "Low"

        if source:
            finding["source"] = source
        if page:
            finding["page"] = page

        findings.append(finding)

    return findings


def main():
    parser = argparse.ArgumentParser(description="Check arithmetic tie-outs")
    parser.add_argument("--json", help="JSON array of claims")
    parser.add_argument("--stdin", action="store_true", help="Read JSON from stdin")
    parser.add_argument("--tolerance", type=float, default=0.005, help="Variance tolerance (default 0.5%%)")
    args = parser.parse_args()

    if args.stdin:
        claims = json.load(sys.stdin)
    elif args.json:
        claims = json.loads(args.json)
    else:
        print("Usage: check_arithmetic.py --json '[...]' or --stdin", file=sys.stderr)
        sys.exit(1)

    findings = check_tieouts(claims, tolerance=args.tolerance)

    # Summary
    passes = sum(1 for f in findings if f["status"] == "PASS")
    fails = sum(1 for f in findings if f["status"] == "FAIL")
    unresolved = sum(1 for f in findings if f["status"] == "UNRESOLVED")

    output = {
        "summary": {"pass": passes, "fail": fails, "unresolved": unresolved},
        "tolerance": args.tolerance,
        "findings": findings,
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
