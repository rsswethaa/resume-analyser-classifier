-- Latest resume/job matches
SELECT r.candidate_ref, j.job_ref, j.title, m.semantic_score, m.skill_score,
       m.final_score, m.classification, m.encoder_version, m.created_at
FROM matches m
JOIN resumes r ON r.id=m.resume_id
JOIN job_descriptions j ON j.id=m.job_id
ORDER BY m.id DESC;

-- Resume skill inventory
SELECT r.candidate_ref, s.skill_name
FROM resume_skills rs
JOIN resumes r ON r.id=rs.resume_id
JOIN skills s ON s.id=rs.skill_id
ORDER BY r.candidate_ref, s.skill_name;

-- Audit timeline
SELECT event_type, entity_type, entity_id, detail, created_at
FROM audit_events ORDER BY id DESC;
