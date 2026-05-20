from __future__ import annotations

import argparse
import math
import shutil
import sys
from pathlib import Path

try:
    import bpy
    from mathutils import Vector
except ModuleNotFoundError as exc:  # pragma: no cover - this runs inside Blender.
    raise SystemExit(
        "Run this script with Blender: blender --background --python "
        "scripts/blender_generate_lingling_avatar.py -- --output "
        "frontend/public/avatar/models/lingling-realistic.glb"
    ) from exc


VISEME_SPECS = {
    "closed": {"width": 0.17, "opening": 0.006, "roundness": 0.18, "lift": 0.0},
    "mbp": {"width": 0.16, "opening": 0.003, "roundness": 0.12, "lift": -0.002},
    "aa": {"width": 0.19, "opening": 0.09, "roundness": 0.52, "lift": -0.01},
    "ee": {"width": 0.24, "opening": 0.035, "roundness": 0.12, "lift": 0.012},
    "oh": {"width": 0.15, "opening": 0.085, "roundness": 0.82, "lift": -0.006},
    "round": {"width": 0.12, "opening": 0.064, "roundness": 1.0, "lift": -0.002},
    "fv": {"width": 0.2, "opening": 0.025, "roundness": 0.16, "lift": -0.006},
    "smile": {"width": 0.25, "opening": 0.022, "roundness": 0.08, "lift": 0.032},
}

REFERENCE_DESIGN_BRIEF = {
    "primary_reference_dir": "数字人形象示例",
    "primary_costume": "古风汉服：浅青绿真丝主面料、透纱宽袖、立领盘扣、花卉刺绣、山水刺绣、玉佩流苏。",
    "face_expression": "柔和年轻女导游气质，默认微笑；口型参考中性、微笑、大笑、说话、惊讶和欢迎表情。",
    "hair_accessory": "黑色高发髻、侧发丝、金色花簪、珍珠和流苏点缀。",
    "future_variants": "导游制服和户外休闲服作为后续可切换服装资产，不覆盖当前主汉服模型。",
}

MPFB_ASSET_NOTICE = (
    "MPFB 2.0.15 Blender extension, MakeHuman Community core base mesh/assets. "
    "MakeHuman/MPFB project documentation describes core graphical assets as CC0; "
    "the Blender add-on code itself is GPL-3.0-or-later."
)


def parse_args() -> argparse.Namespace:
    passthrough = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    parser = argparse.ArgumentParser(
        description="Generate the Lingling full-body guide avatar GLB with viseme morph targets.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("frontend/public/avatar/models/lingling-realistic.glb"),
        help="Final GLB path consumed by the frontend AvatarRenderer.",
    )
    parser.add_argument(
        "--source-output",
        type=Path,
        default=Path("frontend/public/avatar/models/source/lingling-ai-base.glb"),
        help="Traceable source copy for the generated local Blender base asset.",
    )
    parser.add_argument(
        "--mpfb-source-output",
        type=Path,
        default=Path("frontend/public/avatar/models/source/lingling-mpfb-base.glb"),
        help="Source GLB exported immediately after creating the MPFB/MakeHuman base mesh.",
    )
    parser.add_argument(
        "--base-model",
        choices=("mpfb", "procedural", "import"),
        default="mpfb",
        help="Avatar base route: MPFB/MakeHuman base, local procedural fallback, or imported GLB/OBJ.",
    )
    parser.add_argument(
        "--base-model-path",
        type=Path,
        default=None,
        help="External GLB/GLTF/OBJ base model path used when --base-model=import.",
    )
    parser.add_argument(
        "--reference-dir",
        type=Path,
        default=Path(REFERENCE_DESIGN_BRIEF["primary_reference_dir"]),
        help="Directory containing the five Lingling design reference PNGs used for visual matching.",
    )
    return parser.parse_args(passthrough)


def reference_image_names(reference_dir: Path) -> list[str]:
    """Return design-board filenames used to guide this generated asset.

    The images are not texture inputs. They are an auditable local design
    reference for REQ-006 so future agents keep the same clothing, hair,
    expression, and viseme direction when rebuilding the GLB.
    """

    if not reference_dir.exists():
        return []
    return sorted(path.name for path in reference_dir.glob("*.png"))


