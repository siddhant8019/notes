# Suppression & Deduplication

## Purpose
Maintain the suppression list and deduplication logic to prevent unwanted outreach. This skill is called at multiple stages of the pipeline to ensure no contact is emailed who shouldn't be.

## When to Use
- Before any sourcing run (pre-filter)
- Before any enrichment (don't spend credits on suppressed contacts)
- Before any send (final check)
- After any opt-out, bounce, or hostile reply
- When manually adding contacts or domains to suppression

## Inputs
- Suppression list from `memory/suppression-list.md`
- Suppression rules from `memory/suppression-rules.md`
- Duplicate contact rules from `memory/duplicate-contact-rules.md`
- Sent log, replies log, bounce data

## Steps

### Suppression Check
1. **Check email-level suppression**
   - Is this exact email address on the suppression list?

2. **Check domain-level suppression**
   - Is this company domain blocked?
   - Common blocked domains: personal email providers (gmail, yahoo, hotmail, etc.)

3. **Check reason-based suppression**
   - Previously bounced
   - Previously unsubscribed
   - Previously sent hostile reply
   - Previously marked not_relevant
   - Already in another active Teamcast campaign
   - Existing Teamcast customer or relationship

### Deduplication Check
4. **Check for duplicate contacts**
   - Same email address across campaigns
   - Same person (name + company) with different email
   - Same company domain exceeding per-batch limit (max 2)

5. **Check for duplicate sends**
   - Has this contact already received this template?
   - Has this contact been emailed in the last 30 days from any Teamcast campaign?

### Suppression List Updates
6. **Add to suppression when:**
   - Contact bounces (hard bounce)
   - Contact replies with unsubscribe
   - Contact replies with hostile/spam complaint
   - Contact replies with not_relevant
   - Contact is manually flagged by operator
   - Domain is manually blocked

7. **Record format for each suppression entry:**
   - email or domain
   - reason (bounce / unsubscribe / hostile / not_relevant / manual / domain_block)
   - source (which campaign or action triggered it)
   - date added

## Output
- Pass/fail for each contact checked
- Updated suppression list when entries are added
- Deduplication report for batch review

## Constraints
- Suppression checks are mandatory at every pipeline stage — never skip
- Suppression list writes are immediate — never delay an opt-out
- Never remove a contact from suppression without human approval
- Log all suppression additions with reason and timestamp
