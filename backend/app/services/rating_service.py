"""Service for managing visitor spot ratings with sentiment analysis and weighted scoring.

对应需求：
- 观众对景点的个性化评分与反馈
- 支持后续基于用户评分的个性化推荐优化
- 情感分析和评分权重机制
"""
from datetime import datetime
from typing import Any
import re

from sqlalchemy import select, update, func
from sqlalchemy.orm import Session

from app.models.persistence import VisitorSpotRating
from app.schemas.visitor import SpotRatingRequest, SpotRatingResponse


# 情感分析关键词库 (简化版，实际可接入 NLP 模型)
POSITIVE_WORDS = {
    "好", "棒", "美", "赞", "喜欢", "值得", "推荐", "满意", "不错", "精彩",
    "震撼", "壮观", "漂亮", "愉快", "开心", "完美", "优秀", "出色", "迷人",
    "有趣", "好玩", "舒适", "方便", "干净", "整洁", "热情", "友好", "专业"
}

NEGATIVE_WORDS = {
    "差", "糟", "丑", "失望", "不满", "不好", "讨厌", "避免", "坑", "贵",
    "脏", "乱", "吵", "挤", "累", "远", "慢", "旧", "破", "糟糕", "无聊",
    "一般", "普通", "勉强", "凑合", "还行", "不过如此", "浪费时间"
}

INTENSIFIERS = {"非常", "特别", "极其", "十分", "太", "很", "超级", "格外", "异常"}
NEGATORS = {"不", "没", "无", "非", "未", "别", "莫", "勿"}


def analyze_sentiment(comment: str | None) -> dict[str, Any]:
    """分析评论文本的情感倾向。
    
    Returns:
        dict containing:
        - sentiment: "positive", "negative", or "neutral"
        - score: float between -1.0 and 1.0
        - confidence: float between 0.0 and 1.0
        - keywords: list of detected sentiment words
    """
    if not comment:
        return {
            "sentiment": "neutral",
            "score": 0.0,
            "confidence": 0.0,
            "keywords": []
        }
    
    # 分词 (简化版，按字符和常见词组)
    text = comment.lower()
    words = []
    i = 0
    while i < len(text):
        # 检查双字词
        if i + 1 < len(text):
            two_char = text[i:i+2]
            if two_char in INTENSIFIERS or two_char in NEGATORS or two_char in POSITIVE_WORDS or two_char in NEGATIVE_WORDS:
                words.append(two_char)
                i += 2
                continue
        # 单字
        one_char = text[i:i+1]
        if one_char in POSITIVE_WORDS or one_char in NEGATIVE_WORDS:
            words.append(one_char)
        i += 1
    
    positive_count = 0
    negative_count = 0
    detected_keywords = []
    sentiment_scores = []
    
    i = 0
    while i < len(words):
        word = words[i]
        multiplier = 1.0
        is_negated = False
        
        # 检查是否有程度副词修饰
        if i > 0 and words[i-1] in INTENSIFIERS:
            multiplier = 1.5
        
        # 检查是否有否定词
        if i > 0 and words[i-1] in NEGATORS:
            is_negated = True
        
        if word in POSITIVE_WORDS:
            score = 1.0 * multiplier
            if is_negated:
                score = -score * 0.5  # 否定后情感反转但减弱
            positive_count += 1
            sentiment_scores.append(score)
            detected_keywords.append(word)
        elif word in NEGATIVE_WORDS:
            score = -1.0 * multiplier
            if is_negated:
                score = -score * 0.5
            negative_count += 1
            sentiment_scores.append(score)
            detected_keywords.append(word)
        
        i += 1
    
    total_words = positive_count + negative_count
    if total_words == 0:
        return {
            "sentiment": "neutral",
            "score": 0.0,
            "confidence": 0.0,
            "keywords": []
        }
    
    # 计算综合情感得分
    avg_score = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0.0
    # 归一化到 [-1, 1]
    normalized_score = max(-1.0, min(1.0, avg_score))
    
    # 置信度基于检测到的情感词数量
    confidence = min(1.0, total_words / 5.0)
    
    # 确定情感类别
    if normalized_score > 0.2:
        sentiment = "positive"
    elif normalized_score < -0.2:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    
    return {
        "sentiment": sentiment,
        "score": round(normalized_score, 3),
        "confidence": round(confidence, 3),
        "keywords": detected_keywords[:10]  # 限制返回数量
    }