def apply_reference_metadata(reference_dir: Path) -> None:
    """Attach reference provenance and visual brief to the exported scene."""

    names = reference_image_names(reference_dir)
    bpy.context.scene["lingling_reference_dir"] = str(reference_dir)
    bpy.context.scene["lingling_reference_images"] = "; ".join(names)
    bpy.context.scene["lingling_design_brief"] = " | ".join(
        f"{key}: {value}" for key, value in REFERENCE_DESIGN_BRIEF.items()
    )


def apply_asset_metadata(base_model: str, base_model_path: Path | None = None) -> None:
    """Attach source model and license provenance to the exported GLB extras."""

    bpy.context.scene["lingling_base_model"] = base_model
    if base_model_path:
        bpy.context.scene["lingling_base_model_path"] = str(base_model_path)
    if base_model == "mpfb":
        bpy.context.scene["lingling_asset_license_note"] = MPFB_ASSET_NOTICE


def make_material(
    name: str,
    color: tuple[float, float, float, float],
    roughness: float = 0.72,
    metallic: float = 0.0,
) -> bpy.types.Material:
    material = bpy.data.materials.new(name)
    material.diffuse_color = color
    material.use_nodes = True
    material.use_backface_culling = False
    material.blend_method = "BLEND" if color[3] < 1 else "OPAQUE"
    principled = material.node_tree.nodes.get("Principled BSDF")
    if principled:
        if "Base Color" in principled.inputs:
            principled.inputs["Base Color"].default_value = color
        if "Alpha" in principled.inputs:
            principled.inputs["Alpha"].default_value = color[3]
        if "Roughness" in principled.inputs:
            principled.inputs["Roughness"].default_value = roughness
        if "Metallic" in principled.inputs:
            principled.inputs["Metallic"].default_value = metallic
    return material


def assign_material(obj: bpy.types.Object, material: bpy.types.Material) -> bpy.types.Object:
    obj.data.materials.append(material)
    try:
        bpy.ops.object.select_all(action="DESELECT")
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        bpy.ops.object.shade_smooth()
    except RuntimeError:
        pass
    return obj


def add_uv_sphere(
    name: str,
    location: tuple[float, float, float],
    scale: tuple[float, float, float],
    material: bpy.types.Material,
    segments: int = 48,
    rings: int = 24,
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    return assign_material(obj, material)


def add_cone(
    name: str,
    location: tuple[float, float, float],
    radius1: float,
    radius2: float,
    depth: float,
    material: bpy.types.Material,
    vertices: int = 96,
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=radius1, radius2=radius2, depth=depth, location=location)
    obj = bpy.context.object
    obj.name = name
    return assign_material(obj, material)


def add_cylinder_between(
    name: str,
    start: tuple[float, float, float],
    end: tuple[float, float, float],
    radius: float,
    material: bpy.types.Material,
    vertices: int = 32,
) -> bpy.types.Object:
    start_vec = Vector(start)
    end_vec = Vector(end)
    delta = end_vec - start_vec
    midpoint = start_vec + delta * 0.5
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=delta.length, location=midpoint)
    obj = bpy.context.object
    obj.name = name
    obj.rotation_euler = delta.to_track_quat("Z", "Y").to_euler()
    return assign_material(obj, material)


def add_curve(
    name: str,
    points: list[tuple[float, float, float]],
    material: bpy.types.Material,
    bevel_depth: float = 0.01,
) -> bpy.types.Object:
    curve = bpy.data.curves.new(name, "CURVE")
    curve.dimensions = "3D"
    curve.resolution_u = 16
    curve.bevel_depth = bevel_depth
    curve.bevel_resolution = 4
    spline = curve.splines.new("POLY")
    spline.points.add(len(points) - 1)
    for point, coordinate in zip(spline.points, points):
        point.co = (coordinate[0], coordinate[1], coordinate[2], 1.0)
    obj = bpy.data.objects.new(name, curve)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(material)
    return obj


