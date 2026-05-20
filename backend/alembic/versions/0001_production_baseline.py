"""production baseline schema

Revision ID: 0001_production_baseline
Revises:
Create Date: 2026-05-20
"""

from __future__ import annotations

from alembic import op
from sqlalchemy import text

from app.core.database import Base
from app.models import persistence  # noqa: F401


revision = "0001_production_baseline"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    bind.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    Base.metadata.create_all(bind=bind)


def downgrade() -> None:
    bind = op.get_bind()
    Base.metadata.drop_all(bind=bind)
