def dashboard_overview() -> dict:
    return {
        "today_service_count": 128,
        "week_service_count": 860,
        "avg_latency_ms": 2860,
        "satisfaction_score": 4.7,
        "knowledge_hit_rate": 0.91,
        "hot_questions": [
            {"topic": "路线推荐", "count": 42},
            {"topic": "开放时间", "count": 31},
            {"topic": "拍照点", "count": 26},
        ],
        "emotion_trend": [
            {"date": "2026-05-12", "positive": 62, "neutral": 24, "negative": 6},
            {"date": "2026-05-13", "positive": 68, "neutral": 21, "negative": 5},
            {"date": "2026-05-14", "positive": 73, "neutral": 18, "negative": 4},
        ],
    }


def sentiment_report() -> dict:
    return {
        "summary": "本周游客最关注路线推荐、开放时间和拍照点。负面反馈主要集中在洗手间指引不清楚。",
        "suggestions": ["在首页增加洗手间快捷问答", "补充雨天游览路线知识库", "入口处增加亲子路线提示"],
    }
