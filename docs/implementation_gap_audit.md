# 实现缺口核查

核查对象：用户提供的 A5 景区导览服务 AI 数字人系统工程设计说明书。  
核查版本：`v0.0` 基线之后的 `codex/optimize-map-avatar-v0.1` 优化分支。

## 1. 已完成或本轮增强

| 计划项 | 当前状态 | 实现依据 |
|---|---|---|
| 游客端可打开 | 已完成 | [Vue 路由 frontend/src/router/index.ts:L10-L20](../frontend/src/router/index.ts#L10-L20) |
| 数字人可显示 | 已增强 | [DigitalAvatar frontend/src/components/Avatar/DigitalAvatar.vue:L1-L64](../frontend/src/components/Avatar/DigitalAvatar.vue#L1-L64) |
| 文本问答 | 已完成 | [chat_with_text backend/app/services/chat_service.py:L38-L88](../backend/app/services/chat_service.py#L38-L88) |
| 浏览器语音输入 | 部分完成 | [handleListen frontend/src/pages/visitor/ChatGuide.vue:L74-L98](../frontend/src/pages/visitor/ChatGuide.vue#L74-L98) |
| 浏览器语音播报 | 部分完成 | [speakAnswer frontend/src/pages/visitor/ChatGuide.vue:L62-L72](../frontend/src/pages/visitor/ChatGuide.vue#L62-L72) |
| 口型动画 | 已完成 MVP | [simulateSpeaking frontend/src/store/avatar.ts:L16-L32](../frontend/src/store/avatar.ts#L16-L32) |
| 景区知识库问答 | 已完成 | [retrieve_context backend/app/services/vector_store.py:L252-L273](../backend/app/services/vector_store.py#L252-L273) |
| 用户提供资料入库 | 已完成 | [load_scenic_pack_entries backend/app/services/vector_store.py:L191-L216](../backend/app/services/vector_store.py#L191-L216) |
| 真实景区地图 | 本轮增强 | [ScenicMapView frontend/src/components/ScenicMapView.vue:L1-L101](../frontend/src/components/ScenicMapView.vue#L1-L101) |
| 个性化路线推荐 | 已增强 | [recommend_route backend/app/services/route_service.py:L80-L116](../backend/app/services/route_service.py#L80-L116) |
| 管理后台大屏 | 部分完成 | [AdminDashboard frontend/src/pages/admin/AdminDashboard.vue:L1-L75](../frontend/src/pages/admin/AdminDashboard.vue#L1-L75) |
| 可复现本地启动 | 已完成 | [dev_vue_full_stack main scripts/dev_vue_full_stack.py:L52-L95](../scripts/dev_vue_full_stack.py#L52-L95) |
| Vue 完整栈烟测 | 已完成 | [smoke_vue_full_stack main scripts/smoke_vue_full_stack.py:L67-L122](../scripts/smoke_vue_full_stack.py#L67-L122) |

## 2. 仍未完全实现

| 计划项 | 当前缺口 | 建议下一步 |
|---|---|---|
| 后端真实 ASR | 当前语音识别主要依赖浏览器 SpeechRecognition，后端 `/chat/voice` 仍是演示返回 | 在 [voice_chat backend/app/services/chat_service.py:L90-L94](../backend/app/services/chat_service.py#L90-L94) 接入 Whisper/FunASR 或云 ASR |
| 后端真实 TTS 音频文件 | 当前前端用浏览器 SpeechSynthesis，后端 `audio_url` 是演示路径 | 新增 TTS 服务并替换 [chat_with_text backend/app/services/chat_service.py:L82-L87](../backend/app/services/chat_service.py#L82-L87) |
| 多模态大模型图片识景 | `/chat/image` 仍是固定识别灵山大佛 | 在 [image_chat backend/app/services/chat_service.py:L97-L103](../backend/app/services/chat_service.py#L97-L103) 接入 Qwen-VL 或其他视觉模型 |
| 管理后台上传文档 | 当前后台能列出文档和检索测试，上传/重建索引页面未完成 | 在 [KnowledgeManage frontend/src/pages/admin/KnowledgeManage.vue:L1-L24](../frontend/src/pages/admin/KnowledgeManage.vue#L1-L24) 增加上传表单并调用新 API |
| 数字人配置持久化 | 当前配置接口存在，但前端配置页未保存 | 在 [AvatarManage frontend/src/pages/admin/AvatarManage.vue:L1-L24](../frontend/src/pages/admin/AvatarManage.vue#L1-L24) 增加保存动作 |
| PostgreSQL 持久化 | 当前核心演示使用内存数据和本地 JSON 向量库 | 按 [init_db scripts/init_db.sql:L1-L36](../scripts/init_db.sql#L1-L36) 接 SQLAlchemy/Alembic |
| 150 条准确率测试集 | 当前有基础测试，不足 150 条标准问答评测 | 扩充 [data/test_questions.csv:L1-L4](../data/test_questions.csv#L1-L4) 并增加评测脚本 |
| Docker Compose 全链路验证 | Compose 文件存在但本轮主要验证 Python runner | 验证 [deploy/docker-compose.yml:L1-L39](../deploy/docker-compose.yml#L1-L39) 并补充部署测试 |
| 7 分钟演示视频 | 文档有脚本方向，视频文件未生成 | 基于 [docs/user_interaction_guide.md:L1-L120](./user_interaction_guide.md#L1-L120) 录制 |

## 3. 赛题风险排序

1. 最高风险：真实多模态图片识景和后端 TTS/ASR 仍是部分实现。
2. 中风险：管理后台上传、配置保存、数据库持久化还需补齐。
3. 低风险：前端展示、RAG 问答、路线地图、本地运行和烟测已具备演示闭环。

## 4. 当前推荐演示路径

1. 启动系统：[dev_vue_full_stack main scripts/dev_vue_full_stack.py:L52-L95](../scripts/dev_vue_full_stack.py#L52-L95)。
2. 打开数字人导览页：[ChatGuide frontend/src/pages/visitor/ChatGuide.vue:L1-L147](../frontend/src/pages/visitor/ChatGuide.vue#L1-L147)。
3. 提问“我只有两个小时，喜欢历史和拍照，帮我推荐路线”。
4. 展示回答依据和路线卡片：[chat_with_text backend/app/services/chat_service.py:L38-L88](../backend/app/services/chat_service.py#L38-L88)。
5. 打开地图页展示真实点位和路线：[ScenicMap frontend/src/pages/visitor/ScenicMap.vue:L1-L62](../frontend/src/pages/visitor/ScenicMap.vue#L1-L62)。
6. 打开管理大屏展示运营指标：[AdminDashboard frontend/src/pages/admin/AdminDashboard.vue:L1-L75](../frontend/src/pages/admin/AdminDashboard.vue#L1-L75)。
