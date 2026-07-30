"""
Embedding generation for RAG pipeline.
"""
from typing import List
from openai import AsyncOpenAI

from app.core.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


async def generate_embeddings(texts: List[str], model: str = "text-embedding-3-small") -> List[List[float]]:
    """Generate embeddings for a list of texts."""
    response = await client.embeddings.create(input=texts, model=model)
    return [item.embedding for item in response.data]


async def generate_query_embedding(query: str, model: str = "text-embedding-3-small") -> List[float]:
    """Generate embedding for a single query."""
    response = await client.embeddings.create(input=[query], model=model)
    return response.data[0].embedding
