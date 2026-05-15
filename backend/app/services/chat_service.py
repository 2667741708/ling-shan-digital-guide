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


def _is_safe_reference(item: dict) -> bool:
    """Return True when a retrieved item can be shown as a factual answer source."""
    return item.get("category") != "behavior_data" and not item["source"].lower().endswith(".xlsx")


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
        route_query = "灵山胜境 灵山大照壁 五智门 菩提大道 九龙灌浴 灵山大佛 灵山梵宫 五印坛城 推荐路线 历史 拍照"
        context = [item for item in retrieve_context(route_query, top_k=30) if _is_safe_reference(item)][:5]
    else:
        context = [item for item in retrieve_context(payload.message, top_k=30) if _is_safe_reference(item)][:3]
    if not context:
        context = [
            item
            for item in retrieve_context("灵山胜境 灵山大佛 九龙灌浴 灵山梵宫 游览路线 服务设施", top_k=20)
            if _is_safe_reference(item)
        ][:3]
    fallback_answer = (
        "建议您走 2 小时灵山历史文化路线：南门游客中心出发，先看灵山大照壁和五智门，"
        "再沿菩提大道到九龙灌浴，最后重点参观灵山大佛。时间更充裕时可增加灵山梵宫。"
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
        "recognized_spot": {"id": 11, "name": "灵山大佛"},
        "answer": "这张图片很可能对应灵山大佛或其周边核心朝圣区。灵山大佛是灵山胜境标志性建筑，适合安排重点讲解和拍照打卡。",
        "confidence": 0.88,
        "audio_url": "/static/audio/demo-image-answer.mp3",
        "references": [{"document": "灵山胜境：历史、文化、景点特色与个性化游览指南.docx", "chunk_id": 3}],
    }
