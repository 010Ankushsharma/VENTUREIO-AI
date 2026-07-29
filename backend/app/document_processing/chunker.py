"""
Text chunking for RAG pipeline.
"""
from typing import List, Dict, Any


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    metadata: Dict[str, Any] = None,
) -> List[Dict[str, Any]]:
    """Split text into overlapping chunks."""
    if not text:
        return []

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        if end < len(text):
            last_period = chunk.rfind(".")
            last_newline = chunk.rfind("\n")
            break_point = max(last_period, last_newline)
            if break_point > chunk_size * 0.5:
                chunk = chunk[: break_point + 1]
                end = start + break_point + 1

        chunk_meta = {
            "chunk_index": len(chunks),
            "start_char": start,
            "end_char": end,
            **(metadata or {}),
        }

        chunks.append({"text": chunk.strip(), "metadata": chunk_meta})
        start = end - chunk_overlap

    return chunks
