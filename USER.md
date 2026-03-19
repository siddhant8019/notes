# USER.md — Siddhant Patil

## Who Siddhant Is

Siddhant Patil is the Founding AI Engineer of Teamcast.ai, based in Palo Alto, CA. He runs the entire outbound GTM pipeline himself — no SDR, no sales team. He wants the pipeline to work as autonomously as possible. The only decisions that require his direct involvement are: ordering the first send (`send` command), reviewing low-quality drafts, and handling positive replies from hot leads.

---

## Email Accounts

### Reports & Notifications

All agent reports, digests, and system notifications go to:

| Purpose | Recipient |
|---|---|
| Daily digest (`[TEAMCAST-DIGEST]`) | `siddhant.patil@teamcast.ai` |
| Draft review (`[TEAMCAST-DRAFT]`) | `siddhant.patil@teamcast.ai` |
| Send summary (`[TEAMCAST-SEND]`) | `siddhant.patil@teamcast.ai` |
| Follow-up summary (`[TEAMCAST-FOLLOWUP]`) | `siddhant.patil@teamcast.ai` |
| Analysis report (`[TEAMCAST-ANALYZE]`) | `siddhant.patil@teamcast.ai` |
| Feedback confirmation (`[TEAMCAST-FEEDBACK-DONE]`) | `siddhant.patil@teamcast.ai` |
| Lead sourcing report (`[TEAMCAST-LEADS]`) | `siddhant.patil@teamcast.ai` |
| Research summary (`[TEAMCAST-RESEARCH]`) | `siddhant.patil@teamcast.ai` |

### Outbound Senders (Multi-Sender Rotation)

Outreach is NOT sent from a single address. The pipeline rotates across multiple sender email addresses on different domains to stay under spam thresholds and protect domain reputation.

**Configuration:** `data/sender_config.json`

**How it works:**
- Round-robin rotation across all `active: true` senders
- Max **8–10 emails per sender address per day**
- Each sender has its own SMTP credentials (app password in `.env`)
- Before sending, Agent 4 picks the next sender in the rotation that hasn't hit its daily cap
- If ALL senders are at capacity → queue the remaining sends for the next day and notify Siddhant

**Siddhant will provide the actual email list.** Until then, the config has placeholders. Example entries when populated:
```json
{
  "email": "utkarshwag@getteamcastai.com",
  "display_name": "Utkarsh Wagh",
  "domain": "getteamcastai.com",
  "active": true,
  "daily_limit": 10
}
```

Domains may include: `getteamcastai.com`, `teamcast.ai`, and others. No assumptions should be made about sender addresses until they are explicitly added to the config.

---

## Approval Workflow

The pipeline is designed to be **async and autonomous** — NOT manual review for every lead.

**Auto-approve rule:**
- `draft_quality: "high"` → `agent3.approved = true` automatically (no human review needed)
- `draft_quality: "medium"` → `agent3.approved = true` automatically (no human review needed)
- `draft_quality: "low"` → `agent3.approved = false` — HELD for Siddhant's manual review

Agent 3 sets the approval flag at draft time based on quality. Agent 4 still checks `agent3.approved = true` before sending — the gate exists, but it's auto-cleared for high/medium drafts.

**For held (low quality) drafts:**
- Reply to the `[TEAMCAST-DRAFT]` email with subject `[TEAMCAST-FEEDBACK]` and write: `APPROVE {lead_id}`
- Or directly edit `leads.json` and set `agent3.approved: true`

---

## Feedback Workflow

Siddhant communicates pipeline instructions by replying to any agent report email with the subject line `[TEAMCAST-FEEDBACK]`. The feedback skill reads these replies and executes the instructions.

**Supported keywords:**

| Keyword | What happens |
|---|---|
| `APPROVE {lead_id}` | Approves a held low-quality draft for sending |
| `APPROVE ALL` | Approves all held drafts regardless of quality |
| `DISCARD {lead_id}` | Removes lead permanently |
| `SKIP {company_name}` | Adds to blocked.json, never sources from this company again |
| `SKIP PERSON {email/linkedin}` | Adds person to blocked.json |
| `FOCUS ON {persona or industry}` | Updates agent_preferences.json priority |
| `MORE FROM {source}` | Increases weight for that source |
| `LESS FROM {source}` | Reduces weight for that source |
| `NOTE {lead_id}: {text}` | Attaches a note to a lead's siddhant_notes field |
| `PAUSE` | Halts all sourcing runs |
| `RESUME` | Re-enables sourcing |

---

## Communication Preferences

- **Format:** Table format for lead lists. Count totals always visible. Short paragraphs.
- **Reports:** Include counts at the top (total sourced, qualified, in sequence, etc.) before any detail
- **No confirmation needed** for read-only operations (searching Gmail, reading files, checking status)
- **Always confirm** before sending any Step 1 email batch (follow-ups and system emails are autonomous)
- **Language:** Direct and brief. No filler phrases like "Great news!" or "I hope this finds you well."

---

## Repo and Files

| Resource | Path |
|---|---|
| Main repo | `/Users/siddhantpatil/Claude/teamcast-leadgen/` |
| Leads database | `/Users/siddhantpatil/Claude/teamcast-leadgen/data/leads.json` |
| All Python scripts | `/Users/siddhantpatil/Claude/teamcast-leadgen/scripts/` |
| Agent preferences | `/Users/siddhantpatil/Claude/teamcast-leadgen/data/agent_preferences.json` |
| Blocked list | `/Users/siddhantpatil/Claude/teamcast-leadgen/data/blocked.json` |
| Run logs | `/Users/siddhantpatil/Claude/teamcast-leadgen/data/runs/` |
| Sequence config | `/Users/siddhantpatil/Claude/teamcast-leadgen/data/sequence_config.json` |
| Sequence templates | `/Users/siddhantpatil/Claude/teamcast-leadgen/data/sequence_templates.json` |
| **Sender config** | `/Users/siddhantpatil/Claude/teamcast-leadgen/data/sender_config.json` |
