# Pending Follow-Ups

> Contacts eligible for Email 2 follow-up. Populated by the Follow-Up Scheduling skill.

---

## Queue

| Contact ID | First Name | Company | Original Send Date | Original Template | Eligible Date | Status |
|-----------|-----------|---------|-------------------|------------------|--------------|--------|
| [empty] | | | | | | |

---

## Eligibility Criteria (ALL must be true)
- Received Email 1 or Email 3
- No reply of any kind
- No bounce
- No active auto-reply (or return date passed)
- No unsubscribe
- Not on suppression list
- 3+ business days since initial send
- < 7 business days since initial send

## Processing Rules
- Move eligible contacts to `inbox/pending-drafts.md` with template flag: email-02-followup
- Maximum ONE follow-up per contact per campaign
- Follow-up sends on Tuesday-Thursday preferred
