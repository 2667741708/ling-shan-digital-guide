# 数据结构与持久化说明

## DS-001 后台管理员表 `admin_user`

| 项目 | 内容 |
|---|---|
| 用途 | 保存后台管理员账号、PBKDF2 密码哈希、角色、启用状态和最近登录时间 |
| 模型 | [AdminUser backend/app/models/persistence.py:L51-L62](../backend/app/models/persistence.py#L51-L62) |
| 初始化 | [ensure_admin_user backend/app/services/auth_service.py:L55-L74](../backend/app/services/auth_service.py#L55-L74) |
| 初始化方式 | [init_db backend/app/core/database.py:L67-L76](../backend/app/core/database.py#L67-L76) |

## DS-002 知识文档表 `knowledge_document`

| 项目 | 内容 |
|---|---|
| 用途 | 保存知识文档主记录、所属知识库、当前版本、发布状态、存储路径、创建/更新人和软删除时间 |
| 状态 | `draft`、`active`、`archived`、`deleted` |
| 模型 | [KnowledgeDocument backend/app/models/persistence.py:L64-L99](../backend/app/models/persistence.py#L64-L99) |
| 列表查询 | [list_documents backend/app/services/knowledge_service.py:L410-L420](../backend/app/services/knowledge_service.py#L410-L420) |
| 当前版本嵌入状态 | [_document_payload backend/app/services/knowledge_service.py:L134-L159](../backend/app/services/knowledge_service.py#L134-L159) |

## DS-003 知识文档版本表 `knowledge_document_version`

| 项目 | 内容 |
|---|---|
| 用途 | 每次上传或编辑创建不可覆盖版本，保存版本号、内容哈希、版本文件路径、变更说明和创建人 |
| 模型 | [KnowledgeDocumentVersion backend/app/models/persistence.py:L102-L127](../backend/app/models/persistence.py#L102-L127) |
| 创建版本 | [save_document backend/app/services/knowledge_service.py:L187-L259](../backend/app/services/knowledge_service.py#L187-L259), [update_document backend/app/services/knowledge_service.py:L262-L325](../backend/app/services/knowledge_service.py#L262-L325) |
| 版本查询 | [list_versions backend/app/services/knowledge_service.py:L423-L454](../backend/app/services/knowledge_service.py#L423-L454) |
| 与 chunk 关联 | [KnowledgeChunk backend/app/models/persistence.py:L148-L179](../backend/app/models/persistence.py#L148-L179) |

## DS-004 知识操作日志表 `knowledge_operation_log`

| 项目 | 内容 |
|---|---|
| 用途 | 记录上传、更新、发布、归档、删除、重建索引等操作历史 |
| 模型 | [KnowledgeOperationLog backend/app/models/persistence.py:L182-L198](../backend/app/models/persistence.py#L182-L198) |
| 写入日志 | [_log backend/app/services/knowledge_service.py:L111-L128](../backend/app/services/knowledge_service.py#L111-L128) |
| 历史查询 | [list_history backend/app/services/knowledge_service.py:L457-L481](../backend/app/services/knowledge_service.py#L457-L481) |
| 关键动作 | `upload`、`update`、`publish`、`archive`、`delete`、`embed`、`reindex` |

## DS-005 数字人配置表 `avatar_config`

| 项目 | 内容 |
|---|---|
| 用途 | 保存当前启用的数字人名称、风格、服装、音色、语速、欢迎语和表情枚举 |
| 模型 | [AvatarConfig backend/app/models/persistence.py:L200-L213](../backend/app/models/persistence.py#L200-L213) |
| 默认配置 | [ensure_default_avatar backend/app/services/avatar_service.py:L35-L62](../backend/app/services/avatar_service.py#L35-L62) |
| 保存配置 | [save_avatar_config backend/app/services/avatar_service.py:L76-L99](../backend/app/services/avatar_service.py#L76-L99) |
| 初始化方式 | [init_db backend/app/core/database.py:L67-L76](../backend/app/core/database.py#L67-L76) |

## DS-006 知识库表 `knowledge_base`

| 项目 | 内容 |
|---|---|
| 用途 | 保存知识库元数据、向量后端、embedding 维度和启用状态 |
| 模型 | [KnowledgeBase backend/app/models/persistence.py:L130-L145](../backend/app/models/persistence.py#L130-L145) |
| 默认知识库创建 | [ensure_default_knowledge_base backend/app/services/vector_store.py:L303-L329](../backend/app/services/vector_store.py#L303-L329) |
| 后台列表接口 | [admin_knowledge_bases_v1 backend/app/api/v1.py:L245-L247](../backend/app/api/v1.py#L245-L247) |

## DS-007 知识块表 `knowledge_chunk`

| 项目 | 内容 |
|---|---|
| 用途 | 保存切片文本、来源、类别、token 数、embedding 向量以及是否启用到检索中 |
| PostgreSQL 列 | `embedding` 使用 `pgvector` 的 `vector(256)`，`embedding_payload` 仅保留调试导出所需的 JSON 向量副本 |
| 自定义列类型 | [PgVector / EmbeddingType backend/app/models/persistence.py:L18-L48](../backend/app/models/persistence.py#L18-L48) |
| 模型 | [KnowledgeChunk backend/app/models/persistence.py:L148-L179](../backend/app/models/persistence.py#L148-L179) |
| 静态资料入库 | [_persist_static_entries backend/app/services/vector_store.py:L347-L372](../backend/app/services/vector_store.py#L347-L372) |
| 文档版本嵌入 | [_upsert_document_version_chunks backend/app/services/vector_store.py:L392-L421](../backend/app/services/vector_store.py#L392-L421) |
| 文档嵌入入口 | [embed_document backend/app/services/vector_store.py:L434-L464](../backend/app/services/vector_store.py#L434-L464) |
| RAG 检索入口 | [retrieve_context backend/app/services/vector_store.py:L591-L614](../backend/app/services/vector_store.py#L591-L614) |
| 管理端嵌入接口 | [admin_document_embed_v1 backend/app/api/v1.py:L359-L372](../backend/app/api/v1.py#L359-L372) |

## DS-008 导出索引文件

| 项目 | 内容 |
|---|---|
| 文件 | `data/vector_db/scenic_vector_store.json` |
| 用途 | 当前作为数据库已启用 chunk 的导出视图，便于调试、审计和兼容旧脚本 |
| 导出入口 | [load_vector_store backend/app/services/vector_store.py:L548-L586](../backend/app/services/vector_store.py#L548-L586) |
| 重建入口 | [build_knowledge_base backend/app/services/vector_store.py:L467-L505](../backend/app/services/vector_store.py#L467-L505) |