def calculate_rating_weight(rating: VisitorSpotRating, user_history: list[VisitorSpotRating] | None = None) -> float:
    """计算评分的权重。
    
    权重考虑因素：
    - 评分完整性 (填写了更多维度评分的权重更高)
    - 是否有文字反馈 (有详细评论的权重更高)
    - 评论情感与评分的一致性 (一致性高则权重高)
    - 用户历史评分的可信度 (基于历史评分的一致性)
    - 是否为公开分享 (公开的权重略高)
    
    Returns:
        float weight between 0.5 and 1.5
    """
    base_weight = 1.0
    
    # 1. 评分完整性权重 (0.0 - 0.2)
    dimension_count = sum([
        1 if rating.culture_rating is not None else 0,
        1 if rating.nature_rating is not None else 0,
        1 if rating.photo_rating is not None else 0,
        1 if rating.facility_rating is not None else 0,
    ])
    completeness_bonus = (dimension_count / 4.0) * 0.2
    base_weight += completeness_bonus
    
    # 2. 文字反馈权重 (0.0 - 0.2)
    if rating.comment:
        comment_length = len(rating.comment)
        if comment_length > 50:
            base_weight += 0.2
        elif comment_length > 20:
            base_weight += 0.15
        elif comment_length > 10:
            base_weight += 0.1
        else:
            base_weight += 0.05
    
    # 3. 情感一致性权重 (-0.1 - 0.1)
    if rating.comment:
        sentiment_result = analyze_sentiment(rating.comment)
        sentiment_score = sentiment_result["score"]
        # 将 overall_rating (1-5) 转换为 -1 到 1 的范围
        normalized_rating = (rating.overall_rating - 3) / 2.0
        # 计算一致性
        consistency = 1.0 - abs(normalized_rating - sentiment_score)
        if consistency > 0.8:
            base_weight += 0.1
        elif consistency < 0.4:
            base_weight -= 0.1
    
    # 4. 公开分享权重 (0.0 - 0.1)
    if rating.is_public:
        base_weight += 0.05
    
    # 5. 用户历史可信度权重 (-0.1 - 0.1)
    if user_history and len(user_history) >= 2:
        # 计算用户历史评分的标准差，标准差小说明评分稳定可信
        overall_ratings = [r.overall_rating for r in user_history]
        avg_rating = sum(overall_ratings) / len(overall_ratings)
        variance = sum((r - avg_rating) ** 2 for r in overall_ratings) / len(overall_ratings)
        std_dev = variance ** 0.5
        
        # 标准差在 0.5-1.5 之间认为是正常波动，给予正权重
        if 0.5 <= std_dev <= 1.5:
            base_weight += 0.1
        elif std_dev < 0.5:
            base_weight += 0.05  # 过于一致可能有刷分嫌疑
        elif std_dev > 2.0:
            base_weight -= 0.1  # 波动太大可能不够客观
    
    # 限制权重范围
    return max(0.5, min(1.5, base_weight))


