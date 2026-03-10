#!/usr/bin/env python3
"""
Normalize period labels to standard format for cross-document comparison.

Usage:
    python scripts/normalize_periods.py "FY24A"
    python scripts/normalize_periods.py "Q1 2024" "1Q24" "Quarter ending 3/31/24"
    echo '["LTM 6/30/24", "TTM Q2 2024"]' | python scripts/normalize_periods.py --stdin
"""

import argparse
import json
import re
import sys


def normalize_period(label: str) -> dict:
    """Parse a period label and return structured representation."""
    label = label.strip()
    result = {
        "original": label,
        "standard": None,
        "type": None,       # annual, quarterly, ltm, ytd, monthly
        "year": None,
        "quarter": None,
        "status": None,     # actual, budget, projected, None
    }

    # Detect actual/budget/projected status
    lower = label.lower()
    if any(s in lower for s in ["actual", "act", "a"]) and re.search(r'[0-9]a\b', lower):
        result["status"] = "actual"
    elif any(s in lower for s in ["budget", "bud", "b"]) and re.search(r'[0-9]b\b', lower):
        result["status"] = "budget"
    elif any(s in lower for s in ["projected", "proj", "forecast", "fcast", "p", "f"]) and re.search(r'[0-9][pf]\b', lower):
        result["status"] = "projected"

    # FY patterns: FY24, FY2024, FY 2024, FY24A, CY2024
    fy_match = re.match(r'(?:FY|CY)\s*(\d{2,4})\s*([ABPF])?', label, re.IGNORECASE)
    if fy_match:
        year = fy_match.group(1)
        year = f"20{year}" if len(year) == 2 else year
        status_char = (fy_match.group(2) or "").upper()
        if status_char == "A":
            result["status"] = "actual"
        elif status_char == "B":
            result["status"] = "budget"
        elif status_char in ("P", "F"):
            result["status"] = "projected"
        result["type"] = "annual"
        result["year"] = int(year)
        suffix = f" {result['status'].title()}" if result["status"] else ""
        result["standard"] = f"FY {year}{suffix}"
        return result

    # Quarter patterns: 1Q24, Q1 2024, Q1'24, Quarter ending M/DD/YY
    q_match = re.match(r'([1-4])Q\s*[\'.]?(\d{2,4})\s*([ABPF])?', label, re.IGNORECASE)
    if not q_match:
        q_match = re.match(r'Q([1-4])\s*[\'.]?\s*(\d{2,4})\s*([ABPF])?', label, re.IGNORECASE)
    if q_match:
        quarter = int(q_match.group(1))
        year = q_match.group(2)
        year = f"20{year}" if len(year) == 2 else year
        result["type"] = "quarterly"
        result["year"] = int(year)
        result["quarter"] = quarter
        result["standard"] = f"Q{quarter} {year}"
        return result

    # Quarter ending date: "Quarter ending 3/31/24"
    qe_match = re.match(r'[Qq]uarter\s+ending\s+(\d{1,2})/(\d{1,2})/(\d{2,4})', label)
    if qe_match:
        month = int(qe_match.group(1))
        year = qe_match.group(3)
        year = f"20{year}" if len(year) == 2 else year
        quarter_map = {3: 1, 6: 2, 9: 3, 12: 4}
        quarter = quarter_map.get(month)
        if quarter:
            result["type"] = "quarterly"
            result["year"] = int(year)
            result["quarter"] = quarter
            result["standard"] = f"Q{quarter} {year}"
            return result

    # LTM/TTM patterns: LTM 6/30/24, TTM Q2 2024
    ltm_match = re.match(r'(?:LTM|TTM)\s+(\d{1,2})/(\d{1,2})/(\d{2,4})', label, re.IGNORECASE)
    if ltm_match:
        month = int(ltm_match.group(1))
        year = ltm_match.group(3)
        year = f"20{year}" if len(year) == 2 else year
        months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        result["type"] = "ltm"
        result["year"] = int(year)
        result["standard"] = f"LTM {months[month-1]} {year}"
        return result

    ltm_q_match = re.match(r'(?:LTM|TTM)\s+Q([1-4])\s*(\d{2,4})', label, re.IGNORECASE)
    if ltm_q_match:
        quarter = int(ltm_q_match.group(1))
        year = ltm_q_match.group(2)
        year = f"20{year}" if len(year) == 2 else year
        end_months = {1: "Mar", 2: "Jun", 3: "Sep", 4: "Dec"}
        result["type"] = "ltm"
        result["year"] = int(year)
        result["standard"] = f"LTM {end_months[quarter]} {year}"
        return result

    # YTD patterns: YTD Sep 2024, 9M 2024
    ytd_match = re.match(r'YTD\s+(\w+)\s+(\d{4})', label, re.IGNORECASE)
    if ytd_match:
        month_str = ytd_match.group(1)
        year = ytd_match.group(2)
        result["type"] = "ytd"
        result["year"] = int(year)
        result["standard"] = f"YTD {month_str.title()} {year}"
        return result

    nm_match = re.match(r'(\d{1,2})M\s+(\d{4})', label, re.IGNORECASE)
    if nm_match:
        months_count = int(nm_match.group(1))
        year = nm_match.group(2)
        months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        if 1 <= months_count <= 12:
            result["type"] = "ytd"
            result["year"] = int(year)
            result["standard"] = f"YTD {months[months_count-1]} {year}"
            return result

    # Jan-Dec YYYY or Month range
    range_match = re.match(r'(\w+)\s*-\s*(\w+)\s+(\d{4})', label)
    if range_match:
        start = range_match.group(1)
        end = range_match.group(2)
        year = range_match.group(3)
        if start.lower().startswith("jan") and end.lower().startswith("dec"):
            result["type"] = "annual"
            result["year"] = int(year)
            result["standard"] = f"FY {year}"
            return result

    # Fallback: unrecognized
    result["standard"] = label
    result["type"] = "unknown"
    return result


def are_comparable(a: dict, b: dict) -> dict:
    """Check if two normalized periods are comparable."""
    if a["type"] == "unknown" or b["type"] == "unknown":
        return {"comparable": False, "reason": "Unrecognized period format"}
    if a["type"] != b["type"]:
        return {"comparable": False, "reason": f"Different period types: {a['type']} vs {b['type']}"}
    if a["standard"] == b["standard"]:
        return {"comparable": True, "reason": "Exact match"}
    if a["year"] != b["year"]:
        return {"comparable": False, "reason": f"Different years: {a['year']} vs {b['year']}"}
    if a["type"] == "quarterly" and a["quarter"] != b["quarter"]:
        return {"comparable": False, "reason": f"Different quarters: Q{a['quarter']} vs Q{b['quarter']}"}
    return {"comparable": True, "reason": "Same period, different labels"}


def main():
    parser = argparse.ArgumentParser(description="Normalize period labels")
    parser.add_argument("labels", nargs="*", help="Period labels to normalize")
    parser.add_argument("--stdin", action="store_true", help="Read JSON array from stdin")
    parser.add_argument("--compare", action="store_true", help="Compare first two labels")
    args = parser.parse_args()

    if args.stdin:
        labels = json.load(sys.stdin)
    else:
        labels = args.labels

    if not labels:
        print("Usage: normalize_periods.py 'FY24A' 'Q1 2024' ...", file=sys.stderr)
        sys.exit(1)

    results = [normalize_period(label) for label in labels]

    if args.compare and len(results) >= 2:
        comparison = are_comparable(results[0], results[1])
        output = {
            "period_a": results[0],
            "period_b": results[1],
            "comparison": comparison,
        }
        print(json.dumps(output, indent=2))
    else:
        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
