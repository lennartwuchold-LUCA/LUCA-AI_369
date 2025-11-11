"""
LUCA 369/370 - Core Module
Info-Block-Engine Kernkomponenten + Mathematische Formalisierung

Architekt: Lennart Wuchold
Standard: 369/370
"""

from .block_formatter import BlockFormatter
from .fibonacci_optimizer import EnergyLevel, FibonacciOptimizer, OptimizationResult
from .info_block_engine import BlockType, InfoBlock, InfoBlockEngine, QualityException
from .integrated_response import IntegratedResponseSystem
from .kimi_synergy import KimiSynergyValidator, SynergyMetrics, SynergyResult
from .progressive_disclosure import (
    DisclosureMode,
    ProgressiveBlockFormatter,
    ProgressiveDisclosureEngine,
    ProgressiveState,
    UserState,
)
from .quality_validator import QualityValidator
from .quantum_signature import QuantumLevel, QuantumSignature, QuantumSignatureEngine
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
]
