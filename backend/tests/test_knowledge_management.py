import shutil
from pathlib import Path

from app.services import knowledge_service


def test_save_update_delete_admin_knowledge_document(monkeypatch):
    temp_dir = Path("backend/.test_admin_knowledge")
    shutil.rmtree(temp_dir, ignore_errors=True)
    temp_dir.mkdir(parents=True)
    monkeypatch.setattr(knowledge_service, "ADMIN_KNOWLEDGE_DIR", temp_dir)
    monkeypatch.setattr(knowledge_service, "rebuild_index", lambda: {"path": "demo", "entry_count": 1})

    try:
        saved = knowledge_service.save_document("demo.md", "新增讲解词：夜游路线适合从梵宫开始。".encode("utf-8"), "夜游路线")

        assert saved["editable"] is True
        assert (temp_dir / "夜游路线.md").exists()

        updated = knowledge_service.update_document("夜游路线", "夜游 FAQ", "问题：夜游怎么走？答案：从梵宫开始。")

        assert updated["id"] == "夜游_FAQ"
        assert (temp_dir / "夜游_FAQ.md").read_text(encoding="utf-8").startswith("问题")

        deleted = knowledge_service.delete_document("夜游_FAQ")

        assert deleted["status"] == "deleted"
        assert not (temp_dir / "夜游_FAQ.md").exists()
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
