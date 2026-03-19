#!/usr/bin/env python3
"""
Teamcast Lead Deduplication Engine

Removes duplicate leads and enforces blocked company/contact lists.
Primary key: email → Secondary: linkedin_url → Tertiary: full_name + company_name
Newsletter sources: also deduped by company_name (same company in 2 newsletters = 1 lead)

Usage:
    python3 scripts/dedup.py [--input PATH] [--blocked PATH]
"""

import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = BASE_DIR / "data" / "leads.json"
DEFAULT_BLOCKED = BASE_DIR / "data" / "blocked.json"


def normalize(s: str) -> str:
    return (s or "").strip().lower()


def load_blocked(path: Path) -> dict:
    if not path.exists():
        return {"blocked_companies": [], "blocked_contacts": []}
    with open(path, "r") as f:
        return json.load(f)


def dedup_leads(leads: list, blocked: dict) -> tuple:
    """
    Deduplicate leads and enforce blocked lists.
    Returns (deduped_leads, stats_dict).
    Earlier leads (lower index) take priority — later duplicates get marked.
    """
    blocked_companies = {normalize(c) for c in blocked.get("blocked_companies", [])}
    blocked_contacts = set()
    for c in blocked.get("blocked_contacts", []):
        blocked_contacts.add(normalize(c))

    seen_emails = set()
    seen_linkedin = set()
    seen_name_company = set()
    seen_newsletter_companies = set()  # company-level dedup for newsletter-sourced leads

    NEWSLETTER_SOURCES = {
        "newsletter_funding", "newsletter_exec_move", "newsletter_hiring_surge",
    }

    stats = {"duplicates_removed": 0, "blocked_removed": 0, "kept": 0, "total": len(leads)}
    result = []

    for lead in leads:
        contact = lead.get("contact", {})
        company = lead.get("company", {})
        signals = lead.get("signals", {})

        email = normalize(contact.get("email", ""))
        linkedin = normalize(contact.get("linkedin_url", ""))
        full_name = normalize(contact.get("full_name", ""))
        company_name = normalize(company.get("name", ""))
        name_company_key = f"{full_name}||{company_name}" if full_name and company_name else ""
        source = normalize(lead.get("source", ""))
        is_newsletter = source in NEWSLETTER_SOURCES or bool(signals.get("newsletter_source"))

        # Check blocked
        if company_name and company_name in blocked_companies:
            lead["status"] = "discard"
            lead.setdefault("scoring", {})["discard_reason"] = f"Company '{company_name}' is blocked"
            stats["blocked_removed"] += 1
            result.append(lead)
            continue

        if email and email in blocked_contacts:
            lead["status"] = "discard"
            lead.setdefault("scoring", {})["discard_reason"] = f"Contact '{email}' is blocked"
            stats["blocked_removed"] += 1
            result.append(lead)
            continue

        if linkedin and linkedin in blocked_contacts:
            lead["status"] = "discard"
            lead.setdefault("scoring", {})["discard_reason"] = f"Contact '{linkedin}' is blocked"
            stats["blocked_removed"] += 1
            result.append(lead)
            continue

        # Check duplicates
        is_dup = False
        dup_reason = "Duplicate lead"
        if email and email in seen_emails:
            is_dup = True
        elif linkedin and linkedin in seen_linkedin:
            is_dup = True
        elif name_company_key and name_company_key in seen_name_company:
            is_dup = True
        elif is_newsletter and company_name and company_name in seen_newsletter_companies:
            # Same company appeared in multiple newsletters this run — keep first occurrence
            is_dup = True
            dup_reason = f"Company '{company_name}' already sourced from another newsletter — using first occurrence"

        if is_dup:
            lead["status"] = "discard"
            lead.setdefault("scoring", {})["discard_reason"] = dup_reason
            stats["duplicates_removed"] += 1
            result.append(lead)
            continue

        # Mark as seen
        if email:
            seen_emails.add(email)
        if linkedin:
            seen_linkedin.add(linkedin)
        if name_company_key:
            seen_name_company.add(name_company_key)
        if is_newsletter and company_name:
            seen_newsletter_companies.add(company_name)

        stats["kept"] += 1
        result.append(lead)

    return result, stats


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Deduplicate leads")
    parser.add_argument("--input", type=str, default=str(DEFAULT_INPUT))
    parser.add_argument("--blocked", type=str, default=str(DEFAULT_BLOCKED))
    args = parser.parse_args()

    input_path = Path(args.input)
    blocked_path = Path(args.blocked)

    with open(input_path, "r") as f:
        leads = json.load(f)

    blocked = load_blocked(blocked_path)
    deduped, stats = dedup_leads(leads, blocked)

    with open(input_path, "w") as f:
        json.dump(deduped, f, indent=2)

    print(f"Dedup complete: {stats['total']} total → "
          f"{stats['kept']} kept, "
          f"{stats['duplicates_removed']} duplicates removed, "
          f"{stats['blocked_removed']} blocked removed")


if __name__ == "__main__":
    main()
