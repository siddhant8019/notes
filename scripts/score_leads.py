#!/usr/bin/env python3
"""
Teamcast ICP Scoring Engine

Scores leads against Teamcast's Ideal Customer Profile rubric.
Reads from data/leads.json, applies deterministic scoring, writes back.

Usage:
    python3 scripts/score_leads.py [--run-id RUN_ID] [--input PATH] [--output PATH]
"""

import json
import re
import sys
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = BASE_DIR / "data" / "leads.json"


# --- Title matching patterns ---

VP_DIRECTOR_TA_CHRO = re.compile(
    r"(vp|vice\s*president|director|head)\s*(of\s*)?(talent\s*acquisition|recruiting|recruitment)"
    r"|"
    r"(chro|chief\s*(human\s*resources|people)\s*officer|cpo)",
    re.IGNORECASE,
)

HEAD_VP_PEOPLE = re.compile(
    r"(head|vp|vice\s*president|director)\s*(of\s*)?(people|human\s*resources|hr(?!\s*tech))",
    re.IGNORECASE,
)

FOUNDER_CEO = re.compile(
    r"\b(founder|co[\-\s]?founder|ceo|chief\s*executive\s*officer)\b",
    re.IGNORECASE,
)

SENIOR_RECRUITER_TA_LEAD = re.compile(
    r"(senior|sr\.?|lead|principal|staff)\s*(recruiter|recruiting|talent\s*acquisition)"
    r"|"
    r"(talent\s*acquisition|recruiting|recruitment)\s*(lead|manager)",
    re.IGNORECASE,
)

HR_TECH_MANAGER = re.compile(
    r"(manager|head|director)\s*(of\s*)?(hr\s*tech|hris|people\s*ops|people\s*operations|hr\s*technology)",
    re.IGNORECASE,
)

# --- Industry matching ---

MATCHING_INDUSTRIES = {
    "saas", "software", "technology", "fintech", "financial technology",
    "hr tech", "human resources technology", "information technology",
    "computer software", "internet", "it services", "edtech",
    "education technology", "healthcare technology", "healthtech",
}

# --- Disqualifiers ---

DISQUALIFIED_INDUSTRIES = {
    "staffing", "recruiting", "recruitment process outsourcing",
    "rpo", "staffing and recruiting", "human resources services",
    "employment services", "temporary staffing",
}


def score_firmographic_fit(lead: dict) -> tuple:
    """Score firmographic fit (max 4 points)."""
    score = 0.0
    parts = []

    emp = lead.get("company", {}).get("employee_count") or 0
    if isinstance(emp, str):
        emp = int(re.sub(r"[^\d]", "", emp) or 0)

    if 50 <= emp <= 500:
        score += 2.0
        parts.append(f"{emp} employees, 50-500 range (+2)")
    elif 501 <= emp <= 1000:
        score += 1.5
        parts.append(f"{emp} employees, 501-1000 range (+1.5)")
    elif 20 <= emp <= 49:
        score += 1.0
        parts.append(f"{emp} employees, 20-49 range (+1)")
    else:
        parts.append(f"{emp} employees, outside ICP range (+0)")

    industry = (lead.get("company", {}).get("industry") or "").lower().strip()
    if any(ind in industry for ind in MATCHING_INDUSTRIES):
        score += 1.0
        parts.append(f"Industry '{industry}' matches (+1)")
    else:
        parts.append(f"Industry '{industry}' no match (+0)")

    location = (lead.get("contact", {}).get("location") or "").lower()
    company_location = (lead.get("company", {}).get("website") or "").lower()
    if any(loc in location for loc in ["united states", "usa", "u.s.", "remote"]):
        score += 1.0
        parts.append("US-based or remote (+1)")
    elif any(state in location for state in [
        "california", "new york", "texas", "florida", "washington",
        "massachusetts", "illinois", "colorado", "georgia", "virginia",
        "san francisco", "los angeles", "seattle", "boston", "austin",
        "new jersey", "pennsylvania", "north carolina", "arizona",
    ]):
        score += 1.0
        parts.append(f"US state detected: {location} (+1)")
    else:
        parts.append(f"Location '{location}' not US/remote (+0)")

    return min(score, 4.0), "; ".join(parts)


PERSONA_SCORE_MAP = {
    "VP_TA":           (3.0, "VP_TA"),
    "CHRO_CPO":        (3.0, "CHRO_CPO"),
    "SENIOR_RECRUITER":(2.0, "SENIOR_RECRUITER"),
    "HR_TECH":         (1.5, "HR_TECH"),
}


