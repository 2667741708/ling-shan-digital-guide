# 观众个性化评分功能

## 概述

为灵山景区后台程序添加了观众对景点的个性化评分功能，支持用户提交、查看和管理景点评分。

## 功能特性

### 1. 多维度评分体系
- **综合评分** (overall_rating): 1-5 分必填
- **文化体验评分** (culture_rating): 1-5 分可选
- **自然景观评分** (nature_rating): 1-5 分可选
- **拍照价值评分** (photo_rating): 1-5 分可选
- **设施便利评分** (facility_rating): 1-5 分可选

### 2. 丰富的上下文信息
- 文字反馈 (comment)
- 用户标签 (user_tags): 用于个性化推荐
- 访问日期 (visit_date)
- 天气状况 (weather_condition)
- 拥挤程度 (crowd_level)
- 公开分享选项 (is_public)

### 3. API 接口

#### 提交/更新评分
```http
POST /api/visitor/ratings
Content-Type: application/json

{
  "session_uuid": "abc123",
  "spot_id": 6,
  "overall_rating": 5,
  "culture_rating": 4,
  "nature_rating": 3,
  "photo_rating": 5,
  "facility_rating": 4,
  "comment": "九龙灌浴表演非常精彩，值得观看！",
  "user_tags": ["必看", "适合拍照"],
  "visit_date": "2024-01-15",
  "weather_condition": "晴朗",
  "crowd_level": "中等",
  "is_public": true
}
```

#### 查看用户评分历史
```http
GET /api/visitor/sessions/{session_uuid}/ratings
```

#### 查看景点评分统计
```http
GET /api/visitor/spots/{spot_id}/ratings/stats
```

响应示例：
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "spot_id": 6,
    "total_ratings": 128,
    "average_overall": 4.52,
    "average_culture": 4.35,
    "average_nature": 3.80,
    "average_photo": 4.75,
    "average_facility": 4.10
  }
}
```

## 数据模型

### VisitorSpotRating 表结构

| 字段 | 类型 | 说明 |
|------|------|------|
| id | VARCHAR(32) | 主键 ID |
| session_uuid | VARCHAR(64) | 用户会话 ID |
| spot_id | INT | 景点 ID (外键) |
| overall_rating | INT | 综合评分 (1-5) |
| culture_rating | INT | 文化评分 (1-5, 可选) |
| nature_rating | INT | 自然评分 (1-5, 可选) |
| photo_rating | INT | 拍照评分 (1-5, 可选) |
| facility_rating | INT | 设施评分 (1-5, 可选) |
| comment | TEXT | 文字反馈 |
| user_tags | JSONB | 用户标签数组 |
| visit_date | TIMESTAMP | 访问日期 |
| weather_condition | VARCHAR(40) | 天气状况 |
| crowd_level | VARCHAR(40) | 拥挤程度 |
| is_public | BOOLEAN | 是否公开 |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

## 后续优化方向

1. **个性化推荐增强**: 基于用户历史评分优化路线推荐算法
2. **评分权重**: 根据用户可信度、访问时间等因素调整评分权重
3. **情感分析**: 对文字评论进行 NLP 情感分析
4. **评分趋势**: 分析景点评分随时间的变化趋势
5. **用户画像**: 基于评分行为构建用户兴趣画像

## 文件清单

- `backend/app/models/persistence.py`: 添加 VisitorSpotRating 模型
- `backend/app/schemas/visitor.py`: 添加评分请求/响应 Schema
- `backend/app/services/rating_service.py`: 评分业务逻辑服务
- `backend/app/api/visitor.py`: 添加评分相关 API 端点
- `backend/app/models/__init__.py`: 导出新模型
- `scripts/init_db.sql`: 数据库建表脚本
