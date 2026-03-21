# CAB Message Drafting

## Purpose
Draft complete CAB outreach emails by combining the approved templates with prospect data, personalized lines, and persona-aware adjustments. Output ready-for-QA email drafts.

## When to Use
- After personalization generation is complete for a prospect
- When prospects are queued in `inbox/pending-drafts.md`

## Inputs
- Prospect record (name, title, company, persona type, seniority score)
- Personalized line + confidence score
- Signal type and source
- Email templates from `templates/`
- Subject lines from `templates/subject-lines.md`
- Persona emphasis rules from AGENTS.md
- Style rules from SOUL.md
- Current date (for dynamic scheduling)

## Steps

1. **Select template**
   - **Email 1 (Initial)**: Strong personalization signal, primary ICP, high company fit
   - **Email 3 (Alternate)**: Operational/scaling signal, recruiting ops target, "high growth teams" framing fits
   - **Email 2 (Follow-up)**: Only for contacts who received Email 1 or 3 with no reply, no bounce, no auto-reply, no unsubscribe

2. **Insert personalized line**
   - Place into the `{PERSONALIZED LINE}` slot
   - Ensure natural reading flow with surrounding text

3. **Adjust for persona**

   **Head of TA / Director Recruiting:**
   - Emphasize screening consistency, recruiter bandwidth, applicant volume, shortlist quality

   **CPO / VP People:**
   - Emphasize hiring efficiency, evidence-based evaluation, process defensibility, scaling consistency

   **COO / CEO:**
   - Emphasize hiring velocity, recruiter leverage, signal quality, operating efficiency

4. **Select subject lines**
   - Choose 2 options from the approved pool
   - Rank by persona and tone fit
   - Avoid "board seat invite" for less formal personas
   - Never repeat the same subject line to contacts at the same company domain

5. **Set dynamic dates**
   - Replace "tomorrow or Tuesday" with actual dates based on send day
   - Format: day name only (e.g., "Thursday or Monday")
   - Ensure the dates are business days

6. **Improve weak phrases**
   - Replace "I am sure you may have questions" with:
     - "Happy to share more context if helpful"
     - "I can send more details ahead of time if useful"
     - "Happy to share what participation looks like before we speak"
   - Rotate variants to avoid repetition

7. **Assemble final draft**
   - Subject line (primary + alternate)
   - Body with personalized line inserted
   - Signature block (Utkarsh Wagh, Teamcast Inc, San Jose, CA)
   - Opt-out line

## Output
- Complete email draft with metadata:
  - contact_id, subject (primary + alt), body, template_version, personalization_score
- Write to `inbox/pending-qa.md`

## Constraints
- Never send without the opt-out line
- Never use stale date references
- Never repeat subject lines within the same company domain
- Never use phrases from the banned list
- Preserve Utkarsh's voice — professional, warm, peer-like
