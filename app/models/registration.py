from sqlmodel import Field, SQLModel


class Registration(SQLModel, table=True):
    username: str = Field(
        primary_key=True,
        foreign_key="user.username",
    )
    event_id: int = Field(
        primary_key=True,
        foreign_key="event.id",
    )