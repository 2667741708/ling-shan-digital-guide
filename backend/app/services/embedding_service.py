from __future__ import annotations

import hashlib
import json
import math
import re
import urllib.request
from dataclasses import dataclass
from typing import Iterable

from app.core.config import settings


@dataclass(frozen=True)
class EmbeddingResult:
    """
    Normalized embedding vector and provider metadata.

    对应需求：
    - REQ-017 PostgreSQL + pgvector 知识库检索
    - REQ-019 生产级 RAG embedding/rerank 加固
    """

    vector: list[float]
    provider: str
    model: str
    dimension: int


def configured_embedding_dimension() -> int:
    """Return the storage dimension used by pgvector and JSON fallback payloads."""
    return int(settings.embedding_dimension or settings.pgvector_dimension)


def tokenize(text: str) -> list[str]:
    """Tokenize mixed Chinese/English text for deterministic hash embeddings."""
    normalized = text.lower()
    words = re.findall(r"[a-z0-9_]+", normalized)
    chinese_chars = re.findall(r"[\u4e00-\u9fff]", normalized)
    chinese_bigrams = [
        "".join(chinese_chars[index : index + 2])
        for index in range(max(len(chinese_chars) - 1, 0))
    ]
    return words + chinese_chars + chinese_bigrams


def _normalize(vector: Iterable[float], dimension: int) -> list[float]:
    values = [float(item) for item in vector]
    if len(values) > dimension:
        folded = [0.0] * dimension
        for index, value in enumerate(values):
            folded[index % dimension] += value
        values = folded
    elif len(values) < dimension:
        values = [*values, *([0.0] * (dimension - len(values)))]
    norm = math.sqrt(sum(value * value for value in values))
    if norm == 0:
        return values
    return [value / norm for value in values]


def hash_vectorize(text: str, dimension: int | None = None) -> list[float]:
    """Create a deterministic local embedding that keeps tests and demos reproducible."""
    dimension = dimension or configured_embedding_dimension()
    vector = [0.0] * dimension
    for token in tokenize(text):
        digest = hashlib.md5(token.encode("utf-8")).hexdigest()
        index = int(digest[:8], 16) % dimension
        vector[index] += 1.0
    return _normalize(vector, dimension)


def cosine_similarity(left: list[float], right: list[float]) -> float:
    """Calculate cosine similarity for already normalized vectors."""
    return sum(a * b for a, b in zip(left, right))


def _hash_result(text: str) -> EmbeddingResult:
    dimension = configured_embedding_dimension()
    return EmbeddingResult(
        vector=hash_vectorize(text, dimension),
        provider="hash",
        model=f"hash_token_{dimension}",
        dimension=dimension,
    )


def _post_json(url: str, api_key: str, payload: dict, timeout: float) -> dict:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        url=url,
        data=data,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def _openai_embedding(text: str) -> EmbeddingResult:
    dimension = configured_embedding_dimension()
    payload = _post_json(
        f"{settings.embedding_base_url.rstrip('/')}/embeddings",
        settings.embedding_api_key,
        {"model": settings.embedding_model, "input": text},
        settings.embedding_timeout_seconds,
    )
    data = payload.get("data") or []
    if not data or "embedding" not in data[0]:
        raise ValueError("embedding response missing data[0].embedding")
    return EmbeddingResult(
        vector=_normalize(data[0]["embedding"], dimension),
        provider="openai",
        model=settings.embedding_model,
        dimension=dimension,
    )


def embed_text(text: str) -> EmbeddingResult:
    """
    Embed text using the configured provider, falling back to local hash vectors.

    无 `EMBEDDING_API_KEY` 时，OpenAI 兼容 provider 自动回退到 hash，保证本地测试和演示可复现。
    """
    provider = (settings.embedding_provider or "hash").lower()
    if provider in {"openai", "openai-compatible"} and settings.embedding_api_key:
        return _openai_embedding(text)
    return _hash_result(text)


def embedding_metadata() -> dict:
    """Return actual provider metadata that will be written to knowledge_base rows."""
    provider = (settings.embedding_provider or "hash").lower()
    dimension = configured_embedding_dimension()
    if provider in {"openai", "openai-compatible"} and settings.embedding_api_key:
        return {
            "embedding_provider": "openai",
            "embedding_model": settings.embedding_model,
            "embedding_dimension": dimension,
        }
    result = _hash_result("")
    return {
        "embedding_provider": result.provider,
        "embedding_model": result.model,
        "embedding_dimension": result.dimension,
    }


def rerank_hits(query: str, hits: list[dict], top_k: int) -> list[dict]:
    """
    Optionally rerank retrieved chunks with a compatible `/rerank` HTTP endpoint.

    If rerank is not configured or fails, the existing vector score order is preserved.
    """
    fallback = sorted(hits, key=lambda item: item.get("score", 0), reverse=True)[:top_k]
    provider = (settings.rerank_provider or "none").lower()
    if provider not in {"openai", "openai-compatible", "http"} or not settings.rerank_api_key:
        return fallback
    if not hits:
        return []
    base_url = (settings.rerank_base_url or settings.embedding_base_url).rstrip("/")
    try:
        payload = _post_json(
            f"{base_url}/rerank",
            settings.rerank_api_key,
            {
                "model": settings.rerank_model,
                "query": query,
                "documents": [item.get("text", "") for item in hits],
                "top_n": top_k,
            },
            settings.rerank_timeout_seconds,
        )
        results = payload.get("results") or []
        by_index = []
        for item in results:
            index = int(item.get("index", -1))
            if 0 <= index < len(hits):
                updated = dict(hits[index])
                updated["rerank_score"] = float(item.get("relevance_score", updated.get("score", 0)))
                by_index.append(updated)
        if by_index:
            by_index.sort(key=lambda item: item.get("rerank_score", item.get("score", 0)), reverse=True)
            return by_index[:top_k]
    except Exception:
        return fallback
    return fallback
