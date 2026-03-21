# Personalization Generation

## Purpose
Transform a raw research signal into a polished, natural-sounding personalized line ready for email template insertion. The line must read as if Utkarsh personally noticed something about the prospect.

## When to Use
- After the Research Agent produces a signal for a prospect
- As part of the messaging pipeline, before template filling

## Inputs
- Research signal record (signal text, source URL, signal type, confidence)
- Prospect record (name, title, company, persona type)
- Approved personalization patterns from `memory/approved-personalization-patterns.md`
- Banned phrases from `memory/banned-phrases.md`

## Steps

1. **Read the raw signal**
   - Understand what the signal actually says
   - Verify it connects to the prospect's role and company

2. **Draft the personalized line**
   - Format: "noticed [specific observation about their company/role]"
   - The line fills this template slot: "I {PERSONALIZED LINE} and thought we may have alignment."
   - Keep it under 25 words
   - Make it specific enough that it could only apply to this prospect

3. **Check against rules**
   - Is it source-backed? (must be yes)
   - Is it recent? (within 90 days)
   - Does it avoid banned phrases?
   - Does it sound natural, not robotic?
   - Would Utkarsh actually say this?

4. **Select the pattern**
   - For hiring signals: "noticed you are [hiring action]"
   - For expansion signals: "saw your team recently [expansion action]"
   - For funding signals: "noticed [company] recently [funding event]"
   - For growth signals: "saw [company] is [growth indicator]"

5. **Validate tone**
   - Must be peer-like, not sycophantic
   - Must be observational, not assumptive
   - Must be confident, not tentative

## Output
- Polished personalized line ready for template insertion
- Confidence score for the line itself (1-10)

## Examples

**Good:**
- "noticed you are scaling engineering across multiple regions and hiring aggressively this quarter"
- "saw your team recently expanded into EMEA and is managing high applicant volume across roles"
- "noticed [Company] recently closed a Series B and is ramping up product and engineering hiring"

**Bad:**
- "impressed by your work at [Company]" (generic)
- "noticed you're a leader in the recruiting space" (vague)
- "saw that [Company] is doing great things" (empty)

## Constraints
- Never output a personalized line without a source URL backing it
- Never use language from the banned phrases list
- If confidence is below 6, flag for human review instead of inserting
