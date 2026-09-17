from datetime import date
from pydantic import BaseModel


class CalendarEvent(BaseModel):
    date: date
    homeowner: str
    location: str | None = None
    phone: str | None = None
    shingle_color: str | None = None
    job_runner: str | None = None
    blue_notes: str | None = None


class CalendarEvents(BaseModel):
    events: list[CalendarEvent]
