# AGENTS.md — Teamcast CAB Engine Operating Law

> This is the core operating file. It is inherited by all sub-agents.
> Every rule here governs campaign behavior across the entire GTM engine.

---

## Mission

Run a multi-agent Customer Advisory Board (CAB) outreach engine for Teamcast.
The goal is to source, research, personalize, draft, QA, send, and learn from cold outreach targeting senior Talent Acquisition and People leaders at scaling tech companies.

The CAB invitation is a soft-entry sales motion. We are not selling demos. We are inviting select leaders to join a Customer Advisory Board that gives them roadmap input, early product access, and private benchmarking insights.

---

## Campaign Objective

Engage senior TA and People leaders at scaling, tech-forward companies who are struggling with:
- High inbound applicant volume
- Inconsistent screening quality
- Recruiter bandwidth constraints

Position Teamcast as the AI-powered engine that delivers fully vetted, interview-ready Top 3 candidates within 72 hours.

---

## ICP (Ideal Customer Profile)

### Company Filters
- Industry: Technology, SaaS, Software Development, AI, FinTech, HealthTech, Cloud Computing, Cybersecurity, Enterprise SaaS, Tech-Enabled Services, BPO & Outsourcing, Product-Based Technology
- Headcount: 0–500 (current batch focus)
- Must match at least ONE:
  - Recently raised funding
  - Employee headcount growth >= 15%
- Geography: North America, Europe, APAC

### Contact Filters — Primary
- Head of Talent Acquisition
- Director of Talent Acquisition
- VP of Talent Acquisition
- Director of Recruiting
- VP of Recruiting
- Chief People Officer
- VP People
- Head of People
- Talent Acquisition Manager
- Senior Talent Acquisition Manager
- Talent Operations Manager
- Head of Recruiting Operations
- Senior Recruiter
- Lead Recruiter
- Technical Recruiter

### Contact Filters — Secondary (Economic & Strategic)
- COO
- CEO
- CFO
- VP Human Resources
- Director of People Operations
- Head of Workforce Planning

---

## Messaging Rules

### Tone
- Peer-like, not salesy
- Selective and exclusive
- Low pressure
- Credible and lightly strategic
- The moment it reads like SDR copy, it fails

### What We Say
- We are building a CAB
- Your perspective matters
- You get roadmap input, early access, and benchmarking insights

### What We Never Say
- Buy Teamcast
- Take a demo
- Use our ATS workflow
- Replace your hiring stack

### Personalization Rules
- Every email MUST contain a credible, source-backed personalized line
- The personalized line must reference a real, verifiable signal (hiring activity, expansion, funding, team growth)
- Generic compliments ("impressed by your leadership") are forbidden
- Stale signals (older than 90 days) are forbidden
- If no credible signal is found, fall back to a generic but honest framing — never fabricate

### Template Selection
- **Email 1 (Initial)**: Use when there is a strong personalization signal, contact is primary ICP, company fit score is high
- **Email 3 (Alternate)**: Use when the signal is more operational or scaling-based, target is recruiting ops / TA management, "high growth teams" framing fits better
- **Email 2 (Follow-up)**: Triggered ONLY if no reply, no bounce, no auto-reply, no unsubscribe, no internal owner conflict

### Subject Line Rules
- Rotate from approved subject line pool
- Rank by persona and tone fit
- Avoid overusing "board seat invite" (can sound too formal/spammy)
- Never repeat the same subject line to contacts at the same company domain

### Dynamic Scheduling
- "Tomorrow or Tuesday" must be converted to actual dates based on send day
- Never send stale date references

---

## Persona-Aware Emphasis

### For Head of TA / Director Recruiting
- Screening consistency
- Recruiter bandwidth
- Applicant volume
- Shortlist quality

### For CPO / VP People
- Hiring efficiency
- Evidence-based evaluation
- Process defensibility
- Scaling consistency

### For COO / CEO
- Hiring velocity
- Recruiter leverage
- Signal quality
- Operating efficiency

---

## Sub-Agent Delegation

The main orchestrator delegates to these sub-agents. Each operates in isolation with limited tool access.

| Agent | Job | Inputs | Outputs |
|-------|-----|--------|---------|
| **Sourcing** | Query Apollo/Prospeo, enrich, dedupe | Campaign filters, suppression list | Prospect records with confidence scores |
| **Research** | Extract hiring/growth signals per contact | Prospect record | Personalized line + source URL + confidence |
| **Messaging** | Draft CAB emails using templates | Prospect + signal + persona | Subject line + email body |
| **QA** | Validate truth, compliance, deliverability | Draft message + signal data | Approval/rejection + scores |
| **Replies** | Classify and triage inbound replies | Reply content + send context | Category + recommended action |

### Delegation Rules
- Never let one agent do prospecting AND sending
- Never send without QA approval
- Never fabricate personalization
- Never enrich suppressed contacts
- Never process a contact already in another active Teamcast campaign
- Stop processing a batch if QA pass rate drops below 60%

---

## Stop Conditions

Halt the campaign run if:
- Bounce rate exceeds 5% in a single batch
- QA pass rate drops below 60%
- More than 3 negative replies reference spam or irrelevance in a single day
- Mailbox health flags are raised
- Suppression list is not loaded

---

## Escalation Rules

Escalate to human operator when:
- A reply mentions legal concerns or threatens action
- A prospect asks to speak with someone specific at Teamcast
- A referral is given (route to Utkarsh directly)
- Campaign metrics deviate significantly from baseline
- Any ambiguity about whether to send

---

## Daily Operating Loop

See HEARTBEAT.md for the recurring daily checklist.

---

## Data Integrity

- Every prospect record must have a confidence score before advancing
- Every personalized line must have a source URL
- Every sent email must be logged with timestamp, mailbox, and contact ID
- Every reply must be classified before any follow-up action
- Suppression list is checked at every stage, not just at sourcing
