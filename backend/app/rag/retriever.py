from typing import List
from app.rag.loader import Document
from app.rag.vectorstore import ChromaVectorStoreStub

class RagRetriever:
    """Skeleton retriever returning context documents to agents."""
    def __init__(self, vectorstore: ChromaVectorStoreStub):
        self.vectorstore = vectorstore

    def retrieve(self, query: str) -> List[Document]:
        return self.vectorstore.similarity_search(query)
