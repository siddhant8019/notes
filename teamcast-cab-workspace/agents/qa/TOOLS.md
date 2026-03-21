# QA Agent — Tool Permissions

## Allowed Tools
- **Campaign state (read)**: Read draft messages, prospect records, signal data, sent log, replies log
- **Campaign state (write)**: Write approval/rejection decisions
- **Suppression list (read)**: Verify contacts are not suppressed
- **Templates (read)**: Verify drafts match approved templates
- **Memory files (read)**: Read QA rules, banned phrases, compliance notes
- **Review queue (write)**: Write approval/rejection to review queue

## Denied Tools
- Apollo.io API (Sourcing Agent only)
- Prospeo API (Sourcing Agent only)
- LinkedIn browser (Research Agent only)
- Web search (Research Agent only)
- Email sending (Sending Agent only)
- Suppression list (write)
- Memory files (write)
- Templates (write)

## Critical Rule
- QA Agent has NO send permission under any circumstance
- QA Agent has read-only access to all draft content
- QA Agent cannot modify drafts — only approve or reject
