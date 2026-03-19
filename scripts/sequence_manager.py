#!/usr/bin/env python3
"""
sequence_manager.py — CAB sequence state manager for Teamcast.

Tracks per-lead sequence enrollment, step scheduling, and completion.
Called by Agent 4 (send/CLAUDE.md) to manage the full 4-step CAB campaign.

Usage:
    python3 scripts/sequence_manager.py --status
    python3 scripts/sequence_manager.py --enroll <lead_id>
    python3 scripts/sequence_manager.py --due
    python3 scripts/sequence_manager.py --mark-sent <lead_id> <step> <subject> <body> <msg_id> <thread_id>
    python3 scripts/sequence_manager.py --mark-replied <lead_id>
    python3 scripts/sequence_manager.py --unenroll <lead_id>
    python3 scripts/sequence_manager.py --preview <lead_id>
"""

import json
import sys
import os
import argparse
from datetime import datetime, timezone, timedelta

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEADS_PATH = os.path.join(BASE, 'data', 'leads.json')
CONFIG_PATH = os.path.join(BASE, 'data', 'sequence_config.json')
TEMPLATES_PATH = os.path.join(BASE, 'data', 'sequence_templates.json')
RUN_LOG_PATH = os.path.join(BASE, 'data', 'run_log.json')


def load_leads():
    with open(LEADS_PATH) as f:
        return json.load(f)


def save_leads(leads):
    with open(LEADS_PATH, 'w') as f:
        json.dump(leads, f, indent=2)


def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


def load_templates():
    with open(TEMPLATES_PATH) as f:
        return json.load(f)


def now_utc():
    return datetime.now(timezone.utc)


def find_lead(leads, lead_id_prefix):
    matches = [l for l in leads if l['lead_id'].startswith(lead_id_prefix)]
    if len(matches) == 0:
        print(f"ERROR: No lead found with ID prefix '{lead_id_prefix}'", file=sys.stderr)
        sys.exit(1)
    if len(matches) > 1:
        print(f"ERROR: Multiple leads match '{lead_id_prefix}': {[l['lead_id'][:8] for l in matches]}", file=sys.stderr)
        sys.exit(1)
    return matches[0]


def log_event(event_type, data):
    entry = {'timestamp': now_utc().isoformat(), 'type': event_type, **data}
    log = []
    if os.path.exists(RUN_LOG_PATH):
        try:
            with open(RUN_LOG_PATH) as f:
                log = json.load(f)
        except Exception:
            log = []
    if not isinstance(log, list):
        log = [log]
    log.append(entry)
    with open(RUN_LOG_PATH, 'w') as f:
        json.dump(log, f, indent=2)


def get_next_due_step(lead):
    """
    Return the next unsent step dict if its scheduled_send_date has passed, else None.
    Returns None if lead is not in an active sequence or has replied/opted out.
    """
    seq = lead.get('sequence')
    if not seq or seq.get('status') != 'active':
        return None
    if seq.get('replied') or seq.get('opted_out'):
        return None

    today = now_utc().date()
    for step in seq.get('steps', []):
        if step.get('sent_at') is None:
            scheduled = step.get('scheduled_send_date')
            if scheduled:
                sched_date = datetime.fromisoformat(scheduled).date()
                if sched_date <= today:
                    return step
            break  # Only check the next unsent step
    return None