def add_torus(
    name: str,
    location: tuple[float, float, float],
    material: bpy.types.Material,
    major_radius: float = 0.055,
    minor_radius: float = 0.006,
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_torus_add(
        major_radius=major_radius,
        minor_radius=minor_radius,
        major_segments=48,
        minor_segments=12,
        location=location,
    )
    obj = bpy.context.object
    obj.name = name
    obj.rotation_euler[0] = math.radians(90)
    return assign_material(obj, material)


def add_flat_panel(
    name: str,
    vertices: list[tuple[float, float, float]],
    material: bpy.types.Material,
) -> bpy.types.Object:
    mesh = bpy.data.meshes.new(f"{name}Mesh")
    mesh.from_pydata(vertices, [], [(0, 1, 2, 3)])
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return assign_material(obj, material)


def scene_mesh_bounds(objects: list[bpy.types.Object]) -> tuple[Vector, Vector]:
    """Return world-space min/max bounds for mesh objects."""

    min_corner = Vector((float("inf"), float("inf"), float("inf")))
    max_corner = Vector((float("-inf"), float("-inf"), float("-inf")))
    for obj in objects:
        if obj.type != "MESH":
            continue
        for corner in obj.bound_box:
            world = obj.matrix_world @ Vector(corner)
            min_corner.x = min(min_corner.x, world.x)
            min_corner.y = min(min_corner.y, world.y)
            min_corner.z = min(min_corner.z, world.z)
            max_corner.x = max(max_corner.x, world.x)
            max_corner.y = max(max_corner.y, world.y)
            max_corner.z = max(max_corner.z, world.z)
    return min_corner, max_corner


def fit_objects_to_lingling_stage(objects: list[bpy.types.Object], target_height: float = 3.02) -> None:
    """Scale and center imported base meshes into the existing Lingling stage."""

    mesh_objects = [obj for obj in objects if obj.type == "MESH"]
    if not mesh_objects:
        return
    min_corner, max_corner = scene_mesh_bounds(mesh_objects)
    height = max_corner.z - min_corner.z
    if height <= 0:
        return
    scale = target_height / height
    center_x = (min_corner.x + max_corner.x) * 0.5
    center_y = (min_corner.y + max_corner.y) * 0.5
    for obj in mesh_objects:
        obj.location.x = (obj.location.x - center_x) * scale
        obj.location.y = (obj.location.y - center_y) * scale
        obj.location.z = (obj.location.z - min_corner.z) * scale
        obj.scale = (obj.scale.x * scale, obj.scale.y * scale, obj.scale.z * scale)


def apply_object_transform(obj: bpy.types.Object) -> None:
    """Bake the current object transform so vertex edits operate in stage coordinates."""

    bpy.ops.object.select_all(action="DESELECT")
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)


def remove_existing_shape_keys(obj: bpy.types.Object) -> None:
    """Remove inherited base mesh shape keys so only project visemes are exported."""

    if not obj.data.shape_keys:
        return
    bpy.ops.object.select_all(action="DESELECT")
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.shape_key_remove(all=True)


def soften_mpfb_t_pose(obj: bpy.types.Object) -> None:
    """Fold MPFB's default T-pose arms closer to a front-facing guide stance."""

    for vertex in obj.data.vertices:
        x = vertex.co.x
        z = vertex.co.z
        abs_x = abs(x)
        if abs_x <= 0.36 or not 1.05 <= z <= 2.18:
            continue

        side = 1 if x > 0 else -1
        arm_factor = min(1.0, (abs_x - 0.36) / 0.62)
        vertical_factor = max(0.0, min(1.0, (2.12 - z) / 0.98))
        target_x = side * (0.34 + 0.18 * arm_factor)
        target_z = z - (0.62 + 0.18 * vertical_factor) * arm_factor
        target_y = min(vertex.co.y, -0.22)
        vertex.co.x = x * 0.28 + target_x * 0.72
        vertex.co.z = z * 0.35 + target_z * 0.65
        vertex.co.y = vertex.co.y * 0.72 + target_y * 0.28

    obj.data.update()


