import os
from app.rag.loader import RagDocumentLoader
from app.rag.splitter import RagTextSplitter
from app.rag.vectorstore import ChromaVectorStoreStub
from app.core.logging import logger

def ingest_directory(directory_path: str) -> None:
    """
    Ingests all files from a directory into the vector store.
    Prepared skeleton method.
    """
    logger.info(f"RAG: Beginning document ingestion from {directory_path}...")
    if not os.path.exists(directory_path):
        logger.warning(f"RAG: Directory {directory_path} does not exist. Skipping.")
        return

    # 1. Load documents
    loader = RagDocumentLoader(directory_path)
    docs = loader.load()

    # 2. Split documents
    splitter = RagTextSplitter()
    chunks = splitter.split_documents(docs)

    # 3. Write to ChromaDB
    db = ChromaVectorStoreStub()
    db.add_documents(chunks)
    logger.info(f"RAG: Ingested {len(chunks)} document chunks into vectorstore successfully.")

if __name__ == "__main__":
    # Example ingestion run
    ingest_directory("./data")
