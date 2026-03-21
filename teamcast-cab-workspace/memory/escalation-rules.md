# Escalation Rules

> Defines when and how to escalate issues to the human operator.

---

## Immediate Escalation (Pause and Alert)

### Reply-Based
- A reply mentions legal concerns or threatens action
- A reply references spam reporting
- Multiple hostile replies in a single day (3+)
- A reply from someone known to be senior leadership at a major company

### Metric-Based
- Bounce rate exceeds 5% in a single batch
- QA pass rate drops below 60%
- More than 3 negative replies in a single day referencing spam or irrelevance
- Positive reply rate drops below 1% over a full week
- Mailbox health flags raised by email infrastructure

### System-Based
- Suppression list fails to load
- API keys expired or invalid
- Email sending infrastructure errors
- Agent unable to complete assigned task

## Standard Escalation (Flag for Review)

### Routing
- Positive reply received → Route to Utkarsh for personal response
- Referral received → Route to Utkarsh with referral details
- Prospect asks to speak with someone specific → Route to appropriate person
- Meeting booked → Confirm details and notify Utkarsh

### Review
- Low-confidence personalization signals (confidence < 6) → Human reviews before use
- Ambiguous reply classification → Human decides category
- Campaign metrics deviate significantly from baseline → Human reviews before next batch
- New objection pattern detected → Human decides if messaging needs adjustment

## Escalation Channels
- **Primary**: Notify Siddhant via workspace alert
- **Urgent**: Flag in `inbox/blocked-items.md` with URGENT tag
- **Routing to Utkarsh**: Log in `campaigns/cab/replies-log.md` with ROUTE_TO_UTKARSH tag

## Response Expectations
- Immediate escalations: Expect human response before campaign resumes
- Standard escalations: Campaign can continue for non-blocked items while awaiting review
- Routing: Utkarsh should respond to positive leads within 24 hours for best conversion
