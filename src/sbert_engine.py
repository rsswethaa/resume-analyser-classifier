from .text_utils import cosine_similarity

class SBERTEncoder:
    """Lazy Sentence-BERT wrapper so model downloads are opt-in."""
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._model = None

    def _load(self):
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
            except ImportError as exc:
                raise RuntimeError("Install requirements-ml.txt to enable S-BERT") from exc
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def encode(self, texts: list[str]) -> list[list[float]]:
        model = self._load()
        vectors = model.encode(texts, normalize_embeddings=True)
        return [list(map(float, row)) for row in vectors]

    def similarity(self, resume: str, job_description: str) -> float:
        a, b = self.encode([resume, job_description])
        return cosine_similarity(a, b)