def create_or_update_rating(db: Session, payload: SpotRatingRequest) -> VisitorSpotRating:
    """Create a new rating or update existing one for the same session and spot."""
    # Check if rating already exists for this session and spot
    stmt = select(VisitorSpotRating).where(
        VisitorSpotRating.session_uuid == payload.session_uuid,
        VisitorSpotRating.spot_id == payload.spot_id,
    )
    existing = db.execute(stmt).scalar_one_or_none()

    if existing:
        # Update existing rating
        update_data = {
            "overall_rating": payload.overall_rating,
            "culture_rating": payload.culture_rating,
            "nature_rating": payload.nature_rating,
            "photo_rating": payload.photo_rating,
            "facility_rating": payload.facility_rating,
            "comment": payload.comment,
            "user_tags": payload.user_tags,
            "visit_date": datetime.fromisoformat(payload.visit_date) if payload.visit_date else None,
            "weather_condition": payload.weather_condition,
            "crowd_level": payload.crowd_level,
            "is_public": payload.is_public,
            "updated_at": datetime.utcnow(),
        }
        db.execute(
            update(VisitorSpotRating)
            .where(VisitorSpotRating.id == existing.id)
            .values(**update_data)
        )
        db.commit()
        db.refresh(existing)
        return existing
    else:
        # Create new rating
        rating = VisitorSpotRating(
            session_uuid=payload.session_uuid,
            spot_id=payload.spot_id,
            overall_rating=payload.overall_rating,
            culture_rating=payload.culture_rating,
            nature_rating=payload.nature_rating,
            photo_rating=payload.photo_rating,
            facility_rating=payload.facility_rating,
            comment=payload.comment,
            user_tags=payload.user_tags,
            visit_date=datetime.fromisoformat(payload.visit_date) if payload.visit_date else None,
            weather_condition=payload.weather_condition,
            crowd_level=payload.crowd_level,
            is_public=payload.is_public,
        )
        db.add(rating)
        db.commit()
        db.refresh(rating)
        return rating


def get_rating_by_id(db: Session, rating_id: str) -> VisitorSpotRating | None:
    """Get a rating by its ID."""
    stmt = select(VisitorSpotRating).where(VisitorSpotRating.id == rating_id)
    return db.execute(stmt).scalar_one_or_none()


def get_ratings_by_session(db: Session, session_uuid: str) -> list[VisitorSpotRating]:
    """Get all ratings for a specific session."""
    stmt = select(VisitorSpotRating).where(VisitorSpotRating.session_uuid == session_uuid)
    return list(db.execute(stmt).scalars().all())


def get_ratings_by_spot(db: Session, spot_id: int, include_public_only: bool = True) -> list[VisitorSpotRating]:
    """Get all ratings for a specific spot."""
    query = select(VisitorSpotRating).where(VisitorSpotRating.spot_id == spot_id)
    if include_public_only:
        query = query.where(VisitorSpotRating.is_public == True)
    return list(db.execute(query).scalars().all())


def get_spot_statistics(db: Session, spot_id: int) -> dict[str, Any]:
    """Get aggregated statistics for a specific spot with weighted scoring."""
    ratings = get_ratings_by_spot(db, spot_id, include_public_only=False)
    
    if not ratings:
        return {
            "spot_id": spot_id,
            "total_ratings": 0,
            "average_overall": None,
            "average_culture": None,
            "average_nature": None,
            "average_photo": None,
            "average_facility": None,
            "weighted_average_overall": None,
            "sentiment_distribution": {"positive": 0, "neutral": 0, "negative": 0},
        }
    
    total = len(ratings)
    
    # 简单平均
    avg_overall = sum(r.overall_rating for r in ratings) / total
    
    # 加权平均
    weighted_sum = 0.0
    weight_total = 0.0
    sentiment_dist = {"positive": 0, "neutral": 0, "negative": 0}
    
    for rating in ratings:
        weight = calculate_rating_weight(rating)
        weighted_sum += rating.overall_rating * weight
        weight_total += weight
        
        # 情感分析统计
        if rating.comment:
            sentiment_result = analyze_sentiment(rating.comment)
            sentiment_dist[sentiment_result["sentiment"]] += 1
    
    weighted_avg = weighted_sum / weight_total if weight_total > 0 else avg_overall
    
    # Calculate averages for optional fields (only count non-None values)
    culture_ratings = [r.culture_rating for r in ratings if r.culture_rating is not None]
    nature_ratings = [r.nature_rating for r in ratings if r.nature_rating is not None]
    photo_ratings = [r.photo_rating for r in ratings if r.photo_rating is not None]
    facility_ratings = [r.facility_rating for r in ratings if r.facility_rating is not None]
    
    return {
        "spot_id": spot_id,
        "total_ratings": total,
        "average_overall": round(avg_overall, 2) if avg_overall else None,
        "average_culture": round(sum(culture_ratings) / len(culture_ratings), 2) if culture_ratings else None,
        "average_nature": round(sum(nature_ratings) / len(nature_ratings), 2) if nature_ratings else None,
        "average_photo": round(sum(photo_ratings) / len(photo_ratings), 2) if photo_ratings else None,
        "average_facility": round(sum(facility_ratings) / len(facility_ratings), 2) if facility_ratings else None,
        "weighted_average_overall": round(weighted_avg, 2),
        "sentiment_distribution": sentiment_dist,
    }


