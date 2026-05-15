from __future__ import annotations

import argparse
import json
import os
import shutil
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
FRONTEND = ROOT / "frontend"
DATA = ROOT / "data"
BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8000"))
FRONTEND_PORT = int(os.getenv("FRONTEND_PORT", "5173"))


def resolve_command(command: str) -> str:
    candidates = [command]
    if os.name == "nt":
        candidates.extend([f"{command}.cmd", f"{command}.exe", f"{command}.ps1"])
    for candidate in candidates:
        resolved = shutil.which(candidate)
        if resolved:
            return resolved
    raise FileNotFoundError(command)


def run(cmd: list[str], cwd: Path = ROOT, check: bool = True) -> subprocess.CompletedProcess:
    resolved = [resolve_command(cmd[0]), *cmd[1:]]
    print(f"$ {' '.join(cmd)}  (cwd={cwd})")
    return subprocess.run(resolved, cwd=cwd, check=check)


def require_file(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(str(path))


def port_is_busy(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.3)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def check_env() -> None:
    require_file(BACKEND / "requirements.txt")
    require_file(FRONTEND / "package.json")
    require_file(ROOT / "deploy" / "docker-compose.yml")
    require_file(DATA / "faq.csv")
    require_file(DATA / "scenic_spots.csv")
    require_file(DATA / "raw_documents" / "demo_scenic_guide.md")
    print(json.dumps({
        "python": sys.version.split()[0],
        "backend_port_busy": port_is_busy(BACKEND_PORT),
        "frontend_port_busy": port_is_busy(FRONTEND_PORT),
        "deepseek_key_present": bool(os.getenv("DEEPSEEK_API_KEY")),
    }, ensure_ascii=False, indent=2))


def install_backend_deps() -> None:
    run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], cwd=BACKEND)


def install_frontend_deps() -> None:
    run(["npm", "install"], cwd=FRONTEND)


def build_frontend() -> None:
    run(["npm", "run", "build"], cwd=FRONTEND)


def build_knowledge_base() -> None:
    run([sys.executable, "scripts/build_knowledge_base.py"], cwd=ROOT)


def test_backend() -> None:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(BACKEND)
    print(f"$ {sys.executable} -m pytest backend/tests -q  (cwd={ROOT})")
    subprocess.run([sys.executable, "-m", "pytest", "backend/tests", "-q"], cwd=ROOT, env=env, check=True)


def start_backend() -> subprocess.Popen:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(BACKEND)
    return subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "app.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(BACKEND_PORT),
        ],
        cwd=BACKEND,
        env=env,
    )


def wait_health(timeout_seconds: int = 30) -> str:
    url = f"http://127.0.0.1:{BACKEND_PORT}/api/health"
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=2) as response:
                body = response.read().decode("utf-8")
                if response.status == 200 and '"status":"ok"' in body.replace(" ", ""):
                    return body
        except Exception:
            time.sleep(0.5)
    raise TimeoutError(f"Backend health check failed: {url}")


def serve_backend() -> None:
    if port_is_busy(BACKEND_PORT):
        print(f"Backend port {BACKEND_PORT} is already in use; checking health directly.")
        print(wait_health())
        return
    process = start_backend()
    try:
        print(wait_health())
        print(f"Backend running at http://127.0.0.1:{BACKEND_PORT}")
        process.wait()
    finally:
        process.terminate()


def smoke_backend() -> None:
    process: subprocess.Popen | None = None
    if not port_is_busy(BACKEND_PORT):
        process = start_backend()
    try:
        print(wait_health())
        run([sys.executable, "scripts/smoke_test.py"], cwd=ROOT)
    finally:
        if process is not None:
            process.terminate()
            process.wait(timeout=10)


def main() -> int:
    parser = argparse.ArgumentParser(description="LingTour AI reproducible local runner")
    parser.add_argument(
        "command",
        choices=[
            "check-env",
            "install-backend",
            "install-frontend",
            "build-frontend",
            "build-kb",
            "test-backend",
            "serve-backend",
            "smoke-backend",
            "all",
        ],
    )
    args = parser.parse_args()

    if args.command == "check-env":
        check_env()
    elif args.command == "install-backend":
        install_backend_deps()
    elif args.command == "install-frontend":
        install_frontend_deps()
    elif args.command == "build-frontend":
        build_frontend()
    elif args.command == "build-kb":
        build_knowledge_base()
    elif args.command == "test-backend":
        test_backend()
    elif args.command == "serve-backend":
        serve_backend()
    elif args.command == "smoke-backend":
        smoke_backend()
    elif args.command == "all":
        check_env()
        install_backend_deps()
        build_knowledge_base()
        test_backend()
        serve_backend()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
