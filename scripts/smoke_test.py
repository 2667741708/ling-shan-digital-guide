from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8000"))
BASE_URL = f"http://127.0.0.1:{BACKEND_PORT}"


def request_json(path: str, method: str = "GET", payload: dict | None = None) -> dict:
    body = None
    headers = {}
    if payload is not None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(f"{BASE_URL}{path}", data=body, headers=headers, method=method)
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def wait_health(timeout_seconds: int = 30) -> None:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        try:
            data = request_json("/api/health")
            if data["data"]["status"] == "ok":
                print("health ok")
                return
        except (urllib.error.URLError, KeyError):
            time.sleep(0.5)
    raise TimeoutError("health check failed")


def main() -> int:
    wait_health()
    search = request_json("/api/admin/knowledge/search-test", "POST", {"query": "附近哪里有洗手间"})
    chat = request_json(
        "/api/visitor/chat/text",
        "POST",
        {"session_uuid": "smoke", "message": "我只有两个小时喜欢历史和拍照怎么逛？"},
    )
    assert search["data"]["chunks"], search
    assert chat["data"]["answer"], chat
    print(json.dumps({
        "search_top": search["data"]["chunks"][0],
        "chat_model": chat["data"]["model_used"],
        "chat_latency_ms": chat["data"]["latency_ms"],
        "chat_answer_preview": chat["data"]["answer"][:80],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
