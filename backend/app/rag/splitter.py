from typing import List
from app.rag.loader import Document

class RagTextSplitter:
    """Skeleton text splitter for breaking down loaded documents into manageable chunks."""
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_documents(self, documents: List[Document]) -> List[Document]:
        # Placeholder split logic
        chunks = []
        for doc in documents:
            chunks.append(
                Document(
                    page_content=doc.page_content[:self.chunk_size],
                    metadata=doc.metadata
                )
            )
        return chunks
