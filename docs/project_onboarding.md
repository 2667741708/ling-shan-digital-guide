# Project Onboarding

## 1. 项目目标

LingTour AI 是面向中国软件杯 A5 景区导览服务 AI 数字人赛题的工程项目，当前阶段目标是跑通游客问答、DeepSeek RAG、版本化知识库、后台权限、数字人配置、真实地图和管理大屏基础数据。

## 2. 当前包含

- DeepSeek 文本问答：[chat_with_text backend/app/services/chat_service.py:L38-L88](../backend/app/services/chat_service.py#L38-L88)
- 本地知识库和向量检索：[retrieve_context backend/app/services/vector_store.py:L252-L273](../backend/app/services/vector_store.py#L252-L273)
- 灵山真实景点和路线：[SCENIC_SPOTS backend/app/services/scenic_service.py:L14-L225](../backend/app/services/scenic_service.py#L14-L225)、[recommend_route backend/app/services/route_service.py:L80-L116](../backend/app/services/route_service.py#L80-L116)
- 数字人灵灵和真实地图：[DigitalAvatar frontend/src/components/Avatar/DigitalAvatar.vue:L1-L64](../frontend/src/components/Avatar/DigitalAvatar.vue#L1-L64)、[ScenicMapView frontend/src/components/ScenicMapView.vue:L1-L101](../frontend/src/components/ScenicMapView.vue#L1-L101)
- 管理后台登录、知识库版本化和发布流转：[login backend/app/api/admin.py:L15-L16](../backend/app/api/admin.py#L15-L16)、[publish_document backend/app/services/knowledge_service.py:L265-L282](../backend/app/services/knowledge_service.py#L265-L282)
- 数据库持久化模型：[persistence models backend/app/models/persistence.py:L16-L112](../backend/app/models/persistence.py#L16-L112)
- 无 npm 依赖静态演示端：[frontend_static/index.html:L170-L218](../frontend_static/index.html#L170-L218)
- 完整栈烟测：[main scripts/smoke_full_stack.py:L30-L61](../scripts/smoke_full_stack.py#L30-L61)

## 3. 当前不包含

- 真实 ASR/TTS 音频生成仍是 P1。
- Live2D 数字人仍是 P1。
- Docker PostgreSQL 配置已提供，完整 Compose 端到端仍需单独验收。
- ChromaDB / SentenceTransformer 可作为 P2 增强，不是当前 P0 依赖。
- 图片识景接口仍是演示逻辑，真实多模态模型接入是 P1，详见 [实现缺口核查 docs/implementation_gap_audit.md:L1-L51](./implementation_gap_audit.md#L1-L51)。

## 4. 新同事阅读顺序

1. [协作规则](../AGENTS.md)
2. [需求追踪](./requirements_traceability.md)
3. [程序索引](./program_index.md)
4. [API 说明](./api_reference.md)
5. [配置字段](./config_reference.md)
6. [数据结构](./data_schema_reference.md)
7. [测试方式](./test_reference.md)
8. [排错经验](./troubleshooting.md)
9. [项目交互与运行指南](./user_interaction_guide.md)
10. [RAG 与知识库说明](./rag_knowledge_guide.md)

## 5. 常见任务入口

| 任务 | 先看文档 | 代码入口 |
|---|---|---|
| 修改问答逻辑 | [REQ-001](./requirements_traceability.md#req-001-deepseek--本地知识库问答闭环) | [chat_with_text backend/app/services/chat_service.py:L38-L88](../backend/app/services/chat_service.py#L38-L88) |
| 补充景区资料 | [REQ-002](./requirements_traceability.md#req-002-本地知识库和轻量向量库) | [data/raw_documents/demo_scenic_guide.md:L1-L25](../data/raw_documents/demo_scenic_guide.md#L1-L25) |
| 修改真实地图 | [REQ-005](./requirements_traceability.md#req-005-灵山真实景点地图与路线导览) | [ScenicMapView frontend/src/components/ScenicMapView.vue:L1-L101](../frontend/src/components/ScenicMapView.vue#L1-L101) |
| 修改数字人灵灵 | [REQ-006](./requirements_traceability.md#req-006-数字人灵灵真实前端交互体验) | [DigitalAvatar frontend/src/components/Avatar/DigitalAvatar.vue:L1-L64](../frontend/src/components/Avatar/DigitalAvatar.vue#L1-L64) |
| 修改后台知识库发布机制 | [REQ-007](./requirements_traceability.md#req-007-后台知识库管理闭环) | [knowledge_service.py:L153-L324](../backend/app/services/knowledge_service.py#L153-L324) |
| 修改后台权限或数据库 | [REQ-008](./requirements_traceability.md#req-008-后台权限版本化知识库与数据库持久化) | [auth_service.py:L32-L145](../backend/app/services/auth_service.py#L32-L145)、[database.py:L33-L69](../backend/app/core/database.py#L33-L69) |
| 启动本地演示 | [TEST-006](./test_reference.md#test-006-完整栈烟测) | [main scripts/smoke_full_stack.py:L30-L61](../scripts/smoke_full_stack.py#L30-L61) |
| 排查 npm 失败 | [TRB-001](./troubleshooting.md#trb-001-前端-npm-install-超时或-econnreset) | [frontend/.npmrc:L1-L4](../frontend/.npmrc#L1-L4) |
