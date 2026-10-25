from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / 'database' / 'schema.sql'
SEED = ROOT / 'database' / 'seed.sql'


def connect(db_path):
    db = sqlite3.connect(db_path)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA foreign_keys = ON')
    return db


def init_db(db_path, seed=False):
    with connect(db_path) as db:
        db.executescript(SCHEMA.read_text(encoding='utf-8'))
        if seed:
            db.executescript(SEED.read_text(encoding='utf-8'))
    return Path(db_path)


def add_resume(db_path, candidate_ref, resume_text):
    if not resume_text.strip():
        raise ValueError('resume_text is required')
    with connect(db_path) as db:
        cur = db.execute('INSERT INTO resumes(candidate_ref,resume_text) VALUES (?,?)', (candidate_ref, resume_text.strip()))
        db.execute("INSERT INTO audit_events(event_type,entity_type,entity_id,detail) VALUES ('CREATE','resume',?,?)", (cur.lastrowid, candidate_ref))
        return cur.lastrowid


def add_job(db_path, job_ref, title, description_text):
    if not description_text.strip():
        raise ValueError('description_text is required')
    with connect(db_path) as db:
        cur = db.execute('INSERT INTO job_descriptions(job_ref,title,description_text) VALUES (?,?,?)', (job_ref, title, description_text.strip()))
        db.execute("INSERT INTO audit_events(event_type,entity_type,entity_id,detail) VALUES ('CREATE','job',?,?)", (cur.lastrowid, job_ref))
        return cur.lastrowid


def save_match(db_path, resume_id, job_id, semantic_score, skill_score, final_score, classification, encoder_version):
    with connect(db_path) as db:
        cur = db.execute('''INSERT INTO matches(resume_id,job_id,semantic_score,skill_score,final_score,classification,encoder_version)
                            VALUES (?,?,?,?,?,?,?)''',
                         (resume_id, job_id, float(semantic_score), float(skill_score), float(final_score), classification, encoder_version))
        db.execute("INSERT INTO audit_events(event_type,entity_type,entity_id,detail) VALUES ('SCORE','match',?,?)", (cur.lastrowid, encoder_version))
        return cur.lastrowid


def attach_skills(db_path, entity, entity_id, skill_names):
    if entity not in {'resume','job'}:
        raise ValueError('entity must be resume or job')
    link_table = 'resume_skills' if entity == 'resume' else 'job_skills'
    id_col = 'resume_id' if entity == 'resume' else 'job_id'
    with connect(db_path) as db:
        for name in sorted(set(s.lower().strip() for s in skill_names if s.strip())):
            db.execute('INSERT OR IGNORE INTO skills(skill_name) VALUES (?)', (name,))
            skill_id = db.execute('SELECT id FROM skills WHERE skill_name=?', (name,)).fetchone()['id']
            db.execute(f'INSERT OR IGNORE INTO {link_table}({id_col},skill_id) VALUES (?,?)', (entity_id, skill_id))
