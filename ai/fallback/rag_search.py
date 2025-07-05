"""
rag_search.py - Document-based fallback module for RAG (Retrieval-Augmented Generation)

This module is responsible for searching document embeddings from a vector store (e.g., FAISS).
It's used as a mid-layer fallback when RASA fails and user queries may be answered via uploaded docs.

✅ Uses Langchain
✅ Supports HuggingFace embeddings
✅ Search top-3 semantically similar chunks
"""

from typing import Optional
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

# Path where your vector store is saved
VECTOR_INDEX_PATH = "vector_store/index"

def search_documents(query: str) -> Optional[str]:
    """
    Search preloaded vector DB and return top chunks combined.
    :param query: User's message that failed structured intent matching.
    :return: Formatted answer string or None if no match found.
    """
    try:
        # Load embeddings + vector DB
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        db = FAISS.load_local(VECTOR_INDEX_PATH, embeddings)

        # Perform similarity search
        results = db.similarity_search(query, k=3)

        if not results:
            return None

        combined_text = "\n".join([r.page_content for r in results])
        return f"📘 Here’s what I found in the docs:\n{combined_text}"

    except Exception as e:
        print(f"[RAG ERROR] {str(e)}")
        return None