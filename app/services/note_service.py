from fastapi import HTTPException
from sqlmodel import Session

from app.models.note import Note, NoteCreate, NoteUpdate
from app.models.share import ShareRole
from app.repositories.label_repository import LabelRepository
from app.repositories.note_repository import NoteRepository
from app.repositories.share_repository import ShareRepository


class NoteService:
    def __init__(self, db: Session):
        self.db = db
        self.notes = NoteRepository(db)
        self.labels = LabelRepository(db)
        self.shares = ShareRepository(db)

    def user_can_read(self, user_id: int, note: Note) -> bool:
        if note.owner_id == user_id:
            return True
        if self.shares.has_note_share(note_id=note.id, user_id=user_id):
            return True

        label_ids = list(self.labels.list_label_ids_for_note(note.id))
        return self.shares.has_any_label_share(label_ids=label_ids, user_id=user_id)

    def user_can_edit(self, user_id: int, note: Note) -> bool:
        if note.owner_id == user_id:
            return True
        if self.shares.has_note_share(
            note_id=note.id, user_id=user_id, role=ShareRole.EDIT
        ):
            return True
        label_ids = list(self.labels.list_label_ids_for_note(note.id))
        return self.shares.has_any_label_share(
            label_ids=label_ids, user_id=user_id, role=ShareRole.EDIT
        )

    def list_visible(self, user_id: int) -> list[Note]:
        owned_notes = self.notes.list_owned(user_id)
        direct_ids = self.shares.list_note_ids_shared_with_user(user_id)
        share_label_ids = self.shares.list_label_ids_shared_with_user(user_id)
        ids_by_label = self.labels.list_note_ids_by_label_ids(list(share_label_ids))
        all_ids = list({*direct_ids, *ids_by_label})
        shared = self.notes.list_by_ids(all_ids)
        combined = {note.id: note for note in owned_notes}
        for note in shared:
            combined.setdefault(note.id, note)
        return sorted(combined.values(), key=lambda note: note.id, reverse=True)

    def create(self, owner_id: int, payload: NoteCreate) -> Note:
        note = self.notes.create(
            Note(owner_id=owner_id, **payload.model_dump(exclude={"label_ids"}))
        )
        if payload.label_ids:
            self._set_labels(
                label_ids=payload.label_ids, owner_id=owner_id, note_id=note.id
            )
        return note

    def update(self, user_id: int, note_id: int, payload: NoteUpdate) -> Note:
        note = self.notes.get_by_id(note_id)
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        if not self.user_can_edit(user_id, note):
            raise HTTPException(
                status_code=403,
                detail="User does not have permission to edit this note",
            )
        for field in payload.model_fields_set - {"label_ids"}:
            setattr(note, field, getattr(payload, field))
        updates = payload.model_dump(exclude_none=True)
        label_ids = updates.pop("label_ids", None)
        for key, value in updates.items():
            setattr(note, key, value)
        updated_note = self.notes.update(note)

        if label_ids is not None:
            if note.owner_id != user_id:
                raise HTTPException(
                    status_code=403,
                    detail="Only the owner can update labels of this note",
                )
            self._set_labels(label_ids=label_ids, owner_id=user_id, note_id=note.id)
        return updated_note

    def delete(self, user_id: int, note_id: int) -> None:
        note = self.notes.get_by_id(note_id)
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        if note.owner_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="User does not have permission to delete this note",
            )
        self.notes.delete(note)

    # Helpers
    def _set_labels(self, owner_id: int, note_id: int, label_ids: list[int]) -> None:
        valid_ids = self.labels.list_ids_for_owner_subset(owner_id, label_ids or [])
        self.notes.replace_labels(note_id, list(valid_ids))
