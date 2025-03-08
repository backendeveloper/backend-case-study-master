"""
Main entry point for TravelAI application.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from travelai.src.api.config import settings
from travelai.src.api.ledgers.router import router as ledger_router

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description=f"{settings.APP_NAME} API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ledger_router)


@app.get("/")
async def root():
    """
    Root endpoint.
    """
    return {
        "message": f"Welcome to the {settings.APP_NAME} API",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
    }