from sentence_transformers import SentenceTransformer
from src.config.settings import settings

class Embeddings:
    def __init__(self):
        self.model = SentenceTransformer(settings.EMBEDDINGS_MODEL)
        
    def encode(self, texts: list[str]) -> list[list[float]]:
        return self.model.encode(texts, convert_to_numpy=True).tolist()