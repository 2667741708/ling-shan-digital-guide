from fastapi import APIRouter, UploadFile, File, Form

from app.schemas.visitor import (
    ChatTextRequest,
    CreateSessionRequest,
    RouteRecommendRequest,
)
from app.services.chat_service import chat_with_text, create_session, image_chat, voice_chat
from app.services.route_service import recommend_route
from app.services.scenic_service import list_scenic_spots

router = APIRouter()


@router.post("/sessions")
def create_visitor_session(payload: CreateSessionRequest):
    return {"code": 0, "message": "success", "data": create_session(payload)}


@router.post("/chat/text")
def text_chat(payload: ChatTextRequest):
    return {"code": 0, "message": "success", "data": chat_with_text(payload)}


@router.post("/chat/voice")
async def chat_voice(session_uuid: str = Form(...), audio_file: UploadFile = File(...)):
    return {"code": 0, "message": "success", "data": await voice_chat(session_uuid, audio_file)}


@router.post("/chat/image")
async def chat_image(
    session_uuid: str = Form(...),
    question: str = Form("这是哪个景点？"),
    image_file: UploadFile = File(...),
):
    return {"code": 0, "message": "success", "data": await image_chat(session_uuid, question, image_file)}


@router.get("/scenic-spots")
def scenic_spots():
    return {"code": 0, "message": "success", "data": list_scenic_spots()}


@router.post("/routes/recommend")
def routes_recommend(payload: RouteRecommendRequest):
    return {"code": 0, "message": "success", "data": recommend_route(payload)}
