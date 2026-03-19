#!/usr/bin/env python3
"""
research_leads.py — Agent 2 state manager for Teamcast Research Agent

Usage:
  python3 scripts/research_leads.py --status
      Print research coverage: N enriched / N total qualified

  python3 scripts/research_leads.py --list
      Print all leads needing research (pipeline_status=sourced, status=priority|good)

  python3 scripts/research_leads.py --list-priority
      Print only priority leads needing research (score >= 8.0)

  python3 scripts/research_leads.py --write <lead_id> '<agent2_json>'
      Write agent2 block to a specific lead and set pipeline_status=enriched

  python3 scripts/research_leads.py --show <company_name>
      Print the agent2 block for a specific company (case-insensitive)

  python3 scripts/research_leads.py --reset <lead_id>
      Reset a lead back to pipeline_status=sourced (for re-research)

  python3 scripts/research_leads.py --export
      Export enriched leads to data/enriched_leads.json (for Agent 3 input)
"""

import argparse
import json
import sys
import os
from datetime import datetime, timezone

LEADS_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'leads.json')
ENRICHED_EXPORT = os.path.join(os.path.dirname(__file__), '..', 'data', 'enriched_leads.json')
RUN_LOG = os.path.join(os.path.dirname(__file__), '..', 'data', 'run_log.json')

QUALIFIED_STATUSES = {'priority', 'good'}
SCORE_THRESHOLD = 0.0  # Include all qualified leads


def load_leads():
    with open(LEADS_FILE) as f:
        return json.load(f)


def save_leads(leads):
    with open(LEADS_FILE, 'w') as f:
        json.dump(leads, f, indent=2)


def is_qualified(lead):
    return lead.get('status') in QUALIFIED_STATUSES


def needs_research(lead):
    return is_qualified(lead) and lead.get('pipeline_status', 'sourced') == 'sourced'


def is_enriched(lead):
    return lead.get('pipeline_status') == 'enriched'


def cmd_status(leads):
    qualified = [l for l in leads if is_qualified(l)]
    enriched = [l for l in qualified if is_enriched(l)]
    pending = [l for l in qualified if needs_research(l)]
    priority_pending = [l for l in pending if l.get('status') == 'priority']
    good_pending = [l for l in pending if l.get('status') == 'good']

    print(f"\n{'='*55}")
    print(f"  Teamcast Research Agent — Coverage Report")
    print(f"{'='*55}")
    print(f"  Enriched   : {len(enriched):>3} / {len(qualified)} qualified leads")
    print(f"  Pending    : {len(pending):>3}  ({len(priority_pending)} priority, {len(good_pending)} good)")
    print(f"{'='*55}")

    if enriched:
        print(f"\n  ✅ Already enriched ({len(enriched)}):")
        for l in sorted(enriched, key=lambda x: x.get('scoring', {}).get('fit_score', 0), reverse=True):
            name = l['contact'].get('full_name', 'TBD')
            score = l.get('scoring', {}).get('fit_score', '?')
            q = l.get('agent2', {}).get('research_quality', '?')
            print(f"     {score:5} | {l['company']['name']:22s} | {name:25s} | quality={q}")

    if pending:
        print(f"\n  🔴 Needs research ({len(pending)}) — ordered by score:")
        for l in sorted(pending, key=lambda x: x.get('scoring', {}).get('fit_score', 0), reverse=True):
            name = l['contact'].get('full_name', 'TBD')
            score = l.get('scoring', {}).get('fit_score', '?')
            status = l.get('status', '?')
            lid = l.get('lead_id', '')[:8]
            print(f"     {score:5} | {status:8} | {l['company']['name']:22s} | {name:25s} | id={lid}...")
    print()


def cmd_list(leads, priority_only=False):
    pending = [l for l in leads if needs_research(l)]
    if priority_only:
        pending = [l for l in pending if l.get('status') == 'priority']

    pending.sort(key=lambda x: x.get('scoring', {}).get('fit_score', 0), reverse=True)

    if not pending:
        label = "priority " if priority_only else ""
        print(f"No {label}leads pending research.")
        return

    label = "priority " if priority_only else ""
    print(f"\n{len(pending)} {label}leads pending research:\n")
    for i, l in enumerate(pending, 1):
        c = l.get('contact', {})
        co = l.get('company', {})
        sig = l.get('signals', {})
        print(f"  [{i:>2}] {l.get('scoring',{}).get('fit_score','?'):5} | {l.get('status','?'):8} | id={l.get('lead_id','')[:8]}...")
        print(f"       Company : {co.get('name','')}  ({co.get('employee_count','?')} emp, {co.get('ats','')})")
        print(f"       Contact : {c.get('full_name','TBD')} — {c.get('title','')}")
        print(f"       LinkedIn: {c.get('linkedin_url','')}")
        print(f"       Signal  : {sig.get('primary_signal','')} — {sig.get('signal_detail','')[:70]}")
        print(f"       Careers : {co.get('careers_url','')}")
        print()


