from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.data.db import SessionDep
from app.models.event import Event
from app.models.user import User
from app.models.registration import Registration


router = APIRouter()


@router.get("/registrations")
def get_registrations(session: SessionDep):
    """Return the list of all registrations stored in the database."""
    registrations = session.exec(select(Registration)).all()
    return registrations


@router.delete("/registrations")
def delete_registration(username: str, event_id: int, session: SessionDep):
    """Delete a single registration identified by username and event_id."""
    user = session.get(User, username)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    event = session.get(Event, event_id)

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    registration = session.exec(
        select(Registration).where(
            Registration.username == username,
            Registration.event_id == event_id,
        )
    ).first()

    if registration is None:
        raise HTTPException(status_code=404, detail="Registration not found")

    session.delete(registration)
    session.commit()

    return {"message": "Registration deleted"}