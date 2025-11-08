"""
Workload Generators for Benchmarking
Realistic workload simulation for different GPU tasks
"""

import random
import numpy as np
from typing import List, Dict
from dataclasses import dataclass


@dataclass
class Workload:
    """Base workload class"""
    name: str
    intensity: float  # 0.0 - 1.0
    duration: float  # seconds
    memory_mb: int
    compute_ops: int


class WorkloadGenerator:
    """Base workload generator"""

    @staticmethod
    def generate_ml_training(batch_size: int = 32, epochs: int = 10) -> Workload:
        """Generate ML training workload"""
        return Workload(
            name=f"ML Training (batch={batch_size}, epochs={epochs})",
            intensity=0.9,
            duration=epochs * 60.0,
            memory_mb=batch_size * 100,
            compute_ops=batch_size * epochs * 1000000
        )

    @staticmethod
    def generate_inference(requests_per_sec: int = 100) -> Workload:
        """Generate inference workload"""
        return Workload(
            name=f"Inference ({requests_per_sec} req/s)",
            intensity=0.6,
            duration=60.0,
            memory_mb=2048,
            compute_ops=requests_per_sec * 10000
        )

    @staticmethod
    def generate_compute(complexity: str = "medium") -> Workload:
        """Generate general compute workload"""
        complexity_map = {
            "low": (0.3, 30, 1024, 100000),
            "medium": (0.6, 60, 4096, 1000000),
            "high": (0.9, 120, 8192, 10000000)
        }

        intensity, duration, memory, ops = complexity_map.get(complexity, complexity_map["medium"])

        return Workload(
            name=f"Compute ({complexity})",
            intensity=intensity,
            duration=duration,
            memory_mb=memory,
            compute_ops=ops
        )


class MLTrainingWorkload:
    """ML Training workload simulator"""

    @staticmethod
    def generate_batch(model_size: str = "medium") -> List[Workload]:
        """Generate a batch of ML training workloads"""
        size_config = {
            "small": (16, 5),
            "medium": (32, 10),
            "large": (64, 20)
        }

        batch_size, epochs = size_config.get(model_size, size_config["medium"])

        workloads = []
        for i in range(5):
            workload = WorkloadGenerator.generate_ml_training(batch_size, epochs)
            workloads.append(workload)

        return workloads


class InferenceWorkload:
    """Inference workload simulator"""

    @staticmethod
    def generate_stream(duration: int = 60, qps: int = 100) -> List[Workload]:
        """Generate inference workload stream"""
        workloads = []

        for i in range(duration):
            workload = WorkloadGenerator.generate_inference(qps)
            workloads.append(workload)

        return workloads


class ComputeWorkload:
    """General compute workload simulator"""

    @staticmethod
    def generate_mixed() -> List[Workload]:
        """Generate mixed complexity workloads"""
        complexities = ["low", "low", "medium", "medium", "high"]
        workloads = []

        for complexity in complexities:
            workload = WorkloadGenerator.generate_compute(complexity)
            workloads.append(workload)

        return workloads
