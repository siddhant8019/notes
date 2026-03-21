# Scheduling Rules

> Rules for email send timing, follow-up scheduling, and date references.

---

## Send Timing

### Best Days
- **Tuesday, Wednesday, Thursday** — highest open and reply rates for B2B
- **Monday** — acceptable but lower engagement (inbox overload from weekend)
- **Friday** — avoid (end-of-week ignore, lower response rates)

### Best Times (Prospect's Local Timezone)
- **Primary window**: 8:00 AM – 10:00 AM
- **Secondary window**: 1:00 PM – 3:00 PM
- **Avoid**: Before 7:00 AM, after 6:00 PM, lunch hour (12:00-1:00 PM)

### Timezone Handling
- If prospect timezone is known, use it
- If unknown, infer from geography:
  - NA East: EST/EDT
  - NA West: PST/PDT
  - Europe: CET/CEST (default to London GMT for UK)
  - APAC: Use country-specific timezone

---

## Dynamic Date References

### The Problem
The templates say "tomorrow or Tuesday" but this becomes stale if not updated based on send day.

### The Rule
Always convert relative date references to actual day names based on the send date.

### Conversion Logic
| Send Day | "Tomorrow or [Day]" becomes |
|----------|---------------------------|
| Monday | "Tuesday or Wednesday" |
| Tuesday | "Wednesday or Thursday" |
| Wednesday | "Thursday or Friday" |
| Thursday | "Friday or Monday" |
| Friday | DO NOT SEND — skip to Monday |

### Format
- Use day names only, not dates (e.g., "Thursday or Monday", not "March 25 or March 28")
- Keep it natural — "Would Thursday or Monday work for a short conversation?"

---

## Follow-Up Timing

### Initial to Follow-Up
- Minimum gap: **3 business days** after initial send
- Optimal gap: **4-5 business days**
- Maximum gap: **7 business days** (after which the initial email is likely forgotten)

### Follow-Up Send Day
- Same day-of-week rules as initial sends
- Preferred: Tuesday-Thursday
- Avoid: Friday, weekends

---

## Batch Scheduling
- Daily send limit: Start at 20-30 emails
- Spread sends across the send window (not all at once)
- Stagger by 2-5 minutes between sends
- Rotate mailboxes if sending more than 15 emails per mailbox per day

---

## Holidays & Blackout Dates
- Do not send on US federal holidays
- Do not send during the week of Christmas (Dec 23-Jan 1)
- Do not send on prospect-country-specific holidays if known
- Pause sends if a major industry event is happening (prospects may be traveling)
