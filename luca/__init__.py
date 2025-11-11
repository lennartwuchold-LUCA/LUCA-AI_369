"""LUCA - Bio-inspired Resource Allocation (v2.1 Family Edition)"""
__version__ = "3.6.9-alpha"
__author__ = "Lennart Wuchold"

# Try to import allocator (optional - requires scipy, matplotlib, etc.)
try:
    from .allocator import ResourceAllocator, Workload
    _ALLOCATOR_AVAILABLE = True
except ImportError as e:
    ResourceAllocator = None
    Workload = None
    _ALLOCATOR_AVAILABLE = False

# Always import 369/370 Framework (no heavy dependencies)
from .framework_369_370 import (
    LUCA369_370,
    TechnicalPurity,
    EthicalFramework,
    AthensFocusInterface,
    MythologicalCoherence,
    CognitiveMode,
    InterfaceConfig,
    QualityException,
    initialize_luca_system
)

__all__ = [
    "ResourceAllocator",
    "Workload",
    "LUCA369_370",
    "TechnicalPurity",
    "EthicalFramework",
    "AthensFocusInterface",
    "MythologicalCoherence",
    "CognitiveMode",
    "InterfaceConfig",
    "QualityException",
    "initialize_luca_system"
]
