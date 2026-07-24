"""
============================================================
ChromaDB Vector Store Provider
============================================================

Module  : AI Vector Store Layer
Purpose : Persistent vector store provider using ChromaDB with fallback to Mock store.
"""

from typing import Optional, Any

from app.ai.chunking.chunk_models import ContextChunk
from app.ai.config import ai_config
from app.ai.embeddings.embedding_models import EmbeddingRecord
from app.ai.vector_store.providers.base import VectorStoreProvider
from app.ai.vector_store.providers.mock_provider import MockVectorStoreProvider
from app.ai.vector_store.vector_models import SearchFilter, VectorSearchResult

try:
    import chromadb  # type: ignore
    HAS_CHROMADB = True
except ImportError:
    chromadb = None
    HAS_CHROMADB = False


class ChromaDBProvider(VectorStoreProvider):
    """
    VectorStoreProvider using ChromaDB vector engine.
    Gracefully falls back to MockVectorStoreProvider if chromadb is not installed.
    """

    def __init__(self, persist_dir: str = ai_config.CHROMA_PERSIST_DIR):
        self.persist_dir = persist_dir
        self._fallback = MockVectorStoreProvider()
        self._client: Optional[Any] = None
        self._collection: Optional[Any] = None

        if HAS_CHROMADB and chromadb is not None:
            try:
                self._client = chromadb.PersistentClient(path=self.persist_dir)
                self._collection = self._client.get_or_create_collection(name="crimesphere_cases")
            except Exception:
                self._client = None
                self._collection = None

    @property
    def provider_name(self) -> str:
        return "chromadb"

    def upsert(
        self, records: list[EmbeddingRecord], chunks: list[ContextChunk]
    ) -> bool:
        if self._collection is None:
            return self._fallback.upsert(records, chunks)

        try:
            ids = [r.chunk_id for r in records]
            embeddings = [r.vector for r in records]
            chunk_map = {c.chunk_id: c for c in chunks}
            documents = [chunk_map[r.chunk_id].content for r in records]
            metadatas = [
                {
                    "case_id": chunk_map[r.chunk_id].case_id,
                    "chunk_type": chunk_map[r.chunk_id].chunk_type.value,
                    "parent_entity_id": chunk_map[r.chunk_id].parent_entity_id or "",
                }
                for r in records
            ]
            self._collection.upsert(
                ids=ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas,
            )
            return True
        except Exception:
            return self._fallback.upsert(records, chunks)

    def search(
        self,
        query_vector: list[float],
        filter_criteria: SearchFilter,
        top_k: int = 5,
    ) -> list[VectorSearchResult]:
        if self._collection is None:
            return self._fallback.search(query_vector, filter_criteria, top_k)

        try:
            where_clause = {}
            if filter_criteria.case_id:
                where_clause["case_id"] = filter_criteria.case_id

            res = self._collection.query(
                query_embeddings=[query_vector],
                n_results=top_k,
                where=where_clause if where_clause else None,
            )

            results: list[VectorSearchResult] = []
            if res and res.get("ids") and res["ids"][0]:
                for idx in range(len(res["ids"][0])):
                    cid = res["ids"][0][idx]
                    doc = res["documents"][0][idx]
                    meta = res["metadatas"][0][idx]
                    dist = res["distances"][0][idx] if "distances" in res else 0.0
                    score = round(1.0 / (1.0 + dist), 4)

                    results.append(
                        VectorSearchResult(
                            chunk_id=cid,
                            case_id=meta.get("case_id", ""),
                            score=score,
                            content=doc,
                            chunk_type=meta.get("chunk_type", "CASE"),
                            parent_entity_id=meta.get("parent_entity_id"),
                            metadata=meta,
                        )
                    )
            return results
        except Exception:
            return self._fallback.search(query_vector, filter_criteria, top_k)

    def delete(self, case_id: str) -> bool:
        if self._collection is None:
            return self._fallback.delete(case_id)
        try:
            self._collection.delete(where={"case_id": case_id})
            return True
        except Exception:
            return self._fallback.delete(case_id)

    def exists(self, case_id: str) -> bool:
        if self._collection is None:
            return self._fallback.exists(case_id)
        try:
            res = self._collection.get(where={"case_id": case_id}, limit=1)
            return len(res.get("ids", [])) > 0
        except Exception:
            return self._fallback.exists(case_id)

    def count(self, case_id: Optional[str] = None) -> int:
        if self._collection is None:
            return self._fallback.count(case_id)
        try:
            if case_id:
                res = self._collection.get(where={"case_id": case_id})
                return len(res.get("ids", []))
            return self._collection.count()
        except Exception:
            return self._fallback.count(case_id)

    def clear(self) -> bool:
        if self._collection is None:
            return self._fallback.clear()
        try:
            self._client.delete_collection("crimesphere_cases")
            self._collection = self._client.get_or_create_collection(name="crimesphere_cases")
            return True
        except Exception:
            return self._fallback.clear()

    def list_all_case_ids(self) -> list[str]:
        if self._collection is None:
            return self._fallback.list_all_case_ids()
        try:
            res = self._collection.get(include=["metadatas"])
            metas = res.get("metadatas", [])
            return sorted(list({m["case_id"] for m in metas if "case_id" in m}))
        except Exception:
            return self._fallback.list_all_case_ids()