def score_persona_quality(lead: dict) -> tuple:
    """Score persona quality (max 3 points)."""
    title = lead.get("contact", {}).get("title") or ""
    # Use pre-set persona_type field as primary signal when available
    preset = (lead.get("contact", {}).get("persona_type") or "").upper()
    emp = lead.get("company", {}).get("employee_count") or 0
    if isinstance(emp, str):
        emp = int(re.sub(r"[^\d]", "", emp) or 0)

    if preset in PERSONA_SCORE_MAP and preset not in ("UNKNOWN", "FOUNDER_CEO"):
        score, ptype = PERSONA_SCORE_MAP[preset]
        return score, f"'{title}' → {ptype} (preset) (+{score})", ptype

    if preset == "FOUNDER_CEO":
        if emp < 200:
            return 2.5, f"'{title}' → Founder/CEO at {emp} emp (<200) (+2.5)", "FOUNDER_CEO"
        else:
            return 1.0, f"'{title}' → Founder/CEO but {emp} emp (>=200, deprioritized) (+1)", "FOUNDER_CEO"

    if VP_DIRECTOR_TA_CHRO.search(title):
        persona = "VP_TA" if "talent" in title.lower() or "recruit" in title.lower() else "CHRO_CPO"
        return 3.0, f"'{title}' → {persona} (+3)", persona

    if HEAD_VP_PEOPLE.search(title):
        return 3.0, f"'{title}' → Head/VP People (+3)", "CHRO_CPO"

    if FOUNDER_CEO.search(title):
        if emp < 200:
            return 2.5, f"'{title}' → Founder/CEO at {emp} emp (<200) (+2.5)", "FOUNDER_CEO"
        else:
            return 1.0, f"'{title}' → Founder/CEO but {emp} emp (≥200, deprioritized) (+1)", "FOUNDER_CEO"

    if SENIOR_RECRUITER_TA_LEAD.search(title):
        return 2.0, f"'{title}' → Senior Recruiter/TA Lead (+2)", "SENIOR_RECRUITER"

    if HR_TECH_MANAGER.search(title):
        return 1.5, f"'{title}' → HR Tech Manager (+1.5)", "HR_TECH"

    return 0.0, f"'{title}' → No persona match (+0)", "UNKNOWN"


def _raw_signal_score(lead: dict) -> tuple:
    """Inner scoring logic — returns (pts, rationale, tag) before aging penalty."""
    signals = lead.get("signals", {})
    primary = (signals.get("primary_signal") or "").lower()
    detail = (signals.get("signal_detail") or "").lower()
    company = lead.get("company", {})
    # Support both field name variants
    open_roles = company.get("open_role_count") or company.get("open_roles_count") or 0
    if isinstance(open_roles, str):
        open_roles = int(re.sub(r"[^\d]", "", open_roles) or 0)

    # GOLD signals (3 pts)
    # Newsletter exec move: new CHRO/CPO/VP TA = 90-day buying window (highest priority)
    if any(kw in primary for kw in ["newsletter_exec_move", "exec_appointment", "new_chro", "new_cpo", "new_vp_ta"]):
        return 3.0, "GOLD: New exec appointment — 90-day buying window (+3)", "newsletter_exec_move"

    if any(kw in primary for kw in ["hiring_ta_role", "hiring recruiter", "hiring talent"]):
        return 3.0, "GOLD: Hiring recruiter/TA role (+3)", "hiring_ta_role"

    if "10_plus_open_roles" in primary or open_roles >= 10:
        count_str = f"{open_roles} " if open_roles >= 10 else "10+ "
        return 3.0, f"GOLD: {count_str}open roles (+3)", "10_plus_open_roles"

    if any(kw in primary for kw in ["g2_review", "capterra_review", "ats_review"]):
        return 3.0, "GOLD: Recent ATS review on G2/Capterra (+3)", "ats_review"

    if "linkedin_intent" in primary or "linkedin post" in primary:
        return 3.0, "GOLD: LinkedIn hiring pain post (+3)", "linkedin_intent_post"

    # Hiring tech roles (SWE, PM, EM) = active recruiting team = Teamcast buyer
    if any(kw in primary for kw in ["hiring_tech_roles", "hiring_engineering", "hiring_product"]):
        if open_roles >= 10:
            return 3.0, f"GOLD: {open_roles} open roles (+3)", "10_plus_open_roles"
        return 2.5, "Hiring tech roles — active recruiting team (+2.5)", "hiring_tech_roles"

    # Standard signals
    if 5 <= open_roles <= 9:
        return 2.0, f"{open_roles} open roles (+2)", "active_hiring"

    if any(kw in primary for kw in ["recently_funded", "funding", "raised", "newsletter_funding", "newsletter_hiring_surge"]):
        return 2.0, "Recently funded / newsletter signal (+2)", "recently_funded"

    if "yc" in primary or "y_combinator" in primary:
        if any(b in detail for b in ["w24", "s24", "w25", "s25"]):
            return 1.5, f"YC recent batch ({detail}) (+1.5)", "yc_backed"
        return 1.0, "YC-backed but older batch (+1)", "yc_backed"

    if 1 <= open_roles <= 4:
        return 1.0, f"{open_roles} open roles (+1)", "some_hiring"

    if any(kw in primary for kw in ["actively_hiring", "job_board"]):
        return 1.0, "Active hiring signal (+1)", "active_hiring"

    return 0.0, "No signal detected (+0)", "none"


