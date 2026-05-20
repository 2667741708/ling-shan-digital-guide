from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from sqlalchemy import create_engine, text


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
DEFAULT_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@127.0.0.1:5433/lingtour",
)

sys.path.insert(0, str(BACKEND))


def _alembic_config(database_url: str):
    from alembic.config import Config

    config = Config(str(ROOT / "alembic.ini"))
    config.set_main_option("script_location", str(BACKEND / "alembic"))
    config.set_main_option("sqlalchemy.url", database_url)
    return config


def _has_existing_schema_without_alembic(database_url: str) -> bool:
    engine = create_engine(database_url, pool_pre_ping=True)
    try:
        with engine.connect() as connection:
            alembic_table = connection.execute(text("SELECT to_regclass('public.alembic_version')")).scalar()
            if alembic_table:
                return False
            table_count = connection.execute(
                text(
                    """
                    SELECT count(*)
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                      AND table_type = 'BASE TABLE'
                    """
                )
            ).scalar()
            return int(table_count or 0) > 0
    finally:
        engine.dispose()


def upgrade(database_url: str) -> dict:
    from alembic import command

    os.environ["DATABASE_URL"] = database_url
    config = _alembic_config(database_url)
    if _has_existing_schema_without_alembic(database_url):
        command.stamp(config, "head")
        action = "stamp-existing-schema"
    else:
        command.upgrade(config, "head")
        action = "upgrade-head"
    return {"database_url": database_url, "action": action, "revision": "head"}


def stamp(database_url: str) -> dict:
    from alembic import command

    os.environ["DATABASE_URL"] = database_url
    config = _alembic_config(database_url)
    command.stamp(config, "head")
    return {"database_url": database_url, "action": "stamp-head", "revision": "head"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run LingTour PostgreSQL Alembic migrations.")
    parser.add_argument("command", choices=["upgrade", "stamp"], nargs="?", default="upgrade")
    parser.add_argument("--database-url", default=DEFAULT_DATABASE_URL)
    args = parser.parse_args()

    if args.command == "upgrade":
        result = upgrade(args.database_url)
    else:
        result = stamp(args.database_url)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