def configure_mpfb_scene_defaults() -> None:
    """Set MPFB new-human scene properties for a young female Asian guide base."""

    scene = bpy.context.scene
    scene.MPFB_NH_add_phenotype = True
    scene.MPFB_NH_add_breast = True
    scene.MPFB_NH_phenotype_gender = "female"
    scene.MPFB_NH_phenotype_race = "asian"
    scene.MPFB_NH_phenotype_age = "young"
    scene.MPFB_NH_phenotype_weight = "minweight"
    scene.MPFB_NH_phenotype_muscle = "minmuscle"
    scene.MPFB_NH_phenotype_height = "average"
    scene.MPFB_NH_phenotype_proportions = "average"
    scene.MPFB_NH_phenotype_influence = 0.84
    scene.MPFB_NH_breast_influence = 0.08
    scene.MPFB_NH_scale_factor = "METER"
    scene.MPFB_NH_detailed_helpers = True
    scene.MPFB_NH_extra_vertex_groups = True
    scene.MPFB_NH_mask_helpers = True
    scene.MPFB_NH_preselect_group = "body"


def create_mpfb_base(skin_material: bpy.types.Material) -> bpy.types.Object:
    """Create a MakeHuman/MPFB base mesh using the installed Blender extension."""

    if not hasattr(bpy.ops, "mpfb") or not hasattr(bpy.ops.mpfb, "create_human"):
        raise RuntimeError(
            "MPFB is not available. Install it with: blender --online-mode "
            "--command extension install -s -e mpfb"
        )
    before = set(bpy.data.objects)
    configure_mpfb_scene_defaults()
    bpy.ops.mpfb.create_human()
    created = [obj for obj in bpy.data.objects if obj not in before and obj.type == "MESH"]
    basemesh = bpy.data.objects.get("Human") or (created[0] if created else None)
    if basemesh is None:
        raise RuntimeError("MPFB did not create a human mesh.")
    basemesh.name = "Lingling_MPFB_CC0_Base"
    fit_objects_to_lingling_stage([basemesh], target_height=3.02)
    apply_object_transform(basemesh)
    remove_existing_shape_keys(basemesh)
    soften_mpfb_t_pose(basemesh)
    assign_material(basemesh, skin_material)
    basemesh["lingling_source"] = "MPFB/MakeHuman core CC0 base mesh"
    return basemesh


def import_base_model(path: Path) -> list[bpy.types.Object]:
    """Import an external base model and fit it to the Lingling stage."""

    if not path.exists():
        raise FileNotFoundError(f"Base model does not exist: {path}")
    before = set(bpy.data.objects)
    suffix = path.suffix.lower()
    if suffix in {".glb", ".gltf"}:
        bpy.ops.import_scene.gltf(filepath=str(path.resolve()))
    elif suffix == ".obj":
        if hasattr(bpy.ops.wm, "obj_import"):
            bpy.ops.wm.obj_import(filepath=str(path.resolve()))
        else:
            bpy.ops.import_scene.obj(filepath=str(path.resolve()))
    else:
        raise ValueError("Only GLB, GLTF and OBJ base models are supported.")
    created = [obj for obj in bpy.data.objects if obj not in before]
    fit_objects_to_lingling_stage(created, target_height=3.02)
    for obj in created:
        obj["lingling_source"] = str(path)
    return created


def mouth_vertices(spec: dict[str, float], segments: int = 72) -> list[tuple[float, float, float]]:
    vertices: list[tuple[float, float, float]] = []
    for outer in (True, False):
        lip = 0.028 if outer else 0.0
        width = spec["width"] + lip
        opening = max(0.002, spec["opening"] + lip * (0.8 + spec["roundness"]))
        for index in range(segments):
            theta = 2.0 * math.pi * index / segments
            x = math.cos(theta) * width * 0.5
            z = 2.39 + math.sin(theta) * opening * 0.5 + spec["lift"] * (abs(math.cos(theta)) ** 3)
            y = -0.522 - 0.004 * (1.0 - abs(math.sin(theta)))
            vertices.append((x, y, z))
    return vertices


