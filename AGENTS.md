# AGENTS.md — Teamcast GTM Engine Operations

## Session Start Protocol

Every time a session opens, run this checklist **silently** (no output to screen):

1. Read `data/agent_preferences.json` — if `paused: true`, stop immediately and say: "Pipeline is paused. Say `resume` to restart sourcing."
2. Read `data/blocked.json` — load blocked company and contact lists into memory
3. Count leads in `data/leads.json` by `pipeline_status`:
   ```python
   python3 /Users/siddhantpatil/Claude/teamcast-leadgen/scripts/sequence_manager.py --status
   ```
4. Check Gmail for unread `[TEAMCAST-FEEDBACK]` emails — if found, say: "You have unread feedback waiting. Say `feedback` to process it first."
5. Print the status report (only output from session start):

```
Teamcast GTM Engine ready.

Pipeline:  {N} sourced | {N} enriched | {N} drafted | {N} in_sequence | {N} sequence_complete
Leads:     {N} priority | {N} good | {N} in review queue

Commands: run · research · draft · send · followup · analyze · supervisor · feedback · status · pause · resume
```

---

## Skill Routing

When Siddhant types a command, load the corresponding skill and execute it. Do not improvise — the skill file contains the full protocol.

| Command | Skill loaded | What it does |
|---|---|---|
| `run` | `skills/run/SKILL.md` | Source new leads from 5 channels, score, dedup, distribute |
| `feedback` | `skills/feedback/SKILL.md` | Process [TEAMCAST-FEEDBACK] email instructions |
| `research` | `skills/research/SKILL.md` | Enrich sourced leads with company intelligence |
| `research 1` | `skills/research/SKILL.md` | Research single highest-priority lead (test mode) |
| `draft` | `skills/draft/SKILL.md` | Write personalized cold emails for enriched leads |
| `draft 1` | `skills/draft/SKILL.md` | Draft single highest-scoring enriched lead (test mode) |
| `send` | `skills/send/SKILL.md` | Send Step 1 for all approved leads, enroll in sequence |
| `send 1` | `skills/send/SKILL.md` | Send Step 1 for single highest-scoring approved lead |
| `followup` | `skills/send/SKILL.md` | Check due list, send next sequence step for due leads |
| `analyze` | `skills/analyze/SKILL.md` | Scan Gmail for replies, classify sentiment, report |
| `analyze 1` | `skills/analyze/SKILL.md` | Analyze single lead for reply (test mode) |
| `supervisor` | `skills/supervisor/SKILL.md` | Run full pipeline health check + send digest email |
| `status` | (inline) | Print current lead counts from leads.json |
| `show top` | (inline) | Print top 10 leads from qualified_leads.csv |
| `show queue` | (inline) | Print review_queue.json contents |
| `pause` | (inline) | Set paused=true in agent_preferences.json, confirm |
| `resume` | (inline) | Set paused=false in agent_preferences.json, confirm |
| `due` | `skills/send/SKILL.md` | Show all leads with a follow-up step due today |
| `preview [id]` | `skills/send/SKILL.md` | Preview rendered Step N email for a lead |
| `replied [id]` | `skills/send/SKILL.md` | Mark a lead as replied, stop their sequence |
| `unenroll [id]` | `skills/send/SKILL.md` | Pause a lead's sequence (operational stop) |

---

## Automatic Pipeline Advancement Rules

