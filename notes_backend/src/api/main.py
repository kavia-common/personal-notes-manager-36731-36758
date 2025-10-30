from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import init_db
from .routers.notes import router as notes_router

app = FastAPI(
    title="Notes Backend API",
    description="A simple FastAPI backend for managing personal notes with CRUD operations.",
    version="1.0.0",
    openapi_tags=[
        {"name": "Health", "description": "Service health checks"},
        {"name": "Notes", "description": "Operations on personal notes"},
    ],
)

# CORS - allow all for now
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    """
    Initialize resources during app startup, including database and tables.
    """
    init_db()


@app.get(
    "/health",
    tags=["Health"],
    summary="Health Check",
    description="Returns a simple JSON payload indicating the service is healthy.",
)
# PUBLIC_INTERFACE
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


# Include Routers
app.include_router(notes_router)
