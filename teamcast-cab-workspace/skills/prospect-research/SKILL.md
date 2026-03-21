# Prospect Research

## Purpose
For each sourced prospect, find one credible, verifiable hiring or growth signal that can power a personalized outreach line. This is the most important step in the pipeline — the CAB campaign lives or dies on whether personalization feels real.

## When to Use
- After prospect sourcing produces new records
- When prospects are queued in `inbox/pending-research.md`

## Inputs
- Prospect records from sourcing (name, title, company, domain, LinkedIn URL)
- Signal rules from `assets/personalization-rules.md`

## Steps

1. **Check LinkedIn profile**
   - Review the contact's recent activity, headline, role tenure
   - Look for hiring-related posts, team announcements, expansion mentions

2. **Check company LinkedIn page**
   - Look for recent job postings, headcount changes, office expansions
   - Note any recent news or announcements

3. **Check company website**
   - Careers page: count open roles, identify hiring patterns
   - About page: team size, locations, recent milestones
   - Blog/press: funding announcements, product launches, market expansion

4. **Check job boards and news**
   - Search for the company name + "hiring" or "funding" or "expansion"
   - Look for recent press coverage

5. **Extract one outreach-worthy signal**
   - Must be specific, recent (within 90 days), and verifiable
   - Must relate to hiring activity, team growth, geographic expansion, funding, or recruiting complexity

6. **Classify signal quality**

   **Good signals:**
   - Expanded into EMEA
   - Opened multiple engineering roles
   - Recently raised funding and is scaling product/engineering
   - Hiring across regions
   - Growing recruiting operations
   - Launching new teams
   - Hiring aggressively in technical roles

   **Bad signals (never use):**
   - Generic company mission line
   - Vague "impressed by your leadership"
   - Stale news older than 90 days
   - Made-up assumptions about hiring pressure

7. **Format output**
   - personalized_line: The actual line to insert in the email
   - source_url: Where the signal was found
   - signal_type: hiring / expansion / funding / growth / recruiting_ops
   - confidence_score: 1-10
   - freshness: date of signal
   - fallback_to_generic: yes/no

## Output
- One signal record per prospect
- Move completed prospects to `inbox/pending-drafts.md`
- Flag low-confidence signals (score < 6) for human review in `inbox/blocked-items.md`

## Constraints
- Never fabricate a signal
- Never use a signal older than 90 days
- Never use generic flattery as a signal
- If no credible signal is found, mark fallback_to_generic = yes and use an honest generic framing
- Max 30 LinkedIn profile views per session
