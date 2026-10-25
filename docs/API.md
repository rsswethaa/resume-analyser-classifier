# Interface Contracts

## NLP layer
The repository exposes text cleaning, skill extraction, cosine similarity, fit scoring and a lazy `SBERTEncoder` under `src/`.

## Persistence layer
- `init_db(path, seed=False)`
- `add_resume(path, candidate_ref, resume_text)`
- `add_job(path, job_ref, title, description_text)`
- `attach_skills(path, entity, entity_id, skill_names)`
- `save_match(path, resume_id, job_id, semantic_score, skill_score, final_score, classification, encoder_version)`

A production API should authenticate recruiters, authorise access per vacancy and never expose raw applicant data broadly.
