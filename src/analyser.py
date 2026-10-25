import re
from .text_utils import clean_text, extract_skills, lexical_vector, cosine_similarity


def _vocabulary(a: str, b: str) -> list[str]:
    words = re.findall(r"[a-z0-9]+", clean_text(a + " " + b))
    return sorted(set(words))


def analyse_resume(resume: str, job_description: str, semantic_similarity: float | None = None) -> dict:
    vocab = _vocabulary(resume, job_description)
    lexical = cosine_similarity(lexical_vector(resume, vocab), lexical_vector(job_description, vocab)) if vocab else 0.0
    resume_skills = set(extract_skills(resume))
    job_skills = set(extract_skills(job_description))
    skill_coverage = 1.0 if not job_skills else len(resume_skills & job_skills) / len(job_skills)
    semantic = lexical if semantic_similarity is None else max(0.0, min(1.0, semantic_similarity))
    score = round((0.65 * semantic + 0.35 * skill_coverage) * 100, 1)
    classification = "STRONG_MATCH" if score >= 75 else "POTENTIAL_MATCH" if score >= 50 else "LOW_MATCH"
    return {
        "score": score,
        "classification": classification,
        "semantic_similarity": round(semantic, 4),
        "skill_coverage": round(skill_coverage, 4),
        "matched_skills": sorted(resume_skills & job_skills),
        "missing_skills": sorted(job_skills - resume_skills),
    }
