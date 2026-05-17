from fastapi import APIRouter, UploadFile, File, Form

from app.schemas.visitor import (
    ChatTextRequest,
    CreateSessionRequest,
    RouteRecommendRequest,
    SpotRatingRequest,
)
from app.services.chat_service import chat_with_text, create_session, image_chat, voice_chat
from app.services.route_service import recommend_route
from app.services.scenic_service import list_scenic_spots
from app.services.rating_service import (
    create_or_update_rating, 
    get_ratings_by_session, 
    get_spot_statistics, 
    rating_to_response,
    get_user_preference_profile,
    analyze_sentiment,
)

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


@router.post("/ratings")
def submit_rating(payload: SpotRatingRequest, db=None):
    """Submit or update a visitor's rating for a scenic spot."""
    from app.core.database import get_db
    
    # Get database session
    db_session = next(get_db())
    try:
        rating = create_or_update_rating(db_session, payload)
        return {"code": 0, "message": "success", "data": rating_to_response(rating)}
    finally:
        db_session.close()


@router.get("/sessions/{session_uuid}/ratings")
def list_session_ratings(session_uuid: str, db=None):
    """Get all ratings submitted by a specific session."""
    from app.core.database import get_db
    
    db_session = next(get_db())
    try:
        ratings = get_ratings_by_session(db_session, session_uuid)
        return {"code": 0, "message": "success", "data": [rating_to_response(r) for r in ratings]}
    finally:
        db_session.close()


@router.get("/spots/{spot_id}/ratings/stats")
def get_spot_rating_stats(spot_id: int, db=None):
    """Get aggregated rating statistics for a specific spot with weighted scoring and sentiment analysis."""
    from app.core.database import get_db
    
    db_session = next(get_db())
    try:
        stats = get_spot_statistics(db_session, spot_id)
        return {"code": 0, "message": "success", "data": stats}
    finally:
        db_session.close()


@router.get("/sessions/{session_uuid}/preference-profile")
def get_preference_profile(session_uuid: str, db=None):
    """Get user preference profile based on their rating history."""
    from app.core.database import get_db
    
    db_session = next(get_db())
    try:
        profile = get_user_preference_profile(db_session, session_uuid)
        return {"code": 0, "message": "success", "data": profile}
    finally:
        db_session.close()


@router.post("/sentiment/analyze")
def analyze_comment_sentiment(comment: str):
    """Analyze sentiment of a comment text."""
    result = analyze_sentiment(comment)
    return {"code": 0, "message": "success", "data": result}
