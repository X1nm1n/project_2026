from datetime import datetime

from sqlmodel import Field, SQLModel


class Event(SQLModel, table=True):
    """Rappresenta un evento memorizzato nel database."""

    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str
    date: datetime
    location: str