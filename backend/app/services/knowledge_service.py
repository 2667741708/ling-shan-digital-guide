from app.services.vector_store import VECTOR_STORE_PATH, load_vector_store
from app.services.vector_store import retrieve_context as retrieve_vector_context


def retrieve_context(query: str, top_k: int = 2) -> list[dict]:
    chunks = retrieve_vector_context(query, top_k=top_k)
    if chunks:
        return chunks
    return [
        {
            "chunk_id": "fallback_service",
            "source": "fallback",
            "category": "fallback",
            "title": "服务兜底",
            "text": "景区入口设有游客服务中心，可咨询路线、开放时间、失物招领和应急服务。",
            "score": 0,
        }
    ]


def list_documents() -> list[dict]:
    store = load_vector_store()
    source_counts: dict[str, int] = {}
    for entry in store.get("entries", []):
        source_counts[entry["source"]] = source_counts.get(entry["source"], 0) + 1
    return [
        {
            "id": index,
            "title": source,
            "status": "active",
            "chunk_count": count,
            "vector_store": str(VECTOR_STORE_PATH),
        }
        for index, (source, count) in enumerate(source_counts.items(), start=1)
    ]


def search_test(query: str) -> dict:
    return {"query": query, "chunks": retrieve_context(query)}
