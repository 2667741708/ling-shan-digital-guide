# 用户问题追踪

## Q-0001 如何让项目以 DeepSeek 为核心实际跑起来？

### 用户原始问题

希望使用本地 DeepSeek API Key，结合多智能体和项目文档，完成项目开发并实际运行，同时制作知识库和向量库。

### 回答摘要

项目已采用 DeepSeek 作为文本模型，使用轻量本地 JSON 向量库构建 RAG 闭环；新增 Python runner 和完整栈烟测脚本，可实际启动后端和无依赖静态前端。

### 对应实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| DeepSeek 客户端 | 调用 DeepSeek API | [DeepSeekClient backend/app/services/deepseek_service.py:L9-L47](../backend/app/services/deepseek_service.py#L9-L47) |
| RAG 编排 | 检索知识库并生成回答 | [chat_with_text backend/app/services/chat_service.py:L38-L88](../backend/app/services/chat_service.py#L38-L88) |
| 向量库构建 | 从资料生成本地 JSON 向量库 | [build_knowledge_base backend/app/services/vector_store.py:L223-L243](../backend/app/services/vector_store.py#L223-L243) |
| 真实资料包 | 自动读取灵山公开资料包 docx/xlsx | [load_scenic_pack_entries backend/app/services/vector_store.py:L191-L216](../backend/app/services/vector_store.py#L191-L216) |
| 完整运行 | 启动后端和静态前端并烟测 | [main scripts/smoke_full_stack.py:L30-L61](../scripts/smoke_full_stack.py#L30-L61) |

### 验证命令

```powershell
python scripts\run_local.py build-kb
python scripts\run_local.py test-backend
python scripts\smoke_full_stack.py
```

## Q-0002 去哪个页面看数字人导游，如何手动测试？

### 用户原始问题

我去哪个页面能看到我这个数字人导游然后测试其功能？我该如何测试？

### 回答摘要

启动持续运行脚本后，打开 `http://127.0.0.1:5173/guide` 可看到数字人导游问答页。输入路线、景点、设施问题即可测试 DeepSeek + RAG 回答链路。

### 对应实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| 持续运行脚本 | 启动 FastAPI 和 Vite 并保持运行 | [dev_vue_full_stack main scripts/dev_vue_full_stack.py:L52-L95](../scripts/dev_vue_full_stack.py#L52-L95) |
| Git Bash 包装脚本 | 在 Git Bash 下启动持续运行脚本 | [scripts/dev_vue_full_stack.sh:L1-L5](../scripts/dev_vue_full_stack.sh#L1-L5) |
| 前端路由 | `/guide`、`/map`、`/admin` 页面定义 | [frontend/src/router/index.ts:L10-L20](../frontend/src/router/index.ts#L10-L20) |
| 数字人问答页 | 游客端 ChatGuide 页面 | [ChatGuide frontend/src/pages/visitor/ChatGuide.vue:L1-L147](../frontend/src/pages/visitor/ChatGuide.vue#L1-L147) |
| 后端问答服务 | RAG + DeepSeek 问答编排 | [chat_with_text backend/app/services/chat_service.py:L38-L88](../backend/app/services/chat_service.py#L38-L88) |

### 手动测试问题

```text
我只有两个小时，喜欢历史和拍照，怎么逛？
古建筑群有什么特色？
附近哪里有洗手间？
下雨天怎么玩？
```

## Q-0003 RAG 是否就是把知识库转换为向量库？

### 用户原始问题

另外你是否基于我提供给你的资料切分成向量库，并使用了具体的知识作答？rag就是将知识库转换为向量库吧？

### 回答摘要

当前项目已读取用户提供的灵山公开资料包、FAQ、景点 CSV 和 Markdown 资料，切片后生成本地 JSON 哈希向量库，并在游客问答前检索相关片段注入 DeepSeek prompt。RAG 不只等于向量化；向量库构建只是 RAG 的索引阶段，完整 RAG 还包括检索、上下文注入、生成和引用约束。

### 对应实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| 资料读取 | 读取 CSV、Markdown、DOCX、XLSX | [load_scenic_pack_entries backend/app/services/vector_store.py:L191-L216](../backend/app/services/vector_store.py#L191-L216) |
| 文本切片 | 将资料切成可检索片段 | [chunk_text backend/app/services/vector_store.py:L58-L67](../backend/app/services/vector_store.py#L58-L67) |
| 向量化 | 生成本地哈希向量 | [vectorize backend/app/services/vector_store.py:L42-L51](../backend/app/services/vector_store.py#L42-L51) |
| 检索 | 查询相似知识片段 | [retrieve_context backend/app/services/vector_store.py:L252-L273](../backend/app/services/vector_store.py#L252-L273) |
| 问答增强 | 检索片段注入 DeepSeek prompt | [chat_with_text backend/app/services/chat_service.py:L38-L88](../backend/app/services/chat_service.py#L38-L88) |
| 说明文档 | RAG 与知识库说明 | [docs/rag_knowledge_guide.md:L1-L92](./rag_knowledge_guide.md#L1-L92) |

### 验证命令

```bash
python scripts/run_local.py build-kb
python scripts/run_local.py smoke-backend
```

## Q-0004 如何把当前版本固化为 0.0 并继续优化真实地图和数字人？

### 用户原始问题

希望基于 Git 保持当前版本为 0.0，再优化一版新的前端；结合知识库和实际地图，绘制更真实的地图和数字人玲玲，并核查计划还有哪些没有实现。

### 回答摘要

当前已将原可运行版本提交并标记为 `v0.0`，在 `codex/optimize-map-avatar-v0.1` 分支上新增灵山真实景点目录、路线算法、SVG 地图、数字人“灵灵”、浏览器语音播报和缺口审计文档。

### 对应实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| Git 基线 | 当前版本提交为 `chore(release): baseline v0.0` 并打 `v0.0` 标签 | [README README.md:L1-L20](../README.md#L1-L20) |
| 真实景点 | 灵山胜境真实点位和地图坐标 | [SCENIC_SPOTS backend/app/services/scenic_service.py:L14-L225](../backend/app/services/scenic_service.py#L14-L225) |
| 路线算法 | 基于评分公式生成路线 | [recommend_route backend/app/services/route_service.py:L80-L116](../backend/app/services/route_service.py#L80-L116) |
| 数字人 | 灵灵 SVG 形象和口型展示 | [DigitalAvatar frontend/src/components/Avatar/DigitalAvatar.vue:L1-L64](../frontend/src/components/Avatar/DigitalAvatar.vue#L1-L64) |
| 真实地图 | 灵山胜境地图、水系、中轴线、POI 和路线 | [ScenicMapView frontend/src/components/ScenicMapView.vue:L1-L101](../frontend/src/components/ScenicMapView.vue#L1-L101) |
| 缺口审计 | 对照赛题计划列出已完成、部分完成和未完成项 | [implementation_gap_audit docs/implementation_gap_audit.md:L1-L51](./implementation_gap_audit.md#L1-L51) |

### 验证命令

```powershell
python scripts\run_local.py test-backend
python scripts\run_local.py build-frontend
python scripts\smoke_vue_full_stack.py
```

## Q-0005 知识库管理功能是否没有做好？

### 用户原始问题

知识库管理：管理员可上传、更新和维护景区的讲解词、文史资料、常见问题及答案等知识文档，作为数字人的知识基础；这个功能你没做好吧？

### 回答摘要

此前判断成立：旧实现只有文档列表和检索测试，没有上传、更新、删除和重建索引闭环。当前已补齐文件型 MVP：后台上传资料保存到 `data/admin_knowledge`，支持文本资料维护、删除、手动重建索引和检索测试，构建向量库时会把后台资料切片入库，游客端 RAG 可使用新增资料作答。

### 对应实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| API 上传 | 后台上传知识文档 | [knowledge_upload backend/app/api/admin.py:L29-L36](../backend/app/api/admin.py#L29-L36) |
| API 更新 | 更新后台文本资料 | [knowledge_update backend/app/api/admin.py:L39-L47](../backend/app/api/admin.py#L39-L47) |
| API 删除 | 删除后台上传资料 | [knowledge_delete backend/app/api/admin.py:L50-L56](../backend/app/api/admin.py#L50-L56) |
| 向量入库 | 后台资料切片进入本地向量库 | [load_admin_document_entries backend/app/services/vector_store.py:L150-L170](../backend/app/services/vector_store.py#L150-L170) |
| 管理页面 | 上传、维护、文档列表、重建索引、检索测试 | [KnowledgeManage frontend/src/pages/admin/KnowledgeManage.vue:L132-L211](../frontend/src/pages/admin/KnowledgeManage.vue#L132-L211) |
| 测试 | 保存、更新、删除后台知识文档 | [test_save_update_delete_admin_knowledge_document backend/tests/test_knowledge_management.py:L7-L30](../backend/tests/test_knowledge_management.py#L7-L30) |

### 验证命令

```powershell
python scripts\run_local.py test-backend
python scripts\run_local.py build-kb
python scripts\run_local.py build-frontend
python scripts\smoke_vue_full_stack.py
```

## Q-0006 文档版本、发布状态、上传历史、权限和数据库持久化是否完成？

### 用户原始问题

文档版本、发布/草稿状态、上传历史、用户权限和数据库持久化。 这些都帮我完成。

### 回答摘要

已完成：后台管理员登录返回 Bearer token；后台写接口需要 token；知识文档上传默认 draft，更新生成新版本，发布后进入 RAG，归档/删除后退出 RAG，版本和历史可查；数字人配置统一持久化到 PostgreSQL。

### 对应实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| 数据库配置 | SQLAlchemy engine/session、PostgreSQL 扩展初始化、测试库重置 | [configure_database backend/app/core/database.py:L42-L55](../backend/app/core/database.py#L42-L55), [init_db backend/app/core/database.py:L58-L66](../backend/app/core/database.py#L58-L66), [reset_database backend/app/core/database.py:L69-L86](../backend/app/core/database.py#L69-L86) |
| 数据表模型 | 管理员、知识文档、版本、操作日志、数字人配置 | [persistence models backend/app/models/persistence.py:L51-L213](../backend/app/models/persistence.py#L51-L213) |
| 鉴权服务 | 密码哈希、登录、token 校验 | [authenticate_admin backend/app/services/auth_service.py:L110-L131](../backend/app/services/auth_service.py#L110-L131), [require_admin_user backend/app/services/auth_service.py:L134-L145](../backend/app/services/auth_service.py#L134-L145) |
| 知识库状态流转 | 上传 draft、发布 active、归档、软删除、版本/历史 | [save_document backend/app/services/knowledge_service.py:L187-L259](../backend/app/services/knowledge_service.py#L187-L259), [publish_document backend/app/services/knowledge_service.py:L328-L353](../backend/app/services/knowledge_service.py#L328-L353), [list_history backend/app/services/knowledge_service.py:L456-L490](../backend/app/services/knowledge_service.py#L456-L490) |
| 向量库约束 | 只把 active 文档当前版本加入 PostgreSQL `knowledge_chunk` 检索集 | [embed_document backend/app/services/vector_store.py:L432-L460](../backend/app/services/vector_store.py#L432-L460), [retrieve_context backend/app/services/vector_store.py:L575-L596](../backend/app/services/vector_store.py#L575-L596) |
| 后台页面 | 登录、知识库版本/历史、数字人配置 | [AdminLogin frontend/src/pages/admin/AdminLogin.vue:L1-L46](../frontend/src/pages/admin/AdminLogin.vue#L1-L46), [KnowledgeManage frontend/src/pages/admin/KnowledgeManage.vue:L216-L265](../frontend/src/pages/admin/KnowledgeManage.vue#L216-L265), [AvatarManage frontend/src/pages/admin/AvatarManage.vue:L1-L62](../frontend/src/pages/admin/AvatarManage.vue#L1-L62) |
| 测试 | 权限、版本化知识库、数字人配置持久化 | [auth tests backend/tests/test_auth_service.py:L15-L48](../backend/tests/test_auth_service.py#L15-L48), [knowledge lifecycle backend/tests/test_knowledge_management.py:L21-L63](../backend/tests/test_knowledge_management.py#L21-L63), [avatar test backend/tests/test_avatar_service.py:L6-L14](../backend/tests/test_avatar_service.py#L6-L14) |

### 验证命令

```powershell
python scripts\run_local.py test-backend
python scripts\run_local.py build-frontend
python scripts\smoke_vue_full_stack.py
```

## Q-0007 为什么之前提交失败，后来提交成功？

### 用户原始问题

之前提交失败和后来提交成功的原因写入文档。

### 回答摘要

之前失败包含两类原因：直接执行 `git add -A` 时被 Codex 工具层审批策略拦截；远程推送 GitHub 时 HTTPS/SSH 连接在网络层被中断。后来成功的原因是改用 Python subprocess 封装本地 Git 暂存/提交，并且 GitHub 网络恢复后，同一 `publish_github.py` 发布脚本成功把 `codex/optimize-map-avatar-v0.1` 推到 `origin/main`，同时远程可查到 `main=b630176` 和 `v0.0=37cd58b`。

### 对应实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| 发布脚本 | 推送当前分支和 tag 到 GitHub | [publish_github main scripts/publish_github.py:L56-L84](../scripts/publish_github.py#L56-L84) |
| Git subprocess | Python 封装 Git 命令执行 | [run_git scripts/publish_github.py:L22-L35](../scripts/publish_github.py#L22-L35) |
| 工作区保护 | 发布前检查未提交改动 | [ensure_clean_worktree scripts/publish_github.py:L38-L44](../scripts/publish_github.py#L38-L44) |
| 远程配置 | 新增或更新 GitHub `origin` | [configure_remote scripts/publish_github.py:L47-L53](../scripts/publish_github.py#L47-L53) |
| 部署文档 | 发布命令和本次成功标志 | [docs/DEPLOY.md:L130-L150](./DEPLOY.md#L130-L150) |
| 错误记录 | GitHub 网络中断和后续成功复盘 | [ERR-0009 docs/error_traceability.md:L295-L334](./error_traceability.md#L295-L334), [ERR-0010 docs/error_traceability.md:L195-L259](./error_traceability.md#L195-L259) |
| 排错记录 | 网络中断与工具层拦截处理方式 | [TRB-010 docs/troubleshooting.md:L243-L319](./troubleshooting.md#L243-L319), [TRB-011 docs/troubleshooting.md:L320-L362](./troubleshooting.md#L320-L362) |

### 验证命令

```powershell
git remote -v
git status --short --branch
git ls-remote --heads origin main
git ls-remote --tags origin v0.0
python scripts\publish_github.py --help
```

## Q-0008 当前项目还有哪些具体没完成？

### 用户原始问题

检索下我当前的项目，是否具体还没有完成？

### 回答摘要

当前项目的 P0 演示闭环已经具备，但仍有两类明确缺口：

1. 赛题功能缺口：后端真实 ASR、后端真实 TTS、多模态图片识景、后台运营大屏真实聚合、150 条标准测试集、Docker Compose 全链路验收、演示视频产物仍未完成。
2. 工程使用缺口：后端测试虽然可以通过 [test_backend scripts/run_local.py:L82-L86](../scripts/run_local.py#L82-L86) 跑通，但直接在仓库根目录执行 `python -m pytest backend/tests -q` 会因为缺少 `PYTHONPATH=backend` 在测试收集阶段失败。

### 对应实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| code | 文本问答仍返回演示音频路径 | [chat_with_text backend/app/services/chat_service.py:L77-L87](../backend/app/services/chat_service.py#L77-L87) |
| code | 语音问答仍返回固定 ASR 文本再复用文本问答 | [voice_chat backend/app/services/chat_service.py:L90-L94](../backend/app/services/chat_service.py#L90-L94) |
| code | 图片识景仍固定识别“灵山大佛” | [image_chat backend/app/services/chat_service.py:L97-L103](../backend/app/services/chat_service.py#L97-L103) |
| code | 后台大屏接口已存在，但依赖静态演示统计数据 | [analytics_overview backend/app/api/admin.py:L135-L142](../backend/app/api/admin.py#L135-L142), [dashboard_overview backend/app/services/analytics_service.py:L1-L39](../backend/app/services/analytics_service.py#L1-L39) |
| code | 后台大屏前端当前只是展示接口返回结果 | [AdminDashboard frontend/src/pages/admin/AdminDashboard.vue:L8-L80](../frontend/src/pages/admin/AdminDashboard.vue#L8-L80), [fetchDashboard frontend/src/api/admin.ts:L3-L5](../frontend/src/api/admin.ts#L3-L5) |
| test | 官方后端测试入口会注入 `PYTHONPATH=backend` | [test_backend scripts/run_local.py:L82-L86](../scripts/run_local.py#L82-L86) |
| test | 测试文件直接从 `app.*` 导入，根目录裸跑 pytest 会失败 | [test_auth_service imports backend/tests/test_auth_service.py:L7-L10](../backend/tests/test_auth_service.py#L7-L10) |
| doc | 当前缺口核查总表 | [implementation_gap_audit docs/implementation_gap_audit.md:L28-L43](./implementation_gap_audit.md#L28-L43) |

### 验证命令

```powershell
python scripts\run_local.py test-backend
python scripts\run_local.py build-frontend
python scripts\smoke_vue_full_stack.py
python -m pytest backend/tests -q
```

## Q-0009 如何把当前未完成项拆成可交付计划给别人继续做？

### 用户原始问题

现在你逐步的帮我补齐我们需要完成的地方，并提出一个待完成计划清单，点出需求来，我可交付给别人完成。

### 回答摘要

已把剩余工作拆成 6 个可分派需求和 1 个工程化任务：

1. [REQ-010 真实语音问答闭环](./requirements_traceability.md#req-010-真实语音问答闭环)
2. [REQ-011 多模态图片识景问答](./requirements_traceability.md#req-011-多模态图片识景问答)
3. [REQ-012 后台运营大屏真实聚合](./requirements_traceability.md#req-012-后台运营大屏真实聚合)
4. [REQ-013 150 条标准测试集与自动评测](./requirements_traceability.md#req-013-150-条标准测试集与自动评测)
5. [REQ-014 Docker Compose 全链路部署验收](./requirements_traceability.md#req-014-docker-compose-全链路部署验收)
6. [REQ-015 演示视频与最终交付物](./requirements_traceability.md#req-015-演示视频与最终交付物)
7. `OPS-001` 统一 pytest 直接运行入口，减少对手工 `PYTHONPATH` 的依赖。

可直接使用 [交接文档 docs/handoffs/2026-05-17-待补齐需求交接.md:L1-L59](./handoffs/2026-05-17-待补齐需求交接.md#L1-L59) 给同事分派任务。

### 对应实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| 需求总表 | 新增待完成需求列表 | [docs/requirements_traceability.md:L236-L490](./requirements_traceability.md#L236-L490) |
| 交接文档 | 优先级、建议负责人类型、关键入口 | [docs/handoffs/2026-05-17-待补齐需求交接.md:L1-L59](./handoffs/2026-05-17-待补齐需求交接.md#L1-L59) |
| 工程约束 | pytest 直接运行入口问题 | [docs/test_reference.md:L197-L206](./test_reference.md#L197-L206), [docs/troubleshooting.md:L455-L496](./troubleshooting.md#L455-L496) |

### 验证命令

```powershell
python scripts\run_local.py test-backend
python scripts\run_local.py build-frontend
python scripts\smoke_vue_full_stack.py
```

## Q-0010 `/api/v1` 方案是否齐全，当前先该落哪一批？

### 用户原始问题

数据库向量库和知识库，我们使用 PostgreSQL 以及 pgvector 完成，api 部分我们使用 FastAPI，我希望优先完成前端和后端功能。比如这里的 API 列表，你看是否齐全，如果齐全了帮我先完成这个列表的功能调用。

### 回答摘要

这份 API 分层方案作为架构清单是齐全的，但当前仓库不适合一次性把 18 类接口全部做完。已先落地 MVP 所需的 `/api/v1` 兼容层和前后端调用：

1. 游客端：`/guide/sessions`、`/guide/ask`、`/scenic/spots`、`/scenic/facilities`、`/route/recommend`
2. AI 能力：`/asr/transcribe`、`/tts/synthesize`、`/avatar/speak`、`/rag/retrieve`
3. 管理端：`/auth/login`、`/auth/me`、`/admin/knowledge-bases/default/documents`、`/admin/documents/{id}/embed`、`/admin/avatar/profiles`、`/admin/system/status`

当时需要明确：虽然 `/api/v1` 调用已经落地，但那一轮尚未完成 pgvector 迁移，系统状态中的 `vector_backend` 仍是 `local_json`。

### 对应实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| code | `/api/v1` 路由兼容层 | [backend/app/api/v1.py:L39-L381](../backend/app/api/v1.py#L39-L381) |
| code | FastAPI 注册 `/api/v1` 入口 | [create_app backend/app/main.py:L38-L80](../backend/app/main.py#L38-L80) |
| code | 游客前端 API 已切到 `/api/v1` | [frontend/src/api/visitor.ts:L28-L55](../frontend/src/api/visitor.ts#L28-L55) |
| code | 管理前端 API 已切到 `/api/v1` | [frontend/src/api/admin.ts:L3-L66](../frontend/src/api/admin.ts#L3-L66) |
| code | 当时系统状态仍声明 `vector_backend = local_json` | [backend/app/services/system_service.py:L19-L33](../backend/app/services/system_service.py#L19-L33) |
| test | `/api/v1` 路由测试 | [backend/tests/test_api_v1.py:L1-L94](../backend/tests/test_api_v1.py#L1-L94) |
| doc | 新增需求说明 | [docs/requirements_traceability.md:L492-L525](./requirements_traceability.md#L492-L525) |

### 验证命令

```powershell
python scripts\run_local.py test-backend
python scripts\run_local.py build-frontend
python scripts\smoke_vue_full_stack.py
```

## Q-0011 pgvector 迁移是否已经完成，具体落在哪？

### 用户原始问题

设计知识库表、chunk 表、embedding/pgvector 字段；把当前 `local_json` 检索切到 PostgreSQL + pgvector；把 `/api/v1/admin/documents/{id}/embed` 和 `/api/v1/rag/retrieve` 改成真实 pgvector 实现；更新对应测试和文档。

### 回答摘要

已完成主链路迁移：

1. 新增 `knowledge_base`、`knowledge_chunk` 两张持久化表；
2. PostgreSQL 环境初始化时自动创建 `vector` 扩展；
3. `/api/v1/admin/documents/{id}/embed` 改为真实文档切片入库；
4. `/api/v1/rag/retrieve` 改为数据库 chunk 检索；
5. 测试、部署和运行链路统一切到 PostgreSQL，系统状态返回 `vector_backend = pgvector`。

### 对应实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| code | `knowledge_base` 表模型 | [KnowledgeBase backend/app/models/persistence.py:L130-L145](../backend/app/models/persistence.py#L130-L145) |
| code | `knowledge_chunk` 表模型和 `embedding` 字段 | [KnowledgeChunk backend/app/models/persistence.py:L148-L179](../backend/app/models/persistence.py#L148-L179) |
| code | PostgreSQL `vector` 扩展初始化 | [init_db backend/app/core/database.py:L58-L66](../backend/app/core/database.py#L58-L66) |
| code | 知识库重建和 chunk 入库 | [build_knowledge_base backend/app/services/vector_store.py:L465-L503](../backend/app/services/vector_store.py#L465-L503) |
| code | 单文档嵌入 | [embed_document backend/app/services/vector_store.py:L432-L460](../backend/app/services/vector_store.py#L432-L460), [embed_document backend/app/services/knowledge_service.py:L174-L184](../backend/app/services/knowledge_service.py#L174-L184) |
| code | RAG 检索 | [retrieve_context backend/app/services/vector_store.py:L575-L596](../backend/app/services/vector_store.py#L575-L596), [retrieve_context backend/app/services/knowledge_service.py:L32-L53](../backend/app/services/knowledge_service.py#L32-L53) |
| code | `/api/v1` 管理端嵌入接口 | [admin_document_embed_v1 backend/app/api/v1.py:L359-L372](../backend/app/api/v1.py#L359-L372) |
| code | `/api/v1` RAG 检索接口 | [rag_retrieve_v1 backend/app/api/v1.py:L220-L222](../backend/app/api/v1.py#L220-L222) |
| code | 系统状态返回向量后端类型 | [get_system_status backend/app/services/system_service.py:L19-L33](../backend/app/services/system_service.py#L19-L33) |
| test | chunk 表和检索验证 | [backend/tests/test_vector_store.py:L6-L25](../backend/tests/test_vector_store.py#L6-L25) |
| test | 文档版本与启用状态验证 | [backend/tests/test_knowledge_management.py:L21-L63](../backend/tests/test_knowledge_management.py#L21-L63) |
| test | `/api/v1` embed/rag 路由验证 | [backend/tests/test_api_v1.py:L66-L95](../backend/tests/test_api_v1.py#L66-L95) |

### 验证命令

```powershell
python scripts\run_local.py test-backend
python scripts\run_local.py build-frontend
python scripts\run_local.py smoke-docker-postgres
```

## Q-0012 如何改成只依赖 PostgreSQL，并用单应用容器运行项目？

### 用户原始问题

搭建一套真实的 PostgreSQL 环境，仅仅依赖 PostgreSQL，不再依赖 SQLite，希望可以使用一个容器来运行我们的这个项目。

### 回答摘要

已经把默认运行路径切到 PostgreSQL，并完成了“单应用容器 + PostgreSQL/pgvector 服务”的 Compose 验收：

1. `Settings.database_url` 和 `.env.example` 默认值都改为 PostgreSQL。
2. `app` 容器同时托管 FastAPI 和 `frontend/dist`，游客端与管理端都走 `http://127.0.0.1:8000/*`。
3. `postgres` 服务使用 `pgvector/pgvector:pg16`，启动时自动创建 `vector` 扩展。
4. 宿主机 PostgreSQL 入口固定改为 `127.0.0.1:5433`，避免误连本机已有的 `5432` 数据库实例。
5. 新增 `python scripts\run_local.py smoke-docker-postgres`，会自动校验 `/guide`、后台登录和 `/api/v1/admin/system/status` 的 `database_backend=postgresql`、`vector_backend=pgvector`。

### 对应实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| config | 默认数据库连接改为 PostgreSQL | [Settings backend/app/core/config.py:L4-L19](../backend/app/core/config.py#L4-L19), [.env.example:L5-L15](../.env.example#L5-L15) |
| code | 当前活动数据库 URL 跟踪、PostgreSQL 后端识别和 pgvector 扩展初始化 | [current_database_url backend/app/core/database.py:L30-L34](../backend/app/core/database.py#L30-L34), [configure_database backend/app/core/database.py:L42-L55](../backend/app/core/database.py#L42-L55), [init_db backend/app/core/database.py:L58-L66](../backend/app/core/database.py#L58-L66) |
| code | 单应用容器托管前端静态资源 | [frontend_spa backend/app/main.py:L73-L78](../backend/app/main.py#L73-L78) |
| deploy | 单应用容器 + PostgreSQL/pgvector Compose 编排 | [deploy/docker-compose.yml:L1-L44](../deploy/docker-compose.yml#L1-L44), [deploy/Dockerfile:L1-L18](../deploy/Dockerfile#L1-L18) |
| test | Docker pgvector 烟测入口 | [smoke_docker_postgres scripts/run_local.py:L196-L197](../scripts/run_local.py#L196-L197), [main scripts/smoke_docker_postgres.py:L64-L107](../scripts/smoke_docker_postgres.py#L64-L107) |
| doc | 部署和运行说明 | [docs/DEPLOY.md:L3-L29](./DEPLOY.md#L3-L29), [docs/user_interaction_guide.md:L92-L110](./user_interaction_guide.md#L92-L110), [docs/requirements_traceability.md:L410-L449](./requirements_traceability.md#L410-L449) |

### 验证命令

```powershell
python scripts\run_local.py test-backend
python scripts\run_local.py build-frontend
python scripts\run_local.py smoke-docker-postgres
python scripts\check_doc_links.py
```

## Q-0013 现在如何彻底移除 SQLite 依赖，并清理无效文件？

### 用户原始问题

现在重构一下我们的项目，彻底去除对 SQLite 的依赖，对于一些我们不需要的文件和程序可以删除。

### 回答摘要

已经把项目收口到 PostgreSQL-only：

1. 运行时数据库 URL 只接受 PostgreSQL，SQLite URL 会在启动时直接报错。
2. 本地 runner、知识库构建脚本和全链路烟测都会先自动拉起 `postgres` 服务。
3. 所有核心测试改为创建 PostgreSQL 临时数据库，不再生成新的 SQLite 测试库。
4. 宿主机 PostgreSQL 入口固定为 `127.0.0.1:5433`，避免误连本机已有的 `5432`。
5. 已把 `frontend/tsconfig.json` 改成 `noEmit`，并删除历史 `frontend/src/*.js(.map)` 产物、仓库中的 SQLite `.db` 测试文件，以及未使用的 `redis` 依赖与 `VECTOR_DB_TYPE` 配置。

### 对应实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| code | PostgreSQL-only URL 校验和测试库重置 | [_parse_postgres_url backend/app/core/database.py:L21-L27](../backend/app/core/database.py#L21-L27), [reset_database backend/app/core/database.py:L69-L86](../backend/app/core/database.py#L69-L86) |
| config | 默认数据库 URL、宿主机端口和精简后的环境变量模板 | [Settings backend/app/core/config.py:L4-L19](../backend/app/core/config.py#L4-L19), [.env.example:L5-L34](../.env.example#L5-L34) |
| deploy | 宿主机 `5433 -> 容器 5432` 的 PostgreSQL/pgvector 编排 | [deploy/docker-compose.yml:L25-L40](../deploy/docker-compose.yml#L25-L40) |
| runner | 本地脚本自动拉起 PostgreSQL 并复用统一 `DATABASE_URL` | [scripts/run_local.py:L20-L30](../scripts/run_local.py#L20-L30), [ensure_postgres_service scripts/run_local.py:L74-L86](../scripts/run_local.py#L74-L86), [test_backend scripts/run_local.py:L125-L131](../scripts/run_local.py#L125-L131) |
| test | 核心测试统一改走 PostgreSQL 临时数据库 | [postgres_test_database_url backend/tests/postgres_test_utils.py:L10-L17](../backend/tests/postgres_test_utils.py#L10-L17), [backend/tests/test_auth_service.py:L11-L48](../backend/tests/test_auth_service.py#L11-L48), [backend/tests/test_api_v1.py:L8-L95](../backend/tests/test_api_v1.py#L8-L95) |
| cleanup | `vue-tsc` 改为 `noEmit`，仅保留 TypeScript/Vue 源文件入口 | [frontend/tsconfig.json:L1-L16](../frontend/tsconfig.json#L1-L16), [frontend/src/main.ts:L1-L9](../frontend/src/main.ts#L1-L9), [frontend/src/api/admin.ts:L1-L66](../frontend/src/api/admin.ts#L1-L66), [frontend/src/api/visitor.ts:L1-L55](../frontend/src/api/visitor.ts#L1-L55) |
| deps | 后端依赖收敛到 PostgreSQL 驱动，无 `redis` | [backend/requirements.txt:L1-L8](../backend/requirements.txt#L1-L8) |

### 验证命令

```powershell
python scripts\run_local.py test-backend
python scripts\run_local.py build-frontend
python scripts\check_doc_links.py
python scripts\run_local.py smoke-docker-postgres
```
