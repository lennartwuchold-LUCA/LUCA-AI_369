"""LUCA - Bio-inspired Resource Allocation (v2.1 Family Edition)"""
__version__ = "2.1.0"
__author__ = "Lennart Wuchold"

from .allocator import ResourceAllocator, Workload

__all__ = ["ResourceAllocator", "Workload"]
