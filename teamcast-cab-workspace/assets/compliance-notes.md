# Compliance Notes

> Email compliance requirements for the Teamcast CAB campaign.

---

## CAN-SPAM Act (United States)

### Requirements
1. **Don't use false or misleading header information**: From name must be Utkarsh Wagh, Teamcast Inc.
2. **Don't use deceptive subject lines**: Subject must reflect the content (CAB invitation)
3. **Identify the message as an ad**: CAB invitations are borderline — we frame as genuine invitations, not ads
4. **Include physical address**: San Jose, CA (in signature block)
5. **Tell recipients how to opt out**: Every email must include opt-out language
6. **Honor opt-out requests promptly**: Within 10 business days (we aim for 24 hours)
7. **Monitor what others do on your behalf**: All agent actions are logged

### Our Implementation
- Every email includes: sender name, company name, physical location, opt-out line
- Opt-out line: "If you're not open to board opportunities, just let me know and I will step back." (or approved variant)
- Unsubscribes are processed immediately by the Replies Agent
- All sends are logged with full audit trail

---

## GDPR (European Union)

### Relevance
When emailing prospects in EU/EEA countries, GDPR applies.

### Legitimate Interest Basis
- B2B cold outreach can be conducted under "legitimate interest" when:
  - The recipient's business email is used (not personal)
  - The content is relevant to their professional role
  - An easy opt-out mechanism is provided
  - Data processing is proportionate

### Our Implementation
- Only use business email addresses
- Content is directly relevant to their professional role (hiring/recruiting)
- Clear opt-out in every email
- Do not store unnecessary personal data
- Respect all opt-out requests immediately

---

## CASL (Canada)

### Requirements
- Stricter than CAN-SPAM
- Implied consent exists for B2B communications if relevant to recipient's role
- Must identify sender clearly
- Must provide unsubscribe mechanism

### Our Implementation
- Same as CAN-SPAM implementation
- Additional care with Canadian prospects — ensure content is clearly relevant

---

## General Best Practices

### Always
- Include sender identification (Utkarsh Wagh, Teamcast Inc)
- Include physical address (San Jose, CA)
- Include opt-out mechanism
- Use business emails only (never personal emails)
- Honor opt-outs within 24 hours
- Log all sends and opt-outs
- Keep email content relevant to the recipient's professional role

### Never
- Use purchased lists without verification
- Send to personal email addresses
- Ignore opt-out requests
- Use misleading subject lines
- Hide the sender's identity
- Send from spoofed domains
- Continue emailing after an opt-out request

---

## Domain & Sender Reputation

### Protect Reputation By
- Starting with low daily volume (20-30) and scaling gradually
- Monitoring bounce rates (halt if > 5%)
- Using properly warmed-up mailboxes
- Rotating sending domains if needed
- Never sending to invalid or risky email addresses
- Maintaining clean suppression lists
