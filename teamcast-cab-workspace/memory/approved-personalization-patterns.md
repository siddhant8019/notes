# Approved Personalization Patterns

> Patterns that have been validated through campaign performance or human review.
> The Research and Messaging agents should prefer these patterns.

---

## Pattern Templates

### Hiring Signals
- "noticed you are scaling engineering across multiple regions and hiring aggressively this quarter"
- "noticed your team has [X] open roles across [department/region]"
- "saw you're building out [team/function] with several open positions"

### Expansion Signals
- "saw your team recently expanded into EMEA and is managing high applicant volume across roles"
- "noticed [Company] recently opened offices in [region]"
- "saw your team is scaling across [X] regions"

### Funding Signals
- "noticed [Company] recently closed a [Series X] and is ramping up hiring"
- "saw [Company] recently raised [amount] to scale [product/engineering/operations]"

### Growth Signals
- "noticed [Company] has grown [X]% in headcount over the past year"
- "saw [Company] is scaling rapidly and hiring across multiple functions"

### Recruiting Ops Signals
- "noticed your recruiting team has grown recently and is managing increasing volume"
- "saw [Company] is investing in recruiting operations to support scaling"

## Quality Thresholds
- Confidence >= 7: Use directly
- Confidence 5-6: Use with caution, consider human review
- Confidence < 5: Do not use, fall back to generic

## Generic Fallback (When No Signal Found)
- "reaching out to a small group of leaders in the hiring and recruiting space"
- Only use when fallback_to_generic = yes
- Track fallback usage rate — if >30% of batch is fallback, tighten sourcing filters

## Performance Data
- [To be populated as reply data accumulates]
- Track which pattern types correlate with positive replies
