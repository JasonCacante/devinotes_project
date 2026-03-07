from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel


class Label(SQLModel, table=True):
    __tablename__ = "label"  # type: ignore[assignment]
    __table_args__ = (
        UniqueConstraint("owner_id", "name", name="uq_label_owner_name"),
    )  # Asegura que el nombre de la etiqueta sea único por usuario
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, min_length=1, max_length=100)
    owner_id: int = Field(foreign_key="user.id", index=True)


class NoteLabelLink(SQLModel, table=True):
    __tablename__ = "note_label_link"  # type: ignore[assignment]
    __table_args__ = (UniqueConstraint("note_id", "label_id", name="uq_note_label"),)
    id: int = Field(default=None, primary_key=True)
    note_id: int = Field(foreign_key="note.id", index=True)
    label_id: int = Field(foreign_key="label.id", index=True)


# DTO (Data Transfer Object) para crear una nueva etiqueta, sin el campo id ni owner_id, ya que estos serán generados automáticamente.
class LabelCreate(SQLModel):
    name: str = Field(min_length=1, max_length=100)


class LabelRead(SQLModel):
    id: int
    name: str
    model_config = {
        "from_attributes": True
    }  # Permite crear un modelo a partir de un objeto con atributos, como una instancia de SQLAlchemy
