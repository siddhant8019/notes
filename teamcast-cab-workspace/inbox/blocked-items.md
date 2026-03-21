# Blocked Items

> Items that need human attention before they can proceed.
> Includes QA rejections, low-confidence signals, escalations, and system issues.

---

## Queue

| Item ID | Type | Contact/Company | Reason | Severity | Agent | Added Date | Status |
|---------|------|----------------|--------|----------|-------|-----------|--------|
| [empty] | | | | | | | |

---

## Type Key
- **qa_rejection**: Draft failed QA review
- **low_confidence_signal**: Research signal below confidence threshold
- **ambiguous_reply**: Reply classification unclear
- **escalation**: Issue requiring human decision
- **system_error**: Tool or API failure
- **metric_breach**: Campaign threshold exceeded

## Severity Key
- **URGENT**: Campaign paused until resolved
- **HIGH**: Blocks specific contacts but campaign continues
- **MEDIUM**: Needs review before next batch
- **LOW**: Informational, review when convenient

## Status Key
- **open**: Waiting for human review
- **in_review**: Human is reviewing
- **resolved**: Issue addressed, item can proceed or is discarded
- **dismissed**: Item reviewed and deemed not actionable

---

## Resolution Rules
- URGENT items must be resolved before campaign resumes
- QA rejections can be: fixed and re-queued, or discarded
- Low-confidence signals can be: approved by human, or prospect skipped
- Ambiguous replies can be: classified by human, or marked for re-review
- System errors should be investigated and root cause documented
