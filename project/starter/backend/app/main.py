# project/starter/app/main.py
# Module 5 Project — AI-Ready Task Manager API
#
# Run with: uvicorn app.main:app --reload  (from project/starter/ folder)
# Docs at:  http://127.0.0.1:8000/docs

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import auth, tasks

from fastapi import Request
from fastapi.responses import JSONResponse
from app.utils.exceptions import AppException

from fastapi import Depends
from app.auth import get_current_user
from app.schemas.user import UserResponse

# TODO: Import Base, engine from database
# TODO: Import routers

app = FastAPI(
    title="AI-Ready Task Manager",
    description="A task management API with JWT auth and an AI suggestion endpoint.",
    version="1.0.0",
)

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


# TODO: Configure CORS (specific origins, not *)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # TODO: update for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO: Create DB tables
Base.metadata.create_all(bind=engine)

# TODO: Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])


@app.get("/", tags=["health"])
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "message": "Task Manager API is running"}


@app.get("/users/me", response_model=UserResponse, tags=["users"])
def get_current_user_profile(
    current_user=Depends(get_current_user)
):
    """Return the authenticated user's profile."""
    return current_user


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
