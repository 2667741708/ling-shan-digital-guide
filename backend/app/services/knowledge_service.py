from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

from app.services.vector_store import ADMIN_KNOWLEDGE_DIR, VECTOR_STORE_PATH, build_knowledge_base, load_vector_store
from app.services.vector_store import retrieve_context as retrieve_vector_context


SUPPORTED_UPLOAD_SUFFIXES = {".md", ".txt", ".csv", ".json", ".docx", ".xlsx"}


def retrieve_context(query: str, top_k: int = 2) -> list[dict]:
    """
    Retrieve scenic knowledge chunks for visitor answers.

    对应需求：
    - REQ-001 DeepSeek + 本地知识库问答闭环
    - REQ-007 后台知识库管理闭环

    文档：
    - docs/requirements_traceability.md#req-007-后台知识库管理闭环
    - docs/program_index.md#核心后端服务
    """
    chunks = retrieve_vector_context(query, top_k=top_k)
    if chunks:
        return chunks
    return [
        {
            "chunk_id": "fallback_service",
            "source": "fallback",
            "category": "fallback",
            "title": "服务兜底",
            "text": "景区入口设有游客服务中心，可咨询路线、开放时间、失物招领和应急服务。",
            "score": 0,
        }
    ]


def _safe_document_stem(name: str) -> str:
    stem = Path(name).stem.strip() or "knowledge"
    stem = re.sub(r"[^\w\u4e00-\u9fff.-]+", "_", stem)
    return stem[:80] or "knowledge"


def _safe_file_name(file_name: str, title: str | None = None) -> str:
    suffix = Path(file_name).suffix.lower()
    if suffix not in SUPPORTED_UPLOAD_SUFFIXES:
        suffix = ".md"
    return f"{_safe_document_stem(title or file_name)}{suffix}"


def _admin_document_path(document_id: str) -> Path:
    safe_id = _safe_document_stem(document_id)
    for path in ADMIN_KNOWLEDGE_DIR.glob("*"):
        if path.stem == safe_id:
            return path
    raise FileNotFoundError(f"knowledge document not found: {document_id}")


def _preview_text(path: Path, limit: int = 1200) -> str:
    if path.suffix.lower() not in {".md", ".txt", ".csv", ".json"}:
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")[:limit]


def rebuild_index() -> dict:
    """Rebuild the local JSON vector store after knowledge changes."""
    return build_knowledge_base()


def save_document(file_name: str, content: bytes, title: str | None = None) -> dict:
    """
    Save an uploaded knowledge document and rebuild the vector index.

    输入：上传文件名、字节内容、可选标题。
    输出：文档元信息和重建后的向量条目数。
    异常：文件类型不支持或文件为空时抛出 ValueError。
    """
    if not content:
        raise ValueError("uploaded knowledge document is empty")
    target_name = _safe_file_name(file_name, title)
    if Path(target_name).suffix.lower() not in SUPPORTED_UPLOAD_SUFFIXES:
        raise ValueError(f"unsupported knowledge document type: {file_name}")
    ADMIN_KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)
    target = ADMIN_KNOWLEDGE_DIR / target_name
    target.write_bytes(content)
    index_result = rebuild_index()
    return _document_payload(target, editable=True, index_result=index_result)


def update_document(document_id: str, title: str | None = None, content: str | None = None) -> dict:
    """Update an editable text knowledge document and rebuild the vector index."""
    path = _admin_document_path(document_id)
    if content is not None:
        if path.suffix.lower() not in {".md", ".txt", ".csv", ".json"}:
            raise ValueError("only text knowledge documents can be edited in browser")
        path.write_text(content, encoding="utf-8")
    if title and title.strip() and _safe_document_stem(title) != path.stem:
        new_path = path.with_name(f"{_safe_document_stem(title)}{path.suffix.lower()}")
        path.replace(new_path)
        path = new_path
    index_result = rebuild_index()
    return _document_payload(path, editable=True, index_result=index_result)


def delete_document(document_id: str) -> dict:
    """Delete an admin uploaded knowledge document and rebuild the vector index."""
    path = _admin_document_path(document_id)
    deleted = _document_payload(path, editable=True)
    path.unlink()
    index_result = rebuild_index()
    deleted["status"] = "deleted"
    deleted["index_result"] = index_result
    return deleted


def _document_payload(path: Path, editable: bool, index_result: dict | None = None, chunk_count: int = 0) -> dict:
    root_dir = Path(__file__).resolve().parents[3]
    resolved_path = path.resolve()
    try:
        source = str(resolved_path.relative_to(root_dir)).replace("\\", "/")
    except ValueError:
        source = str(resolved_path)
    payload = {
        "id": path.stem,
        "title": path.stem,
        "file_name": path.name,
        "source": source,
        "status": "active",
        "editable": editable,
        "chunk_count": chunk_count,
        "updated_at": datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds"),
        "preview": _preview_text(path),
        "vector_store": str(VECTOR_STORE_PATH),
    }
    if index_result:
        payload["index_result"] = index_result
    return payload


def list_documents() -> list[dict]:
    store = load_vector_store()
    source_counts: dict[str, int] = {}
    for entry in store.get("entries", []):
        source_counts[entry["source"]] = source_counts.get(entry["source"], 0) + 1

    documents: list[dict] = []
    for index, (source, count) in enumerate(source_counts.items(), start=1):
        path = Path(source)
        editable = source.startswith("data/admin_knowledge/")
        if editable:
            disk_path = Path(__file__).resolve().parents[3] / path
            if disk_path.exists():
                documents.append(_document_payload(disk_path, editable=True, chunk_count=count))
                continue
        documents.append(
            {
                "id": f"builtin_{index}",
                "title": source,
                "file_name": path.name,
                "source": source,
                "status": "active",
                "editable": False,
                "chunk_count": count,
                "updated_at": "",
                "preview": "",
                "vector_store": str(VECTOR_STORE_PATH),
            }
        )
    return documents


def search_test(query: str) -> dict:
    return {"query": query, "chunks": retrieve_context(query)}