After each agent completes, suggest the logical next step (do not auto-trigger without Siddhant's order):

- After `run` completes → "N new sourced leads ready. Say `research` to enrich them."
- After `research` completes → "N leads enriched. Say `draft` to write their emails."
- After `draft` completes → Email Siddhant the preview table at siddhant.patil@teamcast.ai. Auto-approved {N} high/medium drafts. If any low-quality drafts held: "N low-quality drafts held for review. Reply APPROVE {lead_id} to approve."
- After `send` completes → Print enrollment dates for all enrolled leads. "Step 2 sends scheduled starting {date}."
- After `followup` completes → If any leads hit `sequence_complete`, say "N leads finished the sequence. Say `analyze` to check for replies."
- After `analyze` completes → If hot leads found, say "N positive replies — review the [TEAMCAST-ANALYZE] email in your inbox."

---

## Pipeline Continuity After Cron Runs

The Supervisor (7am), Followup (9am), and Analyze (10am) crons run in isolated sessions. They do not carry over context from the main session. They read state from `leads.json` and write back to it. After a cron run completes, the main session remains as-is — type `status` to see updated counts.

---

## Memory Protocol

**Write to `MEMORY.md` when:**
- Siddhant gives a new preference ("focus on Series B companies from now on")
- A bug or issue is resolved (so the fix is remembered)
- A new signal type is discovered and validated
- Apollo credits fall below a threshold

**Write to `memory/YYYY-MM-DD.md` when:**
- A run completes (how many leads, which sources worked, any errors)
- Research or draft batch completes (quality summary)
- Any significant pipeline event occurs

**The rule:** If it's not written to a file, it doesn't exist after compaction. Anything Siddhant says that should persist across sessions must be saved immediately.

---

## Exec Tool Usage

All Python scripts live at `/Users/siddhantpatil/Claude/teamcast-leadgen/scripts/`. Always call with absolute paths.

Approved binaries: `python3`, `wc`, `grep`

Examples:
```bash
python3 /Users/siddhantpatil/Claude/teamcast-leadgen/scripts/score_leads.py --run-id {run_id}
python3 /Users/siddhantpatil/Claude/teamcast-leadgen/scripts/sequence_manager.py --status
python3 /Users/siddhantpatil/Claude/teamcast-leadgen/scripts/spintax.py --step 2 --lead-id {lead_id[:8]}
wc -l /Users/siddhantpatil/Claude/teamcast-leadgen/data/leads.json
```

Never chain commands with `&&` or `;` unless both commands are purely read operations.

---

## Safety Rules — Full Canonical List

These apply across ALL agents and ALL skills. No exceptions.

**Lead Sourcing (Agent 1):**
1. NEVER send a cold outreach email — that is Agent 4's job only
2. NEVER modify a lead's score after scoring, unless Siddhant explicitly says APPROVE
3. CHECK staffing agencies, RPO firms, and recruiting consultancies carefully — they are not automatic disqualifiers but evaluate on a case-by-case basis
4. NEVER add a lead from blocked.json
5. NEVER run without checking agent_preferences.json first
6. NEVER skip the deduplication step
7. NEVER invent leads or fabricate data
8. ALWAYS create Gmail draft before attempting SMTP send
9. ALWAYS use absolute paths for all script calls
10. ALWAYS save a run log after every run
11. NEVER mark newsletter emails as read — Gmail newsletter inbox is permanently read-only

**Email Sending (Agent 4):**
12. NEVER send to a lead with `sequence.replied = true`
13. NEVER send to a lead with `sequence.opted_out = true`
14. NEVER send Step N+1 before Step N is marked as sent
15. NEVER send a follow-up early — always check `--due` first
16. NEVER send to a lead with an empty `contact.email`
17. NEVER send without a personalization hook if `{PERSONALIZED LINE}` is in the template
18. ALWAYS call `--mark-sent` immediately after a successful SMTP send
19. ALWAYS enroll a lead in the sequence after sending Step 1
20. ALWAYS send a summary email to siddhant.patil@teamcast.ai after every send batch
21. ALWAYS log to `data/run_log.json` after every send batch
22. WAIT FOR SIDDHANT'S ORDER before sending Step 1 — follow-ups (Steps 2/3) are autonomous via cron

**Reply Analysis (Agent 5):**
23. NEVER mark Gmail messages as read during analysis
24. NEVER send any outbound email during analysis (report to Siddhant is the only exception)
25. ALWAYS call `--mark-replied` before writing the `agent5` block
