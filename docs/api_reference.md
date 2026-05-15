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
| 响应字段 | `query`, `chunks` |
| API 入口 | [knowledge_search_test backend/app/api/admin.py:L27-L28](../backend/app/api/admin.py#L27-L28) |
| 服务函数 | [search_test backend/app/services/knowledge_service.py:L38-L39](../backend/app/services/knowledge_service.py#L38-L39) |

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
