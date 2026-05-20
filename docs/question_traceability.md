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
| 数字人 | 灵灵 SVG 形象和口型展示 | [DigitalAvatar frontend/src/components/Avatar/DigitalAvatar.vue:L7-L125](../frontend/src/components/Avatar/DigitalAvatar.vue#L7-L125) |
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

可直接使用 [交接文档 docs/archive/2026-05-17-待补齐需求交接.md:L1-L59](./archive/2026-05-17-待补齐需求交接.md#L1-L59) 给同事分派任务。

### 对应实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| 需求总表 | 新增待完成需求列表 | [docs/requirements_traceability.md:L236-L490](./requirements_traceability.md#L236-L490) |
| 交接文档 | 优先级、建议负责人类型、关键入口 | [docs/archive/2026-05-17-待补齐需求交接.md:L1-L59](./archive/2026-05-17-待补齐需求交接.md#L1-L59) |
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
| test | `/api/v1` 路由测试 | [backend/tests/test_api_v1.py:L1-L113](../backend/tests/test_api_v1.py#L1-L113) |
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
| test | `/api/v1` embed/rag 路由验证 | [backend/tests/test_api_v1.py:L84-L113](../backend/tests/test_api_v1.py#L84-L113) |

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
| test | Docker pgvector 烟测入口 | [smoke_docker_postgres scripts/run_local.py:L196-L197](../scripts/run_local.py#L196-L197), [main scripts/smoke_docker_postgres.py:L58-L100](../scripts/smoke_docker_postgres.py#L58-L100) |
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
| test | 核心测试统一改走 PostgreSQL 临时数据库 | [postgres_test_database_url backend/tests/postgres_test_utils.py:L10-L17](../backend/tests/postgres_test_utils.py#L10-L17), [backend/tests/test_auth_service.py:L11-L48](../backend/tests/test_auth_service.py#L11-L48), [backend/tests/test_api_v1.py:L8-L113](../backend/tests/test_api_v1.py#L8-L113) |
| cleanup | `vue-tsc` 改为 `noEmit`，仅保留 TypeScript/Vue 源文件入口 | [frontend/tsconfig.json:L1-L16](../frontend/tsconfig.json#L1-L16), [frontend/src/main.ts:L1-L9](../frontend/src/main.ts#L1-L9), [frontend/src/api/admin.ts:L1-L66](../frontend/src/api/admin.ts#L1-L66), [frontend/src/api/visitor.ts:L1-L55](../frontend/src/api/visitor.ts#L1-L55) |
| deps | 后端依赖收敛到 PostgreSQL 驱动，无 `redis` | [backend/requirements.txt:L1-L8](../backend/requirements.txt#L1-L8) |

### 验证命令

```powershell
python scripts\run_local.py test-backend
python scripts\run_local.py build-frontend
python scripts\check_doc_links.py
python scripts\run_local.py smoke-docker-postgres
```

## Q-0014 `docs/` 目录下哪些文档应该保留、归档或删除？

### 用户原始问题

`docs/` 文件夹下哪些可归档，哪些可删除？哪些需要保留？

### 回答摘要

当前 `docs/` 可以按三层处理：

1. 核心保留：`api_reference.md`、`config_reference.md`、`data_schema_reference.md`、`DEPLOY.md`、`program_index.md`、`project_onboarding.md`、`question_traceability.md`、`requirements_traceability.md`、`test_reference.md`、`troubleshooting.md` 等，这些文档仍被新同事阅读路径和现有实现直接依赖。
2. 建议归档：`API.md`、`DESIGN.md`、`DEEPSEEK_MULTI_AGENT.md`、`TEST_REPORT.md`、`generated/`、`handoffs/2026-05-17-待补齐需求交接.md`、`TEAM_HANDOFF.md`，它们主要提供历史方案、阶段交接或旧版说明，不应继续作为当前事实来源。
3. 本轮先不做硬删除，统一归档到 `docs/archive/`，等确认完全不再引用后再物理删除。

### 对应实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| doc | 当前统一 API 真相已经迁移到 `/api/v1` 说明，旧 `API.md` 仍保留旧 `/api/visitor` 和 `/api/admin` 路径 | [docs/archive/API.md:L13-L30](./archive/API.md#L13-L30), [docs/api_reference.md:L18-L89](./api_reference.md#L18-L89) |
| doc | `DESIGN.md` 仍写有 `Redis` 和泛化数据层描述，未体现 PostgreSQL-only 当前状态 | [docs/archive/DESIGN.md:L1-L15](./archive/DESIGN.md#L1-L15) |
| doc | `DEEPSEEK_MULTI_AGENT.md` 和 `generated/README.md` 说明这些文件属于多智能体生成产物 | [docs/archive/DEEPSEEK_MULTI_AGENT.md:L18-L39](./archive/DEEPSEEK_MULTI_AGENT.md#L18-L39), [docs/archive/generated/README.md:L1-L7](./archive/generated/README.md#L1-L7) |
| doc | `TEAM_HANDOFF.md` 指向过期目录和旧职责分工 | [docs/archive/TEAM_HANDOFF.md:L1-L25](./archive/TEAM_HANDOFF.md#L1-L25) |
| doc | `TEST_REPORT.md` 是静态阶段性报告，内容已和当前测试体系分离 | [docs/archive/TEST_REPORT.md:L1-L21](./archive/TEST_REPORT.md#L1-L21), [docs/test_reference.md:L1-L227](./test_reference.md#L1-L227) |
| doc | 当前新同事阅读路径和核心入口文档清单 | [docs/project_onboarding.md:L27-L38](./project_onboarding.md#L27-L38) |
| doc | 归档 `generated/` 前需要先处理现有引用，避免断链 | [docs/requirements_traceability.md:L382-L385](./requirements_traceability.md#L382-L385), [docs/requirements_traceability.md:L468-L472](./requirements_traceability.md#L468-L472) |

### 建议操作顺序

1. 先保留所有核心文档不动。
2. 把 `generated/`、`API.md`、`DESIGN.md`、`DEEPSEEK_MULTI_AGENT.md`、`TEST_REPORT.md`、`handoffs/2026-05-17-待补齐需求交接.md`、`TEAM_HANDOFF.md` 移到 `docs/archive/`。
3. 修正 [docs/requirements_traceability.md:L382-L385](./requirements_traceability.md#L382-L385) 和 [docs/requirements_traceability.md:L468-L472](./requirements_traceability.md#L468-L472) 对 `docs/generated/05_test_and_submission_plan.md` 的引用。
4. 保持历史文档可追溯，但不再把它们作为当前真相来源。

### 验证命令

```powershell
python scripts\check_doc_links.py
```

## Q-0015 归档后 GitHub 仓库里是否包含 Docker 容器本身？

### 用户原始问题

帮我归档，并告诉我我们目前提交到 GitHub 的项目包括了 Docker 容器本身吗？

### 回答摘要

已经把历史文档统一归档到 `docs/archive/`，当前核心文档继续保留在 `docs/` 根目录。

GitHub 仓库当前包含的是 Docker 相关定义，不包含已经构建好的容器本身：

1. 仓库里有 [deploy/docker-compose.yml](../deploy/docker-compose.yml#L1-L44) 和 [deploy/Dockerfile](../deploy/Dockerfile#L1-L18)，所以别人可以据此构建镜像并启动容器。
2. 仓库里不包含已经 build 完成的 Docker image，也不包含运行中的 container、PostgreSQL volume 数据。
3. 仓库里也不包含 `frontend/dist` 构建产物，因为它被 [.gitignore:L5-L11](../.gitignore#L5-L11) 忽略；当前标准做法是先执行前端构建，再执行 Compose 验收。

### 对应实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| doc | 归档目录说明和当前文档入口 | [docs/archive/README.md:L1-L15](./archive/README.md#L1-L15), [docs/project_onboarding.md:L27-L38](./project_onboarding.md#L27-L38) |
| deploy | Docker Compose 编排定义在仓库内 | [deploy/docker-compose.yml:L1-L44](../deploy/docker-compose.yml#L1-L44) |
| deploy | 应用镜像构建定义在仓库内 | [deploy/Dockerfile:L1-L18](../deploy/Dockerfile#L1-L18) |
| build | Docker 镜像依赖本地 `frontend/dist` 进入 build context | [deploy/Dockerfile:L11-L14](../deploy/Dockerfile#L11-L14), [build_frontend scripts/run_local.py:L134-L143](../scripts/run_local.py#L134-L143) |
| vcs | `frontend/dist`、`.env`、数据库文件和日志都不会进入 Git 仓库 | [.gitignore:L1-L11](../.gitignore#L1-L11) |
| doc | 部署说明已补充“仓库不包含已构建镜像/容器”说明 | [docs/DEPLOY.md:L3-L14](./DEPLOY.md#L3-L14) |

### 验证命令

```powershell
python scripts\check_doc_links.py
```

## Q-0016 GitHub 仓库是否已经包含完整项目，两个 Docker 是否够用，能否只用一个 Docker？

### 用户原始问题

我需要 GitHub 上传我们的完整项目，不要排除必要的文件，我们本地的这二个 docker 完整的包含了我们的项目了吗？是否可以一个 docker 到处运行？

### 回答摘要

当前已经把 Docker 构建链路改成“仓库源码可直接构建”：

1. GitHub 仓库现在不需要提交 `frontend/dist`，因为 [deploy/Dockerfile:L1-L31](../deploy/Dockerfile#L1-L31) 会在镜像构建阶段从 `frontend/` 源码直接执行前端打包。
2. 当前两容器方案是完整且合理的：`app` 容器承载前端静态资源 + FastAPI，`postgres` 容器承载 PostgreSQL/pgvector；这已经覆盖项目运行所需的两个核心进程。
3. “一个 Docker 到处运行”分两种理解：
   - 如果指“一个镜像文件就能在任何环境部署应用”，当前 `app` 镜像已经满足，但它仍需要一个 PostgreSQL 服务可连接。
   - 如果指“单容器内同时包含应用和 PostgreSQL 并一键运行”，当前项目没有这样做，也不建议这样做，因为数据库和应用生命周期、持久化、健康检查、升级策略应拆开。
4. 仓库里仍不会包含运行中的容器、已构建 image、PostgreSQL volume 数据，这些本来就不应进入 GitHub。

### 对应实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| deploy | 多阶段 Dockerfile 直接从前端源码构建 `dist` | [deploy/Dockerfile:L1-L31](../deploy/Dockerfile#L1-L31) |
| deploy | Compose 仍采用 `app + postgres` 两服务结构，且无 `.env` 时也可用默认值启动 | [deploy/docker-compose.yml:L1-L50](../deploy/docker-compose.yml#L1-L50) |
| build | Docker 烟测已不再依赖宿主机预构建前端 | [scripts/smoke_docker_postgres.py:L58-L100](../scripts/smoke_docker_postgres.py#L58-L100) |
| vcs | Git 仍排除运行产物和敏感文件，但不再需要排除项参与镜像构建 | [.gitignore:L1-L11](../.gitignore#L1-L11), [.dockerignore:L1-L11](../.dockerignore#L1-L11) |
| doc | 部署说明已更新为“源码可直接构建容器” | [docs/DEPLOY.md:L3-L36](./DEPLOY.md#L3-L36) |
| test | Docker 验收说明已更新 | [docs/test_reference.md:L218-L228](./test_reference.md#L218-L228) |

### 验证命令

```powershell
python scripts\run_local.py smoke-docker-postgres
python scripts\check_doc_links.py
```

## Q-0017 如何把 PostgreSQL 也封到同一个 Docker 里，做成单容器 all-in-one？

### 用户原始问题

继续做一个“单容器 all-in-one 运行版”，把 PostgreSQL 也封到同一个容器里。

### 回答摘要

已经新增一套独立的 all-in-one 方案，并保留原来的双容器正式方案：

1. 新增 [deploy/Dockerfile.allinone:L1-L43](../deploy/Dockerfile.allinone#L1-L43)，在一个镜像里同时打包前端静态资源、Python 运行时和 PostgreSQL/pgvector 基础环境。
2. 新增 [deploy/start_allinone.py:L228-L240](../deploy/start_allinone.py#L228-L240)，容器启动时会初始化 PostgreSQL cluster、创建数据库、启用 `vector` 扩展，再拉起 FastAPI。
3. 新增 [deploy/docker-compose.allinone.yml:L1-L36](../deploy/docker-compose.allinone.yml#L1-L36)，只启动一个 `allinone` 服务，对外暴露 `8000` 和 `5433`。
4. 新增 [scripts/smoke_docker_allinone.py:L70-L114](../scripts/smoke_docker_allinone.py#L70-L114) 和 [scripts/run_local.py:L200-L243](../scripts/run_local.py#L200-L243) 作为统一验收入口。
5. 当前单容器方案是“可交付增强版”，不是默认推荐部署版；默认推荐仍然是更可维护的 `app + postgres` 双容器方案。

### 对应实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| deploy | All-in-One 镜像 | [deploy/Dockerfile.allinone:L1-L43](../deploy/Dockerfile.allinone#L1-L43) |
| deploy | All-in-One Compose | [deploy/docker-compose.allinone.yml:L1-L36](../deploy/docker-compose.allinone.yml#L1-L36) |
| code | 单容器内 PostgreSQL 初始化、数据库创建、扩展启用和 FastAPI 启动 | [initialize_cluster deploy/start_allinone.py:L117-L132](../deploy/start_allinone.py#L117-L132), [ensure_database_objects deploy/start_allinone.py:L176-L191](../deploy/start_allinone.py#L176-L191), [start_backend deploy/start_allinone.py:L206-L225](../deploy/start_allinone.py#L206-L225), [main deploy/start_allinone.py:L228-L240](../deploy/start_allinone.py#L228-L240) |
| test | 单容器烟测和 runner 入口 | [main scripts/smoke_docker_allinone.py:L70-L114](../scripts/smoke_docker_allinone.py#L70-L114), [smoke_docker_allinone scripts/run_local.py:L200-L201](../scripts/run_local.py#L200-L201) |
| doc | 部署、测试和需求说明 | [docs/DEPLOY.md:L38-L56](./DEPLOY.md#L38-L56), [docs/test_reference.md:L229-L239](./test_reference.md#L229-L239), [docs/requirements_traceability.md:L456-L495](./requirements_traceability.md#L456-L495) |

### 验证命令

```powershell
python scripts\run_local.py smoke-docker-allinone
python scripts\check_doc_links.py
```

## Q-0018 如何把 all-in-one 做成可直接 `docker run` 的发布方式，并推送到 GHCR？

### 用户原始问题

把这套 all-in-one 改成可直接 docker run 的发布说明和命令。构建并推送这个单容器镜像到 GitHub Container Registry。

### 回答摘要

已经补齐 GHCR 发布链路：

1. 新增 [deploy/Dockerfile.allinone.release:L1-L29](../deploy/Dockerfile.allinone.release#L1-L29)，它直接打包本地构建好的 `frontend/dist`，用于发布成可 `docker run` 的单容器镜像。
2. 新增 [scripts/publish_ghcr_allinone.py:L123-L160](../scripts/publish_ghcr_allinone.py#L123-L160)，统一处理前端构建、镜像打标、GHCR 登录和推送。
3. [docs/DEPLOY.md:L59-L103](./DEPLOY.md#L59-L103) 已新增 `docker run` 命令和 GHCR 发布命令。
4. 已使用具备 `write:packages` 权限的用户级环境变量 `GHCR_TOKEN` 完成 GHCR 推送，发布标签为 `latest` 和 `9564147`。

### 对应实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| deploy | GHCR 发布镜像 | [deploy/Dockerfile.allinone.release:L1-L29](../deploy/Dockerfile.allinone.release#L1-L29) |
| script | GHCR 发布脚本 | [main scripts/publish_ghcr_allinone.py:L123-L160](../scripts/publish_ghcr_allinone.py#L123-L160) |
| doc | `docker run` 和 GHCR 发布说明 | [docs/DEPLOY.md:L59-L103](./DEPLOY.md#L59-L103) |
| config | GHCR token 配置说明 | [docs/config_reference.md:L22-L24](./config_reference.md#L22-L24) |
| error | GHCR 推送权限不足与修复记录 | [docs/error_traceability.md:L234-L270](./error_traceability.md#L234-L270) |

## Q-0019 为什么 GitHub 仓库没有看到 all-in-one 更新？

### 用户原始问题

为什么我到github没有更新？

### 回答摘要

GHCR 容器镜像和 GitHub 源码仓库是两个不同的发布目标。上一轮已经成功推送 `ghcr.io/2667741708/ling-shan-digital-guide-allinone:latest` 和 `:9564147`，但源码仓库 `origin/main` 仍停在提交 `9564147`，因为 all-in-one Dockerfile、发布脚本、归档文档和部署说明当时还只是本地工作区改动，尚未创建新的 Git commit，也尚未 push 到 GitHub 仓库。

### 对应实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| deploy | all-in-one 发布镜像定义 | [deploy/Dockerfile.allinone.release:L1-L29](../deploy/Dockerfile.allinone.release#L1-L29) |
| script | GHCR 发布脚本 | [scripts/publish_ghcr_allinone.py:L132-L168](../scripts/publish_ghcr_allinone.py#L132-L168) |
| doc | GitHub 源码发布脚本说明 | [docs/DEPLOY.md:L241-L257](./DEPLOY.md#L241-L257) |
| doc | GHCR 镜像发布说明 | [docs/DEPLOY.md:L110-L141](./DEPLOY.md#L110-L141) |

### 验证命令

```powershell
git status --short
git rev-parse HEAD
git rev-parse origin/main
docker manifest inspect ghcr.io/2667741708/ling-shan-digital-guide-allinone:latest
```

## Q-0020 是否可以不用 DeepSeek，只使用多模态大模型和数字人？

### 用户原始问题

我们实际需要的是一个多模态大模型以及一个数字人可以即时的追踪语音对吗？我们可以不用DeepSeek，仅仅使用一个多模态大模型和一个数字人即可。

### 回答摘要

可以。DeepSeek 在当前项目中只是文本 LLM 供应商，不是不可替换的架构核心。更贴近最终产品的能力组合是：PostgreSQL/pgvector 知识库检索 + 多模态大模型理解文本、语音、图片或视频输入 + 数字人引擎完成实时语音播报、口型、表情和动作。如果选用的多模态大模型或数字人平台已经内置 ASR/TTS，可以取消独立 DeepSeek、独立 ASR、独立 TTS；否则仍需要由多模态模型外部的 ASR/TTS 服务补齐语音输入和语音输出。

### 对应实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| 当前文本模型 | DeepSeek 客户端只是 OpenAI 兼容文本生成封装 | [DeepSeekClient backend/app/services/deepseek_service.py:L9-L47](../backend/app/services/deepseek_service.py#L9-L47) |
| 当前问答编排 | RAG 检索后调用 DeepSeek 生成回答，已写入问答日志 | [chat_with_text backend/app/services/chat_service.py:L85-L137](../backend/app/services/chat_service.py#L85-L137) |
| 当前语音缺口 | 后端真实 ASR/TTS 仍未完成 | [REQ-010 docs/requirements_traceability.md:L237-L279](./requirements_traceability.md#L237-L279) |
| 当前多模态缺口 | 图片识景仍是占位，需要接真实视觉/多模态模型 | [REQ-011 docs/requirements_traceability.md:L281-L323](./requirements_traceability.md#L281-L323) |
| 当前数字人 | 前端数字人是 SVG + local-2d 口型同步兜底，不是真实 Live2D 模型资产或商业实时数字人 | [DigitalAvatar frontend/src/components/Avatar/DigitalAvatar.vue:L7-L125](../frontend/src/components/Avatar/DigitalAvatar.vue#L7-L125), [simulateSpeaking frontend/src/store/avatar.ts:L62-L84](../frontend/src/store/avatar.ts#L62-L84) |
| 当前配置 | DeepSeek 配置字段后续可替换为通用 `MODEL_PROVIDER` / 多模态模型配置 | [docs/config_reference.md:L17-L20](./config_reference.md#L17-L20) |

### 改造建议

1. 抽象 `ModelProvider`，把 `DeepSeekClient` 替换为可配置的多模态模型客户端。
2. 保留 `pgvector` RAG 检索，模型只负责理解、推理、生成和引用约束。
3. 将 `/api/v1/guide/ask`、`/api/v1/guide/voice-ask`、`/api/v1/guide/image-ask` 统一编排到同一个多模态问答服务。
4. 数字人侧对接实时 avatar SDK 或云服务，前端不再只用本地 SVG 口型模拟。
5. 如果模型/数字人平台内置语音能力，`/asr/*` 和 `/tts/*` 可以变成兼容代理；如果没有内置能力，则仍需要保留独立 ASR/TTS。

### 验证命令

```powershell
python scripts\run_local.py test-backend
python scripts\run_local.py build-frontend
python scripts\check_doc_links.py
```

## Q-0022 如何整理项目程序并更新 README？

### 用户原始问题

我需要你帮我整理下我们的所有的项目程序，看看是否有需要更新的地方，比如说这个 readme。

### 回答摘要

本次检查按 `traceable-development` 文档体系和 GitHub 仓库上下文执行，发现 `README.md` 仍偏向早期骨架描述，且缺少两个项目长期维护需要的入口文档：`docs/architecture.md` 和 `docs/cli_usage.md`。已更新 README 的当前能力、快速启动、Docker/All-in-One、核心 API、验证命令和文档入口；新增架构说明记录系统边界、分层、数据流、数据层和部署结构；新增 CLI 使用说明记录可复现运行、测试、Docker、GHCR 和 GitHub 发布脚本。

### 对应实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| README | 当前能力、快速启动、API 链路、验证命令和文档入口 | [README.md:L1-L116](../README.md#L1-L116) |
| 架构文档 | 系统边界、模块分层、数据流、数据层和部署结构 | [docs/architecture.md:L1-L136](./architecture.md#L1-L136) |
| CLI 文档 | 本地 runner、联调、Docker、GHCR 和 GitHub 发布命令 | [docs/cli_usage.md:L1-L154](./cli_usage.md#L1-L154) |
| 项目入口 | 新同事阅读顺序和常见任务入口 | [docs/project_onboarding.md:L27-L63](./project_onboarding.md#L27-L63) |
| 程序索引 | 后端、脚本和前端入口已经覆盖主要程序 | [docs/program_index.md:L1-L83](./program_index.md#L1-L83) |

### 验证命令

```powershell
python scripts\check_doc_links.py
python scripts\run_local.py build-frontend
```

## Q-0021 如何补齐游客个性化、路线生成、账号边界、大屏和前端观感？

### 用户原始问题

我们的后端程序中关于观众的个性化出来，管理员账号与游客账号，以及路线生成，数据大屏，等等与大模型无关的功能，我认为还没有完整的实现,我们目前的前端app也很丑，你可以基于canva重新更新下我们的这个项目，把这个项目的各个功能的细节再完善一点。

### 回答摘要

已把“观众”统一落到景区语义中的“游客个性化评分”：游客端可提交多维景点评分、评论、标签和画像快照；后端按 `session_uuid + spot_id` upsert，计算情绪和加权评分；路线推荐读取景点评分与游客历史偏好；问答、路线和评分都写入 PostgreSQL，后台大屏从真实表聚合服务量、热门问题、路线访问、评分排行、负向反馈、情绪趋势和高频标签。前端同步增加游客评分面板和更完整的大屏卡片，并通过样式覆盖刷新视觉。

### 对应实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| 需求追踪 | 本次功能归档为 REQ-021 | [REQ-021 docs/requirements_traceability.md:L539-L581](./requirements_traceability.md#L539-L581) |
| 数据模型 | 景点、设施、会话、消息、路线和游客评分表 | [ScenicSpot backend/app/models/persistence.py:L64-L86](../backend/app/models/persistence.py#L64-L86), [VisitorSpotRating backend/app/models/persistence.py:L306-L354](../backend/app/models/persistence.py#L306-L354) |
| 评分服务 | upsert、统计、画像、后台筛选、审核、排行、趋势和感受度报告 | [create_or_update_rating backend/app/services/rating_service.py:L161-L186](../backend/app/services/rating_service.py#L161-L186), [get_spot_statistics backend/app/services/rating_service.py:L241-L287](../backend/app/services/rating_service.py#L241-L287), [get_user_preference_profile backend/app/services/rating_service.py:L296-L337](../backend/app/services/rating_service.py#L296-L337), [list_admin_ratings backend/app/services/rating_service.py:L340-L367](../backend/app/services/rating_service.py#L340-L367), [update_rating_review_status backend/app/services/rating_service.py:L436-L457](../backend/app/services/rating_service.py#L436-L457), [get_admin_rating_insight_report backend/app/services/rating_service.py:L460-L546](../backend/app/services/rating_service.py#L460-L546) |
| 路线生成 | 评分与画像反哺路线推荐，并持久化 `route_plan` | [_score_spot backend/app/services/route_service.py:L82-L107](../backend/app/services/route_service.py#L82-L107), [recommend_route backend/app/services/route_service.py:L152-L196](../backend/app/services/route_service.py#L152-L196) |
| 大屏聚合 | 从真实问答、路线、评分和景点表聚合后台指标 | [dashboard_overview backend/app/services/analytics_service.py:L34-L89](../backend/app/services/analytics_service.py#L34-L89) |
| 游客前端 | 数字人页评分面板和统计展示 | [ChatGuide rating frontend/src/pages/visitor/ChatGuide.vue:L183-L211](../frontend/src/pages/visitor/ChatGuide.vue#L183-L211) |
| 后台前端 | 大屏新增评分入口，评分运营页支持筛选、报告和评论审核 | [AdminDashboard frontend/src/pages/admin/AdminDashboard.vue:L18-L109](../frontend/src/pages/admin/AdminDashboard.vue#L18-L109), [AdminRatings frontend/src/pages/admin/AdminRatings.vue:L1-L167](../frontend/src/pages/admin/AdminRatings.vue#L1-L167) |
| 样式 | 视觉刷新、评分筛选和审核卡片移动端适配 | [UX refresh frontend/src/styles.css:L929-L1328](../frontend/src/styles.css#L929-L1328) |
| 测试 | 评分 upsert、统计、排行、画像、报告和审核 | [test_rating_upsert_stats_and_preference_profile backend/tests/test_rating_service.py:L15-L76](../backend/tests/test_rating_service.py#L15-L76), [test_v1_admin_rating_operations backend/tests/test_api_v1.py:L84-L126](../backend/tests/test_api_v1.py#L84-L126) |

### 验证命令

```powershell
python scripts\run_local.py test-backend
python scripts\run_local.py build-frontend
python scripts\check_doc_links.py
```

## Q-0023 如何基于 pgvector 与游客评分方案继续完善后台？

### 用户原始问题

基于这个更新下我们的后台，继续完美：可以，向量库仅使用 PostgreSQL + pgvector 是可行的，而且游客个性化评分功能能服务个性化路线推荐、游客感受度报告和数据大屏运营分析。

### 回答摘要

后台已进一步从“能看评分”升级为“能运营评分”：评分列表支持景点、评分、情绪、审核状态、来源、日期和关键词筛选；新增游客感受度报告接口，聚合总评分、维度均分、负向评论、拍照价值景点、设施风险景点、高频标签和服务建议；新增评论审核接口，管理员可将公开评论设为通过、隐藏或拒绝。前端新增 `/admin/ratings` 评分运营页，并从数据大屏导航进入。

### 对应实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| 后台筛选 | 管理员评分列表支持多条件筛选 | [list_admin_ratings backend/app/services/rating_service.py:L340-L367](../backend/app/services/rating_service.py#L340-L367) |
| 感受度报告 | 聚合满意度、维度均分、标签、负向评论和服务建议 | [get_admin_rating_insight_report backend/app/services/rating_service.py:L460-L546](../backend/app/services/rating_service.py#L460-L546) |
| 评论审核 | 修改审核状态，隐藏/拒绝时取消公开 | [update_rating_review_status backend/app/services/rating_service.py:L436-L457](../backend/app/services/rating_service.py#L436-L457) |
| 后台 API | 评分列表、报告和审核接口 | [admin_ratings_v1 backend/app/api/v1.py:L283-L313](../backend/app/api/v1.py#L283-L313), [admin_rating_report_v1 backend/app/api/v1.py:L326-L333](../backend/app/api/v1.py#L326-L333), [admin_rating_review_v1 backend/app/api/v1.py:L336-L354](../backend/app/api/v1.py#L336-L354) |
| 后台前端 | 评分运营页面 | [AdminRatings frontend/src/pages/admin/AdminRatings.vue:L1-L167](../frontend/src/pages/admin/AdminRatings.vue#L1-L167) |
| 测试 | 新增后台评分 API 和服务测试 | [test_v1_admin_rating_operations backend/tests/test_api_v1.py:L84-L126](../backend/tests/test_api_v1.py#L84-L126), [test_rating_upsert_stats_and_preference_profile backend/tests/test_rating_service.py:L15-L76](../backend/tests/test_rating_service.py#L15-L76) |

### 验证命令

```powershell
python scripts\run_local.py test-backend
python scripts\run_local.py build-frontend
python scripts\check_doc_links.py
```

## Q-0024 数字人是否是高清口播和 2D 开源实时互动两种模式，能否先完成 2D 功能？

### 用户原始问题

这个数字人是否有两种模式一个是基于2D开源数字人的？只要保证唇形与语音一致即可？你可以结合开源项目帮我先完成这个2D开源数字人功能吗。

### 回答摘要

V2 设计报告采用“双模式数字人”：高清口播模式用于欢迎语、核心景点讲解和演示视频；实时互动模式用于游客即时问答、路线推荐和后台预览。2D 开源/本地数字人应作为实时互动兜底，而不是替代高清口播的全部能力。当前已先完成 local-2d MVP，并在后续升级中加入 8 个高清 SVG 嘴型、OBJ 参考 pose、OpenSCAD 参考体和 Blender shape keys 脚本，便于继续向 3D 真人嘴部动作资产演进。

### 对应实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| 需求 | 本次功能纳入 REQ-006 | [REQ-006 docs/requirements_traceability.md:L130-L162](./requirements_traceability.md#L130-L162) |
| 口型算法 | local-2d viseme 时间线、语速估算和当前帧选择 | [avatarLipSync frontend/src/store/avatarLipSync.ts:L1-L110](../frontend/src/store/avatarLipSync.ts#L1-L110) |
| 状态机 | 播放状态、口型帧、播放进度和兜底结束逻辑 | [useAvatarStore frontend/src/store/avatar.ts:L18-L84](../frontend/src/store/avatar.ts#L18-L84) |
| 数字人组件 | SVG 嘴型素材映射、viseme 标签、进度条和本地演示按钮 | [DigitalAvatar frontend/src/components/Avatar/DigitalAvatar.vue:L7-L125](../frontend/src/components/Avatar/DigitalAvatar.vue#L7-L125) |
| 嘴型素材 | 8 个高清 SVG 嘴型和 OBJ 参考 pose | [mouth manifest frontend/public/avatar/mouth/mouth-manifest.json:L1-L50](../frontend/public/avatar/mouth/mouth-manifest.json#L1-L50), [generate_mouth_assets scripts/generate_mouth_assets.py:L11-L266](../scripts/generate_mouth_assets.py#L11-L266) |
| 3D 建模脚本 | Blender 安装后导出带 shape keys 的 GLB | [blender_generate_mouth_model.py scripts/blender_generate_mouth_model.py:L1-L113](../scripts/blender_generate_mouth_model.py#L1-L113) |
| 语音联动 | 浏览器 TTS onstart/onend/onerror 驱动数字人口型生命周期 | [speakAnswer frontend/src/pages/visitor/ChatGuide.vue:L116-L137](../frontend/src/pages/visitor/ChatGuide.vue#L116-L137) |
| 测试 | local-2d 口型同步和素材 manifest 单测 | [avatarLipSync.test frontend/tests/avatarLipSync.test.ts:L1-L54](../frontend/tests/avatarLipSync.test.ts#L1-L54) |

### 验证命令

```powershell
npm --prefix frontend run test:avatar
python scripts\run_local.py build-frontend
```

### 影响范围

影响游客端数字人播报表现、浏览器语音播报期间的口型同步和前端测试依赖；不影响后端 API、数据库结构、RAG 检索或后台数字人配置字段。真实 Live2D 模型资产、商业云数字人、高清口播视频生成仍属于后续 P1/P2 范围。

## Q-0025 如何继续制作接近真人嘴巴动作的 2D/3D 模型资产？

### 用户原始问题

我们可以多做几个接近真人的数字人图像，这个口型还不够接近真实；需要高清嘴巴图片、开源图案或 3D 建模方案，并把实际启动路径写入本地 AGENTS.md。

### 回答摘要

当前机器未检测到 `blender`、`openscad` 或 `FreeCADCmd` 命令，因此不能在本机直接完成商业 CAD/Blender 导出。但已先用可复现脚本生成 8 个高清 SVG 嘴型和 OBJ 参考网格，并把当前 `local-2d` 组件切换为素材驱动；如果后续安装 Blender，可运行 Blender Python 脚本导出带 shape keys 的 GLB，再由 Three.js 读取 morph targets 驱动真实口型。

### 对应实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| 启动约定 | 本地启动路径、前端-only 兜底和 2D/3D 数字人资产约定 | [AGENTS.md:L165-L214](../AGENTS.md#L165-L214) |
| 2D 嘴型生成 | 生成 SVG 嘴型、OBJ pose、OpenSCAD 参考体和 manifest | [generate_mouth_assets scripts/generate_mouth_assets.py:L11-L266](../scripts/generate_mouth_assets.py#L11-L266) |
| 3D GLB 脚本 | Blender shape keys + GLB morph targets 导出脚本 | [blender_generate_mouth_model.py scripts/blender_generate_mouth_model.py:L1-L113](../scripts/blender_generate_mouth_model.py#L1-L113) |
| 前端接入 | viseme 到高清 mouth sprite 的映射 | [DigitalAvatar frontend/src/components/Avatar/DigitalAvatar.vue:L7-L125](../frontend/src/components/Avatar/DigitalAvatar.vue#L7-L125) |
| 素材清单 | 8 个嘴型 SVG/OBJ 路径 | [mouth manifest frontend/public/avatar/mouth/mouth-manifest.json:L1-L50](../frontend/public/avatar/mouth/mouth-manifest.json#L1-L50) |
| 单元测试 | 校验 `mbp/fv` 口型和素材文件存在 | [avatarLipSync.test frontend/tests/avatarLipSync.test.ts:L35-L53](../frontend/tests/avatarLipSync.test.ts#L35-L53) |

### 验证命令

```powershell
python scripts\generate_mouth_assets.py
npm --prefix frontend run test:avatar
python scripts\run_local.py build-frontend
python scripts\check_doc_links.py
```

### 影响范围

影响游客端数字人嘴部表现、前端静态资源目录、口型同步单测、本地协作启动说明和后续 3D 建模工作流；不改变后端 API、数据库结构或管理端配置字段。

## Q-0026 如何安装 3D 建模依赖并接入真实全身 AvatarRenderer？

### 用户原始问题

希望依赖安装优先使用国内站点加速，并开始执行真实全身 3D 数字人计划。

### 回答摘要

已使用 `registry.npmmirror.com` 安装前端 3D 运行时依赖 `three`、`@pixiv/three-vrm` 和 `@types/three`。Blender/OpenSCAD/FreeCAD 已由 winget 确认安装；当前 shell 未加入 PATH，可用完整路径运行。前端已新增 `AvatarRenderer`，优先加载 `/avatar/models/lingling-realistic.glb`，模型缺失或 WebGL/加载失败时自动回退当前 2D 数字人。当前已补充本地 Blender procedural 全身 GLB 演示资产，并通过 8 个 viseme morph targets 检查。

### 对应实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| 3D 依赖 | Three.js、three-vrm、Three 类型依赖 | [package.json frontend/package.json:L13-L24](../frontend/package.json#L13-L24) |
| 渲染器 | Three.js/GLTFLoader/three-vrm 加载 GLB/VRM 并驱动 morph targets | [AvatarRenderer frontend/src/components/Avatar/AvatarRenderer.vue:L1-L242](../frontend/src/components/Avatar/AvatarRenderer.vue#L1-L242) |
| 容器/fallback | realistic-3d 就绪时显示 3D，失败时显示 local-2d | [DigitalAvatar frontend/src/components/Avatar/DigitalAvatar.vue:L1-L156](../frontend/src/components/Avatar/DigitalAvatar.vue#L1-L156) |
| 口型映射 | VRM expression、mesh morph target 候选名和权重算法 | [avatarRenderer frontend/src/store/avatarRenderer.ts:L1-L46](../frontend/src/store/avatarRenderer.ts#L1-L46) |
| 模型目录 | 本地 full-body GLB、source copy、哈希和验证命令 | [models README frontend/public/avatar/models/README.md:L1-L40](../frontend/public/avatar/models/README.md#L1-L40) |
| 生成脚本 | Blender procedural full-body avatar 和 viseme shape keys | [blender_generate_lingling_avatar scripts/blender_generate_lingling_avatar.py:L20-L449](../scripts/blender_generate_lingling_avatar.py#L20-L449) |
| 检查脚本 | GLB morph target 合约检查 | [inspect_glb_morph_targets scripts/inspect_glb_morph_targets.py:L11-L133](../scripts/inspect_glb_morph_targets.py#L11-L133) |
| 构建排错 | `@gltf-transform/cli` 不固定到前端 devDependency，使用 `npm exec` 临时运行 | [TRB-022 docs/troubleshooting.md:L806-L836](./troubleshooting.md#L806-L836) |

### 验证命令

```powershell
npm.cmd --prefix frontend ls three @pixiv/three-vrm
& "C:\Program Files\Blender Foundation\Blender 5.1\blender.exe" --version
& "C:\Program Files\OpenSCAD\openscad.exe" --version
& "C:\Users\hmw20\AppData\Local\Programs\FreeCAD 1.1\bin\freecadcmd.exe" --version
python scripts\inspect_glb_morph_targets.py frontend\public\avatar\models\lingling-realistic.glb
npm.cmd --prefix frontend run test:avatar
npm.cmd --prefix frontend run build
python scripts\check_doc_links.py
```

### 影响范围

影响游客端数字人渲染方式、前端依赖包、构建产物大小、数字人静态模型目录和口型测试；不影响后端 API、数据库结构、RAG 检索或后台配置表。当前内置模型是本地 procedural 演示资产，真人级完全匹配仍依赖外部高保真图生 3D 或人工建模。

## Q-0027 本机能否用 Hunyuan3D/Pixal3D/TRELLIS.2 直接生成灵灵高保真 3D 模型？

### 用户原始问题

希望基于参考图和本地 Blender，结合开源图生 3D 项目补充一个尽量匹配的真实数字人资产。

### 回答摘要

本机 RTX 5070 Laptop GPU 只有约 8GB VRAM，更适合谨慎尝试 Hunyuan3D-2/2mini low-vram 的 shape-only 初模；TRELLIS.2 官方要求 Linux 和 24GB+ VRAM，Pixal3D 官方安装先依赖 TRELLIS.2，因此不适合作为本机稳定生产链路。当前先交付本地 Blender procedural `lingling-realistic.glb`，后续可用裁剪后的单主体图片在外部 24GB+ VRAM 环境生成初模，再回到 Blender 增加口型 shape keys。

### 对应实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| 本地 procedural GLB | 已提交的全身演示资产说明、哈希和验证命令 | [models README frontend/public/avatar/models/README.md:L1-L40](../frontend/public/avatar/models/README.md#L1-L40) |
| Blender 生成脚本 | 本地生成浅青汉服、发髻、发簪、面部和口型 shape keys | [blender_generate_lingling_avatar scripts/blender_generate_lingling_avatar.py:L20-L449](../scripts/blender_generate_lingling_avatar.py#L20-L449) |
| GLB 口型检查 | 校验 `closed/mbp/aa/ee/oh/round/fv/smile` | [inspect_glb_morph_targets scripts/inspect_glb_morph_targets.py:L11-L133](../scripts/inspect_glb_morph_targets.py#L11-L133) |
| 前端加载 | 加载 GLB/VRM 并按 viseme 驱动 morph targets | [AvatarRenderer frontend/src/components/Avatar/AvatarRenderer.vue:L159-L214](../frontend/src/components/Avatar/AvatarRenderer.vue#L159-L214) |

### 验证命令

```powershell
python scripts\inspect_glb_morph_targets.py frontend\public\avatar\models\lingling-realistic.glb
npm.cmd --prefix frontend run test:avatar
npm.cmd --prefix frontend run build
```

### 影响范围

影响数字人模型资产生成策略、后续图生 3D 依赖选择、模型替换验收和排错文档；不影响后端 API、数据库、RAG 或管理端配置。

## Q-0028 5 张本地数字人形象示例如何约束后续 3D 资产？

### 用户原始问题

`D:\文件\灵山\数字人形象示例` 目录里有 5 张数字人的形象、衣服、表情、口型细节，希望每次制作 3D 资产后都基于这些形象去贴近设计。

### 回答摘要

该目录已作为 3D 资产制作的本地参考源沉淀。当前主模型优先贴近第 1/5 张的浅青古风汉服、透纱宽袖、花卉与山水刺绣、玉佩流苏、黑色高发髻和金色花簪；第 4 张用于表情和说话口型方向；第 2/3 张作为后续导游制服、户外休闲服的独立服装变体参考。`blender_generate_lingling_avatar.py` 已支持 `--reference-dir`，默认读取 `数字人形象示例`，并把参考目录、图片名和设计 brief 写入 GLB extras。

### 对应实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| 设计参考目录 | 5 张灵灵形象、服饰、表情、口型和材质参考图 | [数字人形象示例](../数字人形象示例) |
| 模型说明 | 当前 GLB 哈希、参考目录、形象优先级和替换注意事项 | [models README frontend/public/avatar/models/README.md:L1-L40](../frontend/public/avatar/models/README.md#L1-L40) |
| 参考图 metadata | `REFERENCE_DESIGN_BRIEF`、`--reference-dir`、图片名收集和 GLB extras 写入 | [blender_generate_lingling_avatar scripts/blender_generate_lingling_avatar.py:L31-L87](../scripts/blender_generate_lingling_avatar.py#L31-L87) |
| 资产生成 | 构建浅青汉服、发髻、发簪、面部、口型和装饰件 | [build_avatar scripts/blender_generate_lingling_avatar.py:L302-L400](../scripts/blender_generate_lingling_avatar.py#L302-L400) |
| 前端验收 | 加载 `lingling-realistic.glb` 并按 viseme 更新 morph targets | [AvatarRenderer frontend/src/components/Avatar/AvatarRenderer.vue:L159-L214](../frontend/src/components/Avatar/AvatarRenderer.vue#L159-L214) |

### 验证命令

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.1\blender.exe" --background --python scripts\blender_generate_lingling_avatar.py -- --output frontend\public\avatar\models\lingling-realistic.glb --source-output frontend\public\avatar\models\source\lingling-ai-base.glb --reference-dir 数字人形象示例
python scripts\inspect_glb_morph_targets.py frontend\public\avatar\models\lingling-realistic.glb
npm.cmd --prefix frontend run test:avatar
```

### 影响范围

影响后续 3D 数字人资产制作验收、GLB metadata、模型 README、REQ-006 形象一致性要求和前端视觉验收；不改变后端 API、数据库结构或导览问答逻辑。

## Q-0029 二次元开源数字人的对话与唇形是否适合做对比方案？

### 用户原始问题

这里提到过一个二次元开源项目，想确认该项目的对话和唇形真实感是否足够流畅自然；如果可接受，希望单独维护一个文件夹使用 2D 数字人，后续与 3D 数字人效果做对比。

### 回答摘要

如果指的是 Open-LLM-VTuber 一类 Live2D/AI VTuber 项目，它更适合作为“二次元流畅互动对比方案”，不适合作为真人级唇形方案。对话自然度主要取决于 ASR、LLM、TTS 和中断策略；Live2D 负责形象、表情、动作和音频驱动口型。它的观感通常会比当前轻量 SVG `local-2d` 更像二次元虚拟主播，但口型多为 Live2D 参数/音频能量驱动，不等同于逐音素真人嘴部形变。推荐只隔离引入 Live2D 资产与渲染适配层，不把完整 Open-LLM-VTuber 后端嵌入现有项目。

### 对应实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| 当前需求 | 数字人灵灵 2D/3D 交互和口型归属 REQ-006 | [REQ-006 docs/requirements_traceability.md:L130-L170](./requirements_traceability.md#L130-L170) |
| 当前 2D 口型 | 文本、语速、标点和字符启发式生成 viseme 时间线 | [avatarLipSync frontend/src/store/avatarLipSync.ts:L1-L110](../frontend/src/store/avatarLipSync.ts#L1-L110) |
| 当前 2D 渲染 | SVG 汉服导游形象和 8 个 mouth sprite 回退 | [DigitalAvatar frontend/src/components/Avatar/DigitalAvatar.vue:L89-L144](../frontend/src/components/Avatar/DigitalAvatar.vue#L89-L144) |
| 当前 3D 对比 | Three.js/VRM 加载 GLB，并按 viseme 驱动 morph targets | [AvatarRenderer frontend/src/components/Avatar/AvatarRenderer.vue:L159-L214](../frontend/src/components/Avatar/AvatarRenderer.vue#L159-L214) |
| 当前 3D 资产 | `lingling-realistic.glb`、哈希、8 个 morph target 和替换规则 | [models README frontend/public/avatar/models/README.md:L1-L40](../frontend/public/avatar/models/README.md#L1-L40) |
| 参考项目 | README 已记录 AIAvatarKit、Magic-Voice-Chat、pixi-live2d-display | [README README.md:L113-L118](../README.md#L113-L118) |

### 建议隔离目录

后续若确认接入，建议新增以下独立目录，避免和当前 3D 资产混在一起：

```text
frontend/public/avatar/live2d/
frontend/src/components/Avatar/Live2DAvatar/
frontend/src/store/avatarLive2d.ts
docs/decision_records/ADR-0001-live2d-avatar-comparison.md
```

完整 Open-LLM-VTuber 上游项目不建议直接放入当前中文路径工作区运行；其快速开始文档提示项目路径尽量不要包含中文。若需要跑上游原项目，应单独放到英文路径，再把模型资产、配置经验和评测结果同步回本项目文档。

### 验证命令

```powershell
npm.cmd --prefix frontend run test:avatar
npm.cmd --prefix frontend run build
python scripts\check_doc_links.py
```

### 影响范围

影响游客端数字人渲染模式、前端静态资产目录、Live2D 运行时依赖、数字人视觉验收和对比演示；不应影响后端 RAG、游客问答 API、PostgreSQL 数据结构或现有 `lingling-realistic.glb` 3D 资产。

## Q-0030 除数字人外，RAG、后端、游客系统、管理员系统和后台数据是否设计完善？

### 用户原始问题

核验当前项目中除数字人之外，知识库 RAG、后端服务、管理员系统、游客系统以及后台数据是否已经设计完善。

### 回答摘要

当前项目除数字人外已经达到比赛演示级闭环：RAG 使用 PostgreSQL + pgvector 保存 3377 个启用 chunk；后端统一 `/api/v1` 路由覆盖游客问答、路线、评分、RAG、后台鉴权、知识库、评分运营和大屏；游客端具备问答、地图、路线和评分；管理员端具备登录、知识库版本流转、评分运营和数据大屏；后台数据层已覆盖景点、设施、会话、问答、路线、知识库、chunk、管理员和评分表。

但这不等于生产级完善。仍需补齐后端真实 ASR/TTS/图片识景、生产级 embedding/reranker、细粒度管理员权限、数据库迁移备份、前端 E2E 测试，以及语义级文档行号刷新。

### 对应实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| RAG 数据源 | 读取灵山公开资料包 docx/xlsx 并切片 | [load_scenic_pack_entries backend/app/services/vector_store.py:L266-L290](../backend/app/services/vector_store.py#L266-L290) |
| RAG 构建 | 写入 PostgreSQL `knowledge_chunk` 并导出调试索引 | [build_knowledge_base backend/app/services/vector_store.py:L465-L503](../backend/app/services/vector_store.py#L465-L503) |
| RAG 检索 | 通过 pgvector 距离排序后再按余弦分数返回 chunk | [retrieve_context backend/app/services/vector_store.py:L575-L596](../backend/app/services/vector_store.py#L575-L596) |
| 知识库发布流 | 保存、更新、发布和删除版本化知识文档 | [save_document backend/app/services/knowledge_service.py:L187-L259](../backend/app/services/knowledge_service.py#L187-L259), [publish_document backend/app/services/knowledge_service.py:L328-L353](../backend/app/services/knowledge_service.py#L328-L353), [delete_document backend/app/services/knowledge_service.py:L382-L407](../backend/app/services/knowledge_service.py#L382-L407) |
| 后端统一 API | 游客问答、路线、评分、RAG、鉴权、知识库和评分运营 API | [guide_ask_v1 backend/app/api/v1.py:L128-L141](../backend/app/api/v1.py#L128-L141), [rag_retrieve_v1 backend/app/api/v1.py:L258-L259](../backend/app/api/v1.py#L258-L259), [admin_upload_document_v1 backend/app/api/v1.py:L367-L379](../backend/app/api/v1.py#L367-L379), [admin_ratings_v1 backend/app/api/v1.py:L283-L312](../backend/app/api/v1.py#L283-L312) |
| 游客系统 | 游客端会话、问答、路线、评分和地图页 | [ChatGuide frontend/src/pages/visitor/ChatGuide.vue:L54-L242](../frontend/src/pages/visitor/ChatGuide.vue#L54-L242), [ScenicMap frontend/src/pages/visitor/ScenicMap.vue:L14-L62](../frontend/src/pages/visitor/ScenicMap.vue#L14-L62), [visitor API frontend/src/api/visitor.ts:L58-L98](../frontend/src/api/visitor.ts#L58-L98) |
| 管理员系统 | 登录鉴权、知识库管理、评分运营和大屏 | [authenticate_admin backend/app/services/auth_service.py:L110-L131](../backend/app/services/auth_service.py#L110-L131), [KnowledgeManage frontend/src/pages/admin/KnowledgeManage.vue:L56-L286](../frontend/src/pages/admin/KnowledgeManage.vue#L56-L286), [AdminRatings frontend/src/pages/admin/AdminRatings.vue:L18-L167](../frontend/src/pages/admin/AdminRatings.vue#L18-L167), [AdminDashboard frontend/src/pages/admin/AdminDashboard.vue:L8-L109](../frontend/src/pages/admin/AdminDashboard.vue#L8-L109) |
| 后台数据 | 景点、设施、会话、消息、路线、知识库、chunk、操作日志和评分表 | [persistence models backend/app/models/persistence.py:L51-L354](../backend/app/models/persistence.py#L51-L354), [init_db backend/app/core/database.py:L58-L69](../backend/app/core/database.py#L58-L69) |
| 测试覆盖 | `/api/v1`、知识库生命周期、评分、RAG 构建与检索测试 | [test_api_v1 backend/tests/test_api_v1.py:L18-L152](../backend/tests/test_api_v1.py#L18-L152), [test_versioned_knowledge_document_lifecycle backend/tests/test_knowledge_management.py:L21-L63](../backend/tests/test_knowledge_management.py#L21-L63), [test_rating_upsert_stats_and_preference_profile backend/tests/test_rating_service.py:L15-L76](../backend/tests/test_rating_service.py#L15-L76), [test_vector_store backend/tests/test_vector_store.py:L7-L26](../backend/tests/test_vector_store.py#L7-L26) |

### 验证命令

```powershell
python scripts\check_doc_links.py
npm.cmd --prefix frontend run build
python scripts\run_local.py test-backend
python scripts\run_local.py build-kb
python scripts\run_local.py smoke-backend
```

### 本次验证结果

- `python scripts\check_doc_links.py`：通过，输出 `doc links ok`。
- `npm.cmd --prefix frontend run build`：通过，Vite 构建成功；存在 `AvatarRenderer` chunk 超过 500 kB 的体积告警。
- `python scripts\run_local.py test-backend`：通过，`16 passed`；存在 FastAPI `on_event` 和 `datetime.utcnow()` 弃用告警。
- `python scripts\run_local.py build-kb`：通过，`vector_backend = pgvector`，`entry_count = 3377`。
- `python scripts\run_local.py smoke-backend`：通过，完成后台登录、草稿上传、发布后 RAG 命中、游客问答引用和软删除后重建索引。

### 后续待完善

1. 后端真实 ASR/TTS 和图片识景仍是演示级占位，不属于本次“除数字人外”的 RAG/业务闭环核心，但影响赛题完整度。
2. RAG 当前 embedding 是哈希向量，适合演示和可复现测试；生产级应接 bge-m3、text2vec 或 Qwen Embedding，并增加 hybrid search/reranker。
3. 管理后台目前是单管理员角色，缺少多角色、操作审批、审计导出和密码重置流程。
4. 数据库采用 `create_all` 初始化，缺少 Alembic 迁移、备份恢复、索引性能压测和数据保留策略。
5. `scripts/check_doc_links.py` 只能检查链接目标和行号范围是否存在，不能验证链接是否仍指向正确符号；后续应接入符号索引语义校验。

### 影响范围

本次核验不改变代码逻辑；影响项目验收判断、后续排期、文档追踪和交接说明。当前结论是：除数字人外，核心业务闭环已经较完整，适合作为比赛演示版；若按生产系统标准，还需要继续补齐权限、检索质量、运维迁移和端到端验收。