def add_mouth(material: bpy.types.Material) -> bpy.types.Object:
    segments = 72
    faces: list[tuple[int, int, int, int]] = []
    for index in range(segments):
        outer_a = index
        outer_b = (index + 1) % segments
        inner_b = segments + ((index + 1) % segments)
        inner_a = segments + index
        faces.append((outer_a, inner_a, inner_b, outer_b))

    mesh = bpy.data.meshes.new("LinglingMouthMesh")
    mesh.from_pydata(mouth_vertices(VISEME_SPECS["closed"], segments), [], faces)
    mesh.update()
    obj = bpy.data.objects.new("Lingling_Mouth_Viseme_Targets", mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(material)

    obj.shape_key_add(name="Basis")
    for name, spec in VISEME_SPECS.items():
        key = obj.shape_key_add(name=name)
        for vertex, coordinate in zip(key.data, mouth_vertices(spec, segments)):
            vertex.co = coordinate

    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    try:
        bpy.ops.object.shade_smooth()
    except RuntimeError:
        pass

    return obj


def add_floral_motif(
    center_x: float,
    center_y: float,
    center_z: float,
    petal_material: bpy.types.Material,
    stem_material: bpy.types.Material,
) -> None:
    add_curve(
        f"Embroidery_Stem_{center_x:.2f}_{center_z:.2f}",
        [(center_x, center_y, center_z - 0.12), (center_x + 0.015, center_y - 0.005, center_z - 0.03), (center_x, center_y, center_z + 0.045)],
        stem_material,
        bevel_depth=0.004,
    )
    for index in range(5):
        theta = 2.0 * math.pi * index / 5.0
        add_uv_sphere(
            f"Embroidery_Petal_{center_x:.2f}_{center_z:.2f}_{index}",
            (center_x + math.cos(theta) * 0.025, center_y - 0.012, center_z + math.sin(theta) * 0.018),
            (0.018, 0.004, 0.012),
            petal_material,
            segments=16,
            rings=8,
        )


def build_avatar(
    base_model: str = "mpfb",
    base_model_path: Path | None = None,
    mpfb_source_output: Path | None = None,
) -> list[bpy.types.Object]:
    skin = make_material("warm_porcelain_skin", (1.0, 0.84, 0.72, 1.0), roughness=0.6)
    blush = make_material("soft_blush", (0.96, 0.42, 0.42, 0.5), roughness=0.78)
    hair = make_material("black_satin_hair", (0.02, 0.025, 0.022, 1.0), roughness=0.42)
    eye = make_material("deep_brown_eye", (0.018, 0.012, 0.008, 1.0), roughness=0.35)
    white = make_material("eye_highlight", (1.0, 0.96, 0.9, 1.0), roughness=0.28)
    lip = make_material("natural_rose_lip", (0.72, 0.18, 0.25, 1.0), roughness=0.5)
    hanfu = make_material("mist_cyan_hanfu", (0.58, 0.82, 0.78, 1.0), roughness=0.74)
    hanfu_light = make_material("translucent_mint_sleeve", (0.72, 0.9, 0.86, 0.72), roughness=0.82)
    inner_robe = make_material("warm_ivory_inner_robe", (0.96, 0.9, 0.8, 1.0), roughness=0.78)
    sash = make_material("jade_sash", (0.18, 0.56, 0.49, 1.0), roughness=0.72)
    gold = make_material("antique_gold_hairpin", (0.98, 0.69, 0.24, 1.0), roughness=0.38, metallic=0.18)
    embroidery = make_material("pale_gold_embroidery", (0.98, 0.85, 0.54, 1.0), roughness=0.65)
    flower = make_material("white_flower_embroidery", (0.98, 0.96, 0.9, 1.0), roughness=0.7)
    mountain = make_material("blue_green_landscape_embroidery", (0.24, 0.55, 0.58, 1.0), roughness=0.7)

    objects: list[bpy.types.Object] = []
    procedural_base = base_model == "procedural"
    if base_model == "mpfb":
        objects.append(create_mpfb_base(skin))
        if mpfb_source_output:
            export_scene_glb(mpfb_source_output)
    elif base_model == "import":
        if not base_model_path:
            raise ValueError("--base-model-path is required when --base-model=import")
        objects.extend(import_base_model(base_model_path))
    elif not procedural_base:
        raise ValueError(f"Unsupported base model: {base_model}")

    objects.append(add_cone("Lingling_Long_Hanfu_Skirt", (0, 0, 0.83), 0.58, 0.31, 1.35, hanfu))
    objects.append(add_cone("Lingling_Upper_Hanfu", (0, -0.01, 1.55), 0.42, 0.25, 0.78, hanfu))
    objects.append(add_flat_panel("Lingling_Ivory_Inner_Robe", [(-0.18, -0.42, 1.9), (0.18, -0.42, 1.9), (0.26, -0.39, 0.78), (-0.26, -0.39, 0.78)], inner_robe))
    objects.append(add_cylinder_between("Lingling_Jade_Sash", (-0.42, -0.42, 1.25), (0.42, -0.42, 1.25), 0.035, sash, vertices=48))

    if procedural_base:
        add_cylinder_between("Lingling_Left_Arm", (-0.34, -0.03, 1.73), (-0.7, -0.2, 1.05), 0.055, skin)
        add_cylinder_between("Lingling_Right_Arm", (0.34, -0.03, 1.73), (0.7, -0.2, 1.05), 0.055, skin)
    add_cylinder_between("Lingling_Left_Wide_Sleeve", (-0.38, -0.02, 1.68), (-0.75, -0.18, 1.03), 0.12, hanfu_light, vertices=48)
    add_cylinder_between("Lingling_Right_Wide_Sleeve", (0.38, -0.02, 1.68), (0.75, -0.18, 1.03), 0.12, hanfu_light, vertices=48)
    if procedural_base:
        add_uv_sphere("Lingling_Left_Hand", (-0.73, -0.22, 0.98), (0.08, 0.035, 0.055), skin, 24, 12)
        add_uv_sphere("Lingling_Right_Hand", (0.73, -0.22, 0.98), (0.08, 0.035, 0.055), skin, 24, 12)
        add_uv_sphere("Lingling_Neck", (0, -0.03, 1.95), (0.13, 0.1, 0.18), skin, 32, 16)
        add_uv_sphere("Lingling_Head", (0, -0.08, 2.48), (0.3, 0.25, 0.39), skin, 64, 32)
    add_uv_sphere("Lingling_Hair_Crown", (0, -0.18, 2.74), (0.28, 0.12, 0.14), hair, 48, 16)
    add_uv_sphere("Lingling_Hair_Left_Wing", (-0.23, -0.18, 2.56), (0.055, 0.055, 0.24), hair, 32, 16)
    add_uv_sphere("Lingling_Hair_Right_Wing", (0.23, -0.18, 2.56), (0.055, 0.055, 0.24), hair, 32, 16)
    add_uv_sphere("Lingling_Hair_Front_Cap", (0, -0.29, 2.69), (0.25, 0.052, 0.095), hair, 48, 16)
    add_uv_sphere("Lingling_Hair_Back_Cap", (0, -0.04, 2.78), (0.31, 0.22, 0.18), hair, 64, 24)
    add_uv_sphere("Lingling_Hair_Top_Cover", (0, -0.03, 2.91), (0.22, 0.17, 0.12), hair, 48, 16)
    add_uv_sphere("Lingling_Top_Bun", (0, 0.0, 3.02), (0.16, 0.135, 0.145), hair, 48, 16)
    add_uv_sphere("Lingling_Left_Side_Lock", (-0.27, -0.23, 2.36), (0.035, 0.03, 0.22), hair, 24, 16)
    add_uv_sphere("Lingling_Right_Side_Lock", (0.27, -0.23, 2.36), (0.035, 0.03, 0.22), hair, 24, 16)
    for strand_index, side in enumerate((-1, 1)):
        add_curve(
            f"Lingling_Face_Fringe_{strand_index}",
            [(0.05 * side, -0.35, 2.75), (0.11 * side, -0.39, 2.63), (0.18 * side, -0.38, 2.48)],
            hair,
            bevel_depth=0.006,
        )
        add_curve(
            f"Lingling_Wispy_Side_Hair_{strand_index}",
            [(0.24 * side, -0.34, 2.57), (0.31 * side, -0.38, 2.42), (0.28 * side, -0.36, 2.21)],
            hair,
            bevel_depth=0.005,
        )

    add_cylinder_between("Lingling_Gold_Hairpin_Main", (-0.24, -0.1, 3.05), (0.34, -0.08, 3.18), 0.012, gold, vertices=20)
    for bead_index, x in enumerate((-0.12, 0.02, 0.16)):
        add_uv_sphere(f"Lingling_Hairpin_Pearl_{bead_index}", (x, -0.13, 3.09 + bead_index * 0.025), (0.025, 0.025, 0.025), flower, 16, 8)
    for branch_index, side in enumerate((-1, 1)):
        add_curve(
            f"Lingling_Hairpin_Flower_Branch_{branch_index}",
            [(0.03 * side, -0.16, 3.08), (0.15 * side, -0.16, 3.14), (0.26 * side, -0.13, 3.13)],
            gold,
            bevel_depth=0.005,
        )
        add_floral_motif(0.22 * side, -0.155, 3.13, flower, gold)

    for x in (-0.12, 0.12):
        add_uv_sphere(f"Lingling_Eye_White_{x}", (x, -0.372, 2.55), (0.052, 0.01, 0.026), white, 24, 12)
        add_uv_sphere(f"Lingling_Iris_{x}", (x, -0.386, 2.548), (0.021, 0.006, 0.021), eye, 24, 12)
        add_uv_sphere(f"Lingling_Eye_Highlight_{x}", (x - 0.008, -0.392, 2.56), (0.007, 0.002, 0.007), white, 12, 6)
    add_curve("Lingling_Left_Upper_Eyelid", [(-0.18, -0.395, 2.57), (-0.12, -0.405, 2.59), (-0.06, -0.395, 2.57)], hair, bevel_depth=0.005)
    add_curve("Lingling_Right_Upper_Eyelid", [(0.06, -0.395, 2.57), (0.12, -0.405, 2.59), (0.18, -0.395, 2.57)], hair, bevel_depth=0.005)
    add_curve("Lingling_Left_Lower_Eyelid", [(-0.17, -0.396, 2.535), (-0.12, -0.402, 2.525), (-0.07, -0.396, 2.535)], blush, bevel_depth=0.003)
    add_curve("Lingling_Right_Lower_Eyelid", [(0.07, -0.396, 2.535), (0.12, -0.402, 2.525), (0.17, -0.396, 2.535)], blush, bevel_depth=0.003)
    add_curve("Lingling_Left_Brow", [(-0.19, -0.392, 2.66), (-0.12, -0.402, 2.69), (-0.04, -0.392, 2.675)], hair, bevel_depth=0.006)
    add_curve("Lingling_Right_Brow", [(0.04, -0.392, 2.675), (0.12, -0.402, 2.69), (0.19, -0.392, 2.66)], hair, bevel_depth=0.006)
    add_uv_sphere("Lingling_Left_Blush", (-0.19, -0.392, 2.43), (0.042, 0.005, 0.025), blush, 20, 8)
    add_uv_sphere("Lingling_Right_Blush", (0.19, -0.392, 2.43), (0.042, 0.005, 0.025), blush, 20, 8)
    add_curve("Lingling_Soft_Nose", [(0.0, -0.397, 2.53), (-0.018, -0.405, 2.48), (0.015, -0.407, 2.45)], skin, bevel_depth=0.006)
    add_mouth(lip)

    for motif in [(-0.18, -0.43, 1.55), (0.18, -0.43, 1.42), (0.0, -0.44, 1.02), (-0.28, -0.38, 0.72), (0.31, -0.38, 0.82)]:
        add_floral_motif(motif[0], motif[1], motif[2], flower, embroidery)

    add_curve("Lingling_Skirt_Mountain_Line_1", [(-0.33, -0.475, 0.68), (-0.21, -0.49, 0.81), (-0.1, -0.485, 0.73), (0.04, -0.49, 0.91), (0.18, -0.48, 0.72), (0.33, -0.47, 0.84)], mountain, bevel_depth=0.006)
    add_curve("Lingling_Skirt_Mountain_Line_2", [(-0.3, -0.478, 0.58), (-0.12, -0.49, 0.62), (0.05, -0.49, 0.59), (0.28, -0.475, 0.66)], mountain, bevel_depth=0.004)
    add_curve("Lingling_Skirt_Water_Line_1", [(-0.26, -0.482, 0.5), (-0.08, -0.49, 0.47), (0.12, -0.49, 0.51), (0.3, -0.482, 0.48)], mountain, bevel_depth=0.003)

    add_curve("Lingling_Collar_Left", [(-0.19, -0.43, 1.88), (-0.06, -0.46, 1.62), (0.0, -0.45, 1.28)], embroidery, bevel_depth=0.006)
    add_curve("Lingling_Collar_Right", [(0.19, -0.43, 1.88), (0.06, -0.46, 1.62), (0.0, -0.45, 1.28)], embroidery, bevel_depth=0.006)
    add_uv_sphere("Lingling_Jade_Button", (0, -0.47, 1.83), (0.035, 0.012, 0.035), sash, 24, 12)
    add_torus("Lingling_Jade_Waist_Ring", (0.0, -0.49, 1.12), sash, major_radius=0.055, minor_radius=0.007)
    add_cylinder_between("Lingling_Jade_Ring_Gold_Link", (0.0, -0.49, 1.18), (0.0, -0.49, 1.05), 0.006, gold, vertices=16)
    for offset in (-0.025, -0.012, 0.0, 0.012, 0.025):
        add_curve(
            f"Lingling_Jade_Tassel_{offset:.3f}",
            [(offset, -0.492, 1.04), (offset * 0.6, -0.5, 0.96), (offset * 0.35, -0.498, 0.88)],
            sash,
            bevel_depth=0.003,
        )

    return objects


def setup_scene() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    render_engines = {item.identifier for item in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items}
    bpy.context.scene.render.engine = "BLENDER_EEVEE_NEXT" if "BLENDER_EEVEE_NEXT" in render_engines else "BLENDER_EEVEE"
    bpy.context.scene.view_settings.view_transform = "Filmic"
    bpy.context.scene.view_settings.look = "Medium High Contrast"
    bpy.ops.object.light_add(type="AREA", location=(0, -3.6, 5.0))
    key = bpy.context.object
    key.name = "Lingling_Key_Light"
    key.data.energy = 520
    key.data.size = 4.2
    bpy.ops.object.camera_add(location=(0, -5.8, 2.45), rotation=(math.radians(73), 0, 0))
    bpy.context.scene.camera = bpy.context.object


def export_scene_glb(output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.export_scene.gltf(
        filepath=str(output.resolve()),
        export_format="GLB",
        export_morph=True,
        export_morph_normal=True,
        export_animations=False,
        export_materials="EXPORT",
        export_extras=True,
    )


def export_avatar(output: Path, source_output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    source_output.parent.mkdir(parents=True, exist_ok=True)
    export_scene_glb(output)
    if source_output.resolve() != output.resolve():
        shutil.copyfile(output, source_output)


def main() -> int:
    args = parse_args()
    setup_scene()
    apply_reference_metadata(args.reference_dir)
    apply_asset_metadata(args.base_model, args.base_model_path)
    build_avatar(args.base_model, args.base_model_path, args.mpfb_source_output)
    export_avatar(args.output, args.source_output)
    print(f"exported {args.output.resolve()}")
    print(f"source-copy {args.source_output.resolve()}")
    if args.base_model == "mpfb":
        print(f"mpfb-base {args.mpfb_source_output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
