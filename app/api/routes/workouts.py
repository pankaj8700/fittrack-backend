from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.api.deps import get_db, get_current_user
from app.db.models import Workout, User
from app.schemas.workouts import WorkoutCreate, WorkoutRead

router = APIRouter(prefix="/api", tags=["workouts"])


@router.get("/workouts", response_model=List[WorkoutRead])
def list_workouts(
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    workouts = session.exec(
        select(Workout)
        .where(Workout.userid == current_user.id)
        .order_by(Workout.date.desc())
    ).all()
    return workouts


@router.post("/workouts", response_model=WorkoutRead, status_code=status.HTTP_201_CREATED)
def create_workout(
    workout_in: WorkoutCreate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    workout = Workout(
        userid=current_user.id,
        date=workout_in.date,
        type=workout_in.type,
        duration=workout_in.duration,
        notes=workout_in.notes,
    )
    session.add(workout)
    session.commit()
    session.refresh(workout)
    return workout
