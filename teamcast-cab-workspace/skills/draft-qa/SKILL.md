# Draft QA

## Purpose
Validate every outbound email draft before it enters the send queue. This is the guardrail agent — nothing goes out without passing QA. The goal is to catch fabricated personalization, compliance gaps, deliverability risks, and quality issues.

## When to Use
- After the Messaging Agent drafts emails
- When drafts are queued in `inbox/pending-qa.md`

## Inputs
- Email draft (subject, body, template version)
- Prospect record (name, title, company, email)
- Signal record (personalized line, source URL, confidence, freshness)
- Suppression list
- Prior send history
- QA rules from `memory/` files

## Steps

1. **Validate personalization**
   - Is the personalized line backed by a source URL?
   - Does the source URL actually support the claim?
   - Is the signal less than 90 days old?
   - Is the line specific to this prospect, not generic?
   - Score: personalization_quality (1-10)

2. **Check for hallucinated claims**
   - Does the email claim anything about the prospect's company that isn't verified?
   - Does it assume hiring pressure without evidence?
   - Does it reference a title, role, or action that doesn't match the prospect record?

3. **Check grammar and tone**
   - Is the language professional and peer-like?
   - Are there awkward phrases or broken sentences?
   - Does it read like Utkarsh wrote it?
   - Are any banned phrases present?

4. **Check compliance**
   - Is the opt-out line present?
   - Is the sender identified (Utkarsh Wagh, Teamcast Inc)?
   - Is the physical address present (San Jose, CA)?
   - Does it comply with CAN-SPAM requirements?

5. **Check for duplicates**
   - Has this contact already been emailed in this campaign?
   - Has this contact already replied?
   - Has this contact bounced?
   - Is this contact on the suppression list?
   - Are too many contacts from this company domain in this batch? (max 2)

6. **Check sequence state**
   - Is this the right email in the sequence? (Email 1/3 first, Email 2 only as follow-up)
   - Has enough time passed since the last email? (minimum 3 business days)
   - Is the follow-up appropriate given reply status?

7. **Score deliverability risk**
   - Check email format validity
   - Check for spam trigger words
   - Check subject line length and formatting
   - Score: deliverability_risk (1-10, lower is better)

8. **Final scoring**
   - personalization_quality (1-10)
   - safety_score (1-10)
   - send_readiness (1-10)
   - deliverability_risk (1-10)

## Hard Fail Cases (Auto-Reject)
- No source-backed personalization
- Fake hiring/expansion claim
- Broken merge tags ({FIRST NAME} still present)
- Contact already replied
- Contact already bounced
- Contact on suppression list
- Contact in another active Teamcast campaign
- More than 2 contacts from same company domain in batch
- Missing opt-out line
- Missing sender identification

## Output
- Approval or rejection for each draft
- Scores for each dimension
- Rejection reason if failed
- Approved drafts move to `campaigns/cab/approved-drafts.md`
- Rejected drafts move to `inbox/blocked-items.md` with reason

## Constraints
- QA agent has read-only access to all draft content
- QA agent has NO send permission
- If batch QA pass rate drops below 60%, halt and alert operator
