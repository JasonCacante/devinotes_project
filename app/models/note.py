from sqlmodel import Field, SQLModel


class Note(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    content: str
    color: str | None = None
    owner_id: int = Field(foreign_key="user.id", index=True)


# DTO (Data Transfer Object) para crear una nueva nota, sin el campo id ni owner_id, ya que estos serán generados automáticamente.
class NoteCreate(SQLModel):
    title: str
    content: str = ""
    color: str | None = None
    label_ids: list[int] | None = None  # Lista de IDs de etiquetas asociadas a la nota


class NoteUpdate(SQLModel):
    title: str | None = None
    content: str | None = None
    color: str | None = None
    label_ids: list[int] | None = None  # Lista de IDs de etiquetas asociadas a la nota


class NoteRead(SQLModel):
    id: int
    title: str
    content: str
    color: str | None = None
    model_config = {
        "from_attributes": True
    }  # Permite crear un modelo a partir de un objeto con atributos, como una
