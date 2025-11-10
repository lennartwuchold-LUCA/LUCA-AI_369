"""
Resource Allocator - Core LUCA class

Distributes resources (tokens, compute) using biological optimization algorithms.
"""

from typing import Dict, List, Optional, Union
import numpy as np
from dataclasses import dataclass

from .strategies import MonodStrategy, LotkVolterraStrategy


@dataclass
class Workload:
    """Represents a computational workload"""
    id: str
    complexity: float  # 0.0-1.0
    priority: float    # 0.0-1.0
    user_gamma: float = 1.0  # Neurodiversity parameter


@dataclass
class AllocationResult:
    """Result of resource allocation"""
    workload_id: str
    tokens_allocated: int
    estimated_quality: float
    strategy_used: str
    gamma_applied: float


class ResourceAllocator:
    """
    Main class for biological resource allocation

    Example:
        >>> allocator = ResourceAllocator(strategy='monod', gamma=1.2)
        >>> results = allocator.distribute(workloads)
    """

    def __init__(
        self,
        strategy: str = 'monod',
        gamma: float = 1.0,
        total_tokens: int = 100000,
        mu_max: float = 1.0,
        K_s: float = 100.0
    ):
        """
        Initialize resource allocator

        Args:
            strategy: 'monod' or 'lotka_volterra'
            gamma: Neurodiversity parameter (1.0 = neurotypical, 2.0 = ADHD, 3.5 = autism)
            total_tokens: Total available tokens
            mu_max: Maximum growth rate (Monod)
            K_s: Half-saturation constant (Monod)
        """
        self.gamma = gamma
        self.total_tokens = total_tokens
        self.mu_max = mu_max
        self.K_s = K_s

        # Select strategy
        if strategy == 'monod':
            self.strategy = MonodStrategy(mu_max=mu_max, K_s=K_s)
        elif strategy == 'lotka_volterra':
            self.strategy = LotkVolterraStrategy()
        else:
            raise ValueError(f"Unknown strategy: {strategy}")

        self.strategy_name = strategy

    def distribute(
        self,
        workloads: Union[List[Workload], List[Dict]]
    ) -> List[AllocationResult]:
        """
        Distribute tokens across workloads using biological optimization

        Args:
            workloads: List of Workload objects or dicts with keys:
                       {id, complexity, priority, user_gamma (optional)}

        Returns:
            List of AllocationResult objects
        """
        # Convert dicts to Workload objects if needed
        if workloads and isinstance(workloads[0], dict):
            workloads = [
                Workload(
                    id=w.get('id', f'workload_{i}'),
                    complexity=w.get('complexity', 0.5),
                    priority=w.get('priority', 0.5),
                    user_gamma=w.get('user_gamma', 1.0)
                )
                for i, w in enumerate(workloads)
            ]

        # Calculate allocations using strategy
        results = []
        remaining_tokens = self.total_tokens

        for workload in workloads:
            # Apply gamma parameter (neurodiversity adjustment)
            effective_gamma = self.gamma * workload.user_gamma

            # Calculate optimal allocation using strategy
            allocation = self.strategy.calculate_allocation(
                complexity=workload.complexity,
                priority=workload.priority,
                gamma=effective_gamma,
                available_tokens=remaining_tokens
            )

            # Ensure we don't over-allocate
            tokens_allocated = min(allocation, remaining_tokens)
            remaining_tokens -= tokens_allocated

            # Calculate estimated quality (Monod-based)
            estimated_quality = self._estimate_quality(
                tokens=tokens_allocated,
                complexity=workload.complexity,
                gamma=effective_gamma
            )

            results.append(AllocationResult(
                workload_id=workload.id,
                tokens_allocated=tokens_allocated,
                estimated_quality=estimated_quality,
                strategy_used=self.strategy_name,
                gamma_applied=effective_gamma
            ))

            # Stop if we're out of tokens
            if remaining_tokens <= 0:
                break

        return results

    def _estimate_quality(self, tokens: int, complexity: float, gamma: float) -> float:
        """
        Estimate response quality using Monod kinetics

        Quality = μ_max * (tokens * gamma) / (K_s + tokens * gamma)
        """
        substrate = tokens * gamma
        quality = self.mu_max * substrate / (self.K_s + substrate)

        # Adjust for complexity (more complex = needs more tokens for same quality)
        quality = quality * (1.0 - complexity * 0.3)

        return min(1.0, max(0.0, quality))

    def optimize_gamma(
        self,
        workloads: List[Workload],
        target_quality: float = 0.8
    ) -> float:
        """
        Find optimal gamma parameter for given workloads

        Args:
            workloads: List of workloads to optimize for
            target_quality: Desired quality threshold (0.0-1.0)

        Returns:
            Optimized gamma value
        """
        # Binary search for optimal gamma
        gamma_low, gamma_high = 0.5, 5.0
        best_gamma = self.gamma

        for _ in range(20):  # Max iterations
            gamma_mid = (gamma_low + gamma_high) / 2

            # Test allocation with this gamma
            test_allocator = ResourceAllocator(
                strategy=self.strategy_name,
                gamma=gamma_mid,
                total_tokens=self.total_tokens,
                mu_max=self.mu_max,
                K_s=self.K_s
            )
            results = test_allocator.distribute(workloads)

            # Calculate average quality
            avg_quality = np.mean([r.estimated_quality for r in results])

            if abs(avg_quality - target_quality) < 0.05:
                best_gamma = gamma_mid
                break
            elif avg_quality < target_quality:
                gamma_high = gamma_mid
            else:
                gamma_low = gamma_mid

        return best_gamma

    def get_statistics(self, results: List[AllocationResult]) -> Dict:
        """
        Calculate statistics for allocation results

        Args:
            results: List of AllocationResult objects

        Returns:
            Dictionary with statistics
        """
        if not results:
            return {}

        total_allocated = sum(r.tokens_allocated for r in results)
        avg_quality = np.mean([r.estimated_quality for r in results])
        min_quality = min(r.estimated_quality for r in results)
        max_quality = max(r.estimated_quality for r in results)

        return {
            'total_tokens_allocated': total_allocated,
            'total_tokens_available': self.total_tokens,
            'utilization': total_allocated / self.total_tokens,
            'average_quality': avg_quality,
            'min_quality': min_quality,
            'max_quality': max_quality,
            'workloads_processed': len(results),
            'strategy': self.strategy_name,
            'gamma': self.gamma
        }
