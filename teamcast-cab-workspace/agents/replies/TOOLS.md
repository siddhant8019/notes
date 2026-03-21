# Replies Agent — Tool Permissions

## Allowed Tools
- **Campaign state (read)**: Read sent log, original send context, contact records
- **Campaign state (write)**: Write reply classifications to replies log
- **Suppression list (write)**: Add bounces, unsubscribes, hostile replies, not_relevant
- **Memory files (read)**: Read reply taxonomy, escalation rules, objections
- **Memory files (write)**: Update reply taxonomy, objections, campaign learnings

## Denied Tools
- Apollo.io API (Sourcing Agent only)
- Prospeo API (Sourcing Agent only)
- LinkedIn browser (Research Agent only)
- Web search (Research Agent only)
- Email sending (Sending Agent only)
- Templates (Messaging Agent only)
- Review queue

## Critical Rules
- Never auto-respond to positive replies
- Process unsubscribes immediately
- Escalate ambiguous replies to human operator
- Never follow up on hostile replies
