from app.schemas.visitor import RouteRecommendRequest
from app.services.scenic_service import SCENIC_SPOTS


def recommend_route(payload: RouteRecommendRequest) -> dict:
    interests = set(payload.interest)
    candidates = []
    for spot in SCENIC_SPOTS:
        match = len(interests.intersection(spot["tags"]))
        score = match * 0.3 + (spot["recommended_duration"] / 40) * 0.2
        candidates.append((score, spot))
    selected = [spot for _, spot in sorted(candidates, key=lambda item: item[0], reverse=True)]
    total = 0
    route_spots = []
    for spot in selected:
        duration = spot["recommended_duration"]
        if total + duration + 8 <= payload.available_time:
            total += duration + 8
            route_spots.append({"id": spot["id"], "name": spot["name"], "stay_minutes": duration})
    return {
        "route_name": f"{payload.available_time // 60 or 1}小时个性化导览路线",
        "total_duration": total,
        "spots": route_spots,
        "reason": "该路线根据游客兴趣、可用时间和景点标签生成，适合比赛演示阶段继续替换为完整打分算法。",
    }


def quick_route_card() -> dict:
    return {"type": "route", "title": "2小时历史文化路线", "spot_ids": [1, 3, 5]}
