#!/usr/bin/env python3
"""
draft_emails.py — Agent 3 state manager for Teamcast Mail Draft Agent

Usage:
  python3 scripts/draft_emails.py --status
      Print draft coverage: N drafted / N enriched

  python3 scripts/draft_emails.py --list
      Print all enriched leads that need a draft (pipeline_status=enriched)

  python3 scripts/draft_emails.py --write <lead_id> '<agent3_json>'
      Write agent3 block to a specific lead and set pipeline_status=drafted

  python3 scripts/draft_emails.py --show <company_name>
      Print the agent3 email draft for a specific company (case-insensitive)

  python3 scripts/draft_emails.py --preview
      Print subject line + first 2 sentences for every drafted lead

  python3 scripts/draft_emails.py --reset <lead_id>
      Reset a lead back to pipeline_status=enriched (for re-drafting)

  python3 scripts/draft_emails.py --export
      Export drafted leads to data/draft_emails.json (for Agent 4 input)

  python3 scripts/draft_emails.py --approve <lead_id>
      Mark a lead as approved for sending (sets agent3.approved=true)
"""

import argparse
import json
import sys
import os
from datetime import datetime, timezone

LEADS_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'leads.json')
DRAFT_EXPORT = os.path.join(os.path.dirname(__file__), '..', 'data', 'draft_emails.json')
RUN_LOG = os.path.join(os.path.dirname(__file__), '..', 'data', 'run_log.json')


def load_leads():
    with open(LEADS_FILE) as f:
        return json.load(f)


def save_leads(leads):
    with open(LEADS_FILE, 'w') as f:
        json.dump(leads, f, indent=2)


def is_enriched(lead):
    return lead.get('pipeline_status') == 'enriched' and lead.get('agent2')


def is_drafted(lead):
    return lead.get('pipeline_status') == 'drafted'


def needs_draft(lead):
    return is_enriched(lead)


def is_qualified(lead):
    return lead.get('status') in {'priority', 'good'}


def cmd_status(leads):
    enriched = [l for l in leads if is_enriched(l) and is_qualified(l)]
    drafted = [l for l in leads if is_drafted(l) and is_qualified(l)]
    pending = [l for l in leads if needs_draft(l) and is_qualified(l)]
    approved = [l for l in drafted if l.get('agent3', {}).get('approved')]

    print(f"\n{'='*60}")
    print(f"  Teamcast Mail Draft Agent — Coverage Report")
    print(f"{'='*60}")
    print(f"  Drafted    : {len(drafted):>3} / {len(enriched) + len(drafted)} enriched leads")
    print(f"  Pending    : {len(pending):>3}  needs a draft")
    print(f"  Approved   : {len(approved):>3}  ready for Agent 4 (Mail Send)")
    print(f"{'='*60}")

    if drafted:
        print(f"\n  ✅ Already drafted ({len(drafted)}):")
        for l in sorted(drafted, key=lambda x: x.get('scoring', {}).get('fit_score', 0), reverse=True):
            name = l['contact'].get('first_name') or l['contact'].get('full_name', 'TBD')
            score = l.get('scoring', {}).get('fit_score', '?')
            a3 = l.get('agent3', {})
            subj = a3.get('subject_line', '(no subject)')[:45]
            quality = a3.get('draft_quality', '?')
            approved_tag = ' ✓APPROVED' if a3.get('approved') else ''
            print(f"     {score:5} | {l['company']['name']:22s} | {name:15s} | q={quality}{approved_tag}")
            print(f"            Subject: {subj}")

    if pending:
        print(f"\n  🔴 Needs draft ({len(pending)}) — ordered by score:")
        for l in sorted(pending, key=lambda x: x.get('scoring', {}).get('fit_score', 0), reverse=True):
            name = l['contact'].get('full_name', 'TBD')
            score = l.get('scoring', {}).get('fit_score', '?')
            lid = l.get('lead_id', '')[:8]
            print(f"     {score:5} | {l['company']['name']:22s} | {name:25s} | id={lid}...")
    print()


def cmd_list(leads):
    pending = [l for l in leads if needs_draft(l) and is_qualified(l)]
    pending.sort(key=lambda x: x.get('scoring', {}).get('fit_score', 0), reverse=True)

    if not pending:
        print("No leads pending draft — all enriched leads have been drafted.")
        return

    print(f"\n{len(pending)} leads pending draft:\n")
    for i, l in enumerate(pending, 1):
        c = l.get('contact', {})
        co = l.get('company', {})
        a2 = l.get('agent2', {})
        print(f"  [{i:>2}] {l.get('scoring',{}).get('fit_score','?'):5} | {l.get('status','?'):8} | id={l.get('lead_id','')[:8]}...")
        print(f"       Company : {co.get('name','')}  ({co.get('employee_count','?')} emp)")
        print(f"       Contact : {c.get('full_name','TBD')} — {c.get('title','')}")
        print(f"       Hook    : {(a2.get('personalization_hooks') or ['(none)'])[0][:80]}")
        print(f"       Roles   : {a2.get('open_roles_count','?')} open | ATS: {a2.get('ats_confirmed','unknown')}")
        print()


