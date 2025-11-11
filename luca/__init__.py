"""LUCA - Bio-inspired Resource Allocation (v2.1 Family Edition)"""
__version__ = "3.6.9-alpha"
__author__ = "Lennart Wuchold"

from .allocator import ResourceAllocator, Workload
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
