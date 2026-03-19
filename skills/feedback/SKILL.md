---
name: feedback
description: Read [TEAMCAST-FEEDBACK] reply emails from Siddhant. Parse APPROVE/DISCARD/SKIP/FOCUS/PAUSE/RESUME/NOTE/MORE FROM/LESS FROM instructions. Update leads.json, blocked.json, and agent_preferences.json. Send confirmation email.
requires: [gmail, exec]
triggers: []
---

# Agent 1 — Feedback Processing Mode

When Siddhant says `feedback`, process his instructions from Gmail reply emails and update the pipeline accordingly.

**Expected output:** Updated `leads.json`, `blocked.json`, and/or `agent_preferences.json`, plus a confirmation email to siddhant.patil@teamcast.ai listing every action taken.

---

## STEP 1 — Search Gmail

```
gmail_search_messages(q: "subject:[TEAMCAST-FEEDBACK] is:unread", maxResults: 10)
```

If none found → reply: "No feedback emails found. Reply to any [TEAMCAST-LEADS] email with subject [TEAMCAST-FEEDBACK] to send instructions."

---

## STEP 2 — Read and Parse

Read each email body via `gmail_read_message`. Do NOT mark as read until all actions are executed.

Parse line by line. Identify instructions using these keywords:

| Keyword | Action |
|---|---|
| `APPROVE {lead_id}` | Update `status` to `"qualified"`, set `agent3.approved: true` if draft exists, add to `qualified_leads.csv` |
| `APPROVE ALL` | Approve all drafted leads where `draft_quality` is `"high"` or `"medium"` |
| `DISCARD {lead_id}` | Update `status` to `"discard"`, update `pipeline_status` to `"discarded"`, remove from all queues |
| `SKIP {company_name}` | Add `company_name` to `blocked.json` companies list. Remove ALL leads from that company from active queues. |
| `SKIP PERSON {email or linkedin}` | Add to `blocked.json` contacts list. Never source this person again. |
| `FOCUS ON {value}` | Update `agent_preferences.json` `priority_personas` or `priority_industries` |
| `LESS FROM {source}` | Update `agent_preferences.json` `reduce_sources` list |
| `MORE FROM {source}` | Update `agent_preferences.json` `expand_sources` list |
| `NOTE {lead_id}: {text}` | Update `leads.json` entry `siddhant_notes` field |
| `PAUSE` | Set `paused: true` in `agent_preferences.json`. Stop all runs. |
| `RESUME` | Set `paused: false` in `agent_preferences.json` |

---

## STEP 3 — Execute Actions

For each parsed instruction, apply to the appropriate data file. Use Python to read/modify/write JSON:

```bash
# Example: approve a lead
python3 -c "
import json
with open('/Users/siddhantpatil/Claude/teamcast-leadgen/data/leads.json') as f:
    leads = json.load(f)
for l in leads:
    if l['lead_id'].startswith('{lead_id_prefix}'):
        l['status'] = 'qualified'
        if l.get('agent3'):
            l['agent3']['approved'] = True
with open('/Users/siddhantpatil/Claude/teamcast-leadgen/data/leads.json', 'w') as f:
    json.dump(leads, f, indent=2)
print('Done')
"
```

After all actions, run dedup + distribute to keep CSVs in sync:
```bash
python3 /Users/siddhantpatil/Claude/teamcast-leadgen/scripts/distribute.py
python3 /Users/siddhantpatil/Claude/teamcast-leadgen/scripts/export_csv.py
```

---

## STEP 4 — Send Confirmation Email

Compose and send to siddhant.patil@teamcast.ai:

**Subject:** `[TEAMCAST-FEEDBACK-DONE] Processed {N} instructions`

**Body includes:**
- ✓ List of all actions taken (with checkmarks)
- ⚠ Any skipped instructions (with reasons — e.g., "lead_id not found")
- Current agent preferences summary (paused status, priority focus, source weights)
- Agent status: active / paused
- Current pipeline count: {N} qualified, {N} in review queue

---

## Rules

1. NEVER mark newsletters as read — if you read any Gmail message during feedback processing, do not alter labels
2. ALWAYS confirm every action in the response email — "APPROVED: loop-abc123" not just "done"
3. NEVER discard a lead silently — always log the discard_reason in the lead record
4. If an instruction is ambiguous (e.g., `SKIP Acme` but there are 3 different companies matching "Acme"), list them and ask Siddhant which one
5. After PAUSE: send a confirmation email and stop all autonomous operations until RESUME is received
