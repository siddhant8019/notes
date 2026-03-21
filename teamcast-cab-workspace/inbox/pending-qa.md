# Pending QA

> Drafted emails waiting for the QA Agent to review and approve/reject.

---

## Queue

| Draft ID | Contact ID | First Name | Company | Template | Personalization Score | Added Date |
|----------|-----------|-----------|---------|----------|----------------------|-----------|
| [empty] | | | | | | |

---

## Processing Rules
- QA Agent reviews all drafts in this queue
- Each draft scored on: personalization_quality, safety_score, send_readiness, deliverability_risk
- Approved drafts (send_readiness >= 7) → `campaigns/cab/approved-drafts.md`
- Rejected drafts → `inbox/blocked-items.md` with rejection reason
- If batch pass rate < 60%, halt and alert operator
