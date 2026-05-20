# Realistic Lingling Avatar Model

The generated local Blender demonstration model is committed here:

```text
frontend/public/avatar/models/lingling-realistic.glb
```

The frontend `AvatarRenderer` loads this file first. If it is missing, WebGL is unavailable, or the file has no compatible mouth morph targets, the visitor guide falls back to the current `local-2d` avatar.

The canonical maintainable copy is now split into the external package `D:/文件/lingling-3d-avatar-assets`. This app directory keeps the runtime copy only.

Current generated asset:

- Generator: `scripts/blender_generate_lingling_avatar.py`
- Base route: MPFB/MakeHuman generated human base plus local Blender skin material, softened arm pose, hanfu/accessory/viseme overlays.
- MPFB source base: `frontend/public/avatar/models/source/lingling-mpfb-base.glb`
- Source copy of final asset: `frontend/public/avatar/models/source/lingling-ai-base.glb`
- Runtime manifest: `frontend/public/avatar/models/lingling-avatar-manifest.json`
- Reference folder: `数字人形象示例` with five PNG design boards for hanfu, guide uniform, outdoor outfit, expression, mouth, fabric, embroidery, jade pendant, and hairpin details.
- Mesh summary: `97` primitives, `8` morph targets total; only the frontend-required viseme targets are exported.
- Final GLB size: `1,739,712` bytes.
- Final SHA-256: `6220D3B94F5EAD52E989DE69422C9DE54D2ECB0514ADDD47F6BEC7CD777BE9D3`
- MPFB base SHA-256: `A1A6303C77EAC2D1DD51B9E8BED65B268808A62D623D54F3D9709EFB36B74415`
- Required morph targets: `closed`, `mbp`, `aa`, `ee`, `oh`, `round`, `fv`, `smile`
- License note: MPFB add-on `2.0.15` is GPL-3.0-or-later code; MakeHuman/MPFB project documentation describes core graphical assets as CC0. No unverified third-party clothes, hair, or texture assets are bundled here.

Validation:

```powershell
python scripts\inspect_glb_morph_targets.py frontend\public\avatar\models\lingling-realistic.glb
```

This is a local MPFB/MakeHuman-based Blender asset for project demonstration. It improves the body and face base compared with the earlier fully procedural model, bakes a softer guide stance, then layers local scripted hanfu, hair, hairpin, jade pendant, embroidery, and mouth morph targets. It is not a mathematically exact reconstruction of the PNG.

Design priority from the local reference boards:

1. Primary shipped model: light cyan ancient-style hanfu with translucent wide sleeves, floral/gold embroidery, landscape skirt pattern, jade pendant tassel, black bun, and gold floral hairpin.
2. Mouth and expression target: neutral, smile, big smile, speaking, surprise, welcome, thinking, and apology expressions should remain visually compatible with the eight viseme morph target names.
3. Later variants: beige guide uniform and outdoor leisure outfit should be added as separate GLB/VRM assets or material/mesh variants instead of replacing the current hanfu model.

Image-to-3D replacement notes:

- Crop `C:/Users/hmw20/Downloads/数字人灵灵.png` to one clean subject before Hunyuan3D/Pixal3D inference; the current file is a design-board collage.
- Use `数字人形象示例` as the local style reference before accepting a generated replacement.
- Keep only authorized photos, meshes, textures, and voice references.
- Keep the browser delivery target below 25 MB unless the frontend is updated with compression/loading UX.
- Preserve the eight frontend viseme names above or update `frontend/src/store/avatarRenderer.ts` and `frontend/tests/avatarLipSync.test.ts`.
