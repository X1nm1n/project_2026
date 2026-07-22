from datetime import datetime

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, StrictStr
from sqlmodel import select

from app.data.db import SessionDep
from app.models.event import Event
from app.models.user import User
from app.models.registration import Registration


router = APIRouter()


class EventCreate(BaseModel):
    title: StrictStr
    description: StrictStr
    date: datetime
    location: StrictStr


class UserRegistration(BaseModel):
    username: StrictStr
    name: StrictStr
    email: StrictStr


@router.get("/events")
def get_events(session: SessionDep):
    """Return the list of all events stored in the database."""
    events = session.exec(select(Event)).all()
    return events


@router.post("/events", status_code=201)
def create_event(event_data: EventCreate, session: SessionDep):
    """Create a new event and store it in the database."""
    event = Event(
        title=event_data.title,
        description=event_data.description,
        date=event_data.date,
        location=event_data.location,
    )

    session.add(event)
    session.commit()
    session.refresh(event)

    return event


@router.get("/events/{id}")
def get_event(id: int, session: SessionDep):
    """Return a single event identified by its id."""
    event = session.get(Event, id)

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    return event


@router.put("/events/{id}")
def update_event(id: int, event_data: EventCreate, session: SessionDep):
    """Update an existing event identified by its id."""
    event = session.get(Event, id)

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    event.title = event_data.title
    event.description = event_data.description
    event.date = event_data.date
    event.location = event_data.location

    session.add(event)
    session.commit()
    session.refresh(event)

    return event


@router.delete("/events")
def delete_events(session: SessionDep):
    """Delete all events and all registrations associated with them."""
    registrations = session.exec(select(Registration)).all()
    for registration in registrations:
        session.delete(registration)

    events = session.exec(select(Event)).all()
    for event in events:
        session.delete(event)

    session.commit()

    return {"message": "All events deleted"}


@router.delete("/events/{id}")
def delete_event(id: int, session: SessionDep):
    """Delete an event and all registrations associated with that event."""
    event = session.get(Event, id)

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    registrations = session.exec(
        select(Registration).where(Registration.event_id == id)
    ).all()

    for registration in registrations:
        session.delete(registration)

    session.delete(event)
    session.commit()

    return {"message": "Event deleted"}


@router.post("/events/{id}/register", status_code=201)
def register_user_to_event(id: int, user_data: UserRegistration, session: SessionDep):
    """Register a user to an event, creating the user if it does not exist."""
    event = session.get(Event, id)

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    user = session.get(User, user_data.username)

    if user is None:
        user = User(
            username=user_data.username,
            name=user_data.name,
            email=user_data.email,
        )
        session.add(user)
        session.commit()
        session.refresh(user)

    existing_registration = session.exec(
        select(Registration).where(
            Registration.username == user_data.username,
            Registration.event_id == id,
        )
    ).first()

    if existing_registration is not None:
        return {"message": "User already registered"}

    registration = Registration(
        username=user_data.username,
        event_id=id,
    )

    session.add(registration)
    session.commit()

    return registration