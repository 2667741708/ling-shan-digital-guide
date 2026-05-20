from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
import time
from datetime import datetime

from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import new_session
from app.models.persistence import AdminUser


PASSWORD_ITERATIONS = 120_000
TOKEN_TTL_SECONDS = 24 * 60 * 60
ROLE_ALIASES = {"admin": "super_admin"}
ROLE_PERMISSIONS: dict[str, set[str]] = {
    "super_admin": {
        "dashboard:read",
        "system:read",
        "knowledge:read",
        "knowledge:write",
        "ratings:read",
        "ratings:review",
        "users:manage",
        "avatar:write",
    },
    "knowledge_manager": {"dashboard:read", "knowledge:read", "knowledge:write"},
    "operator": {"dashboard:read", "ratings:read", "ratings:review", "knowledge:read", "avatar:write"},
    "viewer": {"dashboard:read", "knowledge:read", "ratings:read"},
}


def _b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def _unb64(data: str) -> bytes:
    padded = data + "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(padded.encode("ascii"))


def hash_password(password: str, salt: bytes | None = None) -> str:
    """
    Hash an administrator password with PBKDF2-HMAC-SHA256.

    对应需求：
    - REQ-008 后台权限、版本化知识库与数据库持久化
    """
    salt = salt or secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PASSWORD_ITERATIONS)
    return f"pbkdf2_sha256${PASSWORD_ITERATIONS}${salt.hex()}${digest.hex()}"


def normalize_role(role: str) -> str:
    return ROLE_ALIASES.get(role, role)


def permissions_for_role(role: str) -> list[str]:
    return sorted(ROLE_PERMISSIONS.get(normalize_role(role), set()))


def has_permission(role: str, permission: str) -> bool:
    return permission in ROLE_PERMISSIONS.get(normalize_role(role), set())


def _admin_user_payload(user: AdminUser) -> dict:
    return {
        "id": user.id,
        "username": user.username,
        "role": normalize_role(user.role),
        "permissions": permissions_for_role(user.role),
        "enabled": user.enabled,
        "last_login_at": user.last_login_at.isoformat(timespec="seconds") if user.last_login_at else None,
        "created_at": user.created_at.isoformat(timespec="seconds"),
        "updated_at": user.updated_at.isoformat(timespec="seconds"),
    }


def verify_password(password: str, password_hash: str) -> bool:
    try:
        algorithm, iterations, salt_hex, digest_hex = password_hash.split("$", 3)
    except ValueError:
        return False
    if algorithm != "pbkdf2_sha256":
        return False
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), bytes.fromhex(salt_hex), int(iterations))
    return hmac.compare_digest(digest.hex(), digest_hex)


def ensure_admin_user(db: Session | None = None) -> AdminUser:
    owns_session = db is None
    db = db or new_session()
    try:
        user = db.query(AdminUser).filter(AdminUser.username == settings.admin_username).first()
        if user:
            if normalize_role(user.role) != user.role:
                user.role = normalize_role(user.role)
                user.updated_at = datetime.utcnow()
                db.commit()
                db.refresh(user)
            return user
        user = AdminUser(
            username=settings.admin_username,
            password_hash=hash_password(settings.admin_password),
            role="super_admin",
            enabled=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    finally:
        if owns_session:
            db.close()


def _sign(payload: str) -> str:
    signature = hmac.new(settings.admin_token_secret.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256).digest()
    return _b64(signature)


def create_admin_token(user: AdminUser) -> str:
    payload = _b64(
        json.dumps(
            {
            "sub": user.username,
            "role": normalize_role(user.role),
            "exp": int(time.time()) + TOKEN_TTL_SECONDS,
            },
            ensure_ascii=False,
            separators=(",", ":"),
        ).encode("utf-8")
    )
    return f"{payload}.{_sign(payload)}"


def decode_admin_token(token: str) -> dict:
    try:
        payload, signature = token.split(".", 1)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail="invalid admin token") from exc
    if not hmac.compare_digest(_sign(payload), signature):
        raise HTTPException(status_code=401, detail="invalid admin token")
    data = json.loads(_unb64(payload))
    if int(data.get("exp", 0)) < int(time.time()):
        raise HTTPException(status_code=401, detail="admin token expired")
    return data


