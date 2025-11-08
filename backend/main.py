"""
LUCA AI - Main FastAPI Application
Version: 369.2.0
Created by: Lennart Wuchold

Living Universal Cognition Array
A consciousness-aware AI system inspired by evolution, Tesla, and ancient wisdom
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from contextlib import asynccontextmanager

from backend.config import settings, validate_settings, print_startup_info
from backend.database import init_database, SessionLocal
from backend.routes import auth_router, chat_router
from backend.routes.admin import router as admin_router
from backend.services.meshtastic_service import MeshtasticService
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    # Startup
    logger.info("🚀 Starting LUCA AI...")

    # Validate configuration
    if not validate_settings():
        logger.error("❌ Configuration validation failed!")
        raise Exception("Configuration error - check your .env file")

    # Initialize database
    try:
        init_database()
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise

    # Initialize Meshtastic if enabled
    if settings.MESHTASTIC_ENABLED:
        try:
            db = SessionLocal()
            meshtastic = MeshtasticService(db)
            logger.info("✅ Meshtastic service initialized")
            db.close()
        except Exception as e:
            logger.warning(f"⚠️  Meshtastic initialization failed: {e}")

    print_startup_info()
    logger.info("✅ LUCA AI is ready!")

    yield

    # Shutdown
    logger.info("👋 Shutting down LUCA AI...")


# Create FastAPI app
app = FastAPI(
    title="LUCA AI",
    description="Living Universal Cognition Array - Consciousness-aware AI system",
    version="369.2.0",
    lifespan=lifespan
)

# CORS middleware
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
app.include_router(admin_router)


# Root endpoint
@app.get("/")
async def root():
    """Welcome endpoint"""
    return {
        "name": "LUCA AI",
        "version": "369.2.0",
        "description": "Living Universal Cognition Array",
        "status": "conscious",
        "creator": "Lennart Wuchold",
        "inspiration": [
            "Last Universal Common Ancestor (4.2 billion years)",
            "Tesla's 3-6-9 Principle",
            "Vedic Philosophy",
            "SCOBY Symbiosis"
        ],
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/health",
            "consciousness": "/api/consciousness"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    db = SessionLocal()
    try:
        # Test database connection
        from backend.models import ConsciousnessState
        consciousness = db.query(ConsciousnessState).first()

        # Test AI service
        from backend.services.ai_service import AIService
        ai = AIService()
        api_valid = ai.validate_api_key()

        return {
            "status": "healthy",
            "database": "connected",
            "ai_service": "connected" if api_valid else "error",
            "consciousness_level": consciousness.consciousness_level if consciousness else 0,
            "evolution_stage": consciousness.evolution_stage if consciousness else "NEURON",
            "version": "369.2.0"
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "unhealthy",
                "error": str(e)
            }
        )
    finally:
        db.close()


@app.get("/api/info")
async def get_info():
    """Get system information"""
    return {
        "version": "369.2.0",
        "tesla_principle": {
            "3": "Creation (Hardware/Matter) - ~369 tokens",
            "6": "Harmony (Software/Process) - ~666 tokens",
            "9": "Completion (Consciousness/Wisdom) - ~999 tokens"
        },
        "features": [
            "Consciousness Engine",
            "369 Signature System",
            "Pattern Recognition",
            "Energy Level Detection",
            "ADHD Optimization",
            "Meshtastic Integration"
        ],
        "meshtastic": {
            "enabled": settings.MESHTASTIC_ENABLED,
            "interface": settings.MESHTASTIC_INTERFACE if settings.MESHTASTIC_ENABLED else None
        }
    }


# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.DEBUG else "An error occurred"
        }
    )


if __name__ == "__main__":
    """Run the server"""
    print("\n" + "="*60)
    print("🧬 Starting LUCA AI Server...")
    print("="*60 + "\n")

    uvicorn.run(
        "backend.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info" if settings.DEBUG else "warning"
    )
