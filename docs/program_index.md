# 程序索引

## 核心后端服务

| 程序 | 文件职责 | 核心符号 |
|---|---|---|
| DeepSeek 客户端 | 读取本地 API Key，调用 DeepSeek OpenAI 兼容接口 | [DeepSeekClient backend/app/services/deepseek_service.py:L9-L47](../backend/app/services/deepseek_service.py#L9-L47) |
| 游客问答编排 | 创建会话、文本/语音/图片问答，串联 RAG 与 DeepSeek | [chat_with_text backend/app/services/chat_service.py:L38-L88](../backend/app/services/chat_service.py#L38-L88) |
| 数据库层 | 配置 SQLAlchemy，启动时 `create_all`，支持 SQLite/PostgreSQL 切换 | [configure_database backend/app/core/database.py:L33-L46](../backend/app/core/database.py#L33-L46), [init_db backend/app/core/database.py:L49-L55](../backend/app/core/database.py#L49-L55), [new_session backend/app/core/database.py:L67-L69](../backend/app/core/database.py#L67-L69) |
| 持久化模型 | 管理员、知识文档、文档版本、操作日志、数字人配置 | [persistence models backend/app/models/persistence.py:L16-L112](../backend/app/models/persistence.py#L16-L112) |
| 后台鉴权服务 | 管理员初始化、PBKDF2 密码校验、Bearer token 签发和依赖校验 | [ensure_admin_user backend/app/services/auth_service.py:L55-L74](../backend/app/services/auth_service.py#L55-L74), [authenticate_admin backend/app/services/auth_service.py:L110-L131](../backend/app/services/auth_service.py#L110-L131), [require_admin_user backend/app/services/auth_service.py:L134-L145](../backend/app/services/auth_service.py#L134-L145) |
| 知识库服务 | 为 API 层提供检索、文档列表、上传、更新、发布、归档、软删除、版本和历史 | [retrieve_context backend/app/services/knowledge_service.py:L22-L42](../backend/app/services/knowledge_service.py#L22-L42), [save_document backend/app/services/knowledge_service.py:L153-L213](../backend/app/services/knowledge_service.py#L153-L213), [update_document backend/app/services/knowledge_service.py:L216-L262](../backend/app/services/knowledge_service.py#L216-L262), [publish_document backend/app/services/knowledge_service.py:L265-L282](../backend/app/services/knowledge_service.py#L265-L282), [list_versions backend/app/services/knowledge_service.py:L340-L369](../backend/app/services/knowledge_service.py#L340-L369) |
| 本地向量库 | 基于 CSV/Markdown/真实资料包/已发布后台资料生成 JSON 向量库并检索 | [load_admin_document_entries backend/app/services/vector_store.py:L150-L201](../backend/app/services/vector_store.py#L150-L201), [build_knowledge_base backend/app/services/vector_store.py:L257-L277](../backend/app/services/vector_store.py#L257-L277), [retrieve_context backend/app/services/vector_store.py:L286-L307](../backend/app/services/vector_store.py#L286-L307) |
| 数字人配置服务 | 持久化当前启用的数字人名称、风格、服装、音色、语速和欢迎语 | [get_active_avatar backend/app/services/avatar_service.py:L65-L73](../backend/app/services/avatar_service.py#L65-L73), [save_avatar_config backend/app/services/avatar_service.py:L76-L99](../backend/app/services/avatar_service.py#L76-L99) |
| 真实资料包读取 | 读取灵山公开资料包 docx/xlsx，xlsx 限量抽取避免超时 | [load_scenic_pack_entries backend/app/services/vector_store.py:L191-L216](../backend/app/services/vector_store.py#L191-L216), [extract_xlsx_text backend/app/services/vector_store.py:L151-L188](../backend/app/services/vector_store.py#L151-L188) |
| 灵山景点目录 | 提供真实灵山点位、地图坐标、标签、讲解词和推荐停留时间 | [SCENIC_SPOTS backend/app/services/scenic_service.py:L14-L225](../backend/app/services/scenic_service.py#L14-L225) |
| 路线推荐服务 | 根据兴趣、时间、体力和起点生成灵山推荐路线 | [recommend_route backend/app/services/route_service.py:L80-L116](../backend/app/services/route_service.py#L80-L116) |
| 数据大屏服务 | 输出热门问答、热门景点、路线偏好和情绪趋势 | [dashboard_overview backend/app/services/analytics_service.py:L1-L31](../backend/app/services/analytics_service.py#L1-L31) |
| FastAPI 入口 | 注册游客端、管理端和健康检查接口 | [create_app backend/app/main.py:L9-L28](../backend/app/main.py#L9-L28) |

## 运行与验证脚本

| 程序 | 文件职责 | 核心符号 |
|---|---|---|
| 本地 runner | 环境检查、依赖安装、构建知识库、测试和服务启动 | [main scripts/run_local.py:L149-L189](../scripts/run_local.py#L149-L189) |
| 后端烟测 | 登录后台、上传草稿、发布、检索命中、游客问答引用、删除后不命中 | [main scripts/smoke_test.py:L77-L123](../scripts/smoke_test.py#L77-L123) |
| 完整栈烟测 | 启动后端和静态前端后运行 API 烟测 | [main scripts/smoke_full_stack.py:L30-L61](../scripts/smoke_full_stack.py#L30-L61) |
| Vue 完整栈烟测 | 复用健康服务或启动 FastAPI 与 Vite，验证真实 Vue 工程 | [main scripts/smoke_vue_full_stack.py:L67-L122](../scripts/smoke_vue_full_stack.py#L67-L122) |
| 静态前端服务 | 用 Python http.server 服务无依赖演示端 | [main scripts/serve_static_frontend.py:L14-L23](../scripts/serve_static_frontend.py#L14-L23) |
| DeepSeek 多智能体生成器 | 生成架构、后端、前端、AI/RAG、测试文档建议 | [main scripts/deepseek_multi_agent.py:L203-L240](../scripts/deepseek_multi_agent.py#L203-L240) |
| GitHub 发布脚本 | 配置远程仓库、检查工作区、推送分支和 tag | [main scripts/publish_github.py:L56-L84](../scripts/publish_github.py#L56-L84) |

## 前端入口

| 程序 | 文件职责 | 核心位置 |
|---|---|---|
| Vue 数字人页 | 游客问答、语音输入、语音播报、知识引用和路线卡片 | [ChatGuide frontend/src/pages/visitor/ChatGuide.vue:L1-L147](../frontend/src/pages/visitor/ChatGuide.vue#L1-L147) |
| 数字人灵灵 | SVG 导游形象、口型、状态和字幕 | [DigitalAvatar frontend/src/components/Avatar/DigitalAvatar.vue:L1-L64](../frontend/src/components/Avatar/DigitalAvatar.vue#L1-L64) |
| 灵山地图组件 | SVG 真实景区地图、POI、路线和详情 | [ScenicMapView frontend/src/components/ScenicMapView.vue:L1-L101](../frontend/src/components/ScenicMapView.vue#L1-L101) |
| 地图导览页 | 兴趣/时间筛选并生成路线 | [ScenicMap frontend/src/pages/visitor/ScenicMap.vue:L1-L62](../frontend/src/pages/visitor/ScenicMap.vue#L1-L62) |
| 管理大屏 | 热门问答、热门景点、路线偏好、情绪趋势 | [AdminDashboard frontend/src/pages/admin/AdminDashboard.vue:L1-L75](../frontend/src/pages/admin/AdminDashboard.vue#L1-L75) |
| 后台登录页 | 登录后保存 Bearer token 到 localStorage | [AdminLogin frontend/src/pages/admin/AdminLogin.vue:L1-L46](../frontend/src/pages/admin/AdminLogin.vue#L1-L46) |
| 知识库管理页 | 状态筛选、草稿上传、版本/历史、发布、归档、删除、重建索引和检索测试 | [KnowledgeManage script frontend/src/pages/admin/KnowledgeManage.vue:L33-L156](../frontend/src/pages/admin/KnowledgeManage.vue#L33-L156), [KnowledgeManage template frontend/src/pages/admin/KnowledgeManage.vue:L216-L265](../frontend/src/pages/admin/KnowledgeManage.vue#L216-L265) |
| 数字人配置页 | 保存当前启用数字人配置到数据库 | [AvatarManage frontend/src/pages/admin/AvatarManage.vue:L1-L62](../frontend/src/pages/admin/AvatarManage.vue#L1-L62) |
| 后台 API 客户端 | 登录、知识库版本流转、历史查询、数字人配置请求封装 | [admin api frontend/src/api/admin.ts:L7-L64](../frontend/src/api/admin.ts#L7-L64) |
| HTTP 客户端 | 自动附加 Bearer token，401 跳转登录页 | [http token frontend/src/api/http.ts:L8-L22](../frontend/src/api/http.ts#L8-L22) |
| Vue 应用入口 | 注册 Pinia 和 Router，避免未使用 Element Plus 类型污染 | [frontend/src/main.ts:L1-L9](../frontend/src/main.ts#L1-L9) |
| 静态演示端 | 在 npm 网络异常时保证端到端演示可用 | [frontend_static/index.html:L170-L218](../frontend_static/index.html#L170-L218) |

## 修改风险

- 修改 [chat_with_text backend/app/services/chat_service.py:L38-L88](../backend/app/services/chat_service.py#L38-L88) 会影响游客问答、语音问答复用逻辑和 smoke 测试。
- 修改 [SCENIC_SPOTS backend/app/services/scenic_service.py:L14-L225](../backend/app/services/scenic_service.py#L14-L225) 会影响地图点位、路线推荐、景点列表 API 和前端 POI。
- 修改 [recommend_route backend/app/services/route_service.py:L80-L116](../backend/app/services/route_service.py#L80-L116) 会影响问答路线卡片、地图路线和路线推荐接口。
- 修改 [retrieve_context backend/app/services/vector_store.py:L252-L273](../backend/app/services/vector_store.py#L252-L273) 会影响知识库命中率和回答依据。
- 修改 [load_admin_document_entries backend/app/services/vector_store.py:L150-L170](../backend/app/services/vector_store.py#L150-L170) 会影响后台上传资料是否进入 RAG。
- 修改 [run_local.py 命令分发 scripts/run_local.py:L149-L189](../scripts/run_local.py#L149-L189) 会影响部署、测试和服务器运行流程。
- 修改 [publish_github.py 发布流程 scripts/publish_github.py:L56-L84](../scripts/publish_github.py#L56-L84) 会影响 GitHub 远程发布、分支映射和 tag 推送。