def get_user_preference_profile(db: Session, session_uuid: str) -> dict[str, Any]:
    """基于用户历史评分生成偏好画像。
    
    Returns:
        dict containing:
        - preferred_dimensions: 用户最关注的评分维度
        - average_ratings_by_dimension: 各维度的平均评分
        - preference_tags: 从评论中提取的偏好标签
        - rating_pattern: 用户的评分模式 (strict/lenient/balanced)
    """
    ratings = get_ratings_by_session(db, session_uuid)
    
    if not ratings:
        return {
            "preferred_dimensions": [],
            "average_ratings_by_dimension": {},
            "preference_tags": [],
            "rating_pattern": "unknown",
            "total_ratings": 0,
        }
    
    # 统计各维度评分频率
    dimension_counts = {
        "culture": sum(1 for r in ratings if r.culture_rating is not None),
        "nature": sum(1 for r in ratings if r.nature_rating is not None),
        "photo": sum(1 for r in ratings if r.photo_rating is not None),
        "facility": sum(1 for r in ratings if r.facility_rating is not None),
    }
    
    # 找出用户最常评分的维度 (前 2 个)
    sorted_dimensions = sorted(dimension_counts.items(), key=lambda x: x[1], reverse=True)
    preferred_dimensions = [dim for dim, count in sorted_dimensions if count > 0][:2]
    
    # 计算各维度平均分
    avg_by_dimension = {}
    for dim in ["culture", "nature", "photo", "facility", "overall"]:
        attr = f"{dim}_rating"
        values = [getattr(r, attr) for r in ratings if getattr(r, attr, None) is not None]
        if values:
            avg_by_dimension[dim] = round(sum(values) / len(values), 2)
    
    # 从评论中提取偏好标签
    all_tags = []
    for rating in ratings:
        if rating.user_tags:
            all_tags.extend(rating.user_tags)
        if rating.comment:
            # 简单提取可能的偏好关键词
            sentiment_result = analyze_sentiment(rating.comment)
            if sentiment_result["sentiment"] == "positive" and sentiment_result["keywords"]:
                all_tags.extend(sentiment_result["keywords"][:3])
    
    # 统计标签频率
    from collections import Counter
    tag_counts = Counter(all_tags)
    preference_tags = [tag for tag, count in tag_counts.most_common(5)]
    
    # 判断评分模式
    overall_ratings = [r.overall_rating for r in ratings]
    avg_overall = sum(overall_ratings) / len(overall_ratings)
    if avg_overall >= 4.2:
        rating_pattern = "lenient"  # 宽松型
    elif avg_overall <= 2.8:
        rating_pattern = "strict"  # 严格型
    else:
        rating_pattern = "balanced"  # 平衡型
    
    return {
        "preferred_dimensions": preferred_dimensions,
        "average_ratings_by_dimension": avg_by_dimension,
        "preference_tags": preference_tags,
        "rating_pattern": rating_pattern,
        "total_ratings": len(ratings),
    }


def rating_to_response(rating: VisitorSpotRating) -> SpotRatingResponse:
    """Convert a VisitorSpotRating model to a response schema."""
    return SpotRatingResponse(
        id=rating.id,
        session_uuid=rating.session_uuid,
        spot_id=rating.spot_id,
        overall_rating=rating.overall_rating,
        culture_rating=rating.culture_rating,
        nature_rating=rating.nature_rating,
        photo_rating=rating.photo_rating,
        facility_rating=rating.facility_rating,
        comment=rating.comment,
        user_tags=rating.user_tags or [],
        visit_date=rating.visit_date.isoformat() if rating.visit_date else None,
        weather_condition=rating.weather_condition,
        crowd_level=rating.crowd_level,
        is_public=rating.is_public,
        created_at=rating.created_at.isoformat(),
        updated_at=rating.updated_at.isoformat(),
    )
