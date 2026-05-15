# 需求追踪

## REQ-001 DeepSeek + 本地知识库问答闭环

### 用户场景

游客通过文本向数字人提问，系统从本地景区资料检索依据，再调用 DeepSeek 生成适合语音播报的回答。

### 实现位置

| 类型 | 说明 | 跳转链接 |
|---|---|---|
| API 入口 | 游客文本问答接口 | [backend/app/api/visitor.py:L14-L21](../backend/app/api/visitor.py#L14-L21) |
| 服务编排 | RAG 检索、DeepSeek 调用、降级回答、真实延迟 | [chat_with_text backend/app/services/chat_service.py:L33-L86](../backend/app/services/chat_service.py#L33-L86) |
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

当前真实资料包构建结果为 `entry_count = 3364`。

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
