# Reply Triage

## Purpose
Classify and route inbound replies to CAB outreach emails. Determine the category, sentiment, and recommended next action for each reply.

## When to Use
- Continuously, as replies come in
- During the daily heartbeat reply monitoring step
- When replies are queued in `inbox/pending-reply-triage.md`

## Inputs
- Reply content (email body)
- Original send context (which email was sent, when, to whom)
- Reply taxonomy from `memory/reply-taxonomy.md`
- Escalation rules from `memory/escalation-rules.md`

## Steps

1. **Read the reply**
   - Parse the reply body
   - Identify the core intent

2. **Classify into category**

   | Category | Definition | Example |
   |----------|-----------|---------|
   | **positive** | Interested, willing to talk | "Sure, happy to chat" / "Send me more details" |
   | **defer** | Not now, but not no | "Reach out next quarter" / "Busy this month" |
   | **no_interest** | Polite decline | "Not interested" / "Not a fit right now" |
   | **not_relevant** | Wrong person, wrong company | "I left that role" / "We don't do hiring" |
   | **referral** | Points to someone else | "Talk to [Name], they handle this" |
   | **auto_reply** | Out of office, vacation | "I'm OOO until..." |
   | **bounce** | Delivery failure | Hard bounce / mailbox not found |
   | **unsubscribe** | Explicit opt-out | "Remove me" / "Unsubscribe" |
   | **hostile** | Angry, threatening | "This is spam" / "I'll report this" |

3. **Determine sentiment**
   - positive / neutral / negative

4. **Determine recommended action**

   | Category | Action |
   |----------|--------|
   | positive | Route to Utkarsh immediately. Log as meeting opportunity. |
   | defer | Log defer date. Schedule re-engagement. Do not follow up now. |
   | no_interest | Add to suppression list. Thank them if appropriate. Stop all outreach. |
   | not_relevant | Add to suppression list. Stop all outreach. |
   | referral | Route to Utkarsh with referral details. Log the referral. |
   | auto_reply | Note return date. Pause follow-ups until after return. |
   | bounce | Add to suppression list. Flag email as invalid. |
   | unsubscribe | Add to suppression list immediately. Stop all outreach. Comply within 24 hours. |
   | hostile | Pause campaign for this contact. Add to suppression. Alert operator. |

5. **Log the classification**
   - Write to `campaigns/cab/replies-log.md`
   - Include: reply_id, send_id, category, sentiment, meeting_booked (yes/no), referral_given (yes/no), recommended_action, timestamp

## Output
- Classified reply with category, sentiment, and action
- Updated suppression list if needed
- Routing notification if positive or referral

## Constraints
- When a reply is ambiguous, escalate to human — do not auto-classify
- Never auto-respond to positive replies (Utkarsh should respond personally)
- Process unsubscribes immediately, never delay
- Never follow up on a hostile reply
