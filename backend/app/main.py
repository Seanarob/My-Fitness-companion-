"""
FIT-AI Next Gen - FastAPI Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes import health, users, auth, exercises
from app.db.client import MongoDBClient

app = FastAPI(
    title="FIT-AI API",
    description="FIT-AI Next Gen Backend API",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.frontend_api_base_url,
        settings.ios_api_base_url,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_db_client():
    """Initialize database connection on startup"""
    await MongoDBClient.connect()


@app.on_event("shutdown")
async def shutdown_db_client():
    """Close database connection on shutdown"""
    await MongoDBClient.disconnect()


# Include routers (public routes)
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(exercises.router, prefix="/api/v1", tags=["exercises"])

# Include routers (protected routes)
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "FIT-AI API", "version": "1.0.0"}

