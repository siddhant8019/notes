# Company Filter Rules

> Technical filter definitions for the Sourcing Agent when querying Apollo/Prospeo.

---

## Required Filters (AND logic — all must match)

### Industry
Include companies in ANY of these industries:
```
Computer Software
Software Development
Information Technology & Services
Artificial Intelligence
FinTech / Financial Technology
HealthTech / Health Information Technology
Cloud Computing
Cybersecurity / Network Security
Enterprise SaaS
Tech-Enabled Services
BPO & Outsourcing (tech-focused)
Product-Based Technology Companies
```

### Headcount
```
Min: 0 (or 1)
Max: 500
```

### Geography
```
Regions: North America, Europe, APAC
Countries (if needed for granular filtering):
  NA: United States, Canada
  Europe: United Kingdom, Germany, France, Netherlands, Sweden, Ireland, Switzerland, Spain, Denmark, Norway, Finland
  APAC: Australia, Singapore, India, Japan, South Korea, New Zealand
```

### Growth Signal (OR logic — at least one must match)
```
Recently funded: Yes (any funding round in the last 12 months)
OR
Employee growth: >= 15% (trailing 12 months)
```

## Optional Enrichment Signals
These are not required but improve targeting quality:
- Number of open job postings > 0
- Has a careers page
- Recently posted engineering/product/recruiting roles
- Has a LinkedIn company page with > 50 followers

## Exclusion Filters

### Exclude Industries
```
Government
Education (K-12)
Non-profit (unless tech-focused)
Real Estate
Construction
Manufacturing (non-tech)
Retail (non-tech)
Food & Beverage
```

### Exclude Company Types
```
Personal email domains
Companies with no website
Companies with no LinkedIn presence
Known Teamcast competitors
Known Teamcast customers
```

## Apollo-Specific Query Notes
- Use Apollo's "Technology" and "SaaS" industry tags
- Enable "Recently funded" filter in Apollo's company search
- Use Prospeo's headcount growth filter for the 15% threshold
- TAM reference: Apollo TAM-APOLLO ~186.5K
