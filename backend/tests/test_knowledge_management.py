import shutil
from pathlib import Path
from uuid import uuid4

from app.core.database import reset_database
from app.services import knowledge_service
from app.services.vector_store import build_knowledge_base, retrieve_context


def _reset_persistence(monkeypatch):
    test_id = uuid4().hex
    db_path = Path(f"backend/.test_lingtour_{test_id}.db")
    reset_database(f"sqlite:///{db_path.as_posix()}")
    temp_dir = Path(f"backend/.test_admin_knowledge_{test_id}")
    shutil.rmtree(temp_dir, ignore_errors=True)
    temp_dir.mkdir(parents=True)
    monkeypatch.setattr(knowledge_service, "ADMIN_KNOWLEDGE_DIR", temp_dir)
    return temp_dir


def test_versioned_knowledge_document_lifecycle(monkeypatch):
    temp_dir = _reset_persistence(monkeypatch)
    try:
        saved = knowledge_service.save_document(
            "demo.md",
            "问题：版本化测试知识？\n答案：发布后才能进入游客问答。".encode("utf-8"),
            "版本化测试",
            actor="admin",
        )

        assert saved["status"] == "draft"
        assert saved["current_version"] == 1
        assert all("版本化测试" not in hit["text"] for hit in retrieve_context("版本化测试知识", top_k=5))

        updated = knowledge_service.update_document(
            saved["id"],
            "版本化测试",
            "问题：版本化测试知识？\n答案：第二版发布后进入游客问答。",
            actor="admin",
        )

        assert updated["status"] == "draft"
        assert updated["current_version"] == 2
        assert len(knowledge_service.list_versions(saved["id"])) == 2

        published = knowledge_service.publish_document(saved["id"], actor="admin")
        build_knowledge_base()
        hits = retrieve_context("版本化测试知识", top_k=5)

        assert published["status"] == "active"
        assert hits
        assert hits[0]["source"].startswith("backend/.test_admin_knowledge") or "data/admin_knowledge" in hits[0]["source"]

        deleted = knowledge_service.delete_document(saved["id"], actor="admin")
        build_knowledge_base()

        assert deleted["status"] == "deleted"
        assert knowledge_service.list_history(saved["id"])
        assert all("版本化测试" not in hit["text"] for hit in retrieve_context("版本化测试知识", top_k=5))
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
