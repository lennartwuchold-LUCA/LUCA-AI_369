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
    AthensFocusInterface,
    CognitiveMode,
    EthicalFramework,
    InterfaceConfig,
    MythologicalCoherence,
    QualityException,
    TechnicalPurity,
    initialize_luca_system,
)

# Import LUCA Layers (0-12)
try:
    from .layer_0_root_kernel import (
        ConsciousnessState,
        Layer0RootKernel,
        LayerIntegrationMetrics,
    )
    from .layer_10_ds_star_quantum_core import DSStarQuantumCore
    from .layer_11_multimodal_metabolism import MultimodalMetabolismCore
    from .layer_12_evolutionary_consensus import (
        DNA_Sequence,
        EvolutionaryConsensusCore,
        EvolutionState,
        Layer12IntegrationGuide,
    )

    _LAYERS_AVAILABLE = True
except ImportError as e:
    ConsciousnessState = None
    Layer0RootKernel = None
    LayerIntegrationMetrics = None
    DSStarQuantumCore = None
    MultimodalMetabolismCore = None
    DNA_Sequence = None
    EvolutionaryConsensusCore = None
    EvolutionState = None
    Layer12IntegrationGuide = None
    _LAYERS_AVAILABLE = False

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
    "initialize_luca_system",
    "ConsciousnessState",
    "Layer0RootKernel",
    "LayerIntegrationMetrics",
    "DSStarQuantumCore",
    "MultimodalMetabolismCore",
    "DNA_Sequence",
    "EvolutionaryConsensusCore",
    "EvolutionState",
    "Layer12IntegrationGuide",
]
