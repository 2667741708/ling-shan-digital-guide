# 需求追踪

## REQ-001 DeepSeek + 本地知识库问答闭环

### 用户场景

游客通过文本向数字人提问，系统从本地景区资料检索依据，再调用 DeepSeek 生成适合语音播报的回答。

### 实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| API 入口 | 游客文本问答接口 | [backend/app/api/visitor.py:L14-L21](../backend/app/api/visitor.py#L14-L21) |
| 服务编排 | RAG 检索、DeepSeek 调用、降级回答、真实延迟 | [chat_with_text backend/app/services/chat_service.py:L38-L88](../backend/app/services/chat_service.py#L38-L88) |
| 模型客户端 | DeepSeek OpenAI 兼容接口封装 | [DeepSeekClient backend/app/services/deepseek_service.py:L9-L47](../backend/app/services/deepseek_service.py#L9-L47) |
| 检索入口 | 后端知识库服务入口 | [retrieve_context backend/app/services/knowledge_service.py:L5-L18](../backend/app/services/knowledge_service.py#L5-L18) |
| 向量检索 | 本地 JSON 哈希向量检索 | [retrieve_context backend/app/services/vector_store.py:L252-L273](../backend/app/services/vector_store.py#L252-L273) |
| 测试 | DeepSeek 外部依赖关闭后的问答单测 | [test_chat_with_text_uses_references_and_latency backend/tests/test_chat_service.py:L5-L12](../backend/tests/test_chat_service.py#L5-L12) |

### 配置项

- [DeepSeek 与本地向量库配置 .env.example:L14-L27](../.env.example#L14-L27)

### 验证命令

```powershell
python scripts\run_local.py build-kb
python scripts\run_local.py test-backend
python scripts\run_local.py smoke-backend
```

### 影响范围

影响游客问答、后台知识库检索测试、演示端数字人回答内容和响应时间统计。

## REQ-002 本地知识库和轻量向量库

### 用户场景

团队可以基于现有 `data` 资料生成可检索知识库，避免比赛现场依赖重型向量数据库或大模型 embedding 服务。

### 实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| 数据源 | 示范景区导览资料 | [data/raw_documents/demo_scenic_guide.md:L1-L25](../data/raw_documents/demo_scenic_guide.md#L1-L25) |
| 真实资料包 | 自动读取灵山公开资料包中的 docx/xlsx | [load_scenic_pack_entries backend/app/services/vector_store.py:L191-L216](../backend/app/services/vector_store.py#L191-L216) |
| xlsx 抽取 | 行为数据限制为最多 2500 个文本单元格，避免构建卡死 | [extract_xlsx_text backend/app/services/vector_store.py:L151-L188](../backend/app/services/vector_store.py#L151-L188) |
| 向量构建 | 读取 FAQ、景点和文档后写入 JSON 向量库 | [build_knowledge_base backend/app/services/vector_store.py:L223-L243](../backend/app/services/vector_store.py#L223-L243) |
| 构建脚本 | 可复现知识库构建入口 | [scripts/build_knowledge_base.py:L16-L19](../scripts/build_knowledge_base.py#L16-L19) |
| 单元测试 | 构建条目数和检索命中测试 | [backend/tests/test_vector_store.py:L4-L12](../backend/tests/test_vector_store.py#L4-L12) |

### 验证命令

```powershell
python scripts\run_local.py build-kb
```

当前真实资料包构建结果为 `entry_count = 3377`。

## REQ-003 可复现本地运行与完整栈烟测

### 用户场景

开发者或评委可以用 Python 脚本启动后端、静态前端并验证完整链路，不依赖不可复现的手工命令。

### 实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| 环境检查 | 检查文件、端口、DeepSeek Key | [check_env scripts/run_local.py:L51-L63](../scripts/run_local.py#L51-L63) |
| 后端启动 | 用 Python subprocess 启动 Uvicorn | [start_backend scripts/run_local.py:L89-L105](../scripts/run_local.py#L89-L105) |
| 后端烟测 | 启动后端并调用 API | [smoke_backend scripts/run_local.py:L136-L146](../scripts/run_local.py#L136-L146) |
| 完整栈烟测 | 启动后端 + 静态前端 + API 测试 | [main scripts/smoke_full_stack.py:L30-L61](../scripts/smoke_full_stack.py#L30-L61) |
| 静态演示端 | 无 npm 依赖的游客端与大屏入口 | [frontend_static/index.html:L170-L218](../frontend_static/index.html#L170-L218) |

### 验证命令

```powershell
python scripts\smoke_full_stack.py
```

## REQ-004 文档行号可追踪

### 用户场景

后续 AI 或同事修改代码后，可以重新生成符号索引并检查文档链接，减少“只在聊天记录里知道位置”的风险。

### 实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| 符号索引 | 扫描 Python 类和函数行号 | [generate_symbol_index main scripts/generate_symbol_index.py:L40-L51](../scripts/generate_symbol_index.py#L40-L51) |
| 文档链接检查 | 检查 `docs/` 中相对链接和行号范围 | [check_doc_links main scripts/check_doc_links.py:L13-L37](../scripts/check_doc_links.py#L13-L37) |

### 验证命令

```powershell
python scripts\generate_symbol_index.py
python scripts\check_doc_links.py
```

## REQ-005 灵山真实景点地图与路线导览

### 用户场景

游客进入地图页或数字人问答页后，可以看到基于灵山胜境真实景点的导览地图，并根据兴趣、时间生成可视化路线。

### 实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| 景点数据 | 灵山大照壁、五智门、九龙灌浴、灵山大佛、梵宫、五印坛城等真实点位 | [SCENIC_SPOTS backend/app/services/scenic_service.py:L14-L225](../backend/app/services/scenic_service.py#L14-L225) |
| 路线算法 | 根据兴趣、热度、文化价值、自然价值、拍照价值、设施便利度、距离成本打分 | [_score_spot backend/app/services/route_service.py:L45-L67](../backend/app/services/route_service.py#L45-L67) |
| 路线入口 | 游客端路线推荐服务 | [recommend_route backend/app/services/route_service.py:L80-L116](../backend/app/services/route_service.py#L80-L116) |
| 地图组件 | SVG 地形、水系、中轴线路线和 POI 详情 | [ScenicMapView frontend/src/components/ScenicMapView.vue:L1-L101](../frontend/src/components/ScenicMapView.vue#L1-L101) |
| 地图页面 | 兴趣和时间筛选，重新生成推荐路线 | [ScenicMap frontend/src/pages/visitor/ScenicMap.vue:L1-L62](../frontend/src/pages/visitor/ScenicMap.vue#L1-L62) |
| 样式 | 地图视觉、路线、POI、图例、移动端适配 | [map styles frontend/src/styles.css:L438-L617](../frontend/src/styles.css#L438-L617) |
| 测试 | 验证真实灵山景点和路线输出 | [test_route_service backend/tests/test_route_service.py:L6-L26](../backend/tests/test_route_service.py#L6-L26) |

### 验证命令

```powershell
python scripts\run_local.py test-backend
python scripts\run_local.py build-frontend
```

## REQ-006 数字人灵灵真实前端交互体验

### 用户场景

游客在数字人导览页看到可辨识的“灵灵”导游形象，支持文本提问、浏览器语音输入、浏览器语音播报、嘴部动画、知识引用和推荐路线展示。

### 实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| 数字人状态 | 待机、倾听、思考、讲解、口型模拟和字幕 | [useAvatarStore frontend/src/store/avatar.ts:L1-L33](../frontend/src/store/avatar.ts#L1-L33) |
| 数字人形象 | SVG 汉服导游形象、口型、状态、提示语 | [DigitalAvatar frontend/src/components/Avatar/DigitalAvatar.vue:L1-L64](../frontend/src/components/Avatar/DigitalAvatar.vue#L1-L64) |
| 问答页 | 快捷问题、浏览器语音识别、语音播报、引用和路线卡片 | [ChatGuide frontend/src/pages/visitor/ChatGuide.vue:L1-L147](../frontend/src/pages/visitor/ChatGuide.vue#L1-L147) |
| 聊天面板 | 文字输入、语音按钮和快捷问题 | [ChatPanel frontend/src/components/ChatPanel.vue:L1-L49](../frontend/src/components/ChatPanel.vue#L1-L49) |
| 视觉样式 | 数字人、问答区、路线和引用区响应式布局 | [guide styles frontend/src/styles.css:L143-L437](../frontend/src/styles.css#L143-L437) |

### 验证命令

```powershell
python scripts\run_local.py build-frontend
python scripts\smoke_vue_full_stack.py
```

## REQ-009 GitHub 发布与版本交付

### 用户场景

开发者需要把“灵山数字导游”当前本地项目发布到自己的 GitHub 仓库，并保留 `v0.0` baseline tag，便于参赛交付、协作和回滚。

### 实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| 发布脚本 | 检查工作区、配置 GitHub remote、推送分支和 tags | [publish_github main scripts/publish_github.py:L56-L84](../scripts/publish_github.py#L56-L84) |
| 工作区保护 | 防止未提交改动被意外发布 | [ensure_clean_worktree scripts/publish_github.py:L38-L44](../scripts/publish_github.py#L38-L44) |
| 远程配置 | 新增或更新 `origin` 地址 | [configure_remote scripts/publish_github.py:L47-L53](../scripts/publish_github.py#L47-L53) |
| 发布文档 | GitHub 发布命令和 Git Bash 注意事项 | [docs/DEPLOY.md:L110-L132](./DEPLOY.md#L110-L132) |
| 测试文档 | 帮助命令验证方式 | [docs/test_reference.md:L148-L157](./test_reference.md#L148-L157) |

### 验证命令

```powershell
python scripts\publish_github.py --help
python scripts\publish_github.py --remote-url https://github.com/<your-name>/<repo>.git --branch main --push-tags
```

## REQ-007 后台知识库管理闭环

### 用户场景

管理员可以在后台上传、更新、删除景区讲解词、文史资料、FAQ 和数据表资料；系统保存资料后立即重建本地向量索引，游客端数字人问答可检索到新增内容。

### 实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| API 上传 | 接收 `multipart/form-data` 文件并保存入库 | [knowledge_upload backend/app/api/admin.py:L29-L36](../backend/app/api/admin.py#L29-L36) |
| API 更新 | 修改可编辑文本资料并重建索引 | [knowledge_update backend/app/api/admin.py:L39-L47](../backend/app/api/admin.py#L39-L47) |
| API 删除 | 删除后台上传资料并重建索引 | [knowledge_delete backend/app/api/admin.py:L50-L56](../backend/app/api/admin.py#L50-L56) |
| API 重建 | 手动触发知识库重建 | [knowledge_reindex backend/app/api/admin.py:L59-L61](../backend/app/api/admin.py#L59-L61) |
| 服务层 | 保存、更新、删除和列出后台资料 | [save_document backend/app/services/knowledge_service.py:L73-L90](../backend/app/services/knowledge_service.py#L73-L90), [update_document backend/app/services/knowledge_service.py:L93-L105](../backend/app/services/knowledge_service.py#L93-L105), [delete_document backend/app/services/knowledge_service.py:L108-L116](../backend/app/services/knowledge_service.py#L108-L116), [list_documents backend/app/services/knowledge_service.py:L143-L166](../backend/app/services/knowledge_service.py#L143-L166) |
| 向量入库 | 读取 `data/admin_knowledge` 中的后台资料并切片入向量库 | [load_admin_document_entries backend/app/services/vector_store.py:L150-L170](../backend/app/services/vector_store.py#L150-L170) |
| 前端页面 | 上传表单、文本维护、文档列表、重建索引和检索测试 | [KnowledgeManage frontend/src/pages/admin/KnowledgeManage.vue:L25-L118](../frontend/src/pages/admin/KnowledgeManage.vue#L25-L118), [KnowledgeManage template frontend/src/pages/admin/KnowledgeManage.vue:L132-L211](../frontend/src/pages/admin/KnowledgeManage.vue#L132-L211) |
| 测试 | 保存、更新、删除后台知识文档 | [test_save_update_delete_admin_knowledge_document backend/tests/test_knowledge_management.py:L7-L30](../backend/tests/test_knowledge_management.py#L7-L30) |

### 配置项

- 后台上传资料固定保存到 [ADMIN_KNOWLEDGE_DIR backend/app/services/vector_store.py:L15-L19](../backend/app/services/vector_store.py#L15-L19)，当前路径为 `data/admin_knowledge`。

### 验证命令

```powershell
python scripts\run_local.py test-backend
python scripts\run_local.py build-kb
python scripts\run_local.py build-frontend
```

### 影响范围

影响管理后台知识库页面、后台知识库 API、本地向量库构建、游客端 RAG 回答依据和文档检索测试。
