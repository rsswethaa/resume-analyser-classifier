import os
from pathlib import Path

from flask import Flask, jsonify, render_template, request

from src.document_parser import extract_text
from src.product_analyser import analyse_candidate, rank_candidates
from src.product_storage import audit_summary, persist_analysis, upsert_job, upsert_resume

ROOT = Path(__file__).resolve().parent
app = Flask(__name__)
app.config.update(
    MAX_CONTENT_LENGTH=8 * 1024 * 1024,
    DATABASE=os.getenv('RESUME_DB', str(ROOT / 'resume_analyser.db')),
)


@app.get('/')
def index():
    return render_template('index.html')


@app.post('/api/compare')
def compare():
    job_title = (request.form.get('job_title') or 'Target Role').strip()
    job_description = (request.form.get('job_description') or '').strip()
    use_sbert = (request.form.get('use_sbert') or '').lower() in {'1','true','yes','on'}
    files = request.files.getlist('resumes')
    if not job_description:
        return jsonify({'error':'A job description is required.'}), 400
    if not files:
        return jsonify({'error':'Upload at least one resume.'}), 400
    if len(files) > 10:
        return jsonify({'error':'Upload up to 10 resumes per comparison.'}), 400

    analysed = []
    job_skills = []
    parsed_files = []
    for file in files:
        raw = file.read()
        try:
            text = extract_text(file.filename or 'resume.txt', raw)
        except Exception as exc:
            return jsonify({'error':f'{file.filename}: {exc}'}), 400
        if not text.strip():
            return jsonify({'error':f'{file.filename}: no readable text found.'}), 400
        analysis = analyse_candidate(text, job_description, use_sbert=use_sbert)
        job_skills = analysis['job_skills']
        candidate_name = Path(file.filename or 'Candidate').stem.replace('_',' ').replace('-',' ').title()
        parsed_files.append((candidate_name, file.filename, text, analysis))

    db_path = app.config['DATABASE']
    job_id, job_ref = upsert_job(db_path, job_title, job_description, job_skills)
    for candidate_name, filename, text, analysis in parsed_files:
        resume_id, resume_ref = upsert_resume(db_path, candidate_name, filename, text, analysis['resume_skills'])
        match_id = persist_analysis(db_path, resume_id, job_id, analysis)
        analysed.append({
            'candidate': candidate_name,
            'filename': filename,
            'resume_ref': resume_ref,
            'match_id': match_id,
            'analysis': analysis,
        })

    ranked = rank_candidates(analysed)
    return jsonify({
        'job': {'title': job_title, 'job_ref': job_ref},
        'candidates': ranked,
        'audit': audit_summary(db_path, job_id),
        'scoring_note': 'Ranking is decision support only and must not be used as an autonomous hiring decision.',
    })


@app.get('/api/audit')
def audit():
    return jsonify(audit_summary(app.config['DATABASE']))


@app.get('/health')
def health():
    return jsonify({'status':'ok','service':'resume-analyser'})


@app.errorhandler(413)
def too_large(_):
    return jsonify({'error':'Upload too large. Keep the total request under 8 MB.'}), 413


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT','5000')), debug=True)
