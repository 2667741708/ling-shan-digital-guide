from pathlib import Path
from uuid import uuid4

from app.core.database import reset_database
from app.services.avatar_service import get_active_avatar, save_avatar_config


def test_avatar_config_persists_in_database():
    db_path = Path(f"backend/.test_avatar_{uuid4().hex}.db")
    reset_database(f"sqlite:///{db_path.as_posix()}")

    saved = save_avatar_config({"name": "灵灵测试", "voice_name": "female_test", "opening_text": "欢迎测试。"})
    loaded = get_active_avatar()

    assert saved["name"] == "灵灵测试"
    assert loaded["voice_name"] == "female_test"
    assert loaded["opening_text"] == "欢迎测试。"
