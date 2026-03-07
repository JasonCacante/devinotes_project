from typing import Sequence

from sqlmodel import Session, col, delete, select

from app.models.share import LabelShare, NoteShare, ShareRole


class ShareRepository:
    def __init__(self, db: Session):
        self.db = db

    def upsert_note_share(
        self, note_id: int, user_id: int, role: ShareRole
    ) -> NoteShare:
        share = self.db.exec(
            select(NoteShare).where(
                col(NoteShare.note_id) == note_id, col(NoteShare.user_id) == user_id
            )
        ).first()
        if share:
            share.role = role
        else:
            share = NoteShare(note_id=note_id, user_id=user_id, role=role)
            self.db.add(share)
        self.db.commit()
        self.db.refresh(share)
        return share

    def remove_note_share(self, note_id: int, user_id: int) -> None:
        self.db.exec(
            delete(NoteShare).where(
                col(NoteShare.note_id) == note_id, col(NoteShare.user_id) == user_id
            )
        )
        self.db.commit()

    def upsert_label_share(
        self, label_id: int, user_id: int, role: ShareRole
    ) -> LabelShare:
        share = self.db.exec(
            select(LabelShare).where(
                col(LabelShare.label_id) == label_id, col(LabelShare.user_id) == user_id
            )
        ).first()
        if share:
            share.role = role
        else:
            share = LabelShare(label_id=label_id, user_id=user_id, role=role)
            self.db.add(share)
        self.db.commit()
        self.db.refresh(share)
        return share

    def remove_label_share(self, label_id: int, user_id: int) -> None:
        self.db.exec(
            delete(LabelShare).where(
                col(LabelShare.label_id) == label_id, col(LabelShare.user_id) == user_id
            )
        )
        self.db.commit()

    def has_note_share(
        self, note_id: int, user_id: int, role: ShareRole | None = None
    ) -> bool:
        query = select(NoteShare).where(
            col(NoteShare.note_id) == note_id, col(NoteShare.user_id) == user_id
        )
        if role:
            query = query.where(col(NoteShare.role) == role)
        return self.db.exec(query).first() is not None

    def has_any_label_share(
        self, label_ids: list[int], user_id: int, role: ShareRole | None = None
    ) -> bool:
        if not label_ids:
            return False
        query = select(LabelShare).where(
            col(LabelShare.label_id).in_(label_ids), col(LabelShare.user_id) == user_id
        )
        if role:
            query = query.where(col(LabelShare.role) == role)
        return self.db.exec(query).first() is not None

    def list_note_ids_shared_with_user(self, user_id: int) -> Sequence[int]:
        query = self.db.exec(
            select(NoteShare.note_id).where(col(NoteShare.user_id) == user_id)
        )
        return query.all()

    def list_label_ids_shared_with_user(self, user_id: int) -> Sequence[int]:
        return self.db.exec(
            select(LabelShare.label_id).where(col(LabelShare.user_id) == user_id)
        ).all()
