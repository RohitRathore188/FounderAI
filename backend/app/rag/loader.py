from typing import List, Dict, Any

class Document:
    def __init__(self, page_content: str, metadata: Dict[str, Any] = None):
        self.page_content = page_content
        self.metadata = metadata or {}

class RagDocumentLoader:
    """Skeleton loader for reading startup documents (PDFs, Markdown, etc.)"""
    def __init__(self, source_path: str):
        self.source_path = source_path

    def load(self) -> List[Document]:
        # Placeholder logic for loading files
        return [
            Document(
                page_content="FounderAI corporate governance and compliance checklist guidelines.",
                metadata={"source": self.source_path, "type": "guidelines"}
            )
        ]
