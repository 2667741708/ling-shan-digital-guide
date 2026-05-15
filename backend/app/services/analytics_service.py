def dashboard_overview() -> dict:
    return {
        "today_service_count": 128,
        "week_service_count": 860,
        "avg_latency_ms": 2860,
        "satisfaction_score": 4.7,
        "knowledge_hit_rate": 0.91,
        "hot_questions": [
            {"topic": "2小时路线推荐", "count": 42},
            {"topic": "灵山大佛历史", "count": 35},
            {"topic": "九龙灌浴表演", "count": 31},
            {"topic": "梵宫参观重点", "count": 26},
            {"topic": "亲子轻松路线", "count": 18},
        ],
        "hot_spots": [
            {"name": "灵山大佛", "count": 88},
            {"name": "灵山梵宫", "count": 73},
            {"name": "九龙灌浴", "count": 69},
            {"name": "五印坛城", "count": 41},
        ],
        "route_preferences": [
            {"name": "历史文化", "value": 38},
            {"name": "拍照祈福", "value": 27},
            {"name": "亲子互动", "value": 19},
            {"name": "自然慢行", "value": 16},
        ],
        "emotion_trend": [
            {"date": "2026-05-12", "positive": 62, "neutral": 24, "negative": 6},
            {"date": "2026-05-13", "positive": 68, "neutral": 21, "negative": 5},
            {"date": "2026-05-14", "positive": 73, "neutral": 18, "negative": 4},
        ],
    }


def sentiment_report() -> dict:
    return {
        "summary": "本周游客最关注灵山大佛历史、九龙灌浴表演时间、梵宫参观重点和2小时路线。负面反馈主要集中在洗手间指引不清楚与雨天备用路线不足。",
        "suggestions": ["在数字人首页增加洗手间快捷问答", "补充雨天游览路线知识库", "在入口处增加亲子路线与老人友好路线提示"],
    }
