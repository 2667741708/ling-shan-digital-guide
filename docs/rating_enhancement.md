# 评分权重与情感分析集成文档

## 概述

本文档描述灵山项目后台程序中观众个性化评分系统的增强功能，包括：
1. **情感分析机制** - 自动分析用户评论的情感倾向
2. **评分权重机制** - 基于多维度因素计算评分可信度权重
3. **推荐系统集成** - 将评分数据用于个性化路线推荐优化

## 核心功能

### 1. 情感分析 (`analyze_sentiment`)

#### 功能说明
对用户提交的文字评论进行情感分析，识别正面、负面或中性情感。

#### 算法特点
- **关键词匹配**: 内置正面/负面情感词库
- **程度副词识别**: 识别"非常"、"特别"等强化词，权重×1.5
- **否定词处理**: 识别"不"、"没"等否定词，情感反转但减弱
- **置信度评估**: 基于检测到的情感词数量计算置信度

#### 返回值
```python
{
    "sentiment": "positive",  # 或 "negative", "neutral"
    "score": 0.85,            # -1.0 到 1.0 之间
    "confidence": 0.8,        # 0.0 到 1.0 之间
    "keywords": ["漂亮", "值得", "推荐"]  # 检测到的情感词
}
```

#### 使用示例
```python
from app.services.rating_service import analyze_sentiment

result = analyze_sentiment("非常漂亮，很值得推荐！")
# {'sentiment': 'positive', 'score': 1.0, 'confidence': 0.6, 'keywords': ['漂亮', '值得', '推荐']}
```

### 2. 评分权重计算 (`calculate_rating_weight`)

#### 权重因素
评分权重范围：0.5 - 1.5，考虑以下因素：

| 因素 | 权重范围 | 说明 |
|------|---------|------|
| 评分完整性 | +0.0 ~ +0.2 | 填写的维度评分越多，权重越高 |
| 文字反馈长度 | +0.0 ~ +0.2 | 评论越长，权重越高 |
| 情感一致性 | -0.1 ~ +0.1 | 评分与评论情感一致则加分 |
| 公开分享 | +0.05 | 公开分享的评分略高 |
| 用户历史可信度 | -0.1 ~ +0.1 | 基于历史评分的稳定性 |

#### 使用示例
```python
from app.services.rating_service import calculate_rating_weight

weight = calculate_rating_weight(rating, user_history)
# 返回 0.5-1.5 之间的浮点数
```

### 3. 景点统计增强 (`get_spot_statistics`)

#### 新增字段
- `weighted_average_overall`: 加权平均分
- `sentiment_distribution`: 情感分布统计

#### 返回示例
```json
{
    "spot_id": 1,
    "total_ratings": 150,
    "average_overall": 4.25,
    "weighted_average_overall": 4.38,
    "sentiment_distribution": {
        "positive": 95,
        "neutral": 40,
        "negative": 15
    }
}
```

### 4. 用户偏好画像 (`get_user_preference_profile`)

#### 功能说明
基于用户历史评分生成偏好画像，用于个性化推荐。

#### 返回字段
- `preferred_dimensions`: 用户最关注的评分维度 (如 culture, photo)
- `average_ratings_by_dimension`: 各维度的平均评分
- `preference_tags`: 从评论中提取的偏好标签
- `rating_pattern`: 用户评分模式 (strict/lenient/balanced)
- `total_ratings`: 总评分数量

#### 使用示例
```python
profile = get_user_preference_profile(db, session_uuid)
# {
#     "preferred_dimensions": ["culture", "photo"],
#     "average_ratings_by_dimension": {"overall": 4.2, "culture": 4.5},
#     "preference_tags": ["漂亮", "壮观", "文化"],
#     "rating_pattern": "balanced",
#     "total_ratings": 8
# }
```

### 5. 推荐系统集成 (`score_spot`)

#### 增强功能
在原有评分公式基础上，增加用户偏好调整：

1. **标签匹配奖励** (+0.0 ~ +0.15): 景点标签与用户偏好标签匹配
2. **维度偏好奖励** (+0.0 ~ +0.12): 用户关注维度得分高时加分
3. **评分模式调整** (-0.03 ~ +0.05): 根据用户评分模式微调

#### 使用示例
```python
from ai_service.route.route_recommender import score_spot

user_profile = {
    "preference_tags": ["漂亮", "壮观"],
    "preferred_dimensions": ["culture", "photo"],
    "rating_pattern": "balanced"
}

score = score_spot(spot, interests=['culture'], user_preference_profile=user_profile)
```