def cmd_write(leads, lead_id, agent3_json_str):
    try:
        agent3 = json.loads(agent3_json_str)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON for agent3 block: {e}", file=sys.stderr)
        sys.exit(1)

    now = datetime.now(timezone.utc).isoformat()

    matched = False
    for lead in leads:
        if lead.get('lead_id', '').startswith(lead_id) or lead.get('lead_id') == lead_id:
            if 'draft_completed_at' not in agent3 or not agent3['draft_completed_at']:
                agent3['draft_completed_at'] = now

            lead['agent3'] = agent3
            lead['pipeline_status'] = 'drafted'
            lead['last_updated'] = now
            matched = True

            subj = agent3.get('subject_line', '(no subject)')
            quality = agent3.get('draft_quality', 'unset')
            wc = agent3.get('word_count', '?')
            print(f"✅ Written agent3 draft to: {lead['company']['name']} (id={lead['lead_id'][:8]}...)")
            print(f"   pipeline_status → drafted")
            print(f"   subject_line   : {subj}")
            print(f"   draft_quality  : {quality}")
            print(f"   word_count     : {wc}")
            break

    if not matched:
        print(f"ERROR: No lead found with id starting with '{lead_id}'", file=sys.stderr)
        print("Run --list to see available lead IDs.", file=sys.stderr)
        sys.exit(1)

    save_leads(leads)
    _log_draft_event(lead_id, agent3)


def cmd_show(leads, company_name):
    company_lower = company_name.lower()
    for lead in leads:
        if lead['company']['name'].lower() == company_lower or company_lower in lead['company']['name'].lower():
            print(f"\n{'='*65}")
            print(f"  {lead['company']['name']} — agent3 draft")
            print(f"{'='*65}")
            a3 = lead.get('agent3')
            if not a3:
                print("  No draft yet — this lead hasn't been through Agent 3.")
                print(f"  pipeline_status: {lead.get('pipeline_status', 'enriched')}")
            else:
                print(f"\n  TO      : {lead['contact'].get('full_name','TBD')} <{lead['contact'].get('email','(no email)')}>" )
                print(f"  SUBJECT : {a3.get('subject_line', '')}")
                print(f"\n  ─── BODY ───────────────────────────────────────────────────")
                print()
                print(a3.get('email_body_text', '(no body)'))
                print()
                print(f"  ────────────────────────────────────────────────────────────")
                print(f"\n  quality    : {a3.get('draft_quality', '?')}")
                print(f"  word_count : {a3.get('word_count', '?')}")
                print(f"  hook_used  : {a3.get('persona_hook_used', '?')}")
                print(f"  approved   : {a3.get('approved', False)}")
                print(f"  drafted_at : {a3.get('draft_completed_at', '?')}")
            print(f"\n  pipeline_status: {lead.get('pipeline_status', '?')}")
            print()
            return

    print(f"No lead found matching company name: {company_name}")


def cmd_preview(leads):
    drafted = [l for l in leads if is_drafted(l) and is_qualified(l)]
    drafted.sort(key=lambda x: x.get('scoring', {}).get('fit_score', 0), reverse=True)

    if not drafted:
        print("No drafted emails yet. Run `draft` to generate drafts.")
        return

    print(f"\n{'='*70}")
    print(f"  Email Draft Preview — {len(drafted)} drafts")
    print(f"{'='*70}\n")

    for i, l in enumerate(drafted, 1):
        a3 = l.get('agent3', {})
        contact = l['contact']
        name = contact.get('full_name', 'TBD')
        first = contact.get('first_name', name.split()[0] if name != 'TBD' else 'TBD')
        score = l.get('scoring', {}).get('fit_score', '?')
        quality = a3.get('draft_quality', '?')
        approved = ' ✓' if a3.get('approved') else ''

        body = a3.get('email_body_text', '')
        preview_lines = [s.strip() for s in body.split('\n') if s.strip()]
        preview = ' '.join(preview_lines[:2])[:120] + ('...' if len(' '.join(preview_lines[:2])) > 120 else '')

        print(f"  [{i:>2}] Score {score} | {l['company']['name']} → {name} | q={quality}{approved}")
        print(f"       SUBJ: {a3.get('subject_line', '(none)')}")
        print(f"       PRV : {preview}")
        print()


