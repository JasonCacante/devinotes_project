from fastapi import HTTPException
from sqlmodel import Session

from app.models.label import Label, LabelCreate
from app.repositories.label_repository import LabelRepository


class LabelService:
    def __init__(self, db: Session):
        self.label = LabelRepository(db)

    def list(self, owner_id: int) -> list[Label]:
        return list(self.label.list_by_user(owner_id))

    def create(self, owner_id: int, payload: LabelCreate) -> Label:
        if self.label.get_by_name(owner_id=owner_id, name=payload.name):
            raise HTTPException(
                status_code=400, detail="Label with this name already exists"
            )
        return self.label.create(owner_id=owner_id, name=payload.name)

    def delete(self, owner_id: int, label_id: int) -> None:
        label = self.label.get_by_id(label_id)
        if not label or label.owner_id != owner_id:
            raise HTTPException(status_code=404, detail="Label not found")
        self.label.delete(label)