def cmd_write(leads, lead_id, agent2_json_str):
    try:
        agent2 = json.loads(agent2_json_str)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON for agent2 block: {e}", file=sys.stderr)
        sys.exit(1)

    now = datetime.now(timezone.utc).isoformat()

    matched = False
    for lead in leads:
        if lead.get('lead_id', '').startswith(lead_id) or lead.get('lead_id') == lead_id:
            # Ensure research_completed_at is set
            if 'research_completed_at' not in agent2 or not agent2['research_completed_at']:
                agent2['research_completed_at'] = now

            lead['agent2'] = agent2
            lead['pipeline_status'] = 'enriched'
            lead['last_updated'] = now
            matched = True
            print(f"✅ Written agent2 block to: {lead['company']['name']} (id={lead['lead_id'][:8]}...)")
            print(f"   pipeline_status → enriched")
            print(f"   research_quality: {agent2.get('research_quality', 'unset')}")
            print(f"   open_roles_count: {agent2.get('open_roles_count', '?')}")
            print(f"   pain_points: {len(agent2.get('pain_points', []))}")
            print(f"   hooks: {len(agent2.get('personalization_hooks', []))}")
            break

    if not matched:
        print(f"ERROR: No lead found with id starting with '{lead_id}'", file=sys.stderr)
        print("Run --list to see available lead IDs.", file=sys.stderr)
        sys.exit(1)

    save_leads(leads)
    _log_research_event(lead_id, agent2)


def cmd_show(leads, company_name):
    company_lower = company_name.lower()
    for lead in leads:
        if lead['company']['name'].lower() == company_lower or company_lower in lead['company']['name'].lower():
            print(f"\n{'='*60}")
            print(f"  {lead['company']['name']} — agent2 block")
            print(f"{'='*60}")
            a2 = lead.get('agent2')
            if not a2:
                print("  No agent2 block yet — this lead hasn't been researched.")
            else:
                print(json.dumps(a2, indent=2))
            print(f"\n  pipeline_status: {lead.get('pipeline_status', 'sourced')}")
            print(f"  last_updated:    {lead.get('last_updated', 'never')}")
            print()
            return

    print(f"No lead found matching company name: {company_name}")


def cmd_reset(leads, lead_id):
    for lead in leads:
        if lead.get('lead_id', '').startswith(lead_id):
            lead.pop('agent2', None)
            lead['pipeline_status'] = 'sourced'
            lead['last_updated'] = datetime.now(timezone.utc).isoformat()
            save_leads(leads)
            print(f"✅ Reset {lead['company']['name']} back to pipeline_status=sourced")
            return
    print(f"ERROR: No lead found with id starting with '{lead_id}'")
    sys.exit(1)


def cmd_export(leads):
    enriched = [l for l in leads if is_enriched(l) and is_qualified(l)]
    enriched.sort(key=lambda x: x.get('scoring', {}).get('fit_score', 0), reverse=True)

    with open(ENRICHED_EXPORT, 'w') as f:
        json.dump(enriched, f, indent=2)

    print(f"✅ Exported {len(enriched)} enriched leads → {ENRICHED_EXPORT}")
    print(f"   Ready for Agent 3 (Mail Draft Agent).")

    # Also print coverage
    qualified = [l for l in leads if is_qualified(l)]
    print(f"   Coverage: {len(enriched)} / {len(qualified)} qualified leads enriched")


def _log_research_event(lead_id, agent2):
    """Append a research event to run_log.json"""
    try:
        if os.path.exists(RUN_LOG):
            with open(RUN_LOG) as f:
                log = json.load(f)
        else:
            log = []

        log.append({
            "event": "agent2_research",
            "lead_id": lead_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "research_quality": agent2.get('research_quality', 'unknown'),
            "open_roles_count": agent2.get('open_roles_count', 0),
            "pain_points_count": len(agent2.get('pain_points', [])),
            "hooks_count": len(agent2.get('personalization_hooks', []))
        })

        with open(RUN_LOG, 'w') as f:
            json.dump(log, f, indent=2)
    except Exception:
        pass  # Don't fail research write if log write fails


def main():
    parser = argparse.ArgumentParser(description='Teamcast Research Agent — State Manager')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--status', action='store_true', help='Show research coverage')
    group.add_argument('--list', action='store_true', help='List all leads needing research')
    group.add_argument('--list-priority', action='store_true', help='List priority leads needing research')
    group.add_argument('--write', nargs=2, metavar=('LEAD_ID', 'AGENT2_JSON'), help='Write agent2 block to a lead')
    group.add_argument('--show', metavar='COMPANY_NAME', help='Show agent2 block for a company')
    group.add_argument('--reset', metavar='LEAD_ID', help='Reset a lead to pipeline_status=sourced')
    group.add_argument('--export', action='store_true', help='Export enriched leads for Agent 3')

    args = parser.parse_args()
    leads = load_leads()

    if args.status:
        cmd_status(leads)
    elif args.list:
        cmd_list(leads, priority_only=False)
    elif args.list_priority:
        cmd_list(leads, priority_only=True)
    elif args.write:
        lead_id, agent2_json = args.write
        cmd_write(leads, lead_id, agent2_json)
    elif args.show:
        cmd_show(leads, args.show)
    elif args.reset:
        cmd_reset(leads, args.reset)
    elif args.export:
        cmd_export(leads)


if __name__ == '__main__':
    main()
