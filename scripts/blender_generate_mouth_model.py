from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path


VISEMES = {
    "closed": {"width": 0.44, "opening": 0.012, "lip": 0.052, "roundness": 0.35},
    "mbp": {"width": 0.42, "opening": 0.006, "lip": 0.062, "roundness": 0.28},
    "aa": {"width": 0.46, "opening": 0.17, "lip": 0.065, "roundness": 0.62},
    "ee": {"width": 0.58, "opening": 0.06, "lip": 0.048, "roundness": 0.2},
    "oh": {"width": 0.36, "opening": 0.18, "lip": 0.07, "roundness": 0.82},
    "round": {"width": 0.28, "opening": 0.12, "lip": 0.075, "roundness": 1.0},
    "fv": {"width": 0.48, "opening": 0.055, "lip": 0.05, "roundness": 0.24},
    "smile": {"width": 0.56, "opening": 0.05, "lip": 0.052, "roundness": 0.18},
}


def parse_args() -> argparse.Namespace:
    passthrough = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    parser = argparse.ArgumentParser(description="Create a Blender GLB mouth model with viseme shape keys.")
    parser.add_argument("--output", type=Path, default=Path("frontend/public/avatar/mouth-3d/lingling-mouth.glb"))
    return parser.parse_args(passthrough)


def ring_points(spec: dict[str, float], inner: bool, segments: int) -> list[tuple[float, float, float]]:
    points: list[tuple[float, float, float]] = []
    width = spec["width"] if inner else spec["width"] + spec["lip"] * 2.0
    opening = max(0.01, spec["opening"] if inner else spec["opening"] + spec["lip"] * (1.2 + spec["roundness"]))
    for index in range(segments):
        theta = 2.0 * math.pi * index / segments
        horizontal = math.cos(theta)
        vertical = math.sin(theta)
        x = width * 0.5 * horizontal
        z = opening * 0.5 * vertical
        y = 0.018 * (1.0 - abs(vertical)) + (0.006 if inner else 0.022)
        if not inner:
            z += 0.012 * math.sin(theta * 2.0)
        points.append((x, y, z))
    return points


def pose_vertices(spec: dict[str, float], segments: int) -> list[tuple[float, float, float]]:
    return ring_points(spec, inner=False, segments=segments) + ring_points(spec, inner=True, segments=segments)


def build_faces(segments: int) -> list[tuple[int, int, int, int]]:
    faces: list[tuple[int, int, int, int]] = []
    for index in range(segments):
        outer_a = index
        outer_b = (index + 1) % segments
        inner_b = segments + ((index + 1) % segments)
        inner_a = segments + index
        faces.append((outer_a, outer_b, inner_b, inner_a))
    return faces


def main() -> int:
    import bpy

    args = parse_args()
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()

    segments = 64
    basis_name = "closed"
    mesh = bpy.data.meshes.new("LinglingMouthMesh")
    mesh.from_pydata(pose_vertices(VISEMES[basis_name], segments), [], build_faces(segments))
    mesh.update()

    obj = bpy.data.objects.new("Lingling_Mouth_Viseme_Model", mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    lip_material = bpy.data.materials.new("soft_lip")
    lip_material.diffuse_color = (0.78, 0.22, 0.31, 1.0)
    obj.data.materials.append(lip_material)

    obj.shape_key_add(name="Basis")
    for name, spec in VISEMES.items():
        key = obj.shape_key_add(name=name)
        for vertex, coordinate in zip(key.data, pose_vertices(spec, segments)):
            vertex.co = coordinate

    if obj.data.shape_keys:
        frame = 1
        for name in VISEMES:
            for key in obj.data.shape_keys.key_blocks:
                if key.name != "Basis":
                    key.value = 1.0 if key.name == name else 0.0
                    key.keyframe_insert("value", frame=frame)
            frame += 8
        bpy.context.scene.frame_start = 1
        bpy.context.scene.frame_end = frame

    bpy.ops.export_scene.gltf(
        filepath=str(output),
        export_format="GLB",
        export_morph=True,
        export_animations=True,
    )
    print(f"exported {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
