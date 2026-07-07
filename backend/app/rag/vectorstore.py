from typing import List, Dict, Any
from app.rag.loader import Document
from app.rag.embeddings import GoogleEmbeddingsStub

class ChromaVectorStoreStub:
    """Skeleton interface to ChromaDB vector store."""
    def __init__(self, collection_name: str = "founder_docs"):
        self.collection_name = collection_name
        self.embeddings = GoogleEmbeddingsStub()
        self.db = None # Chroma Client placeholder

    def add_documents(self, documents: List[Document]) -> None:
        # Placeholder integration with chromadb
        pass

    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        # Return standard mock doc result
        return [
            Document(
                page_content="Mock matched text matching vector query in ChromaDB.",
                metadata={"score": 0.95}
            )
        ]
