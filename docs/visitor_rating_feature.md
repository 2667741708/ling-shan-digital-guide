# 游客个性化评分功能

本功能已纳入 [REQ-021 游客个性化评分、路线反哺与数据大屏](./requirements_traceability.md#req-021-游客个性化评分路线反哺与数据大屏)。项目统一使用“游客”，不再使用“观众”称谓。

## 功能范围

游客可以对景点提交综合、文化、自然、拍照、设施五类评分，并附带评论、标签、公开标记、访问上下文、画像快照和来源。后端按 `session_uuid + spot_id` 唯一约束执行 upsert，评分会进入路线推荐、公开评论、后台排行、情绪趋势、游客感受度报告和数据大屏。后台可对公开评论执行通过、隐藏或拒绝。

## API

| 场景 | 方法与路径 | 实现位置 |
|---|---|---|
| 提交或更新评分 | `POST /api/v1/visitor/ratings` | [submit_rating_v1 backend/app/api/v1.py:L232-L235](../backend/app/api/v1.py#L232-L235) |
| 查询会话评分 | `GET /api/v1/visitor/sessions/{session_uuid}/ratings` | [session_ratings_v1 backend/app/api/v1.py:L238-L241](../backend/app/api/v1.py#L238-L241) |
| 景点评分统计 | `GET /api/v1/visitor/spots/{spot_id}/ratings/stats` | [spot_rating_stats_v1 backend/app/api/v1.py:L244-L246](../backend/app/api/v1.py#L244-L246) |
| 公开评论列表 | `GET /api/v1/visitor/spots/{spot_id}/ratings/public` | [spot_public_ratings_v1 backend/app/api/v1.py:L249-L252](../backend/app/api/v1.py#L249-L252) |
| 后台评分列表 | `GET /api/v1/admin/ratings` | [admin_ratings_v1 backend/app/api/v1.py:L283-L313](../backend/app/api/v1.py#L283-L313) |
| 后台评分排行 | `GET /api/v1/admin/ratings/ranking` | [admin_rating_ranking_v1 backend/app/api/v1.py:L316-L317](../backend/app/api/v1.py#L316-L317) |
| 后台评分趋势 | `GET /api/v1/admin/ratings/trend` | [admin_rating_trend_v1 backend/app/api/v1.py:L321-L322](../backend/app/api/v1.py#L321-L322) |
| 游客感受度报告 | `GET /api/v1/admin/ratings/report` | [admin_rating_report_v1 backend/app/api/v1.py:L326-L333](../backend/app/api/v1.py#L326-L333) |
| 公开评论审核 | `PUT /api/v1/admin/ratings/{rating_id}/review` | [admin_rating_review_v1 backend/app/api/v1.py:L336-L354](../backend/app/api/v1.py#L336-L354) |

## 数据模型

| 项目 | 实现位置 |
|---|---|
| 评分表 | [VisitorSpotRating backend/app/models/persistence.py:L306-L354](../backend/app/models/persistence.py#L306-L354) |
| 请求模型 | [SpotRatingRequest backend/app/schemas/visitor.py:L25-L41](../backend/app/schemas/visitor.py#L25-L41) |
| 响应模型 | [SpotRatingResponse backend/app/schemas/visitor.py:L44-L67](../backend/app/schemas/visitor.py#L44-L67) |
| 初始化 SQL | [scripts/init_db.sql:L207-L231](../scripts/init_db.sql#L207-L231) |

## 前端入口

| 页面 | 实现位置 |
|---|---|
| 游客端评分面板 | [ChatGuide rating frontend/src/pages/visitor/ChatGuide.vue:L183-L211](../frontend/src/pages/visitor/ChatGuide.vue#L183-L211) |
| 游客端 API 封装 | [visitor rating API frontend/src/api/visitor.ts:L29-L56](../frontend/src/api/visitor.ts#L29-L56), [submitSpotRating frontend/src/api/visitor.ts:L87-L97](../frontend/src/api/visitor.ts#L87-L97) |
| 管理大屏评分模块 | [AdminDashboard frontend/src/pages/admin/AdminDashboard.vue:L28-L109](../frontend/src/pages/admin/AdminDashboard.vue#L28-L109) |
| 评分运营页 | [AdminRatings frontend/src/pages/admin/AdminRatings.vue:L1-L167](../frontend/src/pages/admin/AdminRatings.vue#L1-L167) |
| 后台评分 API 封装 | [admin rating API frontend/src/api/admin.ts:L7-L24](../frontend/src/api/admin.ts#L7-L24) |

## 验证命令

```powershell
python scripts\run_local.py test-backend
python scripts\run_local.py build-frontend
python scripts\check_doc_links.py
```
