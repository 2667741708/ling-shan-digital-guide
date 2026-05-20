# Realistic Lingling Avatar Model

The generated local Blender demonstration model is committed here:

```text
frontend/public/avatar/models/lingling-realistic.glb
```

The frontend `AvatarRenderer` loads this file first. If it is missing, WebGL is unavailable, or the file has no compatible mouth morph targets, the visitor guide falls back to the current `local-2d` avatar.

Current generated asset:

- Generator: `scripts/blender_generate_lingling_avatar.py`
- Source copy: `frontend/public/avatar/models/source/lingling-ai-base.glb`
- Reference folder: `数字人形象示例` with five PNG design boards for hanfu, guide uniform, outdoor outfit, expression, mouth, fabric, embroidery, jade pendant, and hairpin details.
- Mesh summary: `100` primitives, `8` morph targets.
- SHA-256: `E2A4B4F71D7EB6D9D5BEB090C41DE92C2C70BD3C61FAB9A36FD829740CE1A931`
- Required morph targets: `closed`, `mbp`, `aa`, `ee`, `oh`, `round`, `fv`, `smile`

Validation:

```powershell
python scripts\inspect_glb_morph_targets.py frontend\public\avatar\models\lingling-realistic.glb
```

This is a local procedural Blender asset for project demonstration. It approximates the reference image's black updo, hairpin, soft face, and light cyan hanfu, but it is not a mathematically exact reconstruction of the PNG.

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
