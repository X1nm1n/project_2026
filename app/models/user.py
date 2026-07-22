from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """Rappresenta un utente memorizzato nel database."""

    username: str = Field(primary_key=True)
    name: str
    email: str
