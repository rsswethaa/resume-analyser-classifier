# Database Design

```mermaid
erDiagram
  RESUMES ||--o{ RESUME_SKILLS : has
  SKILLS ||--o{ RESUME_SKILLS : tags
  JOB_DESCRIPTIONS ||--o{ JOB_SKILLS : requires
  SKILLS ||--o{ JOB_SKILLS : tags
  RESUMES ||--o{ MATCHES : evaluated
  JOB_DESCRIPTIONS ||--o{ MATCHES : targets
```

## Tables
- `resumes`: candidate reference and resume text.
- `job_descriptions`: role reference/title/text.
- `skills`: normalised skill catalogue.
- `resume_skills` / `job_skills`: many-to-many explainability links.
- `matches`: semantic, skill and final score plus encoder version.
- `audit_events`: creation/scoring event history.

A production system should store the minimum necessary applicant data, encrypt sensitive content and enforce deletion/retention rules.
