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
| 数字人问答页 | 游客端 ChatGuide 页面 | [frontend/src/pages/visitor/ChatGuide.vue:TODO-LINES](../frontend/src/pages/visitor/ChatGuide.vue) |
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

已完成：本地默认 SQLite、Docker 使用 PostgreSQL；后台管理员登录返回 Bearer token；后台写接口需要 token；知识文档上传默认 draft，更新生成新版本，发布后进入 RAG，归档/删除后退出 RAG，版本和历史可查；数字人配置持久化到数据库。

### 对应实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| 数据库配置 | SQLAlchemy engine/session、SQLite/PostgreSQL 切换 | [configure_database backend/app/core/database.py:L33-L46](../backend/app/core/database.py#L33-L46) |
| 数据表模型 | 管理员、知识文档、版本、操作日志、数字人配置 | [persistence models backend/app/models/persistence.py:L16-L112](../backend/app/models/persistence.py#L16-L112) |
| 鉴权服务 | 密码哈希、登录、token 校验 | [authenticate_admin backend/app/services/auth_service.py:L110-L131](../backend/app/services/auth_service.py#L110-L131), [require_admin_user backend/app/services/auth_service.py:L134-L145](../backend/app/services/auth_service.py#L134-L145) |
| 知识库状态流转 | 上传 draft、发布 active、归档、软删除、版本/历史 | [save_document backend/app/services/knowledge_service.py:L153-L213](../backend/app/services/knowledge_service.py#L153-L213), [publish_document backend/app/services/knowledge_service.py:L265-L282](../backend/app/services/knowledge_service.py#L265-L282), [list_history backend/app/services/knowledge_service.py:L372-L396](../backend/app/services/knowledge_service.py#L372-L396) |
| 向量库约束 | 只把 active 文档当前版本加入 RAG 索引 | [load_admin_document_entries backend/app/services/vector_store.py:L150-L201](../backend/app/services/vector_store.py#L150-L201) |
| 后台页面 | 登录、知识库版本/历史、数字人配置 | [AdminLogin frontend/src/pages/admin/AdminLogin.vue:L1-L46](../frontend/src/pages/admin/AdminLogin.vue#L1-L46), [KnowledgeManage frontend/src/pages/admin/KnowledgeManage.vue:L216-L265](../frontend/src/pages/admin/KnowledgeManage.vue#L216-L265), [AvatarManage frontend/src/pages/admin/AvatarManage.vue:L1-L62](../frontend/src/pages/admin/AvatarManage.vue#L1-L62) |
| 测试 | 权限、版本化知识库、数字人配置持久化 | [auth tests backend/tests/test_auth_service.py:L18-L50](../backend/tests/test_auth_service.py#L18-L50), [knowledge lifecycle backend/tests/test_knowledge_management.py:L18-L58](../backend/tests/test_knowledge_management.py#L18-L58), [avatar test backend/tests/test_avatar_service.py:L8-L17](../backend/tests/test_avatar_service.py#L8-L17) |

### 验证命令

```powershell
python scripts\run_local.py test-backend
python scripts\run_local.py build-frontend
$env:DATABASE_URL='sqlite:///data/.smoke_lingtour.db'; $env:BACKEND_PORT='8011'; $env:FRONTEND_PORT='5174'; python scripts\smoke_vue_full_stack.py
```
