# 程序索引

## 核心后端服务

| 程序 | 文件职责 | 核心符号 |
|---|---|---|
| DeepSeek 客户端 | 读取本地 API Key，调用 DeepSeek OpenAI 兼容接口 | [DeepSeekClient backend/app/services/deepseek_service.py:L9-L47](../backend/app/services/deepseek_service.py#L9-L47) |
| 游客问答编排 | 创建会话、文本/语音/图片问答，串联 RAG 与 DeepSeek | [chat_with_text backend/app/services/chat_service.py:L33-L86](../backend/app/services/chat_service.py#L33-L86) |
| 知识库服务 | 为 API 层提供检索、文档列表、检索测试 | [retrieve_context backend/app/services/knowledge_service.py:L5-L18](../backend/app/services/knowledge_service.py#L5-L18) |
| 本地向量库 | 基于 CSV/Markdown 生成 JSON 向量库并检索 | [build_knowledge_base backend/app/services/vector_store.py:L223-L243](../backend/app/services/vector_store.py#L223-L243), [retrieve_context backend/app/services/vector_store.py:L252-L273](../backend/app/services/vector_store.py#L252-L273) |
| 真实资料包读取 | 读取灵山公开资料包 docx/xlsx，xlsx 限量抽取避免超时 | [load_scenic_pack_entries backend/app/services/vector_store.py:L191-L216](../backend/app/services/vector_store.py#L191-L216), [extract_xlsx_text backend/app/services/vector_store.py:L151-L188](../backend/app/services/vector_store.py#L151-L188) |
| FastAPI 入口 | 注册游客端、管理端和健康检查接口 | [create_app backend/app/main.py:L9-L28](../backend/app/main.py#L9-L28) |

## 运行与验证脚本

| 程序 | 文件职责 | 核心符号 |
|---|---|---|
| 本地 runner | 环境检查、依赖安装、构建知识库、测试和服务启动 | [main scripts/run_local.py:L149-L189](../scripts/run_local.py#L149-L189) |
| 后端烟测 | 调用 health、知识库检索、游客问答 | [main scripts/smoke_test.py:L41-L57](../scripts/smoke_test.py#L41-L57) |
| 完整栈烟测 | 启动后端和静态前端后运行 API 烟测 | [main scripts/smoke_full_stack.py:L30-L61](../scripts/smoke_full_stack.py#L30-L61) |
| Vue 完整栈烟测 | 启动 FastAPI 与 Vite dev server，验证真实 Vue 工程 | [main scripts/smoke_vue_full_stack.py:L56-L94](../scripts/smoke_vue_full_stack.py#L56-L94) |
| 静态前端服务 | 用 Python http.server 服务无依赖演示端 | [main scripts/serve_static_frontend.py:L14-L23](../scripts/serve_static_frontend.py#L14-L23) |
| DeepSeek 多智能体生成器 | 生成架构、后端、前端、AI/RAG、测试文档建议 | [main scripts/deepseek_multi_agent.py:L203-L240](../scripts/deepseek_multi_agent.py#L203-L240) |

## 前端入口

| 程序 | 文件职责 | 核心位置 |
|---|---|---|
| Vue 数字人页 | Vue 工程游客问答页面 | [frontend/src/pages/visitor/ChatGuide.vue:TODO-LINES](../frontend/src/pages/visitor/ChatGuide.vue) |
| Vue 应用入口 | 注册 Pinia 和 Router，避免未使用 Element Plus 类型污染 | [frontend/src/main.ts:L1-L9](../frontend/src/main.ts#L1-L9) |
| 静态演示端 | 在 npm 网络异常时保证端到端演示可用 | [frontend_static/index.html:L170-L218](../frontend_static/index.html#L170-L218) |

## 修改风险

- 修改 [chat_with_text backend/app/services/chat_service.py:L33-L86](../backend/app/services/chat_service.py#L33-L86) 会影响游客问答、语音问答复用逻辑和 smoke 测试。
- 修改 [retrieve_context backend/app/services/vector_store.py:L252-L273](../backend/app/services/vector_store.py#L252-L273) 会影响知识库命中率和回答依据。
- 修改 [run_local.py 命令分发 scripts/run_local.py:L149-L189](../scripts/run_local.py#L149-L189) 会影响部署、测试和服务器运行流程。
