# Research Agent — Tool Permissions

## Allowed Tools
- **LinkedIn browser**: Profile viewing, company page reading (read-only)
- **Web search**: Google/Bing for company news, press releases, funding
- **Job boards browser**: Check active job postings for hiring signal validation
- **Company websites browser**: Careers pages, about pages, team pages, blogs
- **Campaign state (read)**: Read prospect records from the research queue
- **Memory files (read)**: Read personalization rules, approved patterns, banned phrases

## Denied Tools
- Apollo.io API (Sourcing Agent only)
- Prospeo API (Sourcing Agent only)
- Email sending (Sending Agent only)
- Templates (Messaging Agent only)
- Campaign state (write) (no direct write — output goes to messaging queue)
- Memory files (write) (Orchestrator and Replies Agent only)
- Suppression list (write)

## Rate Limits
- LinkedIn: Max 30 profile views per session
- Web search: Batch queries, avoid excessive requests
- Rotate browser sessions to avoid detection
