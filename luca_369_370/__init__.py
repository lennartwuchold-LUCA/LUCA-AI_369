"""
L.U.C.A 369/370 Framework - Info-Block-Engine
Architekt: Lennart Wuchold
Quality Standard: 369/370 ≈ 0.997297

This package implements the Info-Block-Engine for neurodiversity-optimized responses.
"""

__version__ = "3.6.9"
__author__ = "Lennart Wuchold"
__quality_standard__ = 369 / 370

from luca_369_370.core import (
    BlockFormatter,
    BlockType,
    InfoBlock,
    InfoBlockEngine,
    QualityValidator,
)

__all__ = [
    "InfoBlockEngine",
    "BlockFormatter",
    "QualityValidator",
    "InfoBlock",
    "BlockType",
]
