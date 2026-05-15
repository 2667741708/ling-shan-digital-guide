from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.admin import router as admin_router
from app.api.visitor import router as visitor_router
from app.core.database import init_db
from app.core.config import settings
from app.services.auth_service import ensure_admin_user
from app.services.avatar_service import ensure_default_avatar
from app.services.knowledge_service import migrate_existing_admin_documents


def create_app() -> FastAPI:
    app = FastAPI(title="LingTour AI API", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(visitor_router, prefix="/api/visitor", tags=["visitor"])
    app.include_router(admin_router, prefix="/api/admin", tags=["admin"])

    @app.get("/api/health")
    def health():
        return {"code": 0, "message": "success", "data": {"status": "ok"}}

    @app.on_event("startup")
    def startup():
        init_db()
        ensure_admin_user()
        ensure_default_avatar()
        migrate_existing_admin_documents()

    return app


app = create_app()
