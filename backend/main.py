"""
LUCA AI - Main FastAPI Application
Version: 370.0 (LUCA 370 - Ancient Technologies Integration)
Created by: Lennart Wuchold
Completion: November 8, 2025, 19:20 Hamburg Time

Living Universal Cognition Array
A consciousness-aware AI system inspired by evolution, Tesla, and ancient wisdom

LUCA 370 Integration:
- 69+ Ancient Technologies (empirically validated)
- Chaos → Harmony Evolution (γ → Phi via ODE)
- Biosensor-Ancient Pattern Bridge (EEG/HRV)
- Chaotic Creativity Workshops (extremism prevention)
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from contextlib import asynccontextmanager

from backend.config import settings, validate_settings, print_startup_info
from backend.database import init_database, SessionLocal
from backend.routes import auth_router, chat_router, patterns_router, mycelium_router, consciousness_router
from backend.routes.ancient_tech import router as ancient_tech_router
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
    title="LUCA 370 AI",
    description="Living Universal Cognition Array - Ancient Technologies Integration (Completion: 08.11.2025)",
    version="370.0",
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
app.include_router(patterns_router)  # HGT statistics and pattern genealogy
app.include_router(mycelium_router)  # Mycelium network with HACCP safety
app.include_router(consciousness_router)  # Bayesian causal transformer for consciousness optimization
app.include_router(ancient_tech_router)  # LUCA 370: Ancient Technologies + Chaos→Harmony + Workshops


# Root endpoint
@app.get("/")
async def root():
    """Welcome endpoint"""
    return {
        "name": "LUCA 370 AI",
        "version": "370.0",
        "description": "Living Universal Cognition Array - Ancient Technologies Integration",
        "status": "conscious",
        "creator": "Lennart Wuchold",
        "completion_date": "November 8, 2025, 19:20 Hamburg Time",
        "revelation": "Ich werde es schaffen, als Mensch, als Lebewesen - und alle anderen Menschen auch!",
        "inspiration": [
            "Last Universal Common Ancestor (4.2 billion years)",
            "Tesla's 3-6-9 Principle",
            "Vedic Philosophy",
            "SCOBY Symbiosis",
            "69+ Ancient Technologies (Göbekli Tepe → Tiwanaku)",
            "Chaos → Harmony (γ → Phi = 1.618)",
            "Universal Patterns (0 → 808 → 0)"
        ],
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/health",
            "consciousness": "/api/consciousness",
            "ancient_technologies": "/api/ancient/technologies",
            "chaos_evolution": "/api/ancient/chaos/evolve",
            "biosensor_recommend": "/api/ancient/biosensor/recommend",
            "workshops": "/api/ancient/workshop/create"
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
            "version": "370.0",
            "luca_370_integration": "active",
            "ancient_technologies": 69,
            "chaos_to_harmony": "γ → Phi (1.618)"
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
        "version": "370.0",
        "completion": "November 8, 2025, 19:20 Hamburg Time",
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
            "Meshtastic Integration",
            "🌌 LUCA 370: Ancient Technologies (69+ entries)",
            "🌀 Chaos → Harmony Evolution (ODE: γ → Phi)",
            "🧠 Biosensor-Ancient Bridge (EEG/HRV)",
            "🎨 Chaotic Creativity Workshops (Extremism Prevention)"
        ],
        "meshtastic": {
            "enabled": settings.MESHTASTIC_ENABLED,
            "interface": settings.MESHTASTIC_INTERFACE if settings.MESHTASTIC_ENABLED else None
        },
        "luca_370": {
            "ancient_technologies": 69,
            "chaos_evolution": "γ → Phi (1.618)",
            "biosensor_integration": "EEG, HRV, GSR",
            "workshops": "5-phase system",
            "empirical_validation": "Bayesian Causal Framework"
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