def cmd_status(leads):
    """Print sequence coverage table."""
    qualified = [l for l in leads if l.get('status') in ('priority', 'good')]

    not_enrolled = [l for l in qualified if l.get('sequence') is None and l.get('pipeline_status') == 'drafted']
    active = [l for l in qualified if l.get('sequence', {}) and l.get('sequence', {}).get('status') == 'active']
    completed = [l for l in qualified if l.get('sequence', {}) and l.get('sequence', {}).get('status') in ('completed', 'replied', 'opted_out', 'paused')]

    print("=" * 70)
    print("  Teamcast CAB Sequence — Coverage Report")
    print("=" * 70)
    print(f"  Not enrolled (approved & drafted): {len(not_enrolled)}")
    print(f"  Active sequences               : {len(active)}")
    print(f"  Completed / replied / paused   : {len(completed)}")
    print()

    if active:
        print("  ACTIVE SEQUENCES:")
        print(f"  {'Score':<6} {'Company':<22} {'Contact':<22} {'Step':<6} {'Next Due':<12} {'Status'}")
        print("  " + "-" * 80)
        active_sorted = sorted(active, key=lambda l: (
            min(
                (datetime.fromisoformat(s['scheduled_send_date']).date()
                 for s in l['sequence']['steps']
                 if s.get('sent_at') is None and s.get('scheduled_send_date')),
                default=datetime(9999, 1, 1).date()
            )
        ))
        for l in active_sorted:
            seq = l['sequence']
            steps_sent = sum(1 for s in seq['steps'] if s.get('sent_at'))
            next_step = next((s for s in seq['steps'] if s.get('sent_at') is None), None)
            next_date = ''
            if next_step and next_step.get('scheduled_send_date'):
                d = datetime.fromisoformat(next_step['scheduled_send_date']).date()
                today = now_utc().date()
                if d <= today:
                    next_date = f"DUE ({d})"
                else:
                    next_date = str(d)
            print(f"  {l['scoring']['fit_score']:<6} {l['company']['name']:<22} {l['contact']['first_name']:<22} {steps_sent}/4  {next_date:<12} {seq['status']}")

    if not_enrolled:
        print()
        print("  READY TO ENROLL (pipeline_status=drafted, approved):")
        for l in sorted(not_enrolled, key=lambda x: -x['scoring']['fit_score']):
            approved = l.get('agent3', {}).get('approved', False) if l.get('agent3') else False
            print(f"    {l['scoring']['fit_score']:.1f} | {l['company']['name']:<22} | {l['contact']['full_name']:<25} | approved={approved}")

    if completed:
        print()
        print("  COMPLETED:")
        for l in sorted(completed, key=lambda x: -x['scoring']['fit_score']):
            reason = l['sequence'].get('status', 'unknown')
            print(f"    {l['scoring']['fit_score']:.1f} | {l['company']['name']:<22} | {l['contact']['full_name']:<25} | {reason}")

    print()


def cmd_enroll(leads, lead_id_prefix):
    """Enroll a lead into the CAB sequence after Step 1 has been sent."""
    lead = find_lead(leads, lead_id_prefix)
    config = load_config()

    # Validate preconditions
    if lead.get('sequence') is not None:
        print(f"ERROR: {lead['company']['name']} is already enrolled (status: {lead['sequence']['status']})")
        sys.exit(1)
    if lead.get('pipeline_status') != 'sent':
        print(f"ERROR: pipeline_status must be 'sent' before enrollment. Current: {lead.get('pipeline_status')}")
        sys.exit(1)

    agent3 = lead.get('agent3', {})
    if not agent3:
        print(f"ERROR: No agent3 block found — Step 1 was not drafted.")
        sys.exit(1)
    if not agent3.get('approved'):
        print(f"ERROR: agent3.approved must be True before enrollment.")
        sys.exit(1)

    # Check personalization hook
    hooks = lead.get('agent2', {}).get('personalization_hooks', []) if lead.get('agent2') else []
    if not hooks and config['conditions'].get('block_if_no_personalization_hook', True):
        print(f"BLOCKED: {lead['company']['name']} has no personalization hook. Re-run Agent 2 research first.")
        sys.exit(1)

    # Get Step 1 metadata from agent3
    step1_sent_at = agent3.get('sent_at') or now_utc().isoformat()
    step1_sent_date = datetime.fromisoformat(step1_sent_at).replace(tzinfo=timezone.utc) if step1_sent_at else now_utc()

    # Compute scheduled dates
    gaps = config['timing']
    step2_date = (step1_sent_date + timedelta(days=gaps['step_1_to_step_2_days'])).isoformat()
    step3_date = (step1_sent_date + timedelta(days=gaps['step_1_to_step_2_days'] + gaps['step_2_to_step_3_days'])).isoformat()
    step4_date = (step1_sent_date + timedelta(days=gaps['step_1_to_step_2_days'] + gaps['step_2_to_step_3_days'] + gaps['step_3_to_step_4_days'])).isoformat()

    sequence = {
        "campaign": "CAB",
        "enrolled_at": now_utc().isoformat(),
        "status": "active",
        "replied": False,
        "replied_at": None,
        "opted_out": False,
        "opted_out_at": None,
        "steps": [
            {
                "step_number": 1,
                "is_thread_reply": False,
                "sent_at": step1_sent_at,
                "scheduled_send_date": step1_sent_at,
                "subject_rendered": agent3.get('subject_line', ''),
                "body_rendered_text": agent3.get('email_body_text', ''),
                "source": "agent3",
                "gmail_message_id": agent3.get('gmail_message_id'),
                "gmail_thread_id": agent3.get('gmail_thread_id')
            },
            {
                "step_number": 2,
                "is_thread_reply": True,
                "scheduled_send_date": step2_date,
                "sent_at": None,
                "subject_rendered": None,
                "body_rendered_text": None,
                "source": "sequence_templates",
                "gmail_message_id": None,
                "gmail_thread_id": None
            },
            {
                "step_number": 3,
                "is_thread_reply": False,
                "scheduled_send_date": step3_date,
                "sent_at": None,
                "subject_rendered": None,
                "body_rendered_text": None,
                "source": "sequence_templates",
                "gmail_message_id": None,
                "gmail_thread_id": None
            },
            {
                "step_number": 4,
                "is_thread_reply": False,
                "scheduled_send_date": step4_date,
                "sent_at": None,
                "subject_rendered": None,
                "body_rendered_text": None,
                "source": "sequence_templates",
                "gmail_message_id": None,
                "gmail_thread_id": None
            }
        ]
    }

    lead['sequence'] = sequence
    lead['pipeline_status'] = 'in_sequence'
    lead['last_updated'] = now_utc().isoformat()
    save_leads(leads)

    log_event('sequence_enrolled', {
        'lead_id': lead['lead_id'],
        'company': lead['company']['name'],
        'contact': lead['contact']['full_name'],
        'step2_due': step2_date[:10],
        'step3_due': step3_date[:10],
        'step4_due': step4_date[:10],
    })

    print(f"  ✓ Enrolled {lead['contact']['full_name']} @ {lead['company']['name']}")
    print(f"    Step 2 due: {step2_date[:10]}")
    print(f"    Step 3 due: {step3_date[:10]}")
    print(f"    Step 4 due: {step4_date[:10]}")


