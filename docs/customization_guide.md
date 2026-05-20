# 定制化开发指南

## 数字人嘴型与 3D 模型资产

当前 `local-2d` 数字人先用高清 SVG mouth sprites 提升口型真实感；`realistic-3d` 已内置 MPFB/MakeHuman 基座 + 本地 Blender 精修的 `lingling-realistic.glb`，后续真人级资产仍可继续走单主体图生 3D 初模 + Blender shape keys + GLB morph targets。每次重做 3D 数字人前先看 [数字人形象示例](../数字人形象示例)：当前主资产以浅青古风汉服为准，导游制服和户外休闲服作为后续独立服装变体。

| 定制目标 | 修改位置 | 验证命令 |
|---|---|---|
| 调整 viseme 类型和文本到嘴型的映射 | [avatarLipSync frontend/src/store/avatarLipSync.ts:L1-L110](../frontend/src/store/avatarLipSync.ts#L1-L110) | `npm --prefix frontend run test:avatar` |
| 替换前端 mouth sprite 映射或 3D 回退逻辑 | [DigitalAvatar frontend/src/components/Avatar/DigitalAvatar.vue:L1-L156](../frontend/src/components/Avatar/DigitalAvatar.vue#L1-L156) | `python scripts\run_local.py build-frontend` |
| 接入或替换真实全身 GLB/VRM 数字人 | [AvatarRenderer frontend/src/components/Avatar/AvatarRenderer.vue:L1-L242](../frontend/src/components/Avatar/AvatarRenderer.vue#L1-L242), [models README frontend/public/avatar/models/README.md:L1-L48](../frontend/public/avatar/models/README.md#L1-L48) | `npm --prefix frontend run build` |
| 从独立资产包同步 3D 灵灵 | [lingling-avatar-manifest frontend/public/avatar/models/lingling-avatar-manifest.json:L1-L33](../frontend/public/avatar/models/lingling-avatar-manifest.json#L1-L33), `D:/文件/lingling-3d-avatar-assets/INTERFACE.md` | `powershell -ExecutionPolicy Bypass -File D:/文件/lingling-3d-avatar-assets/scripts/sync_to_lingtour.ps1` |
| 检查灵灵形象参考和设计优先级 | [models README frontend/public/avatar/models/README.md:L13-L37](../frontend/public/avatar/models/README.md#L13-L37), [数字人形象示例](../数字人形象示例) | 视觉确认主服装、发型、表情和口型方向 |
| 调整 realistic-3d 口型 morph target 映射 | [avatarRenderer frontend/src/store/avatarRenderer.ts:L1-L46](../frontend/src/store/avatarRenderer.ts#L1-L46) | `npm --prefix frontend run test:avatar` |
| 重新生成 SVG/OBJ/OpenSCAD 嘴型资产 | [generate_mouth_assets scripts/generate_mouth_assets.py:L11-L266](../scripts/generate_mouth_assets.py#L11-L266) | `python scripts\generate_mouth_assets.py` |
| 安装 Blender 后导出 GLB shape keys 模型 | [blender_generate_mouth_model.py scripts/blender_generate_mouth_model.py:L1-L113](../scripts/blender_generate_mouth_model.py#L1-L113) | `blender --background --python scripts\blender_generate_mouth_model.py -- --output frontend/public/avatar/mouth-3d/lingling-mouth.glb` |
| 重新生成全身灵灵 GLB 并检查口型 targets | [blender_generate_lingling_avatar scripts/blender_generate_lingling_avatar.py:L20-L662](../scripts/blender_generate_lingling_avatar.py#L20-L662), [inspect_glb_morph_targets scripts/inspect_glb_morph_targets.py:L11-L133](../scripts/inspect_glb_morph_targets.py#L11-L133) | `python scripts\inspect_glb_morph_targets.py frontend\public\avatar\models\lingling-realistic.glb` |

### 推荐流程

1. 先改 [generate_mouth_assets scripts/generate_mouth_assets.py:L24-L94](../scripts/generate_mouth_assets.py#L24-L94) 中的 viseme 参数或 SVG path。
2. 运行 `python scripts\generate_mouth_assets.py`，生成到 `frontend/public/avatar/mouth/` 和 `frontend/public/avatar/mouth-3d/`。
3. 如果只做 2D 展示，确认 [mouth manifest frontend/public/avatar/mouth/mouth-manifest.json:L1-L50](../frontend/public/avatar/mouth/mouth-manifest.json#L1-L50) 路径完整，并可打开 [mouth-preview frontend/public/avatar/mouth-preview.html:L1-L96](../frontend/public/avatar/mouth-preview.html#L1-L96) 查看全部嘴型。
4. 如果要上 3D，先按 [数字人形象示例](../数字人形象示例) 确认形象方向，再安装 Blender 后运行全身 GLB 导出命令，并用 `inspect_glb_morph_targets.py` 检查 GLB 的 morph targets。
5. 最后运行：

```powershell
npm --prefix frontend run test:avatar
python scripts\run_local.py build-frontend
python scripts\check_doc_links.py
```

### 风险说明

- OBJ 只能作为静态参考 pose，不携带连续口型动画。
- OpenSCAD 更适合参数化 CAD 阻塞，不适合最终真人嘴唇软体形变。
- 真实口型与语音完全一致需要音素级时间戳或音频能量/viseme 序列；当前 `local-2d` 是文本和浏览器 TTS 生命周期驱动的轻量兜底。
