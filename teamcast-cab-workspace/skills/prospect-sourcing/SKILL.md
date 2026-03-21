# Prospect Sourcing

## Purpose
Query Apollo.io and Prospeo to find companies and contacts matching the current CAB campaign filters. Output normalized, deduplicated prospect records with confidence scores.

## When to Use
- At the start of each daily campaign run
- When the orchestrator requests a new batch of prospects
- When campaign filters are updated and a fresh pull is needed

## Inputs
- Campaign filters from `assets/company-filter-rules.md` and `assets/contact-title-rules.md`
- Current suppression list from `memory/suppression-list.md`
- Prior send history from `campaigns/cab/sent-log.md`

## Steps

1. **Load filters**
   - Read current company filters: industry, headcount (0-500), funding status, growth >= 15%
   - Read current contact title filters (primary and secondary)
   - Read geography filters: NA, Europe, APAC

2. **Query Apollo.io**
   - Search companies matching filters
   - For each matching company, search contacts by title
   - Use lookalike searches where TAM is defined
   - Respect API rate limits (max 100 contact lookups per run)

3. **Query Prospeo (if needed)**
   - Enrich contacts missing verified emails
   - Cross-reference headcount growth data
   - Max 50 enrichments per run

4. **Normalize records**
   - Each prospect record must include:
     - first_name, last_name, title, seniority_score
     - company, company_domain, industry, headcount
     - recent_funding_flag, employee_growth_pct
     - geography, linkedin_url, work_email
     - source_tool, confidence_score, campaign_fit_reason

5. **Deduplicate**
   - Check against suppression list
   - Check against prior sends and active campaigns
   - Check against bounced contacts
   - Check against existing Teamcast relationships
   - Remove duplicates by email address

6. **Score and output**
   - Assign confidence_score based on data completeness and filter match strength
   - Do not forward any record without a confidence score
   - Write approved prospects to `inbox/pending-research.md`

## Output
- List of prospect records in structured format
- Each record ready for the Research Agent

## Constraints
- Never source contacts on the suppression list
- Never exceed API rate limits
- Never forward records without confidence scores
- Max 2 contacts per company domain per batch
