SCENIC_SPOTS = [
    {
        "id": 1,
        "name": "景区入口",
        "description": "游客服务中心、导览图和检票入口所在地。",
        "map_x": 12,
        "map_y": 78,
        "tags": ["service", "start"],
        "recommended_duration": 5,
    },
    {
        "id": 3,
        "name": "古建筑群",
        "description": "集中展示传统建筑风貌和历史文化故事。",
        "map_x": 42,
        "map_y": 48,
        "tags": ["history", "photo"],
        "recommended_duration": 30,
    },
    {
        "id": 5,
        "name": "文化展馆",
        "description": "展示地方文史、非遗资料和研学内容。",
        "map_x": 62,
        "map_y": 44,
        "tags": ["history", "research"],
        "recommended_duration": 25,
    },
    {
        "id": 8,
        "name": "观景台",
        "description": "适合远眺全景和拍照打卡。",
        "map_x": 82,
        "map_y": 26,
        "tags": ["nature", "photo"],
        "recommended_duration": 35,
    },
]


def list_scenic_spots() -> list[dict]:
    return SCENIC_SPOTS
