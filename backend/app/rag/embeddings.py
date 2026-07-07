from typing import List

class GoogleEmbeddingsStub:
    """Skeleton wrapper for Google Embeddings API using the official SDK."""
    def __init__(self, model_name: str = "text-embedding-004"):
        self.model_name = model_name

    def embed_query(self, text: str) -> List[float]:
        # Placeholder vector output
        return [0.1] * 768

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        # Placeholder matrix output
        return [[0.1] * 768 for _ in texts]
