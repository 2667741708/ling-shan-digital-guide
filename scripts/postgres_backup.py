from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path

from sqlalchemy.engine import make_url


ROOT = Path(__file__).resolve().parents[1]
COMPOSE_FILE = ROOT / "deploy" / "docker-compose.yml"
DEFAULT_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@127.0.0.1:5433/lingtour",
)
DEFAULT_BACKUP_DIR = ROOT / "data" / "backups"


def _libpq_url(database_url: str) -> str:
    parsed = make_url(database_url)
    driver = parsed.drivername.split("+", 1)[0]
    return parsed.set(drivername=driver).render_as_string(hide_password=False)


def _resolve(command: str) -> str:
    resolved = shutil.which(command)
    if not resolved:
        raise FileNotFoundError(f"{command} not found in PATH")
    return resolved


def _postgres_parts(database_url: str) -> tuple[str, str, str]:
    parsed = make_url(database_url)
    return parsed.username or "postgres", parsed.password or "", parsed.database or "lingtour"


def _ensure_compose_postgres() -> None:
    docker = _resolve("docker")
    subprocess.run([docker, "compose", "-f", str(COMPOSE_FILE), "up", "-d", "postgres"], cwd=ROOT, check=True)


def backup(database_url: str, output: Path) -> dict:
    output.parent.mkdir(parents=True, exist_ok=True)
    pg_dump = shutil.which("pg_dump")
    if pg_dump:
        cmd = [pg_dump, "-Fc", "--no-owner", "--no-acl", "-d", _libpq_url(database_url), "-f", str(output)]
        subprocess.run(cmd, cwd=ROOT, check=True)
    else:
        _ensure_compose_postgres()
        user, password, database = _postgres_parts(database_url)
        docker = _resolve("docker")
        env = os.environ.copy()
        if password:
            env["PGPASSWORD"] = password
        cmd = [
            docker,
            "compose",
            "-f",
            str(COMPOSE_FILE),
            "exec",
            "-T",
            "postgres",
            "pg_dump",
            "-U",
            user,
            "-d",
            database,
            "-Fc",
            "--no-owner",
            "--no-acl",
        ]
        with output.open("wb") as file:
            subprocess.run(cmd, cwd=ROOT, env=env, stdout=file, check=True)
    return {"action": "backup", "database_url": database_url, "output": str(output)}


def restore(database_url: str, input_path: Path, clean: bool) -> dict:
    if not input_path.exists():
        raise FileNotFoundError(str(input_path))
    pg_restore = shutil.which("pg_restore")
    if pg_restore:
        cmd = [pg_restore, "-d", _libpq_url(database_url), "--no-owner"]
        if clean:
            cmd.extend(["--clean", "--if-exists"])
        cmd.append(str(input_path))
        subprocess.run(cmd, cwd=ROOT, check=True)
    else:
        _ensure_compose_postgres()
        user, password, database = _postgres_parts(database_url)
        docker = _resolve("docker")
        env = os.environ.copy()
        if password:
            env["PGPASSWORD"] = password
        cmd = [
            docker,
            "compose",
            "-f",
            str(COMPOSE_FILE),
            "exec",
            "-T",
            "postgres",
            "pg_restore",
            "-U",
            user,
            "-d",
            database,
            "--no-owner",
        ]
        if clean:
            cmd.extend(["--clean", "--if-exists"])
        with input_path.open("rb") as file:
            subprocess.run(cmd, cwd=ROOT, env=env, stdin=file, check=True)
    return {"action": "restore", "database_url": database_url, "input": str(input_path), "clean": clean}


def main() -> int:
    parser = argparse.ArgumentParser(description="Backup or restore the LingTour PostgreSQL database.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    backup_parser = subparsers.add_parser("backup")
    backup_parser.add_argument("--database-url", default=DEFAULT_DATABASE_URL)
    backup_parser.add_argument("--output", type=Path, default=DEFAULT_BACKUP_DIR / "lingtour.dump")

    restore_parser = subparsers.add_parser("restore")
    restore_parser.add_argument("--database-url", default=DEFAULT_DATABASE_URL)
    restore_parser.add_argument("--input", type=Path, required=True)
    restore_parser.add_argument("--clean", action="store_true")

    args = parser.parse_args()
    if args.command == "backup":
        result = backup(args.database_url, args.output)
    else:
        result = restore(args.database_url, args.input, args.clean)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
