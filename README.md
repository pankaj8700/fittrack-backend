FitTrack Backend
Backend API for FitTrack built with FastAPI, SQLModel, PostgreSQL, and Alembic migrations. Dependency management via uv.

Stack
FastAPI
SQLModel / SQLAlchemy
PostgreSQL (psycopg2)
Alembic (migrations)
JWT Auth
Project Structure
main.py – FastAPI app entry
config.py – configuration (env vars / .env)
security.py – password hashing + JWT helpers
models.py – SQLModel tables
session.py – DB engine/session
auth.py – auth routes
workouts.py – workout routes
deps.py – dependencies (e.g., current user)
alembic – migrations
alembic.ini – Alembic config
Requirements
Python 3.11+ (recommended)
PostgreSQL running locally or via Docker
uv installed
Environment Variables
Create a .env file in project root (.env):

DATABASE_URL=postgresql+psycopg2://postgres:<PASSWORD>@localhost:5432/fittrack
JWT_SECRET_KEY=change-this-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

Notes:

.env is ignored by git (don’t commit secrets).
In production (Render) you set these in the dashboard.
Local Setup (Windows / PowerShell)
1) Install dependencies
uv sync
2) Run migrations
uv run alembic upgrade head
3) Start the server
API: http://127.0.0.1:8000
Swagger Docs: http://127.0.0.1:8000/docs
Health: http://127.0.0.1:8000/health
Database Migrations (Alembic)
Create a new migration (autogenerate)
uv run alembic revision --autogenerate -m "message"
Apply migrations
uv run alembic upgrade head
Roll back (one revision)
uv run alembic downgrade -1
Important:

alembic and alembic/versions/*.py must be committed to git.
Only ignore caches like __pycache__.
API Usage
Health
GET /health

Response:
{ "status": "ok" }
Authentication (JWT)
Your auth routes are in auth.py. Common pattern:

Register user (or create user)
Login → get JWT access token
Send token in headers for protected routes:
Authorization: Bearer <token>
Example: Login
(Adjust endpoint names if your route path differs.)

Request:

POST /auth/login
Content-Type: application/json
{
  "username": "testuser",
  "password": "testpass"
}
Response (example):

{
  "access_token": "<JWT>",
  "token_type": "bearer"
}
Using token
Authorization: Bearer <JWT>
Workouts API
Workout routes are in workouts.py.

Typical operations:

Create workout
List workouts
Get workout by id
Update workout
Delete workout
Example payload (based on models)
From models.py, workout fields include:

date (date)
type (string)
duration (int)
notes (optional)
Example request:

POST /workouts
Authorization: Bearer <JWT>
Content-Type: application/json
{
  "date": "2026-02-07",
  "type": "Running",
  "duration": 30,
  "notes": "Easy pace"
}

CORS / Middleware
CORS middleware is added in main.py (recommended for frontend usage).
Update allowed origins according to your frontend URL (localhost / deployed domain).

Deploy to Render (FastAPI + Alembic)
1) Create PostgreSQL on Render
Render Dashboard → New → PostgreSQL
Copy the database URL.

2) Create Web Service
Render Dashboard → New → Web Service → connect GitHub repo.

3) Set Environment Variables (Render → Web Service → Environment)
DATABASE_URL = Render Postgres URL
JWT_SECRET_KEY = strong secret
JWT_ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 60
4) Build / Start commands
Build Command

uv sync

Start Command (run migrations then start)

uv run alembic upgrade head && uv run uvicorn app.main:app --host 0.0.0.0 --port $PORT

Why this works:

Ensures DB schema is up-to-date before the app starts.
Troubleshooting
Alembic can’t parse alembic.ini
alembic.ini must be valid INI. Don’t put Python code like:

from app.core.config import settings inside it.
.env not loading
Ensure .env format is correct: KEY=VALUE (no spaces around =)
Ensure config.py uses SettingsConfigDict(env_file=".env").
“password authentication failed for user postgres”
Your DB password is wrong for that database. Fix DATABASE_URL.