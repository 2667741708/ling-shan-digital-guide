from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "frontend" / "public" / "avatar"


@dataclass(frozen=True)
class VisemeSpec:
    key: str
    title: str
    width: float
    opening: float
    lip: float
    roundness: float


VISEMES: tuple[VisemeSpec, ...] = (
    VisemeSpec("closed", "closed neutral lips", 0.44, 0.012, 0.052, 0.35),
    VisemeSpec("mbp", "pressed m/b/p lips", 0.42, 0.006, 0.062, 0.28),
    VisemeSpec("aa", "open aa/a mouth", 0.46, 0.17, 0.065, 0.62),
    VisemeSpec("ee", "wide ee/i mouth", 0.58, 0.06, 0.048, 0.2),
    VisemeSpec("oh", "oval oh/o mouth", 0.36, 0.18, 0.07, 0.82),
    VisemeSpec("round", "rounded u/w mouth", 0.28, 0.12, 0.075, 1.0),
    VisemeSpec("fv", "f/v lower-lip contact", 0.48, 0.055, 0.05, 0.24),
    VisemeSpec("smile", "soft smile vowel", 0.56, 0.05, 0.052, 0.18),
)


SVG_PATHS: dict[str, dict[str, str]] = {
    "closed": {
        "upper": "M86 132 C130 97 185 103 230 123 C246 130 266 130 282 123 C327 103 382 97 426 132 C370 156 319 161 256 150 C193 161 142 156 86 132 Z",
        "lower": "M92 134 C144 155 195 164 256 153 C317 164 368 155 420 134 C375 176 310 190 256 176 C202 190 137 176 92 134 Z",
        "opening": "M104 132 C154 143 202 148 256 144 C310 148 358 143 408 132 C360 145 307 153 256 150 C205 153 152 145 104 132 Z",
        "teeth": "",
        "accent": "M112 131 C164 145 206 148 256 145 C306 148 348 145 400 131",
    },
    "mbp": {
        "upper": "M88 134 C138 104 186 111 226 128 C246 136 266 136 286 128 C326 111 374 104 424 134 C365 156 314 162 256 154 C198 162 147 156 88 134 Z",
        "lower": "M94 136 C148 158 200 166 256 158 C312 166 364 158 418 136 C370 172 312 181 256 171 C200 181 142 172 94 136 Z",
        "opening": "M122 135 C172 142 211 145 256 143 C301 145 340 142 390 135 C338 146 302 150 256 148 C210 150 174 146 122 135 Z",
        "teeth": "",
        "accent": "M126 134 C172 143 212 146 256 144 C300 146 340 143 386 134",
    },
    "aa": {
        "upper": "M82 120 C132 78 188 84 229 111 C246 122 266 122 283 111 C324 84 380 78 430 120 C378 144 317 156 256 143 C195 156 134 144 82 120 Z",
        "lower": "M86 143 C132 201 195 222 256 211 C317 222 380 201 426 143 C370 178 318 190 256 182 C194 190 142 178 86 143 Z",
        "opening": "M118 130 C150 105 196 101 229 121 C247 132 266 132 283 121 C316 101 362 105 394 130 C374 181 319 204 256 194 C193 204 138 181 118 130 Z",
        "teeth": "M142 127 C176 118 218 125 256 132 C294 125 336 118 370 127 C355 139 317 148 256 144 C195 148 157 139 142 127 Z",
        "accent": "M104 126 C160 151 210 154 256 148 C302 154 352 151 408 126",
    },
    "ee": {
        "upper": "M70 130 C124 98 188 105 231 123 C248 130 264 130 281 123 C324 105 388 98 442 130 C376 151 318 157 256 146 C194 157 136 151 70 130 Z",
        "lower": "M78 140 C136 170 198 176 256 164 C314 176 376 170 434 140 C379 186 314 194 256 179 C198 194 133 186 78 140 Z",
        "opening": "M106 132 C157 125 207 129 256 135 C305 129 355 125 406 132 C365 157 312 167 256 159 C200 167 147 157 106 132 Z",
        "teeth": "M110 130 C160 124 210 129 256 135 C302 129 352 124 402 130 C365 149 312 157 256 151 C200 157 147 149 110 130 Z",
        "accent": "M100 134 C153 155 205 159 256 153 C307 159 359 155 412 134",
    },
    "oh": {
        "upper": "M134 114 C168 71 220 72 244 103 C251 111 261 111 268 103 C292 72 344 71 378 114 C342 135 305 141 256 134 C207 141 170 135 134 114 Z",
        "lower": "M128 145 C159 205 206 229 256 221 C306 229 353 205 384 145 C348 178 305 190 256 183 C207 190 164 178 128 145 Z",
        "opening": "M168 130 C174 83 226 65 256 98 C286 65 338 83 344 130 C338 190 288 212 256 181 C224 212 174 190 168 130 Z",
        "teeth": "",
        "accent": "M162 126 C185 150 219 158 256 151 C293 158 327 150 350 126",
    },
    "round": {
        "upper": "M160 118 C188 78 225 82 246 105 C252 111 260 111 266 105 C287 82 324 78 352 118 C324 138 292 146 256 139 C220 146 188 138 160 118 Z",
        "lower": "M154 144 C177 198 215 219 256 211 C297 219 335 198 358 144 C328 176 293 188 256 180 C219 188 184 176 154 144 Z",
        "opening": "M198 131 C198 92 231 75 256 101 C281 75 314 92 314 131 C314 175 281 196 256 171 C231 196 198 175 198 131 Z",
        "teeth": "",
        "accent": "M190 127 C208 148 231 155 256 151 C281 155 304 148 322 127",
    },
    "fv": {
        "upper": "M82 125 C133 89 190 96 231 118 C248 127 264 127 281 118 C322 96 379 89 430 125 C374 150 317 157 256 145 C195 157 138 150 82 125 Z",
        "lower": "M96 147 C148 181 203 187 256 173 C309 187 364 181 416 147 C370 191 312 201 256 184 C200 201 142 191 96 147 Z",
        "opening": "M114 130 C162 122 211 127 256 134 C301 127 350 122 398 130 C366 158 309 171 256 164 C203 171 146 158 114 130 Z",
        "teeth": "M128 122 C169 114 214 119 256 127 C298 119 343 114 384 122 L370 145 C326 151 292 153 256 150 C220 153 186 151 142 145 Z",
        "accent": "M124 146 C170 162 214 166 256 160 C298 166 342 162 388 146",
    },
    "smile": {
        "upper": "M70 126 C128 91 190 101 232 121 C249 129 263 129 280 121 C322 101 384 91 442 126 C376 146 317 152 256 142 C195 152 136 146 70 126 Z",
        "lower": "M82 139 C143 178 201 184 256 170 C311 184 369 178 430 139 C375 194 313 205 256 185 C199 205 137 194 82 139 Z",
        "opening": "M103 129 C155 127 207 133 256 140 C305 133 357 127 409 129 C368 163 312 176 256 166 C200 176 144 163 103 129 Z",
        "teeth": "M112 130 C161 127 210 132 256 139 C302 132 351 127 400 130 C361 151 309 160 256 154 C203 160 151 151 112 130 Z",
        "accent": "M92 136 C150 166 205 172 256 162 C307 172 362 166 420 136",
    },
}


