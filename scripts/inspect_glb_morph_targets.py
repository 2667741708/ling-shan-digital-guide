from __future__ import annotations

import argparse
import json
import struct
import sys
from pathlib import Path
from typing import Any


DEFAULT_REQUIRED_TARGETS = ("closed", "mbp", "aa", "ee", "oh", "round", "fv", "smile")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect GLB/glTF morph target names for the Lingling avatar.")
    parser.add_argument("model", type=Path, help="Path to a .glb or .gltf file.")
    parser.add_argument(
        "--required",
        nargs="*",
        default=list(DEFAULT_REQUIRED_TARGETS),
        help="Required morph target names. Defaults to the frontend viseme contract.",
    )
    parser.add_argument("--json", action="store_true", help="Print a machine-readable JSON summary.")
    return parser.parse_args()


def load_gltf_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    if path.suffix.lower() == ".gltf":
        return json.loads(path.read_text(encoding="utf-8"))
    if path.suffix.lower() != ".glb":
        raise ValueError(f"expected .glb or .gltf, got {path.suffix}")

    with path.open("rb") as file:
        header = file.read(12)
        if len(header) != 12:
            raise ValueError("file is too small to be a GLB")
        magic, version, total_length = struct.unpack("<4sII", header)
        if magic != b"glTF" or version != 2:
            raise ValueError("file is not a glTF 2.0 binary")
        if total_length != path.stat().st_size:
            raise ValueError("GLB header length does not match file size")

        chunk_header = file.read(8)
        if len(chunk_header) != 8:
            raise ValueError("GLB is missing the JSON chunk")
        chunk_length, chunk_type = struct.unpack("<II", chunk_header)
        if chunk_type != 0x4E4F534A:
            raise ValueError("first GLB chunk is not JSON")
        return json.loads(file.read(chunk_length).decode("utf-8"))


def collect_morph_targets(gltf: dict[str, Any]) -> dict[str, Any]:
    meshes = gltf.get("meshes", [])
    all_names: set[str] = set()
    mesh_summaries: list[dict[str, Any]] = []
    primitive_count = 0
    target_count = 0

    for mesh_index, mesh in enumerate(meshes):
        extras = mesh.get("extras", {}) if isinstance(mesh, dict) else {}
        mesh_names = list(extras.get("targetNames", []) or [])
        primitive_summaries: list[dict[str, Any]] = []
        for primitive_index, primitive in enumerate(mesh.get("primitives", []) or []):
            primitive_count += 1
            targets = primitive.get("targets", []) or []
            target_count += len(targets)
            primitive_names = mesh_names[: len(targets)]
            if not primitive_names:
                primitive_extras = primitive.get("extras", {}) if isinstance(primitive, dict) else {}
                primitive_names = list(primitive_extras.get("targetNames", []) or [])
            all_names.update(str(name) for name in primitive_names)
            primitive_summaries.append(
                {
                    "primitive": primitive_index,
                    "target_count": len(targets),
                    "target_names": primitive_names,
                }
            )
        mesh_summaries.append(
            {
                "mesh": mesh_index,
                "name": mesh.get("name", f"mesh_{mesh_index}"),
                "target_names": mesh_names,
                "primitives": primitive_summaries,
            }
        )

    return {
        "mesh_count": len(meshes),
        "primitive_count": primitive_count,
        "target_count": target_count,
        "morph_target_names": sorted(all_names),
        "meshes": mesh_summaries,
    }


def inspect_model(path: Path, required: list[str]) -> dict[str, Any]:
    gltf = load_gltf_json(path)
    summary = collect_morph_targets(gltf)
    names = set(summary["morph_target_names"])
    summary["path"] = str(path)
    summary["asset_version"] = gltf.get("asset", {}).get("version")
    summary["required"] = required
    summary["missing"] = [name for name in required if name not in names]
    summary["ok"] = not summary["missing"] and summary["mesh_count"] > 0 and summary["target_count"] >= len(required)
    return summary


def main() -> int:
    args = parse_args()
    try:
        summary = inspect_model(args.model, args.required)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(f"model: {summary['path']}")
        print(f"asset: glTF {summary.get('asset_version')}")
        print(f"meshes: {summary['mesh_count']} primitives: {summary['primitive_count']} targets: {summary['target_count']}")
        print("morph targets: " + ", ".join(summary["morph_target_names"]))
        if summary["missing"]:
            print("missing required targets: " + ", ".join(summary["missing"]), file=sys.stderr)

    return 0 if summary["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
