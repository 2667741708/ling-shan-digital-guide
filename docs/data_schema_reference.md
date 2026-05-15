# 数据结构与持久化说明

## DS-001 后台管理员表 `admin_user`

| 项目 | 内容 |
|---|---|
| 用途 | 保存后台管理员账号、PBKDF2 密码哈希、角色、启用状态和最近登录时间 |
| 模型 | [AdminUser backend/app/models/persistence.py:L16-L27](../backend/app/models/persistence.py#L16-L27) |
| 初始化 | [ensure_admin_user backend/app/services/auth_service.py:L55-L74](../backend/app/services/auth_service.py#L55-L74) |
| SQL | [scripts/init_db.sql:L38-L48](../scripts/init_db.sql#L38-L48) |

## DS-002 知识文档表 `knowledge_document`

| 项目 | 内容 |
|---|---|
| 用途 | 保存知识文档主记录、当前版本、发布状态、存储路径、创建/更新人和软删除时间 |
| 状态 | `draft`、`active`、`archived`、`deleted` |
| 模型 | [KnowledgeDocument backend/app/models/persistence.py:L29-L57](../backend/app/models/persistence.py#L29-L57) |
| 列表查询 | [list_documents backend/app/services/knowledge_service.py:L327-L337](../backend/app/services/knowledge_service.py#L327-L337) |
| SQL | [scripts/init_db.sql:L50-L63](../scripts/init_db.sql#L50-L63) |

## DS-003 知识文档版本表 `knowledge_document_version`

| 项目 | 内容 |
|---|---|
| 用途 | 每次上传或编辑创建不可覆盖版本，保存版本号、内容哈希、版本文件路径、变更说明和创建人 |
| 模型 | [KnowledgeDocumentVersion backend/app/models/persistence.py:L59-L79](../backend/app/models/persistence.py#L59-L79) |
| 创建版本 | [save_document backend/app/services/knowledge_service.py:L153-L213](../backend/app/services/knowledge_service.py#L153-L213), [update_document backend/app/services/knowledge_service.py:L216-L262](../backend/app/services/knowledge_service.py#L216-L262) |
| 版本查询 | [list_versions backend/app/services/knowledge_service.py:L340-L369](../backend/app/services/knowledge_service.py#L340-L369) |
| SQL | [scripts/init_db.sql:L66-L80](../scripts/init_db.sql#L66-L80) |

## DS-004 知识操作日志表 `knowledge_operation_log`

| 项目 | 内容 |
|---|---|
| 用途 | 记录上传、更新、发布、归档、删除、重建索引等操作历史 |
| 模型 | [KnowledgeOperationLog backend/app/models/persistence.py:L81-L97](../backend/app/models/persistence.py#L81-L97) |
| 写入日志 | [_log backend/app/services/knowledge_service.py:L96-L105](../backend/app/services/knowledge_service.py#L96-L105) |
| 历史查询 | [list_history backend/app/services/knowledge_service.py:L372-L396](../backend/app/services/knowledge_service.py#L372-L396) |
| SQL | [scripts/init_db.sql:L82-L92](../scripts/init_db.sql#L82-L92) |

## DS-005 数字人配置表 `avatar_config`

| 项目 | 内容 |
|---|---|
| 用途 | 保存当前启用的数字人名称、风格、服装、音色、语速、欢迎语和表情枚举 |
| 模型 | [AvatarConfig backend/app/models/persistence.py:L99-L112](../backend/app/models/persistence.py#L99-L112) |
| 默认配置 | [ensure_default_avatar backend/app/services/avatar_service.py:L35-L62](../backend/app/services/avatar_service.py#L35-L62) |
| 保存配置 | [save_avatar_config backend/app/services/avatar_service.py:L76-L99](../backend/app/services/avatar_service.py#L76-L99) |
| SQL | [scripts/init_db.sql:L94-L108](../scripts/init_db.sql#L94-L108) |

## DS-006 向量索引文件

| 项目 | 内容 |
|---|---|
| 文件 | `data/vector_db/scenic_vector_store.json` |
| 用途 | 保存轻量本地 JSON 向量索引。数据库保存事实源与版本历史，向量文件保存检索索引 |
| 构建入口 | [build_knowledge_base backend/app/services/vector_store.py:L257-L277](../backend/app/services/vector_store.py#L257-L277) |
| 后台文档入库 | [load_admin_document_entries backend/app/services/vector_store.py:L150-L201](../backend/app/services/vector_store.py#L150-L201) |
| 检索入口 | [retrieve_context backend/app/services/vector_store.py:L286-L307](../backend/app/services/vector_store.py#L286-L307) |