def mouth_svg(spec: VisemeSpec) -> str:
    paths = SVG_PATHS[spec.key]
    teeth = (
        f'<path d="{paths["teeth"]}" fill="url(#tooth)" opacity="0.94"/>\n      '
        if paths["teeth"]
        else ""
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="512" viewBox="0 0 512 256" role="img" aria-label="{spec.title}">
  <defs>
    <linearGradient id="upperLip" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0" stop-color="#d86575"/>
      <stop offset="0.55" stop-color="#b73d52"/>
      <stop offset="1" stop-color="#7d2334"/>
    </linearGradient>
    <linearGradient id="lowerLip" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0" stop-color="#e9828a"/>
      <stop offset="0.62" stop-color="#c54b5c"/>
      <stop offset="1" stop-color="#87283a"/>
    </linearGradient>
    <radialGradient id="innerMouth" cx="50%" cy="48%" r="58%">
      <stop offset="0" stop-color="#221019"/>
      <stop offset="0.72" stop-color="#3a1622"/>
      <stop offset="1" stop-color="#12070c"/>
    </radialGradient>
    <linearGradient id="tooth" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#fff7ea"/>
      <stop offset="1" stop-color="#dfd3bf"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feDropShadow dx="0" dy="8" stdDeviation="8" flood-color="#39151f" flood-opacity="0.22"/>
    </filter>
  </defs>
  <g filter="url(#softShadow)">
    <path d="{paths["opening"]}" fill="url(#innerMouth)"/>
    {teeth}<path d="{paths["upper"]}" fill="url(#upperLip)"/>
    <path d="{paths["lower"]}" fill="url(#lowerLip)"/>
    <path d="{paths["accent"]}" fill="none" stroke="#f4a2a8" stroke-width="7" stroke-linecap="round" opacity="0.38"/>
    <path d="M112 118 C166 98 211 108 242 124" fill="none" stroke="#ffd0cc" stroke-width="8" stroke-linecap="round" opacity="0.34"/>
    <path d="M270 124 C302 108 346 98 400 118" fill="none" stroke="#ffd0cc" stroke-width="8" stroke-linecap="round" opacity="0.25"/>
  </g>
</svg>
'''


def ring_points(spec: VisemeSpec, inner: bool, segments: int) -> list[tuple[float, float, float]]:
    points: list[tuple[float, float, float]] = []
    width = spec.width if inner else spec.width + spec.lip * 2.0
    opening = max(0.01, spec.opening if inner else spec.opening + spec.lip * (1.2 + spec.roundness))
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


def obj_for_viseme(spec: VisemeSpec, segments: int = 64) -> str:
    outer = ring_points(spec, inner=False, segments=segments)
    inner = ring_points(spec, inner=True, segments=segments)
    lines = [
        f"# LingTour AI parametric mouth viseme: {spec.key}",
        "mtllib lingling-mouth.mtl",
        f"o viseme_{spec.key}",
        "usemtl lip",
    ]
    for point in outer + inner:
        lines.append(f"v {point[0]:.6f} {point[1]:.6f} {point[2]:.6f}")
    for index in range(segments):
        outer_a = index + 1
        outer_b = ((index + 1) % segments) + 1
        inner_b = segments + ((index + 1) % segments) + 1
        inner_a = segments + index + 1
        lines.append(f"f {outer_a} {outer_b} {inner_b} {inner_a}")
    if spec.opening > 0.025:
        lines.append("usemtl mouth_cavity")
        center_index = segments * 2 + 1
        lines.append("v 0.000000 -0.018000 0.000000")
        for index in range(segments):
            inner_a = segments + index + 1
            inner_b = segments + ((index + 1) % segments) + 1
            lines.append(f"f {center_index} {inner_a} {inner_b}")
    return "\n".join(lines) + "\n"


def scad_source() -> str:
    return """// LingTour AI parametric lip reference.
// OpenSCAD is useful for reproducible CAD-like blocking, while Blender shape
// keys are the recommended route for web lip-sync morph targets.
$fn = 64;

module lip_pose(width = 44, opening = 12, lip = 6) {
  difference() {
    scale([width / 2 + lip, lip * 0.55, opening / 2 + lip])
      sphere(r = 1);
    translate([0, -lip, 0])
      scale([max(width, 1) / 2, lip * 1.2, max(opening, 1) / 2])
        sphere(r = 1);
  }
}

lip_pose(width = 46, opening = 17, lip = 6.5);
"""


def write_assets(output: Path) -> None:
    mouth_dir = output / "mouth"
    model_dir = output / "mouth-3d"
    mouth_dir.mkdir(parents=True, exist_ok=True)
    model_dir.mkdir(parents=True, exist_ok=True)

    manifest: dict[str, object] = {
        "version": "local-2d-mouth-v1",
        "viewBox": "0 0 512 256",
        "visemes": {},
        "modelAssets": {
            "objDirectory": "/avatar/mouth-3d/",
            "blenderScript": "scripts/blender_generate_mouth_model.py",
        },
    }
    for spec in VISEMES:
        svg_file = mouth_dir / f"viseme-{spec.key}.svg"
        svg_file.write_text(mouth_svg(spec), encoding="utf-8")
        obj_file = model_dir / f"viseme-{spec.key}.obj"
        obj_file.write_text(obj_for_viseme(spec), encoding="utf-8")
        manifest["visemes"][spec.key] = {
            "title": spec.title,
            "svg": f"/avatar/mouth/viseme-{spec.key}.svg",
            "obj": f"/avatar/mouth-3d/viseme-{spec.key}.obj",
        }

    (mouth_dir / "mouth-manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    (model_dir / "lingling-mouth.mtl").write_text(
        "\n".join(
            [
                "newmtl lip",
                "Kd 0.78 0.22 0.31",
                "Ks 0.18 0.05 0.06",
                "Ns 18",
                "",
                "newmtl mouth_cavity",
                "Kd 0.08 0.02 0.035",
                "Ks 0.02 0.01 0.01",
                "Ns 4",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (model_dir / "lingling_mouth_parametric.scad").write_text(scad_source(), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate local-2d mouth SVGs and 3D OBJ reference poses.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Output directory, default frontend/public/avatar")
    args = parser.parse_args()

    write_assets(args.output)
    print(f"generated mouth assets under {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
