from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree


ROOT_DIR = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT_DIR / "data"
VECTOR_DB_DIR = DATA_DIR / "vector_db"
VECTOR_STORE_PATH = VECTOR_DB_DIR / "scenic_vector_store.json"
VECTOR_DIMENSION = 256


@dataclass
class KnowledgeEntry:
    id: str
    text: str
    source: str
    category: str
    title: str


def tokenize(text: str) -> list[str]:
    normalized = text.lower()
    words = re.findall(r"[a-z0-9_]+", normalized)
    chinese_chars = re.findall(r"[\u4e00-\u9fff]", normalized)
    chinese_bigrams = [
        "".join(chinese_chars[index : index + 2])
        for index in range(max(len(chinese_chars) - 1, 0))
    ]
    return words + chinese_chars + chinese_bigrams


def vectorize(text: str, dimension: int = VECTOR_DIMENSION) -> list[float]:
    vector = [0.0] * dimension
    for token in tokenize(text):
        digest = hashlib.md5(token.encode("utf-8")).hexdigest()
        index = int(digest[:8], 16) % dimension
        vector[index] += 1.0
    norm = math.sqrt(sum(value * value for value in vector))
    if norm == 0:
        return vector
    return [value / norm for value in vector]


def cosine_similarity(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right))


def chunk_text(text: str, chunk_size: int = 420, overlap: int = 80) -> Iterable[str]:
    compact = re.sub(r"\s+", " ", text).strip()
    if not compact:
        return
    start = 0
    while start < len(compact):
        yield compact[start : start + chunk_size]
        if start + chunk_size >= len(compact):
            break
        start += chunk_size - overlap


def load_faq_entries() -> list[KnowledgeEntry]:
    path = DATA_DIR / "faq.csv"
    if not path.exists():
        return []
    entries: list[KnowledgeEntry] = []
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        for row in csv.DictReader(file):
            text = f"问题：{row.get('question', '')}\n答案：{row.get('answer', '')}\n关键词：{row.get('keywords', '')}"
            entries.append(
                KnowledgeEntry(
                    id=f"faq_{row.get('id')}",
                    text=text,
                    source="data/faq.csv",
                    category=row.get("category", "faq"),
                    title=row.get("question", "FAQ"),
                )
            )
    return entries


def load_spot_entries() -> list[KnowledgeEntry]:
    path = DATA_DIR / "scenic_spots.csv"
    if not path.exists():
        return []
    entries: list[KnowledgeEntry] = []
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        for row in csv.DictReader(file):
            text = (
                f"景点：{row.get('name', '')}\n"
                f"标签：{row.get('tags', '')}\n"
                f"建议游览：{row.get('recommended_duration', '')} 分钟\n"
                f"地图坐标：x={row.get('map_x', '')}, y={row.get('map_y', '')}\n"
                f"介绍：{row.get('description', '')}"
            )
            entries.append(
                KnowledgeEntry(
                    id=f"spot_{row.get('id')}",
                    text=text,
                    source="data/scenic_spots.csv",
                    category="scenic_spot",
                    title=row.get("name", "景点"),
                )
            )
    return entries


def load_raw_document_entries() -> list[KnowledgeEntry]:
    raw_dir = DATA_DIR / "raw_documents"
    if not raw_dir.exists():
        return []
    entries: list[KnowledgeEntry] = []
    for path in sorted(raw_dir.glob("*")):
        if path.suffix.lower() not in {".md", ".txt"}:
            continue
        content = path.read_text(encoding="utf-8", errors="ignore")
        for index, chunk in enumerate(chunk_text(content), start=1):
            entries.append(
                KnowledgeEntry(
                    id=f"doc_{path.stem}_{index}",
                    text=chunk,
                    source=f"data/raw_documents/{path.name}",
                    category="guide_document",
                    title=f"{path.stem}#{index}",
                )
            )
    return entries


def xml_text(path: Path, member: str) -> str:
    with zipfile.ZipFile(path) as archive:
        if member not in archive.namelist():
            return ""
        xml = archive.read(member)
    root = ElementTree.fromstring(xml)
    return "\n".join(node.text or "" for node in root.iter() if node.text)


