# HEARTBEAT.md — Daily GTM Loop

> This checklist runs daily (or on the configured cron schedule).
> Each step should complete before the next begins.

---

## Morning Run

### 1. Health Check
- [ ] Verify mailbox health and domain reputation
- [ ] Confirm suppression list is loaded and current
- [ ] Check API keys and tool connectivity (Apollo, Prospeo, email infra)
- [ ] Verify Discord channel connectivity (`#cab-alerts`, `#cab-pipeline`, `#cab-replies`, `#cab-reports`, `#cab-review`)
- [ ] Review previous day's bounce rate — halt if > 5%
- [ ] If any health check fails, post to `#cab-alerts` and halt

### 2. Source New Prospects
- [ ] Run Sourcing Agent with current batch filters
- [ ] Dedupe against prior sends, CRM, bounced contacts, blocked domains, existing Teamcast relationships
- [ ] Validate prospect records have confidence scores
- [ ] Queue approved prospects for research

### 3. Research & Personalize
- [ ] Run Research Agent on queued prospects
- [ ] Extract one credible, source-backed hiring/growth signal per contact
- [ ] Score signal confidence and freshness
- [ ] Flag low-confidence signals for human review
- [ ] Move researched prospects to messaging queue

### 4. Draft Messages
- [ ] Run Messaging Agent on researched prospects
- [ ] Select Email 1 or Email 3 based on signal type and persona
- [ ] Insert personalized line and dynamic date references
- [ ] Generate 2 subject line options per draft
- [ ] Queue drafts for QA

### 5. Quality Assurance
- [ ] Run QA Agent on all pending drafts
- [ ] Validate personalization is real and source-backed
- [ ] Check for broken merge tags, duplicate sends, compliance issues
- [ ] Score each draft: personalization_quality, safety_score, send_readiness, deliverability_risk
- [ ] Approve drafts above threshold, reject and flag others
- [ ] Post approved drafts to `#cab-review` for human approval (Phase 1)
- [ ] If QA pass rate < 60%, halt the batch and post alert to `#cab-alerts`

### 6. Send (Phase 2+)
- [ ] Run Sending Agent on approved drafts only
- [ ] Throttle sends per daily limit
- [ ] Rotate mailboxes as configured
- [ ] Log every send with timestamp, mailbox, contact ID, message ID
- [ ] Post daily send summary to `#cab-pipeline` (sent count, delivered, bounced)

---

## Continuous / Afternoon

### 7. Monitor Replies
- [ ] Check inbound replies since last run
- [ ] Classify each reply: positive / no interest / not relevant / defer / referral / auto-reply / bounce
- [ ] Route positive replies and referrals to Utkarsh
- [ ] Post positive replies and referrals to `#cab-replies` (first name + company only, no email)
- [ ] Post hostile replies or spam complaints to `#cab-alerts`
- [ ] Add opt-outs to suppression list immediately
- [ ] Log all classifications

### 8. Follow-Up Check
- [ ] Identify contacts eligible for Email 2 follow-up (no reply, no bounce, no auto-reply, no unsubscribe, appropriate time gap)
- [ ] Queue eligible contacts for follow-up drafting
- [ ] Run through QA before sending

---

## Weekly

### 9. Campaign Learning
- [ ] Run Learning Agent on accumulated reply data
- [ ] Identify which industries, titles, subject lines, and personalization patterns perform best
- [ ] Compare Email 1 vs Email 3 performance
- [ ] Compare recently-funded vs headcount-growth companies
- [ ] Update campaign playbooks and memory files with findings
- [ ] Surface actionable insights for human review

### 10. Report
- [ ] Generate weekly summary: leads sourced, contacts found, personalization pass rate, QA pass rate, delivery rate, bounce rate, positive reply rate, meetings booked
- [ ] Post weekly report to `#cab-reports`
- [ ] Flag any concerning trends
- [ ] Recommend adjustments for next week

---

## Discord Pipeline Summary (End of Morning Run)

After steps 2-6, post a single consolidated summary to `#cab-pipeline`:

```
📊 **CAB Pipeline — [Date]**
• Sourced: [X] prospects ([Y] after dedupe)
• Researched: [X] signals ([Y] strong, [Z] fallback)
• Drafted: [X] emails (Email 1: [A], Email 3: [B])
• QA: [X] approved, [Y] rejected (pass rate: [Z]%)
• Sent: [X] delivered, [Y] bounced
• Pending review: [X] drafts in #cab-review
```

Do NOT post individual updates per step — one consolidated message only.
