from datetime import datetime
from time import perf_counter
from uuid import uuid4

from fastapi import UploadFile

from app.schemas.visitor import ChatTextRequest, CreateSessionRequest
from app.services.avatar_service import get_active_avatar
from app.services.deepseek_service import DeepSeekClient
from app.services.knowledge_service import retrieve_context
from app.services.route_service import quick_route_card


GUIDE_SYSTEM_PROMPT = """你是景区 AI 数字人导游，名字叫“灵灵”。
请严格遵守：
1. 优先依据景区知识库回答，不确定时说明资料中未明确记录。
2. 回答适合语音播报，控制在 80 到 200 字。
3. 涉及开放时间、票价、安全事项时，提醒以景区现场公告为准。
4. 如果用户需要路线，给出景点顺序、预计时间和推荐理由。
5. 只能使用【景区知识库】中出现的景点、设施和事实，不要新增未出现的景点名。
6. 语气亲切、自然，像真人导游。
"""


def create_session(payload: CreateSessionRequest) -> dict:
    return {
        "session_uuid": f"s_{datetime.now().strftime('%Y%m%d')}_{uuid4().hex[:8]}",
        "avatar_config": get_active_avatar(),
        "user_profile": payload.user_profile,
    }


def chat_with_text(payload: ChatTextRequest) -> dict:
    started_at = perf_counter()
    need_route = any(word in payload.message for word in ["路线", "怎么逛", "两个小时", "2小时"])
    if need_route:
        route_query = "景区入口 古建筑群 文化展馆 观景台 推荐路线 历史 拍照"
        context = [
            item
            for item in retrieve_context(route_query, top_k=30)
            if item.get("category") != "behavior_data" and not item["source"].lower().endswith(".xlsx")
        ][:5]
    else:
        context = [
            item
            for item in retrieve_context(payload.message, top_k=30)
            if item.get("category") != "behavior_data" and not item["source"].lower().endswith(".xlsx")
        ][:3]
    if not context:
        context = retrieve_context(payload.message)
    fallback_answer = (
        "建议您选择 2 小时历史文化路线，从景区入口出发，依次参观古建筑群、文化展馆和观景台。"
        "这条路线步行距离适中，兼顾历史讲解和拍照体验。"
        if need_route
        else f"灵灵为您查到：{context[0]['text']} 具体开放信息请以景区现场公告为准。"
    )
    answer = fallback_answer
    model_used = "mock-fallback"

    client = DeepSeekClient()
    if client.enabled():
        retrieved_context = "\n".join(f"- [{item['chunk_id']}] {item['text']}" for item in context)
        user_prompt = f"""【景区知识库】
{retrieved_context}

【游客问题】
{payload.message}

请直接输出给游客听的回答，不要输出分析过程。"""
        try:
            answer = client.chat(GUIDE_SYSTEM_PROMPT, user_prompt)
            model_used = client.model
        except RuntimeError:
            answer = fallback_answer

    return {
        "answer": answer,
        "intent": "route_recommendation" if need_route else "scenic_qa",
        "emotion": "happy" if need_route else "thinking",
        "model_used": model_used,
        "audio_url": "/static/audio/demo-answer.mp3",
        "lip_sync": {"mode": "rms", "duration_ms": 5200},
        "cards": [quick_route_card()] if need_route else [],
        "references": [{"document": item["source"], "chunk_id": item["chunk_id"]} for item in context],
        "latency_ms": int((perf_counter() - started_at) * 1000),
    }


async def voice_chat(session_uuid: str, audio_file: UploadFile) -> dict:
    return {
        "asr_text": "我第一次来这个景区，应该怎么逛？",
        **chat_with_text(ChatTextRequest(session_uuid=session_uuid, message="我第一次来这个景区，应该怎么逛？")),
    }


async def image_chat(session_uuid: str, question: str, image_file: UploadFile) -> dict:
    return {
        "recognized_spot": {"id": 3, "name": "古建筑群"},
        "answer": "这张图片很可能是古建筑群区域。这里是景区最具历史特色的区域之一，适合安排 20 到 30 分钟讲解和拍照。",
        "confidence": 0.88,
        "audio_url": "/static/audio/demo-image-answer.mp3",
        "references": [{"document": "示范景区资料包-历史文化篇", "chunk_id": 3}],
    }
