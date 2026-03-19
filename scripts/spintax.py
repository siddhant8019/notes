#!/usr/bin/env python3
"""
spintax.py — Spintax renderer and merge tag substitutor for Teamcast email sequences.

Usage (CLI):
    python3 scripts/spintax.py --render "text" --tags '{"FIRST_NAME": "Alyssa"}'
    python3 scripts/spintax.py --preview --step 3 --lead-id <lead_id_prefix>
"""

import re
import random
import json
import sys
import argparse


def render_spintax(text: str) -> str:
    """
    Resolve all spintax groups in text by randomly selecting one option from
    each {option1|option2|...} group. Works iteratively from innermost to
    outermost, so nested spintax like {Hi {FIRST_NAME},|Hello {FIRST_NAME},}
    resolves correctly.

    Does NOT substitute merge tags — call substitute_merge_tags() after this.
    Tags like {FIRST_NAME} contain no pipe, so they are untouched.
    """
    # Pattern: match {group} where group contains at least one | and no nested braces
    pattern = re.compile(r'\{([^{}]*\|[^{}]*)\}')

    for _ in range(20):  # max 20 passes for deeply nested spintax
        match = pattern.search(text)
        if not match:
            break
        options = match.group(1).split('|')
        chosen = random.choice(options)
        text = text[:match.start()] + chosen + text[match.end():]

    return text


def substitute_merge_tags(text: str, merge_tags: dict) -> str:
    """
    Replace all {TAG_NAME} placeholders in text with values from merge_tags.
    Tags are matched case-insensitively. Unknown tags are left as-is.

    Also lowercases the first character of PERSONALIZED LINE values so the
    rendered sentence reads: "I noticed AlphaSense..." not "I Noticed AlphaSense..."
    """
    def replacer(m):
        tag = m.group(1)
        for key, value in merge_tags.items():
            if key.upper() == tag.upper():
                val = str(value)
                # Lowercase first char of PERSONALIZED LINE to fit "I {PERSONALIZED LINE}" template
                if key.upper() == 'PERSONALIZED LINE' and val:
                    val = val[0].lower() + val[1:]
                return val
        return m.group(0)  # leave unknown tags untouched

    return re.sub(r'\{([^{}|]+)\}', replacer, text)


def render(spintax_text: str, merge_tags: dict) -> str:
    """
    Full render pipeline using multi-pass strategy to handle merge tags nested
    inside spintax groups (e.g. {Hi {FIRST_NAME},|Hello {FIRST_NAME},}).

    Pass 1: resolve innermost spintax groups (no nested braces)
    Pass 2: substitute merge tags (expands {FIRST_NAME} → "Alyssa")
    Pass 3: resolve any remaining spintax groups (now that merge tags are gone)

    Args:
        spintax_text: Raw template string with {opt1|opt2} groups and {TAG} placeholders.
        merge_tags: Dict of tag name -> value (e.g. {"FIRST_NAME": "Alyssa"})

    Returns:
        Fully rendered, ready-to-send string.
    """
    # Pass 1: resolve innermost (non-nested) spintax groups
    text = render_spintax(spintax_text)
    # Pass 2: substitute merge tags
    text = substitute_merge_tags(text, merge_tags)
    # Pass 3: resolve any remaining spintax groups (were blocked by nested merge tags in pass 1)
    text = render_spintax(text)
    return text


def preview(spintax_text: str, merge_tags: dict, n: int = 3) -> list:
    """
    Render n independent variants of a spintax template for preview.
    Each call to render() is independent so variants differ.
    """
    return [render(spintax_text, merge_tags) for _ in range(n)]


def build_merge_tags(lead: dict) -> dict:
    """Build the standard merge tag dict from a lead object."""
    first_name = lead.get('contact', {}).get('first_name', '')
    hooks = lead.get('agent2', {}).get('personalization_hooks', []) if lead.get('agent2') else []
    personalized_line = hooks[0] if hooks else ''
    return {
        'FIRST_NAME': first_name,
        'PERSONALIZED LINE': personalized_line,
    }


def main():
    parser = argparse.ArgumentParser(description='Spintax renderer for Teamcast email sequences')
    parser.add_argument('--render', metavar='TEXT', help='Render a spintax string directly')
    parser.add_argument('--tags', metavar='JSON', help='JSON dict of merge tags', default='{}')
    parser.add_argument('--preview', action='store_true', help='Show 3 rendered variants')
    parser.add_argument('--step', type=int, choices=[2, 3, 4], help='Sequence step number to preview')
    parser.add_argument('--lead-id', metavar='ID', help='Lead ID prefix for --step preview')
    parser.add_argument('--n', type=int, default=3, help='Number of preview variants (default 3)')
    args = parser.parse_args()

    if args.render:
        tags = json.loads(args.tags)
        if args.preview:
            variants = preview(args.render, tags, args.n)
            for i, v in enumerate(variants, 1):
                print(f"\n--- Variant {i} ---\n{v}")
        else:
            print(render(args.render, tags))

    elif args.step and args.lead_id:
        import os
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        templates_path = os.path.join(base, 'data', 'sequence_templates.json')
        leads_path = os.path.join(base, 'data', 'leads.json')

        with open(templates_path) as f:
            templates = json.load(f)
        with open(leads_path) as f:
            leads = json.load(f)

        step_template = templates['steps'][str(args.step)]
        lead = next((l for l in leads if l['lead_id'].startswith(args.lead_id)), None)
        if not lead:
            print(f"ERROR: Lead {args.lead_id} not found", file=sys.stderr)
            sys.exit(1)

        tags = build_merge_tags(lead)
        body_spintax = step_template.get('body_spintax', '')
        subject_spintax = step_template.get('subject_spintax', '')

        print(f"\n=== Step {args.step} preview for {lead['contact']['full_name']} @ {lead['company']['name']} ===")
        print(f"MERGE TAGS: {json.dumps(tags, indent=2)}\n")

        for i in range(args.n):
            print(f"--- Variant {i+1} ---")
            if subject_spintax:
                print(f"SUBJECT: {render(subject_spintax, tags)}")
            else:
                seq = lead.get('sequence', {})
                steps = seq.get('steps', []) if seq else []
                step1 = next((s for s in steps if s['step_number'] == 1), {})
                orig_subject = step1.get('subject_rendered', '[Step 1 subject not found]')
                print(f"SUBJECT: Re: {orig_subject}")
            print(f"BODY:\n{render(body_spintax, tags)}")
            print()

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
