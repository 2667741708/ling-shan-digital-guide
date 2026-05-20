import json

from app.services import embedding_service


def test_hash_embedding_fallback_is_deterministic(monkeypatch) -> None:
    monkeypatch.setattr(embedding_service.settings, "embedding_provider", "hash")
    monkeypatch.setattr(embedding_service.settings, "embedding_dimension", 16)

    first = embedding_service.embed_text("灵山大佛 文化 讲解")
    second = embedding_service.embed_text("灵山大佛 文化 讲解")

    assert first == second
    assert len(first.vector) == 16
    assert first.provider == "hash"
    assert first.model == "hash_token_16"


def test_openai_compatible_embedding_provider(monkeypatch) -> None:
    calls = []

    class FakeResponse:
        status = 200

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self):
            return json.dumps({"data": [{"embedding": [1.0, 2.0, 3.0, 4.0]}]}).encode("utf-8")

    def fake_urlopen(request, timeout):
        calls.append((request, timeout))
        return FakeResponse()

    monkeypatch.setattr(embedding_service.settings, "embedding_provider", "openai")
    monkeypatch.setattr(embedding_service.settings, "embedding_base_url", "https://example.test/v1")
    monkeypatch.setattr(embedding_service.settings, "embedding_api_key", "test-key")
    monkeypatch.setattr(embedding_service.settings, "embedding_model", "text-embedding-test")
    monkeypatch.setattr(embedding_service.settings, "embedding_dimension", 3)
    monkeypatch.setattr(embedding_service.urllib.request, "urlopen", fake_urlopen)

    result = embedding_service.embed_text("测试文本")
    body = json.loads(calls[0][0].data.decode("utf-8"))

    assert result.provider == "openai"
    assert result.model == "text-embedding-test"
    assert len(result.vector) == 3
    assert body == {"model": "text-embedding-test", "input": "测试文本"}
    assert calls[0][0].headers["Authorization"] == "Bearer test-key"


def test_rerank_falls_back_without_remote_key(monkeypatch) -> None:
    monkeypatch.setattr(embedding_service.settings, "rerank_provider", "openai")
    monkeypatch.setattr(embedding_service.settings, "rerank_api_key", "")
    hits = [
        {"chunk_id": "a", "text": "普通介绍", "score": 0.2},
        {"chunk_id": "b", "text": "灵山大佛", "score": 0.8},
    ]

    assert embedding_service.rerank_hits("灵山大佛", hits, top_k=1)[0]["chunk_id"] == "b"
