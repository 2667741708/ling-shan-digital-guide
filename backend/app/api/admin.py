from fastapi import APIRouter

from app.schemas.admin import LoginRequest
from app.services.analytics_service import dashboard_overview, sentiment_report
from app.services.avatar_service import get_active_avatar, save_avatar_config
from app.services.knowledge_service import list_documents, search_test
from app.services.scenic_service import list_scenic_spots

router = APIRouter()


@router.post("/login")
def login(payload: LoginRequest):
    token = "demo-admin-token" if payload.username and payload.password else ""
    return {"code": 0, "message": "success", "data": {"token": token}}


@router.get("/scenic-spots")
def scenic_spots():
    return {"code": 0, "message": "success", "data": list_scenic_spots()}


@router.get("/knowledge/documents")
def knowledge_documents():
    return {"code": 0, "message": "success", "data": list_documents()}


@router.post("/knowledge/search-test")
def knowledge_search_test(query: dict):
    return {"code": 0, "message": "success", "data": search_test(query.get("query", ""))}


@router.get("/avatar-configs/active")
def active_avatar():
    return {"code": 0, "message": "success", "data": get_active_avatar()}


@router.post("/avatar-configs")
def avatar_configs(payload: dict):
    return {"code": 0, "message": "success", "data": save_avatar_config(payload)}


@router.get("/analytics/overview")
def analytics_overview():
    return {"code": 0, "message": "success", "data": dashboard_overview()}


@router.get("/analytics/report")
def analytics_report():
    return {"code": 0, "message": "success", "data": sentiment_report()}
