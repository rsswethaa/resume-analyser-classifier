import re
from collections import Counter

from .analyser import analyse_resume
from .sbert_engine import SBERTEncoder
from .text_utils import clean_text, extract_skills, lexical_vector, cosine_similarity

SECTION_ALIASES = {
    'summary': {'summary','profile','objective','about'},
    'experience': {'experience','work experience','employment','professional experience','work history'},
    'education': {'education','academic background','academics','qualification','qualifications'},
    'skills': {'skills','technical skills','core skills','competencies','technologies'},
    'projects': {'projects','project experience','academic projects','personal projects'},
    'certifications': {'certifications','certificates','licenses','licences'},
}
STOPWORDS = {'and','the','with','for','from','that','this','you','your','our','are','will','have','has','into','using','use','who','job','role','team','work','skills','experience','years','a','an','to','of','in','on','is','be','as','or','at','by'}


def extract_sections(text: str) -> dict[str, str]:
    sections = {key: '' for key in SECTION_ALIASES}
    sections['other'] = ''
    current = 'other'
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        normalized = re.sub(r'[^a-z ]', '', line.lower()).strip()
        matched = None
        for canonical, aliases in SECTION_ALIASES.items():
            if normalized in aliases:
                matched = canonical
                break
        if matched:
            current = matched
        else:
            sections[current] += ('\n' if sections[current] else '') + line
    return sections


def _lexical_similarity(a: str, b: str) -> float:
    words = sorted(set(re.findall(r'[a-z0-9]+', clean_text(a + ' ' + b))))
    if not words:
        return 0.0
    return cosine_similarity(lexical_vector(a, words), lexical_vector(b, words))


def _semantic_similarity(a: str, b: str, use_sbert: bool) -> tuple[float, str]:
    if use_sbert:
        try:
            encoder = SBERTEncoder()
            return encoder.similarity(a, b), encoder.model_name
        except Exception:
            pass
    return _lexical_similarity(a, b), 'lexical-fallback-v2'


def keyword_gaps(resume: str, job_description: str, limit: int = 12) -> list[str]:
    resume_words = set(re.findall(r'[a-z][a-z0-9+#.-]{2,}', clean_text(resume)))
    job_words = [w for w in re.findall(r'[a-z][a-z0-9+#.-]{2,}', clean_text(job_description)) if w not in STOPWORDS]
    counts = Counter(job_words)
    return [word for word, _ in counts.most_common() if word not in resume_words][:limit]


def estimate_experience_years(text: str) -> float | None:
    explicit = [float(x) for x in re.findall(r'\b(\d+(?:\.\d+)?)\+?\s*(?:years|yrs)\b', text.lower())]
    if explicit:
        return max(explicit)
    ranges = re.findall(r'\b(20\d{2}|19\d{2})\s*[-–]\s*(20\d{2}|19\d{2})\b', text)
    durations = [max(0, int(end)-int(start)) for start, end in ranges]
    return float(sum(durations)) if durations else None


def analyse_candidate(resume: str, job_description: str, use_sbert: bool = False) -> dict:
    sections = extract_sections(resume)
    weights = {'experience':0.35,'skills':0.30,'projects':0.20,'education':0.15}
    weighted = 0.0
    used = 0.0
    section_scores = {}
    encoder_versions = set()
    for section, weight in weights.items():
        content = sections.get(section, '').strip()
        if not content:
            continue
        score, encoder = _semantic_similarity(content, job_description, use_sbert)
        section_scores[section] = round(score, 4)
        encoder_versions.add(encoder)
        weighted += score * weight
        used += weight
    if used == 0:
        semantic, encoder = _semantic_similarity(resume, job_description, use_sbert)
        encoder_versions.add(encoder)
    else:
        semantic = weighted / used
    base = analyse_resume(resume, job_description, semantic_similarity=semantic)
    years = estimate_experience_years(sections.get('experience','') or resume)
    base.update({
        'section_scores': section_scores,
        'sections_found': [k for k,v in sections.items() if v.strip() and k != 'other'],
        'experience_years_detected': years,
        'keyword_gaps': keyword_gaps(resume, job_description),
        'resume_skills': extract_skills(resume),
        'job_skills': extract_skills(job_description),
        'encoder_version': ','.join(sorted(encoder_versions)) or 'lexical-fallback-v2',
        'explanation': {
            'semantic_weight': 0.65,
            'skill_weight': 0.35,
            'protected_attributes_used': [],
            'ranking_basis': ['semantic alignment','job-related skill coverage','section-aware evidence'],
        },
    })
    return base


def rank_candidates(candidates: list[dict]) -> list[dict]:
    ranked = sorted(candidates, key=lambda item: item['analysis']['score'], reverse=True)
    for index, item in enumerate(ranked, start=1):
        item['rank'] = index
        item['rank_reason'] = f"Ranked on documented job-related features only; score {item['analysis']['score']}/100."
    return ranked