## API 接口

### 新增端点

#### 1. 获取用户偏好画像
```
GET /api/visitor/sessions/{session_uuid}/preference-profile
```

**响应示例:**
```json
{
    "code": 0,
    "message": "success",
    "data": {
        "preferred_dimensions": ["culture", "photo"],
        "average_ratings_by_dimension": {"overall": 4.2},
        "preference_tags": ["漂亮", "壮观"],
        "rating_pattern": "balanced",
        "total_ratings": 5
    }
}
```

#### 2. 分析评论情感
```
POST /api/visitor/sentiment/analyze?comment=非常漂亮的景点
```

**响应示例:**
```json
{
    "code": 0,
    "message": "success",
    "data": {
        "sentiment": "positive",
        "score": 1.0,
        "confidence": 0.6,
        "keywords": ["漂亮"]
    }
}
```

#### 3. 景点评分统计 (增强版)
```
GET /api/visitor/spots/{spot_id}/ratings/stats
```

**响应示例:**
```json
{
    "code": 0,
    "message": "success",
    "data": {
        "spot_id": 1,
        "total_ratings": 150,
        "average_overall": 4.25,
        "average_culture": 4.5,
        "average_nature": 3.8,
        "average_photo": 4.6,
        "average_facility": 4.0,
        "weighted_average_overall": 4.38,
        "sentiment_distribution": {
            "positive": 95,
            "neutral": 40,
            "negative": 15
        }
    }
}
```

## 技术实现细节

### 情感词库

#### 正面词汇 (部分)
好、棒、美、赞、喜欢、值得、推荐、满意、不错、精彩、震撼、壮观、漂亮、愉快、开心、完美、优秀、出色、迷人、有趣、好玩、舒适、方便、干净、整洁、热情、友好、专业

#### 负面词汇 (部分)
差、糟、丑、失望、不满、不好、讨厌、避免、坑、贵、脏、乱、吵、挤、累、远、慢、旧、破、糟糕、无聊、一般、普通、勉强、凑合、还行、不过如此、浪费时间

#### 程度副词
非常、特别、极其、十分、太、很、超级、格外、异常

#### 否定词
不、没、无、非、未、别、莫、勿

### 权重计算公式

```
base_weight = 1.0

# 1. 完整性 bonus
completeness_bonus = (filled_dimensions / 4) * 0.2

# 2. 评论长度 bonus
if len(comment) > 50: length_bonus = 0.2
elif len(comment) > 20: length_bonus = 0.15
elif len(comment) > 10: length_bonus = 0.1
else: length_bonus = 0.05

# 3. 情感一致性
consistency = 1.0 - abs(normalized_rating - sentiment_score)
if consistency > 0.8: consistency_bonus = 0.1
elif consistency < 0.4: consistency_bonus = -0.1

# 4. 公开分享
public_bonus = 0.05 if is_public else 0

# 5. 历史可信度
std_dev = standard_deviation(user_history_ratings)
if 0.5 <= std_dev <= 1.5: history_bonus = 0.1
elif std_dev < 0.5: history_bonus = 0.05
elif std_dev > 2.0: history_bonus = -0.1

final_weight = clamp(base_weight + all_bonuses, 0.5, 1.5)
```

### 推荐分数调整公式

```
base_score = 0.30*interest + 0.20*popularity + 0.15*culture + 
             0.15*nature + 0.10*photo + 0.10*facility - 
             0.15*distance - 0.10*crowd

# 用户偏好调整
tag_match_bonus = min(count(matching_tags) * 0.05, 0.15)
dim_bonus = min(sum(high_scoring_preferred_dims * 0.08), 0.12)
pattern_adjustment = 0.05 if strict else (-0.03 if lenient else 0)

final_score = base_score + tag_match_bonus + dim_bonus + pattern_adjustment
```

## 后续优化建议

1. **接入专业 NLP 模型**: 替换简化版情感分析为 BERT 等预训练模型
2. **多语言支持**: 扩展情感词库支持英文等其他语言
3. **实时权重更新**: 动态调整用户可信度权重
4. **A/B 测试框架**: 验证权重机制对推荐质量的影响
5. **反作弊机制**: 识别并降低刷分行为的权重
6. **情感趋势分析**: 跟踪景点情感变化趋势

## 测试验证

所有功能已通过单元测试验证：
- 情感分析准确率测试
- 权重计算边界测试
- 推荐积分调整测试
- API 端点集成测试
