# Suppression Rules

> Defines when and why a contact or domain should be added to the suppression list.
> Checked at every pipeline stage by all agents with suppression access.

---

## Automatic Suppression Triggers

### Contact-Level
| Trigger | Action | Reversible? |
|---------|--------|-------------|
| Hard bounce | Suppress email permanently | No |
| Unsubscribe request | Suppress within 24 hours | No |
| Hostile/spam reply | Suppress immediately | No |
| "Not relevant" reply | Suppress permanently | No |
| "No interest" reply | Suppress permanently | No |
| Contact in another active Teamcast campaign | Block from this campaign | Yes (when other campaign ends) |
| Contact is existing Teamcast customer | Suppress from cold outreach | Yes (with operator approval) |
| Email format invalid | Suppress until corrected | Yes |

### Domain-Level
| Trigger | Action | Reversible? |
|---------|--------|-------------|
| Personal email provider (gmail, yahoo, hotmail, outlook personal) | Block from sourcing | No |
| Company domain with 3+ bounces | Block domain temporarily | Yes (after investigation) |
| Company domain with hostile reply | Watch list for 90 days | Yes |
| Competitor domain | Block from sourcing | No |

## Manual Suppression
- Operator can add any contact or domain with a reason
- Manual suppressions require a reason field
- Manual suppressions are never automatically removed

## Suppression Check Points
1. **Before sourcing**: Don't query for contacts at suppressed domains
2. **Before enrichment**: Don't spend API credits on suppressed contacts
3. **Before research**: Don't research suppressed contacts
4. **Before drafting**: Don't draft for suppressed contacts
5. **Before sending**: Final check — never send to suppressed contacts

## Suppression Removal
- Only by human operator approval
- Must document reason for removal
- Re-suppressed contacts get permanent suppression on second trigger
