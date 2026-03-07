from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    full_name: str = Field(default="")
    hashed_password: str


class UserCreate(SQLModel):
    email: str
    full_name: str = Field(default="")
    password: str


class UserRead(SQLModel):
    id: int
    email: str
    full_name: str
    model_config = {
        "from_attributes": True
    }  # Puede crear un modelo a partir de un objeto con atributos, como una instancia de SQLAlchemy
