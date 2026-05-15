# API 说明

统一响应格式：

```json
{"code": 0, "message": "success", "data": {}}
```

## API-001 健康检查

| 项目 | 内容 |
|---|---|
| 方法与路径 | `GET /api/health` |
| 实现位置 | [health backend/app/main.py:L21-L23](../backend/app/main.py#L21-L23) |
| 响应字段 | `data.status` |
| 测试 | [test_health backend/tests/test_health.py:L6-L10](../backend/tests/test_health.py#L6-L10) |

## API-002 游客文本问答

| 项目 | 内容 |
|---|---|
| 方法与路径 | `POST /api/visitor/chat/text` |
| 请求字段 | `session_uuid`, `message`, `current_location` |
| 响应字段 | `answer`, `intent`, `emotion`, `model_used`, `audio_url`, `lip_sync`, `cards`, `references`, `latency_ms` |
| API 入口 | [text_chat backend/app/api/visitor.py:L20-L21](../backend/app/api/visitor.py#L20-L21) |
| 服务函数 | [chat_with_text backend/app/services/chat_service.py:L38-L88](../backend/app/services/chat_service.py#L38-L88) |
| 验证脚本 | [smoke_test main scripts/smoke_test.py:L41-L57](../scripts/smoke_test.py#L41-L57) |

示例请求：

```json
{"session_uuid": "demo", "message": "我只有两个小时喜欢历史和拍照怎么逛？"}
```

## API-003 后台知识库检索测试

| 项目 | 内容 |
|---|---|
| 方法与路径 | `POST /api/admin/knowledge/search-test` |
| 请求字段 | `query` |
| 鉴权 | `Authorization: Bearer <token>` |
| 响应字段 | `query`, `chunks` |
| API 入口 | [knowledge_search_test backend/app/api/admin.py:L121-L122](../backend/app/api/admin.py#L121-L122) |
| 服务函数 | [search_test backend/app/services/knowledge_service.py:L399-L400](../backend/app/services/knowledge_service.py#L399-L400) |

## API-011 管理员登录与身份校验

| 项目 | 内容 |
|---|---|
| 方法与路径 | `POST /api/admin/login`, `GET /api/admin/me` |
| 请求字段 | 登录：`username`, `password` |
| 响应字段 | 登录：`token`, `token_type`, `username`, `role` |
| API 入口 | [login backend/app/api/admin.py:L15-L16](../backend/app/api/admin.py#L15-L16), [me backend/app/api/admin.py:L20-L21](../backend/app/api/admin.py#L20-L21) |
| 服务函数 | [authenticate_admin backend/app/services/auth_service.py:L110-L131](../backend/app/services/auth_service.py#L110-L131), [require_admin_user backend/app/services/auth_service.py:L134-L145](../backend/app/services/auth_service.py#L134-L145) |
| 前端使用 | [loginAdmin frontend/src/api/admin.ts:L7-L8](../frontend/src/api/admin.ts#L7-L8), [AdminLogin frontend/src/pages/admin/AdminLogin.vue:L1-L46](../frontend/src/pages/admin/AdminLogin.vue#L1-L46) |

## API-007 后台知识文档上传

| 项目 | 内容 |
|---|---|
| 方法与路径 | `POST /api/admin/knowledge/upload` |
| 鉴权 | `Authorization: Bearer <token>` |
| 请求字段 | `multipart/form-data`: `file`, `title`, `change_note` |
| 响应字段 | `id`, `title`, `file_name`, `source`, `status=draft`, `current_version`, `version_count`, `history_count` |
| API 入口 | [knowledge_upload backend/app/api/admin.py:L39-L50](../backend/app/api/admin.py#L39-L50) |
| 服务函数 | [save_document backend/app/services/knowledge_service.py:L153-L213](../backend/app/services/knowledge_service.py#L153-L213) |
| 前端使用 | [uploadKnowledgeDocument frontend/src/api/admin.ts:L19-L25](../frontend/src/api/admin.ts#L19-L25) |

## API-008 后台知识文档更新

| 项目 | 内容 |
|---|---|
| 方法与路径 | `PUT /api/admin/knowledge/documents/{document_id}` |
| 鉴权 | `Authorization: Bearer <token>` |
| 请求字段 | `title`, `content`, `change_note` |
| 响应字段 | `id`, `title`, `source`, `status=draft`, `current_version` |
| API 入口 | [knowledge_update backend/app/api/admin.py:L54-L67](../backend/app/api/admin.py#L54-L67) |
| 服务函数 | [update_document backend/app/services/knowledge_service.py:L216-L262](../backend/app/services/knowledge_service.py#L216-L262) |
| 前端使用 | [updateKnowledgeDocument frontend/src/api/admin.ts:L27-L29](../frontend/src/api/admin.ts#L27-L29) |

## API-009 后台知识文档删除

| 项目 | 内容 |
|---|---|
| 方法与路径 | `DELETE /api/admin/knowledge/documents/{document_id}` |
| 鉴权 | `Authorization: Bearer <token>` |
| 请求字段 | path 参数 `document_id` |
| 响应字段 | `id`, `title`, `status`, `index_result` |
| API 入口 | [knowledge_delete backend/app/api/admin.py:L89-L94](../backend/app/api/admin.py#L89-L94) |
| 服务函数 | [delete_document backend/app/services/knowledge_service.py:L305-L324](../backend/app/services/knowledge_service.py#L305-L324) |
| 前端使用 | [deleteKnowledgeDocument frontend/src/api/admin.ts:L39-L41](../frontend/src/api/admin.ts#L39-L41) |

## API-010 后台知识库重建索引

| 项目 | 内容 |
|---|---|
| 方法与路径 | `POST /api/admin/knowledge/reindex` |
| 鉴权 | `Authorization: Bearer <token>` |
| 请求字段 | 无 |
| 响应字段 | `path`, `entry_count` |
| API 入口 | [knowledge_reindex backend/app/api/admin.py:L116-L117](../backend/app/api/admin.py#L116-L117) |
| 服务函数 | [rebuild_index backend/app/services/knowledge_service.py:L141-L150](../backend/app/services/knowledge_service.py#L141-L150) |
| 前端使用 | [reindexKnowledgeBase frontend/src/api/admin.ts:L51-L53](../frontend/src/api/admin.ts#L51-L53) |

## API-012 后台知识文档状态、版本和历史

| 项目 | 内容 |
|---|---|
| 方法与路径 | `GET /api/admin/knowledge/documents?status=all|draft|active|archived|deleted` |
| 版本与历史 | `GET /api/admin/knowledge/documents/{document_id}/versions`, `GET /api/admin/knowledge/documents/{document_id}/history` |
| 状态流转 | `POST /api/admin/knowledge/documents/{document_id}/publish`, `POST /api/admin/knowledge/documents/{document_id}/archive` |
| 鉴权 | `Authorization: Bearer <token>` |
| API 入口 | [knowledge_documents backend/app/api/admin.py:L30-L35](../backend/app/api/admin.py#L30-L35), [knowledge_publish backend/app/api/admin.py:L71-L76](../backend/app/api/admin.py#L71-L76), [knowledge_archive backend/app/api/admin.py:L80-L85](../backend/app/api/admin.py#L80-L85), [knowledge_versions backend/app/api/admin.py:L98-L103](../backend/app/api/admin.py#L98-L103), [knowledge_history backend/app/api/admin.py:L107-L112](../backend/app/api/admin.py#L107-L112) |
| 服务函数 | [list_documents backend/app/services/knowledge_service.py:L327-L337](../backend/app/services/knowledge_service.py#L327-L337), [publish_document backend/app/services/knowledge_service.py:L265-L282](../backend/app/services/knowledge_service.py#L265-L282), [archive_document backend/app/services/knowledge_service.py:L285-L302](../backend/app/services/knowledge_service.py#L285-L302), [list_versions backend/app/services/knowledge_service.py:L340-L369](../backend/app/services/knowledge_service.py#L340-L369), [list_history backend/app/services/knowledge_service.py:L372-L396](../backend/app/services/knowledge_service.py#L372-L396) |

## API-013 后台数字人配置

| 项目 | 内容 |
|---|---|
| 方法与路径 | `GET /api/admin/avatar-configs/active`, `POST /api/admin/avatar-configs` |
| 鉴权 | `Authorization: Bearer <token>` |
| 请求字段 | `name`, `avatar_style`, `clothes`, `voice_name`, `voice_speed`, `opening_text`, `expressions` |
| 响应字段 | 当前启用的数字人配置 |
| API 入口 | [active_avatar backend/app/api/admin.py:L126-L127](../backend/app/api/admin.py#L126-L127), [avatar_configs backend/app/api/admin.py:L131-L132](../backend/app/api/admin.py#L131-L132) |
| 服务函数 | [get_active_avatar backend/app/services/avatar_service.py:L65-L73](../backend/app/services/avatar_service.py#L65-L73), [save_avatar_config backend/app/services/avatar_service.py:L76-L99](../backend/app/services/avatar_service.py#L76-L99) |

## API-004 管理后台数据大屏

| 项目 | 内容 |
|---|---|
| 方法与路径 | `GET /api/admin/analytics/overview` |
| 响应字段 | `today_service_count`, `week_service_count`, `avg_latency_ms`, `satisfaction_score`, `knowledge_hit_rate`, `hot_questions`, `hot_spots`, `route_preferences`, `emotion_trend` |
| API 入口 | [analytics_overview backend/app/api/admin.py:L42-L43](../backend/app/api/admin.py#L42-L43) |
| 服务函数 | [dashboard_overview backend/app/services/analytics_service.py:L1-L31](../backend/app/services/analytics_service.py#L1-L31) |

## API-005 游客景点列表

| 项目 | 内容 |
|---|---|
| 方法与路径 | `GET /api/visitor/scenic-spots` |
| 响应字段 | `id`, `name`, `description`, `guide_text`, `map_x`, `map_y`, `tags`, `recommended_duration`, score 字段 |
| API 入口 | [scenic_spots backend/app/api/visitor.py:L35-L36](../backend/app/api/visitor.py#L35-L36) |
| 服务函数 | [list_scenic_spots backend/app/services/scenic_service.py:L228-L230](../backend/app/services/scenic_service.py#L228-L230) |
| 前端使用 | [fetchScenicSpots frontend/src/api/visitor.ts:L40-L42](../frontend/src/api/visitor.ts#L40-L42) |

## API-006 游客路线推荐

| 项目 | 内容 |
|---|---|
| 方法与路径 | `POST /api/visitor/routes/recommend` |
| 请求字段 | `session_uuid`, `interest`, `available_time`, `physical_strength`, `start_spot_id`, `avoid_crowd` |
| 响应字段 | `route_name`, `total_duration`, `spots`, `reason` |
| API 入口 | [routes_recommend backend/app/api/visitor.py:L39-L40](../backend/app/api/visitor.py#L39-L40) |
| 服务函数 | [recommend_route backend/app/services/route_service.py:L80-L116](../backend/app/services/route_service.py#L80-L116) |
| 前端使用 | [recommendRoute frontend/src/api/visitor.ts:L44-L53](../frontend/src/api/visitor.ts#L44-L53) |

## 验证命令

```powershell
python scripts\run_local.py smoke-backend
```
