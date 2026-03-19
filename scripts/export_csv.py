#!/usr/bin/env python3
"""
Teamcast CSV Exporter

Exports qualified leads (score >= 6) from leads.json to qualified_leads.csv.

Usage:
    python3 scripts/export_csv.py [--input PATH] [--output PATH] [--min-score N]
"""

import csv
import json
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = BASE_DIR / "data" / "leads.json"
DEFAULT_OUTPUT = BASE_DIR / "data" / "qualified_leads.csv"

CSV_COLUMNS = [
    "lead_id", "full_name", "title", "company_name", "email",
    "employee_count", "industry", "fit_score", "persona_type",
    "primary_signal", "strongest_signal", "linkedin_url",
    "source", "run_id", "status",
]


def flatten_lead(lead: dict) -> dict:
    """Flatten nested lead JSON into a flat dict for CSV."""
    contact = lead.get("contact", {})
    company = lead.get("company", {})
    signals = lead.get("signals", {})
    scoring = lead.get("scoring", {})

    return {
        "lead_id": lead.get("lead_id", ""),
        "full_name": contact.get("full_name", ""),
        "title": contact.get("title", ""),
        "company_name": company.get("name", ""),
        "email": contact.get("email", ""),
        "employee_count": company.get("employee_count", ""),
        "industry": company.get("industry", ""),
        "fit_score": scoring.get("fit_score", 0),
        "persona_type": contact.get("persona_type", ""),
        "primary_signal": signals.get("primary_signal", ""),
        "strongest_signal": scoring.get("strongest_signal", ""),
        "linkedin_url": contact.get("linkedin_url", ""),
        "source": lead.get("source", ""),
        "run_id": lead.get("run_id", ""),
        "status": lead.get("status", ""),
    }


def main():
    parser = argparse.ArgumentParser(description="Export qualified leads to CSV")
    parser.add_argument("--input", type=str, default=str(DEFAULT_INPUT))
    parser.add_argument("--output", type=str, default=str(DEFAULT_OUTPUT))
    parser.add_argument("--min-score", type=float, default=6.0)
    args = parser.parse_args()

    with open(args.input, "r") as f:
        leads = json.load(f)

    qualified = [
        lead for lead in leads
        if lead.get("status") in ("priority", "good")
        and lead.get("scoring", {}).get("fit_score", 0) >= args.min_score
    ]

    qualified.sort(key=lambda x: x.get("scoring", {}).get("fit_score", 0), reverse=True)

    with open(args.output, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for lead in qualified:
            writer.writerow(flatten_lead(lead))

    print(f"Exported {len(qualified)} qualified leads to {args.output}")


if __name__ == "__main__":
    main()
