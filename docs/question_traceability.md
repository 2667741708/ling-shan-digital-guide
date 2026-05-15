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
| RAG 编排 | 检索知识库并生成回答 | [chat_with_text backend/app/services/chat_service.py:L33-L86](../backend/app/services/chat_service.py#L33-L86) |
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
| 后端问答服务 | RAG + DeepSeek 问答编排 | [chat_with_text backend/app/services/chat_service.py:L33-L86](../backend/app/services/chat_service.py#L33-L86) |

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
| 问答增强 | 检索片段注入 DeepSeek prompt | [chat_with_text backend/app/services/chat_service.py:L33-L86](../backend/app/services/chat_service.py#L33-L86) |
| 说明文档 | RAG 与知识库说明 | [docs/rag_knowledge_guide.md:L1-L92](./rag_knowledge_guide.md#L1-L92) |

### 验证命令

```bash
python scripts/run_local.py build-kb
python scripts/run_local.py smoke-backend
```
