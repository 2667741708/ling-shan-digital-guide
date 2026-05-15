# Project Onboarding

## 1. 项目目标

LingTour AI 是面向中国软件杯 A5 景区导览服务 AI 数字人赛题的工程项目，当前阶段目标是跑通游客问答、DeepSeek RAG、本地知识库、数字人演示端和管理大屏基础数据。

## 2. 当前包含

- DeepSeek 文本问答：[chat_with_text backend/app/services/chat_service.py:L33-L86](../backend/app/services/chat_service.py#L33-L86)
- 本地知识库和向量检索：[retrieve_context backend/app/services/vector_store.py:L252-L273](../backend/app/services/vector_store.py#L252-L273)
- 管理后台知识库检索测试：[knowledge_search_test backend/app/api/admin.py:L27-L28](../backend/app/api/admin.py#L27-L28)
- 无 npm 依赖静态演示端：[frontend_static/index.html:L170-L218](../frontend_static/index.html#L170-L218)
- 完整栈烟测：[main scripts/smoke_full_stack.py:L30-L61](../scripts/smoke_full_stack.py#L30-L61)

## 3. 当前不包含

- 真实 ASR/TTS 音频生成仍是 P1。
- Live2D 数字人仍是 P1。
- PostgreSQL 会话持久化仍是 P1。
- ChromaDB / SentenceTransformer 可作为 P2 增强，不是当前 P0 依赖。

## 4. 新同事阅读顺序

1. [协作规则](../AGENTS.md)
2. [需求追踪](./requirements_traceability.md)
3. [程序索引](./program_index.md)
4. [API 说明](./api_reference.md)
5. [配置字段](./config_reference.md)
6. [测试方式](./test_reference.md)
7. [排错经验](./troubleshooting.md)
8. [项目交互与运行指南](./user_interaction_guide.md)
9. [RAG 与知识库说明](./rag_knowledge_guide.md)

## 5. 常见任务入口

| 任务 | 先看文档 | 代码入口 |
|---|---|---|
| 修改问答逻辑 | [REQ-001](./requirements_traceability.md#req-001-deepseek--本地知识库问答闭环) | [chat_with_text backend/app/services/chat_service.py:L33-L86](../backend/app/services/chat_service.py#L33-L86) |
| 补充景区资料 | [REQ-002](./requirements_traceability.md#req-002-本地知识库和轻量向量库) | [data/raw_documents/demo_scenic_guide.md:L1-L25](../data/raw_documents/demo_scenic_guide.md#L1-L25) |
| 启动本地演示 | [TEST-006](./test_reference.md#test-006-完整栈烟测) | [main scripts/smoke_full_stack.py:L30-L61](../scripts/smoke_full_stack.py#L30-L61) |
| 排查 npm 失败 | [TRB-001](./troubleshooting.md#trb-001-前端-npm-install-超时或-econnreset) | [frontend/.npmrc:L1-L4](../frontend/.npmrc#L1-L4) |
