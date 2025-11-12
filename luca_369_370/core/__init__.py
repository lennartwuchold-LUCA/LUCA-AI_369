"""
LUCA 369/370 - Core Module
Info-Block-Engine Kernkomponenten + Mathematische Formalisierung

Architekt: Lennart Wuchold
Standard: 369/370
"""

from .block_formatter import BlockFormatter
from .fibonacci_optimizer import EnergyLevel, FibonacciOptimizer, OptimizationResult
from .growth_kinetics import (
    GrowthKineticsEngine,
    GrowthParameters,
    GrowthPhase,
    GrowthState,
    calculate_monod_growth,
    simulate_fermentation_batch,
)
from .info_block_engine import BlockType, InfoBlock, InfoBlockEngine, QualityException
from .integrated_response import IntegratedResponseSystem
from .kimi_synergy import KimiSynergyValidator, SynergyMetrics, SynergyResult
from .metabolic_pathways import (
    MetabolicMode,
    MetabolicParameters,
    MetabolicPathwayEngine,
    MetabolicState,
    ReasoningDepth,
    calculate_atp_yield,
    optimize_metabolic_strategy,
    simulate_metabolic_scenario,
    verify_metabolic_quality,
)
from .population_dynamics import (
    InteractionType,
    PopulationDynamicsEngine,
    PopulationParameters,
    PopulationState,
    UserState,
    simulate_scoby_dynamics,
)
from .progressive_disclosure import (
    DisclosureMode,
    ProgressiveBlockFormatter,
    ProgressiveDisclosureEngine,
    ProgressiveState,
    UserState,
)
from .quality_validator import QualityValidator
from .quantum_signature import QuantumLevel, QuantumSignature, QuantumSignatureEngine
from .scoby_orchestration import (
    AgentRole,
    SCOBYAgent,
    SCOBYOrchestrationEngine,
    SCOBYState,
    Task,
    TaskType,
    simulate_scoby_collective,
    verify_scoby_quality,
)
from .ds_star_quantum import (
    AnalysisType,
    CulturalContext,
    CulturalResonance,
    DSStarAnalysisResult,
    DSStarQuantumCore,
    NetworkRoutingPrediction,
    ResourceForecast,
    analyze_data,
    generate_sample_data,
    verify_ds_star_quality,
)
from .token_validator import TokenCountMethod, TokenLengthValidator, ValidationResult

__all__ = [
    # Info-Block-Engine
    "InfoBlockEngine",
    "InfoBlock",
    "BlockType",
    "QualityException",
    "BlockFormatter",
    "QualityValidator",
    # Progressive Disclosure
    "ProgressiveDisclosureEngine",
    "ProgressiveBlockFormatter",
    "DisclosureMode",
    "UserState",
    "ProgressiveState",
    "IntegratedResponseSystem",
    # Mathematische Formalisierung (3-6-9)
    "QuantumSignatureEngine",
    "QuantumSignature",
    "QuantumLevel",
    "TokenLengthValidator",
    "ValidationResult",
    "TokenCountMethod",
    "FibonacciOptimizer",
    "OptimizationResult",
    "EnergyLevel",
    # Kimi-Synergie-Validierung
    "KimiSynergyValidator",
    "SynergyMetrics",
    "SynergyResult",
    # Layer 6: Growth Kinetics (Bio-inspired)
    "GrowthKineticsEngine",
    "GrowthParameters",
    "GrowthPhase",
    "GrowthState",
    "calculate_monod_growth",
    "simulate_fermentation_batch",
    # Layer 7: Population Dynamics (SCOBY-inspired)
    "PopulationDynamicsEngine",
    "PopulationParameters",
    "PopulationState",
    "UserState",
    "InteractionType",
    "simulate_scoby_dynamics",
    # Layer 8: Metabolic Pathways (HRM-inspired)
    "MetabolicMode",
    "MetabolicParameters",
    "MetabolicPathwayEngine",
    "MetabolicState",
    "ReasoningDepth",
    "calculate_atp_yield",
    "optimize_metabolic_strategy",
    "simulate_metabolic_scenario",
    "verify_metabolic_quality",
    # Layer 9: SCOBY Orchestration (Collective Intelligence)
    "AgentRole",
    "SCOBYAgent",
    "SCOBYOrchestrationEngine",
    "SCOBYState",
    "Task",
    "TaskType",
    "simulate_scoby_collective",
    "verify_scoby_quality",
    # Layer 10: DS-STAR Quantum Core (Data Science with Cultural Cosmology)
    "AnalysisType",
    "CulturalContext",
    "CulturalResonance",
    "DSStarAnalysisResult",
    "DSStarQuantumCore",
    "NetworkRoutingPrediction",
    "ResourceForecast",
    "analyze_data",
    "generate_sample_data",
    "verify_ds_star_quality",
]
