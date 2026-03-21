# Messaging Agent — Tool Permissions

## Allowed Tools
- **Templates (read)**: Read email templates and subject line pool
- **Campaign state (read)**: Read prospect records and signal data from messaging queue
- **Campaign state (write)**: Write drafted messages to QA queue
- **Memory files (read)**: Read banned phrases, persona notes, approved patterns, style rules
- **Review queue (write)**: Write drafts for QA review

## Denied Tools
- Apollo.io API (Sourcing Agent only)
- Prospeo API (Sourcing Agent only)
- LinkedIn browser (Research Agent only)
- Web search (Research Agent only)
- Email sending (Sending Agent only)
- Suppression list (read/write)
- Memory files (write)

## Rules
- Always include opt-out line
- Always use dynamic dates (never static "tomorrow or Tuesday")
- Always rotate subject lines — no repeats within same company domain
- Never use phrases from banned-phrases.md
