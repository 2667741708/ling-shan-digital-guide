from app.schemas.visitor import RouteRecommendRequest
from app.services.scenic_service import SCENIC_SPOTS


TAG_ALIASES = {
    "history": {"history", "culture", "research", "must"},
    "culture": {"history", "culture", "research", "prayer"},
    "nature": {"nature"},
    "photo": {"photo", "must"},
    "parent_child": {"family", "show"},
    "family": {"family", "show"},
    "elderly": {"elderly", "service"},
    "research": {"research", "history", "culture"},
    "food": {"service"},
}

AXIS_ORDER = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 14: 9, 9: 10, 10: 11, 11: 12, 12: 13, 13: 14}


def _distance_cost(spot: dict, start_spot: dict) -> float:
    """Return a normalized map distance cost between two percentage points."""
    distance = abs(spot["map_x"] - start_spot["map_x"]) + abs(spot["map_y"] - start_spot["map_y"])
    return min(distance / 120, 1.0)


def _interest_score(spot: dict, interests: set[str]) -> float:
    spot_tags = set(spot.get("tags", []))
    expanded = set()
    for interest in interests:
        expanded.update(TAG_ALIASES.get(interest, {interest}))
    if not expanded:
        expanded = {"history", "culture", "photo"}
    return min(len(spot_tags.intersection(expanded)) / 2, 1.0)


def _physical_penalty(spot: dict, physical_strength: str) -> float:
    duration = spot.get("recommended_duration", 10)
    if physical_strength in {"easy", "light", "elderly"} and duration >= 35:
        return 0.16
    if physical_strength in {"deep", "strong"}:
        return -0.05
    return 0.0


def _score_spot(spot: dict, payload: RouteRecommendRequest, start_spot: dict) -> float:
    """Score a scenic spot according to the engineering design formula."""
    interests = set(payload.interest)
    crowd_penalty = 0.05 if payload.avoid_crowd and spot.get("popularity_score", 0.5) > 0.92 else 0.0
    must_bonus = 0.22 if "must" in spot.get("tags", []) and (not interests or {"history", "culture", "photo"}.intersection(interests)) else 0.0
    return (
        0.30 * _interest_score(spot, interests)
        + 0.20 * spot.get("popularity_score", 0.5)
        + 0.15 * spot.get("culture_score", 0.5)
        + 0.15 * spot.get("nature_score", 0.5)
        + 0.10 * spot.get("photo_score", 0.5)
        + 0.10 * spot.get("facility_score", 0.5)
        + must_bonus
        - 0.15 * _distance_cost(spot, start_spot)
        - crowd_penalty
        - _physical_penalty(spot, payload.physical_strength)
    )


def _route_name(payload: RouteRecommendRequest) -> str:
    hours = max(1, round(payload.available_time / 60))
    labels = {
        "history": "历史文化",
        "culture": "文化研学",
        "photo": "拍照祈福",
        "nature": "自然慢行",
        "parent_child": "亲子互动",
        "family": "亲子互动",
        "elderly": "轻松友好",
        "research": "研学深度",
    }
    first_label = next((labels[item] for item in payload.interest if item in labels), "经典")
    return f"{hours}小时{first_label}灵山导览路线"


def recommend_route(payload: RouteRecommendRequest) -> dict:
    start_spot = next((spot for spot in SCENIC_SPOTS if spot["id"] == payload.start_spot_id), SCENIC_SPOTS[0])
    candidates = []
    for spot in SCENIC_SPOTS:
        if spot["id"] == start_spot["id"]:
            continue
        score = _score_spot(spot, payload, start_spot)
        candidates.append((score, spot))

    selected = [start_spot] + [spot for _, spot in sorted(candidates, key=lambda item: item[0], reverse=True)]
    total = start_spot["recommended_duration"]
    route_spots = [{"id": start_spot["id"], "name": start_spot["name"], "stay_minutes": start_spot["recommended_duration"]}]

    for spot in selected:
        if spot["id"] == start_spot["id"]:
            continue
        duration = spot["recommended_duration"]
        walk_minutes = 8 + round(_distance_cost(spot, start_spot) * 10)
        if total + duration + walk_minutes <= payload.available_time:
            total += duration + walk_minutes
            route_spots.append(
                {
                    "id": spot["id"],
                    "name": spot["name"],
                    "stay_minutes": duration,
                    "reason": spot["guide_text"],
                }
            )
        if len(route_spots) >= 6:
            break

    return {
        "route_name": _route_name(payload),
        "total_duration": total,
        "spots": sorted(route_spots, key=lambda item: AXIS_ORDER.get(item["id"], 999)),
        "reason": "该路线基于灵山胜境真实景点标签、文化价值、拍照价值、设施便利度和步行成本生成，适合在地图上按顺序展示。",
    }


def quick_route_card() -> dict:
    return {"type": "route", "title": "2小时灵山历史文化路线", "spot_ids": [1, 2, 4, 6, 11]}
