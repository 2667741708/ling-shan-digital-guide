ACTIVE_AVATAR = {
    "name": "灵灵",
    "avatar_style": "ancient",
    "clothes": "traditional_blue",
    "voice_name": "female_warm",
    "voice_speed": 1.0,
    "opening_text": "您好，我是您的 AI 数字人导游灵灵。",
    "expressions": ["idle", "listening", "thinking", "speaking", "happy", "concerned"],
}


def get_active_avatar() -> dict:
    return ACTIVE_AVATAR


def save_avatar_config(payload: dict) -> dict:
    ACTIVE_AVATAR.update(payload)
    return ACTIVE_AVATAR
