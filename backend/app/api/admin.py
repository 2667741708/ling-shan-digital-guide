from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.schemas.admin import LoginRequest
from app.services.analytics_service import dashboard_overview, sentiment_report
from app.services.avatar_service import get_active_avatar, save_avatar_config
from app.services.knowledge_service import delete_document, list_documents, rebuild_index, save_document, search_test
from app.services.knowledge_service import update_document
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


@router.post("/knowledge/upload")
async def knowledge_upload(file: UploadFile = File(...), title: str = Form("")):
    try:
        data = await file.read()
        document = save_document(file.filename or "knowledge.md", data, title or None)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"code": 0, "message": "success", "data": document}


@router.put("/knowledge/documents/{document_id}")
def knowledge_update(document_id: str, payload: dict):
    try:
        document = update_document(document_id, payload.get("title"), payload.get("content"))
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"code": 0, "message": "success", "data": document}


@router.delete("/knowledge/documents/{document_id}")
def knowledge_delete(document_id: str):
    try:
        document = delete_document(document_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"code": 0, "message": "success", "data": document}


@router.post("/knowledge/reindex")
def knowledge_reindex():
    return {"code": 0, "message": "success", "data": rebuild_index()}


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
