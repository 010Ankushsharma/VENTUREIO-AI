"""
RAG Retriever — combines embedding search with context formatting.
"""
from typing import List, Dict, Any, Optional

from app.rag.embeddings import generate_query_embedding
from app.rag.vector_store import vector_store


async def retrieve_context(
    query: str,
    deal_id: Optional[str] = None,
    top_k: int = 10,
) -> List[Dict[str, Any]]:
    """
    Retrieve relevant document chunks for a query.
    """
    query_embedding = await generate_query_embedding(query)
    results = await vector_store.search(
        query_embedding=query_embedding,
        deal_id=deal_id,
        top_k=top_k,
    )
    return results


def format_context(chunks: List[Dict[str, Any]]) -> str:
    """Format retrieved chunks into a context string for LLM."""
    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        source = chunk.get("metadata", {}).get("source", "Unknown")
        text = chunk.get("text", "")
        context_parts.append(f"[Source {i}: {source}]\n{text}")
    return "\n\n---\n\n".join(context_parts)
