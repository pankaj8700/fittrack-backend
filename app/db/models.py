from datetime import datetime, date
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship


class Workout(SQLModel, table=True):
    __tablename__ = "workouts"  # optional, for clarity

    id: Optional[int] = Field(default=None, primary_key=True)
    userid: int = Field(foreign_key="users.id", index=True)
    date: date
    type: str = Field(max_length=50)
    duration: int  # minutes
    notes: Optional[str] = None
    createdat: datetime = Field(default_factory=datetime.utcnow)

    user: "User" = Relationship(back_populates="workouts")


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(max_length=50, index=True)
    email: str = Field(max_length=100, index=True)
    passwordhash: str = Field(max_length=255)
    createdat: datetime = Field(default_factory=datetime.utcnow)

    workouts: List[Workout] = Relationship(back_populates="user")
