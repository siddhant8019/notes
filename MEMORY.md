# Teamcast GTM Engine — Memory

## Pipeline State (March 2026)

- Total leads in system: 31 (22 qualified, 9 in review queue)
- Verified emails: 9 confirmed | 13 staging (need real emails before outreach)
- Active campaign: CAB (Customer Advisory Board), 3-step sequence
- Sequence timing: Step 1→2: 8 days | Step 2→3: 3 days
- Step 1: new thread (initial email) | Step 2: new thread (first follow-up) | Step 3: thread reply to Step 2
- Sender rotation: multiple addresses across domains (see data/sender_config.json), round-robin, 8-10 per address/day
- No Step 1 emails sent yet as of March 2026 — pipeline at "drafted" stage

## Accounts + Keys

- Outreach senders: multi-sender rotation (config in data/sender_config.json — Siddhant to populate)
- Reports + notifications: siddhant.patil@teamcast.ai
- Apollo API: paid plan active (key in .env — never log the key value)
- Repo path: /Users/siddhantpatil/Claude/teamcast-leadgen

## Sourcing Preferences

- Primary source: Gmail newsletters (Step 4 of run protocol) — newsletter-first since March 2026
- Secondary: Apollo bulk search (apollo_mixed_people_api_search), Greenhouse/Lever job boards, YC directory
- Last resort: LinkedIn (fragile — CAPTCHA risk)
- GOLD signal priority: newsletter_exec_move, hiring_ta_role, ats_review, 10_plus_open_roles

## Known Issues (March 2026)

- 13 leads have staging emails — real emails needed before actual outreach to those leads
- Ricky Sahu (1upHealth) and Jessica Widel (Infisical) may have changed companies — re-qualify before sending
- apollo_bulk_match was blocked on old free-plan key — resolved with paid key 4bvQuOek_Ew9Dk5PGiORvA

## Rules Learned

- NEVER mark newsletter emails as read (learned: newsletters are primary source — any read-flag disrupts discovery)
- NEVER predict email addresses based on domain patterns — use only explicitly verified emails or staging fallback
- NEVER send Step 1 without explicit "send" command from Siddhant (follow-ups are autonomous)
- Auto-approve high/medium quality drafts — only hold low-quality for manual review
- ICP is NOT limited to companies hiring TA roles — any company with 3+ open roles qualifies
- apollo_search_people does NOT exist in the MCP package — use apollo_mixed_people_api_search for bulk search
- apollo_search_news_articles does NOT exist in the MCP package — use web_search for news

## Verified Emails (as of March 2026)

- Alyssa Croucher (AlphaSense) → acroucher@alpha-sense.com
- Arup Banerjee (Windfall) → arup@windfall.com
- Neha Chellaney (Sigma Computing) → neha@sigmacomputing.com
- Johannes Jaeckle (Heron Data) → johannes@herondata.io
- Girish Redekar (Sprinto) → girish@sprinto.com
- Ali Khokhar (Amigo) → ali@amigo.ai
- Steve Sonnenberg (Awardco) → steve@awardco.com
- Isabella DiGiovanni (Rebet) → bella@rebet.app
- Katey McGregor Ross (Tactacam) → kross@tactacam.com