def extract_docx_text(path: Path) -> str:
    return xml_text(path, "word/document.xml")


def extract_xlsx_text(path: Path, max_cells: int = 2500) -> str:
    texts: list[str] = []
    collected = 0
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        shared_strings: list[str] = []
        if "xl/sharedStrings.xml" in names:
            root = ElementTree.fromstring(archive.read("xl/sharedStrings.xml"))
            shared_strings = ["".join(node.itertext()) for node in root]
        sheet_names = [name for name in names if name.startswith("xl/worksheets/sheet") and name.endswith(".xml")]
        for sheet_name in sheet_names:
            root = ElementTree.fromstring(archive.read(sheet_name))
            values = []
            for cell in root.iter():
                if collected >= max_cells:
                    break
                if not cell.tag.endswith("}c"):
                    continue
                cell_type = cell.attrib.get("t")
                value_node = next((child for child in cell if child.tag.endswith("}v")), None)
                if value_node is None or value_node.text is None:
                    inline_text = "".join(cell.itertext()).strip()
                    if inline_text:
                        values.append(inline_text)
                        collected += 1
                    continue
                if cell_type == "s" and shared_strings:
                    index = int(value_node.text)
                    if 0 <= index < len(shared_strings):
                        values.append(shared_strings[index])
                        collected += 1
                else:
                    if re.search(r"[\u4e00-\u9fffA-Za-z]", value_node.text):
                        values.append(value_node.text)
                        collected += 1
            if values:
                texts.append("\n".join(values))
    return "\n\n".join(texts)


def load_scenic_pack_entries() -> list[KnowledgeEntry]:
    pack_dir = ROOT_DIR / "灵山" / "示范景区公开资料包"
    if not pack_dir.exists():
        return []
    entries: list[KnowledgeEntry] = []
    for path in sorted(pack_dir.glob("*")):
        if path.suffix.lower() == ".docx":
            content = extract_docx_text(path)
        elif path.suffix.lower() == ".xlsx":
            content = extract_xlsx_text(path)
            category = "behavior_data"
        else:
            continue
        if path.suffix.lower() != ".xlsx":
            category = "scenic_pack"
        for index, chunk in enumerate(chunk_text(content, chunk_size=520, overlap=100), start=1):
            entries.append(
                KnowledgeEntry(
                    id=f"pack_{path.stem}_{index}",
                    text=chunk,
                    source=f"灵山/示范景区公开资料包/{path.name}",
                    category=category,
                    title=f"{path.stem}#{index}",
                )
            )
    return entries


def load_knowledge_entries() -> list[KnowledgeEntry]:
    return load_faq_entries() + load_spot_entries() + load_raw_document_entries() + load_scenic_pack_entries()


def build_knowledge_base(output_path: Path = VECTOR_STORE_PATH) -> dict:
    entries = load_knowledge_entries()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": 1,
        "dimension": VECTOR_DIMENSION,
        "entry_count": len(entries),
        "entries": [
            {
                "id": entry.id,
                "text": entry.text,
                "source": entry.source,
                "category": entry.category,
                "title": entry.title,
                "vector": vectorize(entry.text),
            }
            for entry in entries
        ],
    }
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"path": str(output_path), "entry_count": len(entries)}


def load_vector_store(path: Path = VECTOR_STORE_PATH) -> dict:
    if not path.exists():
        build_knowledge_base(path)
    return json.loads(path.read_text(encoding="utf-8"))


def retrieve_context(query: str, top_k: int = 5) -> list[dict]:
    store = load_vector_store()
    query_vector = vectorize(query)
    scored = []
    for entry in store.get("entries", []):
        score = cosine_similarity(query_vector, entry["vector"])
        if query and query in entry["text"]:
            score += 0.25
        scored.append((score, entry))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [
        {
            "chunk_id": entry["id"],
            "source": entry["source"],
            "category": entry["category"],
            "title": entry["title"],
            "text": entry["text"],
            "score": round(score, 4),
        }
        for score, entry in scored[:top_k]
        if score > 0
    ]
