from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, StrictStr
from sqlmodel import select

from app.data.db import SessionDep
from app.models.user import User
from app.models.registration import Registration


router = APIRouter()


class UserCreate(BaseModel):
    username: StrictStr
    name: StrictStr
    email: StrictStr


@router.get("/users")
def get_users(session: SessionDep):
    """Return the list of all users stored in the database."""
    users = session.exec(select(User)).all()
    return users


@router.post("/users", status_code=201)
def create_user(user_data: UserCreate, session: SessionDep):
    """Create a new user if the username does not already exist."""
    existing_user = session.get(User, user_data.username)

    if existing_user is not None:
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(
        username=user_data.username,
        name=user_data.name,
        email=user_data.email,
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@router.get("/users/{username}")
def get_user(username: str, session: SessionDep):
    """Return a single user identified by username."""
    user = session.get(User, username)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.delete("/users")
def delete_users(session: SessionDep):
    """Delete all users and all registrations associated with them."""
    registrations = session.exec(select(Registration)).all()
    for registration in registrations:
        session.delete(registration)

    users = session.exec(select(User)).all()
    for user in users:
        session.delete(user)

    session.commit()

    return {"message": "All users deleted"}


@router.delete("/users/{username}")
def delete_user(username: str, session: SessionDep):
    """Delete a user and all registrations associated with that user."""
    user = session.get(User, username)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    registrations = session.exec(
        select(Registration).where(Registration.username == username)
    ).all()

    for registration in registrations:
        session.delete(registration)

    session.delete(user)
    session.commit()

    return {"message": "User deleted"}