def score_spot(spot: dict, interests: list[str], distance_cost: float = 0, crowd_penalty: float = 0) -> float:
    tags = set(spot.get("tags", []))
    interest_score = len(tags.intersection(interests)) / max(len(interests), 1)
    return (
        0.30 * interest_score
        + 0.20 * spot.get("popularity_score", 0.5)
        + 0.15 * spot.get("culture_score", 0.5)
        + 0.15 * spot.get("nature_score", 0.5)
        + 0.10 * spot.get("photo_score", 0.5)
        + 0.10 * spot.get("facility_score", 0.5)
        - 0.15 * distance_cost
        - 0.10 * crowd_penalty
    )
