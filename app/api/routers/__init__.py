from app.api.routers.auth_router import router as auth_router
from app.api.routers.label_router import router as label_router
from app.api.routers.notes_router import router as notes_router
from app.api.routers.share_router import router as share_router

__all__ = ["auth_router", "label_router", "notes_router", "share_router"]
