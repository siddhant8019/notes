# TOOLS.md — Teamcast CAB Engine Tool Permissions & Boundaries

> This file is inherited by all sub-agents. Tool access rules here are binding.

---

## Available Tools

### Prospect Sourcing

- **Apollo.io API** — Company search, contact search, enrichment, lookalike searches
- **Prospeo** — Email finding, domain enrichment, headcount growth data
- **LinkedIn (browser-based)** — Profile viewing, job posting checks, company page signals

### Research & Signals

- **Web search** — Google/Bing for company news, press releases, funding announcements
- **LinkedIn browser** — Read-only profile and company page access for signal extraction
- **Job boards (browser)** — Check active job postings for hiring signal validation
- **Company websites (browser)** — About pages, careers pages, team pages

### Email Infrastructure

- **SMTP / Google Workspace** — Primary sending infrastructure
- **Resend / SES** — Backup sending infrastructure (if configured)
- **Mailbox rotation** — Managed via sending agent

### CRM & Data

- **Campaign state store** — Read/write campaign data (contacts, signals, messages, sends, replies)
- **Suppression list** — Read at every stage, write when contacts opt out or bounce
- **Review queue** — Write drafts for human review, read approval status

### Calendar

- **Calendly / scheduling link** — Reference only, do not auto-book

---

## Tool Access by Agent


| Tool                     | Orchestrator | Sourcing | Research | Messaging | QA  | Sending | Replies |
| ------------------------ | ------------ | -------- | -------- | --------- | --- | ------- | ------- |
| Apollo API               | -            | YES      | -        | -         | -   | -       | -       |
| Prospeo API              | -            | YES      | -        | -         | -   | -       | -       |
| LinkedIn browser         | -            | -        | YES      | -         | -   | -       | -       |
| Web search               | -            | -        | YES      | -         | -   | -       | -       |
| Job boards browser       | -            | -        | YES      | -         | -   | -       | -       |
| Company websites         | -            | -        | YES      | -         | -   | -       | -       |
| Email sending            | -            | -        | -        | -         | -   | YES     | -       |
| Mailbox rotation         | -            | -        | -        | -         | -   | YES     | -       |
| Campaign state (read)    | YES          | YES      | YES      | YES       | YES | YES     | YES     |
| Campaign state (write)   | YES          | YES      | -        | YES       | YES | YES     | YES     |
| Suppression list (read)  | YES          | YES      | -        | -         | YES | YES     | -       |
| Suppression list (write) | YES          | -        | -        | -         | -   | -       | YES     |
| Review queue (write)     | -            | -        | -        | YES       | YES | -       | -       |
| Review queue (read)      | YES          | -        | -        | -         | -   | YES     | -       |
| Templates (read)         | -            | -        | -        | YES       | YES | -       | -       |
| Memory files (read)      | YES          | YES      | YES      | YES       | YES | -       | YES     |
| Memory files (write)     | YES          | -        | -        | -         | -   | -       | YES     |


---

## Hard Constraints (All Agents)

### Never Do

- Fabricate a personalization line without a verifiable source
- Enrich or research a contact on the suppression list
- Send to a contact who has already replied (any category)
- Send to a contact who has bounced
- Send to a contact already in another active Teamcast campaign
- Send more than 2 contacts from the same company domain in a single batch
- Exceed the daily send limit defined in campaign config
- Auto-book meetings without human confirmation
- Access tools not assigned to your agent role
- Store API keys, passwords, or secrets in any .md file
- Modify AGENTS.md or TOOLS.md during a campaign run

### Always Do

- Check the suppression list before any enrichment or send action
- Log every action with timestamp and agent ID
- Include opt-out language in every outbound email
- Convert relative date references ("tomorrow", "Tuesday") to actual dates
- Validate email format before queuing for send
- Flag low-confidence signals for human review

---

## Rate Limits & Throttling

- **Apollo**: Respect API rate limits. Max 100 contact lookups per run.
- **Prospeo**: Max 50 enrichments per run.
- **Email sending**: Max daily limit defined in campaign config (start conservative: 20-30/day)
- **LinkedIn browser**: Max 30 profile views per session. Rotate sessions.
- **Web search**: No hard limit, but batch research to avoid excessive queries.

---

## Credential Management

- All API keys are stored in environment variables, never in workspace files
- Browser sessions use workspace-level auth, not shared credentials
- Each agent session should use its own auth context where possible
- Rotate mailbox credentials on the schedule defined in deliverability rules