def cmd_due(leads):
    """Print all leads where next step's scheduled_send_date has passed."""
    due = []
    for l in leads:
        step = get_next_due_step(l)
        if step:
            due.append((l, step))

    if not due:
        print("No follow-up steps due today.")
        return

    print(f"\n{'Company':<22} {'Contact':<22} {'Step':<6} {'Scheduled':<12} {'Days Overdue'}")
    print("-" * 75)
    today = now_utc().date()
    for l, step in sorted(due, key=lambda x: x[1]['scheduled_send_date']):
        sched = datetime.fromisoformat(step['scheduled_send_date']).date()
        overdue = (today - sched).days
        print(f"{l['company']['name']:<22} {l['contact']['first_name']:<22} Step {step['step_number']}  {str(sched):<12} {overdue}d")
    print(f"\nTotal due: {len(due)}")


def cmd_mark_sent(leads, lead_id_prefix, step_number, subject, body, gmail_message_id, gmail_thread_id):
    """Record that a sequence step was successfully sent."""
    lead = find_lead(leads, lead_id_prefix)
    seq = lead.get('sequence')
    if not seq:
        print(f"ERROR: {lead['company']['name']} is not enrolled in a sequence.")
        sys.exit(1)

    step = next((s for s in seq['steps'] if s['step_number'] == step_number), None)
    if not step:
        print(f"ERROR: Step {step_number} not found in sequence.")
        sys.exit(1)
    if step.get('sent_at'):
        print(f"WARNING: Step {step_number} for {lead['company']['name']} already marked sent at {step['sent_at']}.")
        return

    step['sent_at'] = now_utc().isoformat()
    step['subject_rendered'] = subject
    step['body_rendered_text'] = body
    step['gmail_message_id'] = gmail_message_id
    step['gmail_thread_id'] = gmail_thread_id

    # Check if all steps are now done
    all_sent = all(s.get('sent_at') for s in seq['steps'])
    if all_sent:
        seq['status'] = 'completed'
        lead['pipeline_status'] = 'sequence_complete'
    elif step_number > 1:
        lead['pipeline_status'] = 'in_sequence'

    lead['last_updated'] = now_utc().isoformat()
    save_leads(leads)

    log_event('sequence_step_sent', {
        'lead_id': lead['lead_id'],
        'company': lead['company']['name'],
        'step': step_number,
        'subject': subject,
        'gmail_message_id': gmail_message_id,
    })

    status = "SEQUENCE COMPLETE" if all_sent else f"Step {step_number} sent"
    print(f"  ✓ {status}: {lead['contact']['full_name']} @ {lead['company']['name']}")


def cmd_mark_replied(leads, lead_id_prefix):
    """Mark a lead as having replied. Stops the sequence."""
    lead = find_lead(leads, lead_id_prefix)
    seq = lead.get('sequence')
    if not seq:
        print(f"ERROR: {lead['company']['name']} is not enrolled in a sequence.")
        sys.exit(1)

    seq['replied'] = True
    seq['replied_at'] = now_utc().isoformat()
    seq['status'] = 'replied'
    lead['pipeline_status'] = 'sequence_complete'
    lead['last_updated'] = now_utc().isoformat()
    save_leads(leads)

    log_event('sequence_replied', {
        'lead_id': lead['lead_id'],
        'company': lead['company']['name'],
        'contact': lead['contact']['full_name'],
    })

    print(f"  ✓ Marked replied: {lead['contact']['full_name']} @ {lead['company']['name']} — sequence stopped.")


