# Sourcing Agent — Tool Permissions

## Allowed Tools
- **Apollo.io API**: Company search, contact search, enrichment, lookalike searches
- **Prospeo API**: Email finding, domain enrichment, headcount growth data
- **Campaign state (read)**: Read campaign filters, suppression list, prior sends
- **Campaign state (write)**: Write new prospect records to the research queue
- **Memory files (read)**: Read suppression rules, company fit rules, duplicate contact rules

## Denied Tools
- LinkedIn browser (Research Agent only)
- Web search (Research Agent only)
- Email sending (Sending Agent only)
- Templates (Messaging Agent only)
- Memory files (write) (Orchestrator and Replies Agent only)
- Review queue (Messaging and QA Agents only)

## Rate Limits
- Apollo: Max 100 contact lookups per run
- Prospeo: Max 50 enrichments per run
- Respect all API rate limits and backoff requirements
