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
| 服务函数 | [chat_with_text backend/app/services/chat_service.py:L33-L86](../backend/app/services/chat_service.py#L33-L86) |
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
| 响应字段 | `today_service_count`, `week_service_count`, `avg_latency_ms`, `satisfaction_score`, `knowledge_hit_rate`, `hot_questions`, `emotion_trend` |
| API 入口 | [analytics_overview backend/app/api/admin.py:L42-L43](../backend/app/api/admin.py#L42-L43) |
| 服务函数 | [dashboard_overview backend/app/services/analytics_service.py:TODO-LINES](../backend/app/services/analytics_service.py) |

## 验证命令

```powershell
python scripts\run_local.py smoke-backend
```
