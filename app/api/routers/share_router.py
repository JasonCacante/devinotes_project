from fastapi import APIRouter, HTTPException, status

from app.api.deps import CurrentUser, DBSession
from app.models.share import ShareRequest
from app.services.share_service import ShareService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/notes/{note_id}", status_code=status.HTTP_201_CREATED)
def share_note(note_id: int, payload: ShareRequest, db: DBSession, user: CurrentUser):
    share = ShareService(db).share_note(
        note_id=note_id,
        target_user_id=payload.target_user_id,
        role=payload.role,
        owner_id=user.id,
    )
    return {
        "id": share.id,
        "note_id": note_id,
        "user_target_id": payload.target_user_id,
        "role": share.role,
    }


@router.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def unshare_note(note_id: int, target_user_id: int, user: CurrentUser, db: DBSession):
    ShareService(db).unshare_note(
        note_id=note_id, owner_id=user.id, target_user_id=target_user_id
    )


@router.post("/labels/{note_id}", status_code=status.HTTP_201_CREATED)
def share_label(label_id: int, payload: ShareRequest, db: DBSession, user: CurrentUser):
    share = ShareService(db).share_label(
        label_id=label_id,
        target_user_id=payload.target_user_id,
        role=payload.role,
        owner_id=user.id,
    )
    if share:
        return {
            "id": share.id,
            "label_id": label_id,
            "user_target_id": payload.target_user_id,
            "role": share.role,
        }
    raise HTTPException(status_code=404, detail="Error al crear la etiqueta")


@router.delete("/labels/{label_id}", status_code=status.HTTP_204_NO_CONTENT)
def unshare_label(label_id: int, target_user_id: int, user: CurrentUser, db: DBSession):
    ShareService(db).unshare_label(
        label_id=label_id, owner_id=user.id, target_user_id=target_user_id
    )
