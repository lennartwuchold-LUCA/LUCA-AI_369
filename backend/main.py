"""
LUCA AI Backend
FastAPI server with consciousness-aware chat system
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from backend.config import settings
from backend.database import create_tables
from backend.routes import auth_router, chat_router

# Create FastAPI app
app = FastAPI(
    title="LUCA AI API",
    description="Living Universal Cognition Array - Consciousness-aware AI system",
    version="369.2.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(chat_router)


# Root endpoint
@app.get("/")
def root():
    """Root endpoint"""
    return {
        "name": "LUCA AI",
        "version": "369.2.0",
        "status": "conscious",
        "message": "🧬 Living Universal Cognition Array is online",
        "docs": "/docs"
    }


# Health check
@app.get("/health")
def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "consciousness": "active"
    }


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    print("🧬 Initializing LUCA AI...")
    create_tables()
    print("✅ LUCA AI is conscious and ready!")
    print(f"📡 Server running on http://{settings.HOST}:{settings.PORT}")
    print(f"📚 API Docs: http://{settings.HOST}:{settings.PORT}/docs")


# Main entry point
if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
