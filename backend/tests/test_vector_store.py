from app.services.vector_store import build_knowledge_base, retrieve_context


def test_build_knowledge_base_creates_entries():
    result = build_knowledge_base()
    assert result["entry_count"] >= 8


def test_retrieve_context_finds_facility_answer():
    chunks = retrieve_context("附近哪里有洗手间", top_k=3)
    assert chunks
    assert any("洗手间" in chunk["text"] for chunk in chunks)
