# Duplicate Contact Rules

> Deduplication logic applied during sourcing and before sending.

---

## Deduplication Checks

### 1. Exact Email Match
- If the same email address exists in any active campaign, skip
- If the same email was sent to in the last 30 days from any Teamcast campaign, skip

### 2. Same Person, Different Email
- Match by: first_name + last_name + company_domain
- If a match exists, keep the record with the higher confidence email
- Do not send to both emails

### 3. Company Domain Limits
- Maximum 2 contacts per company domain per batch
- If more than 2 contacts are found at the same company, prioritize by:
  1. Seniority score (higher = better)
  2. Title match to primary ICP (primary > secondary)
  3. Email confidence score

### 4. Cross-Campaign Deduplication
- Check all active Teamcast campaigns, not just CAB
- A contact in any active campaign is blocked from other campaigns
- Exception: operator can manually approve cross-campaign outreach

### 5. CRM Deduplication
- Check against existing Teamcast customers and relationships
- Never cold-email an existing customer
- Never cold-email someone who has an active conversation with Teamcast

## Resolution Priority
When duplicates are found:
1. Keep the record with the highest confidence score
2. If tied, keep the one from the more authoritative source (Apollo > Prospeo)
3. If still tied, keep the one with the more complete data record
4. Log the discarded duplicate with reason
