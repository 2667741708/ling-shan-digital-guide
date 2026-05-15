from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


def new_id() -> str:
    return uuid4().hex


class AdminUser(Base):
    __tablename__ = "admin_user"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=new_id)
    username: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(256))
    role: Mapped[str] = mapped_column(String(40), default="admin")
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class KnowledgeDocument(Base):
    __tablename__ = "knowledge_document"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=new_id)
    title: Mapped[str] = mapped_column(String(200))
    file_name: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(20), default="draft", index=True)
    current_version: Mapped[int] = mapped_column(Integer, default=1)
    current_version_id: Mapped[str | None] = mapped_column(String(32), nullable=True)
    storage_path: Mapped[str] = mapped_column(Text)
    created_by: Mapped[str] = mapped_column(String(80), default="system")
    updated_by: Mapped[str] = mapped_column(String(80), default="system")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    versions: Mapped[list["KnowledgeDocumentVersion"]] = relationship(
        "KnowledgeDocumentVersion",
        back_populates="document",
        cascade="all, delete-orphan",
        foreign_keys="KnowledgeDocumentVersion.document_id",
    )
    logs: Mapped[list["KnowledgeOperationLog"]] = relationship(
        "KnowledgeOperationLog",
        back_populates="document",
        cascade="all, delete-orphan",
        foreign_keys="KnowledgeOperationLog.document_id",
    )


class KnowledgeDocumentVersion(Base):
    __tablename__ = "knowledge_document_version"
    __table_args__ = (UniqueConstraint("document_id", "version", name="uq_knowledge_document_version"),)

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=new_id)
    document_id: Mapped[str] = mapped_column(ForeignKey("knowledge_document.id"), index=True)
    version: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String(200))
    file_name: Mapped[str] = mapped_column(String(255))
    storage_path: Mapped[str] = mapped_column(Text)
    content_hash: Mapped[str] = mapped_column(String(64))
    change_note: Mapped[str] = mapped_column(Text, default="")
    created_by: Mapped[str] = mapped_column(String(80), default="system")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    document: Mapped[KnowledgeDocument] = relationship(
        "KnowledgeDocument",
        back_populates="versions",
        foreign_keys=[document_id],
    )


class KnowledgeOperationLog(Base):
    __tablename__ = "knowledge_operation_log"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=new_id)
    document_id: Mapped[str | None] = mapped_column(ForeignKey("knowledge_document.id"), nullable=True, index=True)
    version_id: Mapped[str | None] = mapped_column(String(32), nullable=True)
    action: Mapped[str] = mapped_column(String(40))
    actor: Mapped[str] = mapped_column(String(80), default="system")
    detail: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    document: Mapped[KnowledgeDocument | None] = relationship(
        "KnowledgeDocument",
        back_populates="logs",
        foreign_keys=[document_id],
    )


class AvatarConfig(Base):
    __tablename__ = "avatar_config"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=new_id)
    name: Mapped[str] = mapped_column(String(100), default="灵灵")
    avatar_style: Mapped[str] = mapped_column(String(100), default="ancient")
    clothes: Mapped[str] = mapped_column(String(100), default="traditional_blue")
    voice_name: Mapped[str] = mapped_column(String(100), default="female_warm")
    voice_speed: Mapped[float] = mapped_column(Float, default=1.0)
    opening_text: Mapped[str] = mapped_column(Text, default="您好，我是您的 AI 数字人导游灵灵。")
    expressions_json: Mapped[str] = mapped_column(Text, default='["idle","listening","thinking","speaking","happy","concerned"]')
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
