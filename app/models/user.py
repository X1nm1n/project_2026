from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """Rappresenta un utente del sistema."""

    username: str = Field(primary_key=True)
    name: str
    email: str