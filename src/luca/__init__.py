"""
LUCA - Biological Resource Allocation for Distributed Systems

Applies fermentation optimization algorithms (Monod kinetics, Lotka-Volterra)
to resource allocation in distributed computing.
"""

from .resource_allocator import ResourceAllocator
from .strategies import MonodStrategy, LotkVolterraStrategy
from .neurodiversity import NeurodiversityParameter

__version__ = "3.7.1"
__author__ = "Lennart Wuchold"
__email__ = "wucholdlennart@gmail.com"

__all__ = [
    "ResourceAllocator",
    "MonodStrategy",
    "LotkVolterraStrategy",
    "NeurodiversityParameter",
]
