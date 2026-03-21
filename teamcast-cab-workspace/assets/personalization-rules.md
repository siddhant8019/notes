# Personalization Rules

> Rules governing how personalized lines are generated and validated.

---

## Core Principle
Every personalized line must be **specific, source-backed, recent, and verifiable**. The CAB campaign's credibility depends entirely on this. One fabricated line can destroy trust.

## What Makes a Good Personalized Line

### Must Be
- Based on a real, findable fact (with source URL)
- Recent (within 90 days)
- Specific to this prospect or their company
- Relevant to hiring, recruiting, scaling, or team growth
- Natural-sounding — something Utkarsh would actually say
- Under 25 words

### Must Not Be
- Fabricated or embellished
- Based on assumptions without evidence
- Generic flattery
- Older than 90 days
- About the prospect's personal life
- Sycophantic or over-the-top

## Signal Hierarchy (Best to Worst)

1. **Active hiring signal**: Company has open roles in relevant departments
2. **Expansion signal**: Company expanding into new regions or markets
3. **Funding signal**: Recent funding round with stated plans to grow team
4. **Growth signal**: Headcount growth metrics indicating scaling
5. **Recruiting ops signal**: Company investing in recruiting infrastructure
6. **Generic fallback**: No specific signal found — use honest generic framing

## Template Slot
The personalized line fills this exact slot:
```
I {PERSONALIZED LINE} and thought we may have alignment.
```

So the line should start with a verb that follows "I":
- "noticed you are..."
- "saw your team recently..."
- "noticed [Company] recently..."
- "saw [Company] is..."

## Confidence Thresholds
- **8-10**: Strong signal, use directly
- **6-7**: Acceptable, use with standard QA
- **4-5**: Weak signal, flag for human review
- **1-3**: Do not use, fall back to generic

## Generic Fallback
When no credible signal is found:
```
reaching out to a small group of leaders in the hiring and recruiting space
```
- Track fallback rate per batch
- If fallback rate > 30%, sourcing filters may need tightening

## Source Requirements
Every personalized line must have:
- `source_url`: The URL where the signal was found
- `signal_type`: hiring / expansion / funding / growth / recruiting_ops
- `freshness`: Date the signal was observed or published
- `confidence_score`: 1-10
