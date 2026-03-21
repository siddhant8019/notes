# Contact Title Rules

> Title matching logic for the Sourcing Agent.

---

## Primary Titles (Talent & Recruiting)

### Exact Match
```
Head of Talent Acquisition
Director of Talent Acquisition
VP of Talent Acquisition
Vice President of Talent Acquisition
Director of Recruiting
VP of Recruiting
Vice President of Recruiting
Chief People Officer
VP People
Vice President, People
Head of People
Talent Acquisition Manager
Senior Talent Acquisition Manager
Talent Operations Manager
Head of Recruiting Operations
Senior Recruiter
Lead Recruiter
Technical Recruiter
```

### Fuzzy Match (Include Variants)
```
*Talent Acquisition*Director*
*Talent Acquisition*Head*
*Talent Acquisition*VP*
*Recruiting*Director*
*Recruiting*VP*
*Recruiting*Head*
*People*VP*
*People*Head*
*People*Chief*
*TA Manager*
*Recruitment Manager*
*Hiring Manager* (only if clearly TA-focused, not line manager)
```

### Seniority Scoring
| Seniority | Score | Titles |
|-----------|-------|--------|
| C-Level | 10 | Chief People Officer |
| VP | 9 | VP Talent Acquisition, VP Recruiting, VP People |
| Head | 8 | Head of TA, Head of People, Head of Recruiting Ops |
| Director | 7 | Director of TA, Director of Recruiting |
| Senior Manager | 6 | Senior TA Manager, Talent Ops Manager |
| Manager | 5 | TA Manager, Recruitment Manager |
| Senior Individual | 4 | Senior Recruiter, Lead Recruiter |
| Individual | 3 | Technical Recruiter |

---

## Secondary Titles (Economic & Strategic)

### Exact Match
```
COO
Chief Operating Officer
CEO
Chief Executive Officer
CFO
Chief Financial Officer
VP Human Resources
Vice President Human Resources
Director of People Operations
Head of Workforce Planning
```

### Seniority Scoring
| Seniority | Score | Titles |
|-----------|-------|--------|
| C-Level | 10 | CEO, COO, CFO |
| VP | 9 | VP Human Resources |
| Director/Head | 7 | Director People Ops, Head Workforce Planning |

---

## Title Exclusions
Do NOT target:
```
Recruiter (without Senior/Lead/Technical qualifier)
HR Coordinator
HR Assistant
Recruiting Coordinator
Talent Sourcer (junior)
HR Generalist
Payroll Manager
Benefits Manager
Compensation Analyst
```

## Prioritization
When multiple contacts exist at the same company:
1. Highest seniority score wins
2. Primary title > Secondary title at same seniority
3. Max 2 contacts per company domain per batch