def score_signal_strength(lead: dict) -> tuple:
    """Score signal strength (max 3 points). Applies 90-day aging penalty for old signals."""
    pts, rationale, tag = _raw_signal_score(lead)

    # Apply aging penalty: signals older than 90 days score at 50%
    freshness = (lead.get("signals") or {}).get("signal_freshness_days") or 0
    if freshness > 90 and pts > 0:
        pts = round(pts * 0.5, 1)
        rationale += f" [Signal aged {freshness}d — score halved]"

    return pts, rationale, tag


def classify_lead(total_score: float) -> str:
    """Classify lead by total score."""
    if total_score >= 8:
        return "priority"
    if total_score >= 6:
        return "good"
    if total_score >= 4:
        return "hold"
    return "discard"


def is_disqualified(lead: dict) -> str:
    """Check hard disqualifiers. Returns reason string or empty."""
    industry = (lead.get("company", {}).get("industry") or "").lower()
    for dq in DISQUALIFIED_INDUSTRIES:
        if dq in industry:
            return f"Disqualified industry: {industry} (staffing/RPO/recruiting)"

    emp = lead.get("company", {}).get("employee_count") or 0
    if isinstance(emp, str):
        emp = int(re.sub(r"[^\d]", "", emp) or 0)
    if emp > 5000:
        return f"Fortune 500 / too large: {emp} employees"

    open_roles = lead.get("company", {}).get("open_role_count") or 0
    if isinstance(open_roles, str):
        open_roles = int(re.sub(r"[^\d]", "", open_roles) or 0)

    return ""


def score_lead(lead: dict) -> dict:
    """Score a single lead and update its scoring fields."""
    # Check disqualifiers first
    dq_reason = is_disqualified(lead)
    if dq_reason:
        lead.setdefault("scoring", {})
        lead["scoring"]["fit_score"] = 0
        lead["scoring"]["fit_rationale"] = dq_reason
        lead["scoring"]["strongest_signal"] = "disqualified"
        lead["scoring"]["discard_reason"] = dq_reason
        lead["status"] = "discard"
        return lead

    firmo_score, firmo_rationale = score_firmographic_fit(lead)
    persona_score, persona_rationale, persona_type = score_persona_quality(lead)
    signal_score, signal_rationale, strongest_signal = score_signal_strength(lead)

    total = firmo_score + persona_score + signal_score
    status = classify_lead(total)

    lead.setdefault("scoring", {})
    lead["scoring"]["fit_score"] = total
    lead["scoring"]["fit_rationale"] = (
        f"Firmographic({firmo_score}/4): {firmo_rationale} | "
        f"Persona({persona_score}/3): {persona_rationale} | "
        f"Signal({signal_score}/3): {signal_rationale}"
    )
    lead["scoring"]["strongest_signal"] = strongest_signal
    lead["scoring"]["discard_reason"] = "" if status != "discard" else "Score below threshold"

    lead["status"] = status
    # Only overwrite persona_type if we detected something meaningful;
    # preserve the original field value when scoring falls back to UNKNOWN
    if persona_type != "UNKNOWN":
        lead["contact"]["persona_type"] = persona_type
    lead["agent2_queued"] = status in ("priority", "good")

    return lead


def main():
    parser = argparse.ArgumentParser(description="Score leads against Teamcast ICP")
    parser.add_argument("--input", type=str, default=str(DEFAULT_INPUT))
    parser.add_argument("--output", type=str, default=None)
    parser.add_argument("--run-id", type=str, default=None)
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output) if args.output else input_path

    with open(input_path, "r") as f:
        leads = json.load(f)

    counts = {"priority": 0, "good": 0, "hold": 0, "discard": 0}
    scored = 0

    for lead in leads:
        if args.run_id and lead.get("run_id") != args.run_id:
            continue
        # Skip leads already marked discard by dedup
        if lead.get("status") == "discard" and lead.get("scoring", {}).get("discard_reason"):
            counts["discard"] += 1
            scored += 1
            continue
        score_lead(lead)
        counts[lead["status"]] = counts.get(lead["status"], 0) + 1
        scored += 1

    with open(output_path, "w") as f:
        json.dump(leads, f, indent=2)

    print(f"Scored {scored} leads: "
          f"{counts['priority']} priority, "
          f"{counts['good']} good, "
          f"{counts['hold']} hold, "
          f"{counts['discard']} discard")

    return counts


if __name__ == "__main__":
    main()
