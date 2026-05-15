from pathlib import Path
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import new_session, reset_database
from app.models.persistence import AdminUser
from app.services.auth_service import authenticate_admin, ensure_admin_user


def _reset_auth_db():
    db_path = Path(f"backend/.test_auth_{uuid4().hex}.db")
    reset_database(f"sqlite:///{db_path.as_posix()}")


def test_admin_login_success_and_invalid_password():
    _reset_auth_db()

    token = authenticate_admin("admin", "123456")

    assert token["token"]
    assert token["role"] == "admin"

    with pytest.raises(Exception):
        authenticate_admin("admin", "bad-password")


def test_disabled_admin_user_cannot_login():
    _reset_auth_db()
    user = ensure_admin_user()

    db = new_session()
    try:
        row = db.get(AdminUser, user.id)
        row.enabled = False
        db.commit()
    finally:
        db.close()

    with pytest.raises(Exception):
        authenticate_admin("admin", "123456")


def test_admin_write_api_requires_bearer_token():
    with TestClient(app) as client:
        response = client.post("/api/admin/knowledge/reindex")

    assert response.status_code == 401
