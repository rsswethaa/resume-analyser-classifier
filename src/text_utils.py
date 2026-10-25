import math
import re
from collections import Counter

SKILLS = {
    "python","sql","excel","power bi","tableau","machine learning","deep learning",
    "finance","accounting","communication","research","data analysis","stakeholder management"
}


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def extract_skills(text: str) -> list[str]:
    cleaned = clean_text(text)
    return sorted(skill for skill in SKILLS if skill in cleaned)


def lexical_vector(text: str, vocabulary: list[str]) -> list[float]:
    counts = Counter(re.findall(r"[a-z0-9]+", clean_text(text)))
    return [float(counts[word]) for word in vocabulary]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    if len(a) != len(b) or not a:
        raise ValueError("vectors must be non-empty and the same length")
    dot = sum(x*y for x, y in zip(a,b))
    na = math.sqrt(sum(x*x for x in a))
    nb = math.sqrt(sum(y*y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return round(dot/(na*nb), 6)