def authenticate_admin(username: str, password: str, db: Session | None = None) -> dict:
    owns_session = db is None
    db = db or new_session()
    try:
        ensure_admin_user(db)
        user = db.query(AdminUser).filter(AdminUser.username == username).first()
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="invalid username or password")
        if not user.enabled:
            raise HTTPException(status_code=403, detail="admin user disabled")
        user.last_login_at = datetime.utcnow()
        user.updated_at = datetime.utcnow()
        db.commit()
        return {
            "token": create_admin_token(user),
            "token_type": "bearer",
            "username": user.username,
            "role": normalize_role(user.role),
            "permissions": permissions_for_role(user.role),
        }
    finally:
        if owns_session:
            db.close()


def require_admin_user(authorization: str | None = Header(default=None)) -> dict:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="missing bearer token")
    data = decode_admin_token(authorization.split(" ", 1)[1].strip())
    db = new_session()
    try:
        user = db.query(AdminUser).filter(AdminUser.username == data.get("sub")).first()
        if not user or not user.enabled:
            raise HTTPException(status_code=401, detail="admin user disabled or missing")
        return {
            "username": user.username,
            "role": normalize_role(user.role),
            "permissions": permissions_for_role(user.role),
        }
    finally:
        db.close()


def require_admin_permission(permission: str):
    def dependency(admin=Depends(require_admin_user)) -> dict:
        if not has_permission(admin["role"], permission):
            raise HTTPException(status_code=403, detail=f"missing admin permission: {permission}")
        return admin

    return dependency


def list_admin_users(db: Session | None = None) -> list[dict]:
    owns_session = db is None
    db = db or new_session()
    try:
        ensure_admin_user(db)
        rows = db.query(AdminUser).order_by(AdminUser.created_at.asc()).all()
        return [_admin_user_payload(user) for user in rows]
    finally:
        if owns_session:
            db.close()


def create_admin_user(username: str, password: str, role: str, db: Session | None = None) -> dict:
    normalized_role = normalize_role(role)
    if normalized_role not in ROLE_PERMISSIONS:
        raise ValueError(f"unsupported admin role: {role}")
    if len(username.strip()) < 3:
        raise ValueError("admin username must be at least 3 characters")
    if len(password) < 8:
        raise ValueError("admin password must be at least 8 characters")

    owns_session = db is None
    db = db or new_session()
    try:
        ensure_admin_user(db)
        if db.query(AdminUser).filter(AdminUser.username == username.strip()).first():
            raise ValueError(f"admin username already exists: {username}")
        user = AdminUser(
            username=username.strip(),
            password_hash=hash_password(password),
            role=normalized_role,
            enabled=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return _admin_user_payload(user)
    finally:
        if owns_session:
            db.close()


def _get_admin_user_or_error(db: Session, user_id: str) -> AdminUser:
    user = db.get(AdminUser, user_id)
    if not user:
        raise FileNotFoundError(f"admin user not found: {user_id}")
    return user


def set_admin_user_enabled(user_id: str, enabled: bool, db: Session | None = None) -> dict:
    owns_session = db is None
    db = db or new_session()
    try:
        user = _get_admin_user_or_error(db, user_id)
        if not enabled and normalize_role(user.role) == "super_admin":
            active_super_admin_count = (
                db.query(AdminUser)
                .filter(AdminUser.enabled.is_(True), AdminUser.role.in_(["super_admin", "admin"]))
                .count()
            )
            if active_super_admin_count <= 1:
                raise ValueError("cannot disable the last enabled super_admin")
        user.enabled = enabled
        user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(user)
        return _admin_user_payload(user)
    finally:
        if owns_session:
            db.close()


def reset_admin_password(user_id: str, password: str, db: Session | None = None) -> dict:
    if len(password) < 8:
        raise ValueError("admin password must be at least 8 characters")
    owns_session = db is None
    db = db or new_session()
    try:
        user = _get_admin_user_or_error(db, user_id)
        user.password_hash = hash_password(password)
        user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(user)
        return _admin_user_payload(user)
    finally:
        if owns_session:
            db.close()
