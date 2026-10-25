import hashlib
from pathlib import Path

from .storage import connect, init_db, attach_skills, save_match


def ensure_ready(db_path):
    path = Path(db_path)
    if not path.exists():
        init_db(path, seed=False)
    return path


def stable_ref(prefix: str, *parts: str) -> str:
    raw = '||'.join(parts).encode('utf-8', errors='ignore')
    return f"{prefix}-{hashlib.sha256(raw).hexdigest()[:16]}"


def upsert_resume(db_path, candidate_name: str, filename: str, resume_text: str, skills: list[str]):
    ensure_ready(db_path)
    ref = stable_ref('resume', candidate_name, filename, resume_text)
    with connect(db_path) as db:
        row = db.execute('SELECT id FROM resumes WHERE candidate_ref=?', (ref,)).fetchone()
        if row:
            resume_id = row['id']
        else:
            cur = db.execute('INSERT INTO resumes(candidate_ref,resume_text) VALUES (?,?)', (ref, resume_text))
            resume_id = cur.lastrowid
            db.execute("INSERT INTO audit_events(event_type,entity_type,entity_id,detail) VALUES ('CREATE','resume',?,?)", (resume_id, f"candidate={candidate_name};file={filename}"))
    attach_skills(db_path, 'resume', resume_id, skills)
    return resume_id, ref


def upsert_job(db_path, title: str, description: str, skills: list[str]):
    ensure_ready(db_path)
    ref = stable_ref('job', title, description)
    with connect(db_path) as db:
        row = db.execute('SELECT id FROM job_descriptions WHERE job_ref=?', (ref,)).fetchone()
        if row:
            job_id = row['id']
        else:
            cur = db.execute('INSERT INTO job_descriptions(job_ref,title,description_text) VALUES (?,?,?)', (ref, title, description))
            job_id = cur.lastrowid
            db.execute("INSERT INTO audit_events(event_type,entity_type,entity_id,detail) VALUES ('CREATE','job',?,?)", (job_id, title))
    attach_skills(db_path, 'job', job_id, skills)
    return job_id, ref


def persist_analysis(db_path, resume_id, job_id, analysis):
    return save_match(
        db_path,
        resume_id,
        job_id,
        analysis['semantic_similarity'],
        analysis['skill_coverage'],
        analysis['score'],
        analysis['classification'],
        analysis['encoder_version'],
    )


def audit_summary(db_path, job_id=None):
    ensure_ready(db_path)
    with connect(db_path) as db:
        where = 'WHERE m.job_id=?' if job_id else ''
        args = (job_id,) if job_id else ()
        row = db.execute(f'''SELECT COUNT(*) AS scored_candidates,
                                   ROUND(AVG(final_score),1) AS average_score,
                                   MIN(final_score) AS min_score,
                                   MAX(final_score) AS max_score
                            FROM matches m {where}''', args).fetchone()
        versions = db.execute(f'''SELECT encoder_version, COUNT(*) AS uses FROM matches m {where}
                                 GROUP BY encoder_version ORDER BY uses DESC''', args).fetchall()
        return {'metrics': dict(row), 'encoder_versions': [dict(v) for v in versions],
                'protected_attributes_used': [],
                'fairness_note': 'This prototype intentionally excludes protected demographic attributes. Absence of those fields does not prove fairness; production use requires outcome testing on representative data.'}
