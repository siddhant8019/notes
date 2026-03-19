#!/usr/bin/env python3
"""
Teamcast Lead Distributor

Sorts scored leads into qualified, review queue, and disqualified files.

Usage:
    python3 scripts/distribute.py [--input PATH]
"""

import json
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = BASE_DIR / "data" / "leads.json"
REVIEW_QUEUE = BASE_DIR / "data" / "review_queue.json"
DISQUALIFIED = BASE_DIR / "data" / "disqualified_leads.json"


def main():
    parser = argparse.ArgumentParser(description="Distribute scored leads")
    parser.add_argument("--input", type=str, default=str(DEFAULT_INPUT))
    args = parser.parse_args()

    input_path = Path(args.input)

    with open(input_path, "r") as f:
        leads = json.load(f)

    # Load existing queues
    existing_review = []
    if REVIEW_QUEUE.exists():
        with open(REVIEW_QUEUE, "r") as f:
            existing_review = json.load(f)

    existing_disqualified = []
    if DISQUALIFIED.exists():
        with open(DISQUALIFIED, "r") as f:
            existing_disqualified = json.load(f)

    # Sort leads
    qualified = []
    new_review = []
    new_disqualified = []

    for lead in leads:
        status = lead.get("status", "")
        if status in ("priority", "good"):
            qualified.append(lead)
        elif status == "hold":
            new_review.append(lead)
        elif status == "discard":
            new_disqualified.append(lead)
        else:
            qualified.append(lead)  # keep unsorted leads in main file

    # Append to existing queues
    existing_review.extend(new_review)
    existing_disqualified.extend(new_disqualified)

    # Write all files
    with open(input_path, "w") as f:
        json.dump(qualified, f, indent=2)

    with open(REVIEW_QUEUE, "w") as f:
        json.dump(existing_review, f, indent=2)

    with open(DISQUALIFIED, "w") as f:
        json.dump(existing_disqualified, f, indent=2)

    print(f"Distributed: {len(qualified)} qualified, "
          f"{len(new_review)} to review queue (total {len(existing_review)}), "
          f"{len(new_disqualified)} disqualified (total {len(existing_disqualified)})")


if __name__ == "__main__":
    main()
