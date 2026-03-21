# Follow-Up Scheduling

## Purpose
Determine which contacts are eligible for Email 2 (follow-up) and schedule them appropriately. Ensure follow-ups are timely, relevant, and never sent to contacts who should be suppressed.

## When to Use
- During the daily heartbeat follow-up check
- After reply triage is complete for the day

## Inputs
- Sent log from `campaigns/cab/sent-log.md`
- Replies log from `campaigns/cab/replies-log.md`
- Suppression list from `memory/suppression-list.md`
- Sequencing rules from AGENTS.md

## Steps

1. **Identify candidates**
   - Find contacts who received Email 1 or Email 3
   - Filter for contacts with NO reply of any kind
   - Minimum time gap: 3 business days since initial send

2. **Check eligibility**
   Each candidate must pass ALL of these:
   - [ ] No reply received (any category)
   - [ ] No bounce recorded
   - [ ] No auto-reply active (or auto-reply return date has passed)
   - [ ] No unsubscribe request
   - [ ] Not on suppression list
   - [ ] No internal owner conflict (not claimed by another team member)
   - [ ] Company domain not flagged for too many sends

3. **Queue eligible contacts**
   - Write eligible contacts to `inbox/pending-drafts.md` with flag: template = email-02-followup
   - Include original send context for the Messaging Agent

4. **Set scheduling**
   - Follow-ups should be sent on business days only
   - Avoid Mondays (inbox overload) and Fridays (end-of-week ignore)
   - Preferred: Tuesday, Wednesday, Thursday
   - Time: match the timezone of the prospect if available

## Output
- List of contacts eligible for follow-up
- Each queued with original send context and template flag
- Ineligible contacts logged with reason

## Constraints
- Maximum one follow-up per contact per campaign
- Never follow up on a bounced email
- Never follow up on a contact who replied in any category
- Never follow up on a suppressed contact
- If in doubt about eligibility, skip — do not send
