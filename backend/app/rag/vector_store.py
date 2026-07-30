"""
Qdrant Vector Store — manages document embeddings for RAG.
"""
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
)
import uuid

from app.core.config import settings


class VectorStore:
    def __init__(self):
        self.client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)
        self.collection = settings.QDRANT_COLLECTION
        self.vector_size = 1536  # OpenAI ada-002 dimensions

    async def ensure_collection(self):
        """Create collection if it doesn't exist."""
        collections = self.client.get_collections().collections
        names = [c.name for c in collections]
        if self.collection not in names:
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(
                    size=self.vector_size, distance=Distance.COSINE
                ),
            )

    async def upsert_documents(
        self,
        texts: List[str],
        embeddings: List[List[float]],
        metadata: List[Dict[str, Any]],
    ):
        """Insert document chunks with embeddings."""
        points = [
            PointStruct(
                id=str(uuid.uuid4()),
                vector=emb,
                payload={"text": text, **meta},
            )
            for text, emb, meta in zip(texts, embeddings, metadata)
        ]
        self.client.upsert(collection_name=self.collection, points=points)

    async def search(
        self,
        query_embedding: List[float],
        deal_id: Optional[str] = None,
        top_k: int = 10,
    ) -> List[Dict[str, Any]]:
        """Semantic search over stored documents."""
        query_filter = None
        if deal_id:
            query_filter = Filter(
                must=[FieldCondition(key="deal_id", match=MatchValue(value=deal_id))]
            )

        results = self.client.search(
            collection_name=self.collection,
            query_vector=query_embedding,
            query_filter=query_filter,
            limit=top_k,
        )

        return [
            {
                "text": hit.payload.get("text", ""),
                "score": hit.score,
                "metadata": {k: v for k, v in hit.payload.items() if k != "text"},
            }
            for hit in results
        ]


vector_store = VectorStore()
