# Pending Reply Triage

> Inbound replies waiting for the Replies Agent to classify and route.

---

## Queue

| Reply ID | Send ID | Contact ID | First Name | Company | Reply Preview | Received Date | Status |
|----------|---------|-----------|-----------|---------|--------------|--------------|--------|
| [empty] | | | | | | | |

---

## Processing Rules
- Replies Agent classifies each reply into taxonomy categories
- Positive replies and referrals routed to Utkarsh immediately
- Bounces and unsubscribes added to suppression list immediately
- Hostile replies trigger operator alert
- Ambiguous replies escalated to human (marked needs_review)
- All classifications logged to `campaigns/cab/replies-log.md`