def cmd_unenroll(leads, lead_id_prefix):
    """Pause/stop a lead's sequence without marking as replied or opted-out."""
    lead = find_lead(leads, lead_id_prefix)
    seq = lead.get('sequence')
    if not seq:
        print(f"ERROR: {lead['company']['name']} is not enrolled.")
        sys.exit(1)

    seq['status'] = 'paused'
    lead['pipeline_status'] = 'sequence_complete'
    lead['last_updated'] = now_utc().isoformat()
    save_leads(leads)

    log_event('sequence_unenrolled', {
        'lead_id': lead['lead_id'],
        'company': lead['company']['name'],
    })

    print(f"  ✓ Unenrolled (paused): {lead['contact']['full_name']} @ {lead['company']['name']}")


def cmd_preview(leads, lead_id_prefix, n=3):
    """Preview the next due step for a lead using rendered spintax."""
    from spintax import render, preview as spintax_preview, build_merge_tags

    lead = find_lead(leads, lead_id_prefix)
    templates = load_templates()

    seq = lead.get('sequence')
    next_step_num = None

    if seq:
        next_step = next((s for s in seq['steps'] if s.get('sent_at') is None), None)
        if next_step:
            next_step_num = next_step['step_number']
    else:
        next_step_num = 1

    if next_step_num is None:
        print(f"No pending steps for {lead['company']['name']}.")
        return

    template = templates['steps'][str(next_step_num)]
    tags = build_merge_tags(lead)

    print(f"\n=== Step {next_step_num} preview: {lead['contact']['full_name']} @ {lead['company']['name']} ===")
    print(f"MERGE TAGS: FIRST_NAME={tags['FIRST_NAME']}")
    print(f"            PERSONALIZED LINE={tags['PERSONALIZED LINE'][:80]}...")
    print()

    body_spintax = template.get('body_spintax', '')
    subject_spintax = template.get('subject_spintax')

    for i in range(n):
        print(f"--- Variant {i+1} ---")
        if subject_spintax:
            print(f"SUBJECT: {render(subject_spintax, tags)}")
        elif next_step_num == 2 and seq:
            step1 = next((s for s in seq['steps'] if s['step_number'] == 1), {})
            print(f"SUBJECT: Re: {step1.get('subject_rendered', '[Step 1 subject]')}")
        print(f"BODY:\n{render(body_spintax, tags)}")
        print()


def migrate_add_sequence_field(leads):
    """One-time migration: add sequence=null to all leads that don't have it."""
    updated = 0
    for l in leads:
        if 'sequence' not in l:
            l['sequence'] = None
            updated += 1
    return updated


def main():
    parser = argparse.ArgumentParser(description='CAB Sequence Manager')
    parser.add_argument('--status', action='store_true', help='Show sequence coverage')
    parser.add_argument('--enroll', metavar='LEAD_ID', help='Enroll a lead after Step 1 is sent')
    parser.add_argument('--due', action='store_true', help='Show leads with next step due today')
    parser.add_argument('--mark-sent', nargs=6,
                        metavar=('LEAD_ID', 'STEP', 'SUBJECT', 'BODY', 'MSG_ID', 'THREAD_ID'),
                        help='Mark a step as sent')
    parser.add_argument('--mark-replied', metavar='LEAD_ID', help='Mark a lead as replied')
    parser.add_argument('--unenroll', metavar='LEAD_ID', help='Stop sequence for a lead')
    parser.add_argument('--preview', metavar='LEAD_ID', help='Preview next step for a lead')
    parser.add_argument('--migrate', action='store_true', help='Add sequence=null to all leads (one-time setup)')
    args = parser.parse_args()

    leads = load_leads()

    if args.migrate:
        n = migrate_add_sequence_field(leads)
        save_leads(leads)
        print(f"Migration complete: added sequence=null to {n} leads.")

    elif args.status:
        cmd_status(leads)

    elif args.enroll:
        cmd_enroll(leads, args.enroll)

    elif args.due:
        cmd_due(leads)

    elif args.mark_sent:
        lead_id, step, subject, body, msg_id, thread_id = args.mark_sent
        cmd_mark_sent(leads, lead_id, int(step), subject, body, msg_id, thread_id)

    elif args.mark_replied:
        cmd_mark_replied(leads, args.mark_replied)

    elif args.unenroll:
        cmd_unenroll(leads, args.unenroll)

    elif args.preview:
        cmd_preview(leads, args.preview)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
