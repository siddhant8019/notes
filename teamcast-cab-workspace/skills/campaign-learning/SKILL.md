# Campaign Learning

## Purpose
Analyze campaign performance data to identify what works and what doesn't. Feed insights back into the system to improve targeting, messaging, and personalization over time. This is what makes the engine Inboxly-like — it gets smarter with every batch.

## When to Use
- Weekly, as part of the heartbeat learning cycle
- After significant reply volume accumulates (10+ replies)
- When the operator requests a performance review

## Inputs
- Sent log from `campaigns/cab/sent-log.md`
- Replies log from `campaigns/cab/replies-log.md`
- Outcomes from `campaigns/cab/outcomes.md`
- Campaign learnings from `memory/campaign-learnings.md`
- Subject line performance from `memory/high-performing-subject-lines.md`

## Steps

1. **Analyze reply rates by segment**
   - Which industries reply most?
   - Which job titles convert to meetings?
   - Which company sizes respond best?
   - Do recently-funded startups outperform headcount-growth companies?
   - Which geographies perform best?

2. **Analyze messaging performance**
   - Email 1 vs Email 3: which gets more positive replies?
   - Which subject lines have the highest open/reply rates?
   - Which subject lines underperform or trigger negative replies?
   - Which personalization patterns (signal types) correlate with positive replies?
   - Are certain phrases correlated with lower response rates?

3. **Analyze personalization quality**
   - Do high-confidence signals (8+) actually perform better than medium (5-7)?
   - Which signal types (hiring / expansion / funding / growth) work best?
   - Is "EMEA expansion" language overused or still effective?
   - Do generic fallback lines perform acceptably or should they be filtered out?

4. **Analyze follow-up effectiveness**
   - What percentage of Email 2 follow-ups generate replies?
   - Is the follow-up timing optimal (3 business days)?
   - Should follow-up messaging be adjusted?

5. **Detect concerning patterns**
   - Rising bounce rate trend
   - Increasing negative/hostile replies
   - Declining positive reply rate
   - Specific domains or industries generating complaints

6. **Generate recommendations**
   - Which filters should be tightened or loosened?
   - Which subject lines should be retired?
   - Which personalization patterns should be promoted?
   - Should daily send volume increase or decrease?
   - Are there new objection patterns to document?

7. **Update memory files**
   - Write findings to `memory/campaign-learnings.md`
   - Update `memory/high-performing-subject-lines.md`
   - Update `memory/approved-personalization-patterns.md`
   - Add new objections to `memory/objections-and-responses.md`
   - Update `memory/banned-phrases.md` if new phrases underperform

## Output
- Weekly performance summary
- Specific recommendations for next batch
- Updated memory files with learnings
- Alerts for any concerning trends

## Key Metrics to Track

### Top of Funnel
- Leads sourced per batch
- Valid contacts found
- Personalization pass rate
- QA pass rate

### Send Quality
- Delivery rate
- Bounce rate
- Open rate (if tracked)
- Positive reply rate
- Neutral reply rate
- Negative / unsubscribe rate

### Business Outcome
- Meetings booked
- Meetings attended
- CAB-qualified conversations
- Referral rate
- Product-interest conversion after CAB conversation

## Constraints
- Learning agent has read access to all campaign data
- Learning agent writes only to memory files
- Recommendations are suggestions — human operator decides on changes
- Never auto-modify campaign filters or templates based on learning alone
