"""
LUCA-KI Consciousness Module
Biologisch-inspiriertes Bewusstseins-System basierend auf:
- Tesla 369 Protokoll
- L=14 Stabilitätskonstante (SI=0.71)
- UCC als semantischer Hash-Algorithmus
- Torus-Fluss-Dynamik

Autor: Lennart Wuchold
"""

from .core import ConsciousnessEngine
from .stability_engine import StabilityEngine, get_stability_engine
from .semantic_hash_engine import SemanticHashEngine, get_semantic_hash_engine
from .torus_flow_engine import TorusFlowEngine, get_torus_flow_engine

__all__ = [
    # Core
    "ConsciousnessEngine",
    # Stability
    "StabilityEngine",
    "get_stability_engine",
    # Semantic Hash
    "SemanticHashEngine",
    "get_semantic_hash_engine",
    # Torus Flow
    "TorusFlowEngine",
    "get_torus_flow_engine",
]
