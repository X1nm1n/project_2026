from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    """Represents a user stored in the database."""

    username: str = Field(primary_key=True)
    name: str
    email: str