from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from app.db.session import engine
from app.api.routes import auth, workouts

app = FastAPI(title="FitTrack API")

# Middleware (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173", "https://fittrack-frontend-34i5.onrender.com/"],  # adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# For dev only; prod me migrations hi use karo
# SQLModel.metadata.create_all(engine)

app.include_router(auth.router)
app.include_router(workouts.router)


@app.get("/health")
def health():
    return {"status": "ok"}