def cmd_reset(leads, lead_id):
    for lead in leads:
        if lead.get('lead_id', '').startswith(lead_id):
            lead.pop('agent3', None)
            lead['pipeline_status'] = 'enriched'
            lead['last_updated'] = datetime.now(timezone.utc).isoformat()
            save_leads(leads)
            print(f"✅ Reset {lead['company']['name']} back to pipeline_status=enriched")
            return
    print(f"ERROR: No lead found with id starting with '{lead_id}'")
    sys.exit(1)


def cmd_approve(leads, lead_id):
    for lead in leads:
        if lead.get('lead_id', '').startswith(lead_id):
            if not lead.get('agent3'):
                print(f"ERROR: {lead['company']['name']} has no draft yet.")
                sys.exit(1)
            lead['agent3']['approved'] = True
            lead['agent3']['approved_at'] = datetime.now(timezone.utc).isoformat()
            lead['last_updated'] = datetime.now(timezone.utc).isoformat()
            save_leads(leads)
            print(f"✅ Approved draft for: {lead['company']['name']}")
            print(f"   Subject: {lead['agent3'].get('subject_line','')}")
            print(f"   Ready for Agent 4 (Mail Send).")
            return
    print(f"ERROR: No lead found with id starting with '{lead_id}'")
    sys.exit(1)


def cmd_export(leads):
    drafted = [l for l in leads if is_drafted(l) and is_qualified(l)]
    drafted.sort(key=lambda x: x.get('scoring', {}).get('fit_score', 0), reverse=True)

    approved = [l for l in drafted if l.get('agent3', {}).get('approved')]
    unapproved = [l for l in drafted if not l.get('agent3', {}).get('approved')]

    with open(DRAFT_EXPORT, 'w') as f:
        json.dump(drafted, f, indent=2)

    print(f"✅ Exported {len(drafted)} drafted leads → {DRAFT_EXPORT}")
    print(f"   Approved (ready to send): {len(approved)}")
    print(f"   Pending approval        : {len(unapproved)}")
    print(f"   Ready for Agent 4 (Mail Send Agent).")

    enriched_all = [l for l in leads if (is_enriched(l) or is_drafted(l)) and is_qualified(l)]
    print(f"   Coverage: {len(drafted)} / {len(enriched_all)} enriched leads drafted")


def _log_draft_event(lead_id, agent3):
    """Append a draft event to run_log.json"""
    try:
        if os.path.exists(RUN_LOG):
            with open(RUN_LOG) as f:
                log = json.load(f)
        else:
            log = []

        log.append({
            "event": "agent3_draft",
            "lead_id": lead_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "draft_quality": agent3.get('draft_quality', 'unknown'),
            "word_count": agent3.get('word_count', 0),
            "subject_line": agent3.get('subject_line', ''),
            "approved": agent3.get('approved', False)
        })

        with open(RUN_LOG, 'w') as f:
            json.dump(log, f, indent=2)
    except Exception:
        pass


def main():
    parser = argparse.ArgumentParser(description='Teamcast Mail Draft Agent — State Manager')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--status', action='store_true', help='Show draft coverage')
    group.add_argument('--list', action='store_true', help='List all leads needing a draft')
    group.add_argument('--write', nargs=2, metavar=('LEAD_ID', 'AGENT3_JSON'), help='Write agent3 draft to a lead')
    group.add_argument('--show', metavar='COMPANY_NAME', help='Show agent3 draft for a company')
    group.add_argument('--preview', action='store_true', help='Preview all drafted emails (subject + opener)')
    group.add_argument('--reset', metavar='LEAD_ID', help='Reset a lead to pipeline_status=enriched')
    group.add_argument('--approve', metavar='LEAD_ID', help='Approve a draft for sending (Agent 4)')
    group.add_argument('--export', action='store_true', help='Export drafted leads for Agent 4')

    args = parser.parse_args()
    leads = load_leads()

    if args.status:
        cmd_status(leads)
    elif args.list:
        cmd_list(leads)
    elif args.write:
        lead_id, agent3_json = args.write
        cmd_write(leads, lead_id, agent3_json)
    elif args.show:
        cmd_show(leads, args.show)
    elif args.preview:
        cmd_preview(leads)
    elif args.reset:
        cmd_reset(leads, args.reset)
    elif args.approve:
        cmd_approve(leads, args.approve)
    elif args.export:
        cmd_export(leads)


if __name__ == '__main__':
    main()
