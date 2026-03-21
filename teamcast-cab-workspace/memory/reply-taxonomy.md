# Reply Taxonomy

> Standardized classification system for inbound replies.
> Used by the Replies Agent to consistently categorize responses.

---

## Categories

### positive
**Definition**: Prospect expresses interest in learning more or participating
**Signal words**: "sure", "happy to chat", "interested", "tell me more", "send details", "let's schedule", "sounds interesting"
**Action**: Route to Utkarsh immediately
**Suppression**: No

### defer
**Definition**: Not now, but not a no. Prospect indicates future interest or timing constraint.
**Signal words**: "next quarter", "reach out later", "busy right now", "not the right time", "mid-reorg", "check back in [month]"
**Action**: Log defer date. Schedule re-engagement. No follow-up now.
**Suppression**: No (but pause outreach until defer date)

### no_interest
**Definition**: Polite decline with no hostility
**Signal words**: "not interested", "no thanks", "not a fit", "we're good", "pass"
**Action**: Respect and stop. Add to suppression.
**Suppression**: Yes

### not_relevant
**Definition**: Wrong person, wrong company, or mismatched context
**Signal words**: "I left [company]", "wrong person", "I don't handle this", "we don't do hiring"
**Action**: Suppress. Stop outreach.
**Suppression**: Yes

### referral
**Definition**: Prospect points to someone else who might be interested
**Signal words**: "talk to [Name]", "reach out to [Name]", "[Name] handles this", "copying [Name]"
**Action**: Route referral to Utkarsh. Log the referral. Thank the referrer.
**Suppression**: Suppress original contact from follow-up

### auto_reply
**Definition**: Automated out-of-office or vacation response
**Signal words**: "out of office", "OOO", "on vacation", "will return on [date]", "limited access"
**Action**: Note return date. Pause follow-ups until after return date.
**Suppression**: No (temporary pause only)

### bounce
**Definition**: Email delivery failure
**Signal words**: "mailbox not found", "undeliverable", "user unknown", "550 error"
**Action**: Suppress email permanently. Flag as invalid.
**Suppression**: Yes

### unsubscribe
**Definition**: Explicit opt-out request
**Signal words**: "remove me", "unsubscribe", "stop emailing", "take me off your list", "opt out"
**Action**: Suppress immediately. Comply within 24 hours.
**Suppression**: Yes

### hostile
**Definition**: Angry response, spam complaint, or legal threat
**Signal words**: "this is spam", "I'll report this", "how dare you", "harassment", "legal action", "reported"
**Action**: Suppress immediately. Alert operator. Do not respond.
**Suppression**: Yes

---

## Ambiguous Cases

When a reply doesn't clearly fit a category:
- Do NOT auto-classify
- Mark as "needs_review"
- Escalate to human operator
- Include the full reply text and your best guess with confidence level

## Edge Cases
- **"Interesting, but I'm leaving the company next month"** → defer + not_relevant. Suppress from this campaign but note the company for a different contact.
- **"Forward this to my assistant"** → positive signal. Route to Utkarsh with note.
- **"We already use [competitor]"** → no_interest. Log competitive intel.
- **"Who are you?"** → escalate. Could be hostile or curious.
