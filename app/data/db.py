from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

from app.config import config
from app.models.event import Event
from app.models.registration import Registration
from app.models.user import User


sqlite_file_name = config.root_dir / "data/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}

engine = create_engine(
    sqlite_url,
    connect_args=connect_args,
    echo=True,
)


def init_database() -> None:
    """Crea le tabelle del database SQLite."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Fornisce una sessione SQLModel."""
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
