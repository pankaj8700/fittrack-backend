from datetime import date
from pydantic import BaseModel

class WorkoutCreate(BaseModel):
    date: date
    type: str
    duration: int
    notes: str | None = None

class WorkoutRead(WorkoutCreate):
    id: int

    class Config:
        from_attributes = True
