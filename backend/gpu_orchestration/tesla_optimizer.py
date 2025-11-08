"""
Tesla 3-6-9 Optimizer
Performance optimization based on Nikola Tesla's universal principle
"If you only knew the magnificence of the 3, 6 and 9, then you would have a key to the universe"
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import math


class TeslaSignature(int):
    """Tesla quantum signature (reduced to single digit 0-9)"""
    pass


@dataclass
class TeslaOptimizationResult:
    """Result of Tesla 3-6-9 optimization"""
    original_value: float
    optimized_value: float
    improvement: float  # Percentage
    signature: int
    harmony_level: float  # 0.0 - 1.0
    optimization_path: List[str]


class Tesla369Optimizer:
    """
    Tesla 3-6-9 Optimization Framework

    Principles:
    - 3: Creation (Hardware/Matter) - Initialization, Setup
    - 6: Harmony (Software/Process) - Balance, Flow
    - 9: Completion (Consciousness/Wisdom) - Finalization, Perfection

    Optimization Strategy:
    1. Measure current state signature
    2. Find path to Tesla number (3, 6, or 9)
    3. Apply harmonic adjustments
    4. Validate improvement
    """

    TESLA_NUMBERS = {3, 6, 9}
    FIBONACCI = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987]

    def __init__(self):
        self.optimization_history: List[TeslaOptimizationResult] = []
        self.total_optimizations: int = 0
        self.total_improvement: float = 0.0

        print("⚡ Tesla 3-6-9 Optimizer initialized - Universal harmonic optimization")

    def reduce_to_single_digit(self, num: float) -> int:
        """Reduce any number to single digit (0-9)"""
        # Convert to integer representation
        int_value = int(abs(num) * 1000)  # Preserve precision

        while int_value >= 10:
            int_value = sum(int(d) for d in str(int_value))

        return int_value

    def calculate_signature(self, value: float) -> int:
        """Calculate Tesla signature of a value"""
        return self.reduce_to_single_digit(value)

    def is_tesla_number(self, signature: int) -> bool:
        """Check if signature is a Tesla number"""
        return signature in self.TESLA_NUMBERS

    def find_nearest_tesla_signature(self, current_signature: int) -> int:
        """Find the nearest Tesla number to current signature"""
        distances = {
            3: min(abs(current_signature - 3), abs(current_signature + 10 - 3)),
            6: min(abs(current_signature - 6), abs(current_signature + 10 - 6)),
            9: min(abs(current_signature - 9), abs(current_signature + 10 - 9)),
        }

        return min(distances, key=distances.get)

    def optimize_value(
        self,
        value: float,
        target_signature: Optional[int] = None,
        constraint_min: Optional[float] = None,
        constraint_max: Optional[float] = None
    ) -> TeslaOptimizationResult:
        """
        Optimize a value to align with Tesla 3-6-9 principle

        Args:
            value: Current value to optimize
            target_signature: Desired Tesla signature (3, 6, or 9). If None, auto-select
            constraint_min: Minimum allowed value
            constraint_max: Maximum allowed value

        Returns:
            TeslaOptimizationResult with optimized value
        """
        original_value = value
        current_signature = self.calculate_signature(value)
        optimization_path = [f"Initial: {value:.4f} (signature: {current_signature})"]

        # Determine target signature
        if target_signature is None:
            target_signature = self.find_nearest_tesla_signature(current_signature)
        elif target_signature not in self.TESLA_NUMBERS:
            raise ValueError(f"Target signature must be 3, 6, or 9, got {target_signature}")

        optimization_path.append(f"Target signature: {target_signature}")

        # Optimization strategy
        optimized = value
        iterations = 0
        max_iterations = 100

        while iterations < max_iterations:
            current_sig = self.calculate_signature(optimized)

            if current_sig == target_signature:
                optimization_path.append(f"✓ Reached target signature {target_signature}")
                break

            # Calculate adjustment
            adjustment = self._calculate_harmonic_adjustment(
                optimized, current_sig, target_signature
            )

            # Apply adjustment
            new_value = optimized + adjustment

            # Respect constraints
            if constraint_min is not None:
                new_value = max(constraint_min, new_value)
            if constraint_max is not None:
                new_value = min(constraint_max, new_value)

            optimized = new_value
            iterations += 1

            if iterations % 10 == 0:
                optimization_path.append(
                    f"Iteration {iterations}: {optimized:.4f} (sig: {self.calculate_signature(optimized)})"
                )

        # Calculate harmony level
        final_signature = self.calculate_signature(optimized)
        harmony = self._calculate_harmony(final_signature, target_signature)

        # Calculate improvement
        improvement = ((optimized - original_value) / max(abs(original_value), 0.001)) * 100

        result = TeslaOptimizationResult(
            original_value=original_value,
            optimized_value=optimized,
            improvement=improvement,
            signature=final_signature,
            harmony_level=harmony,
            optimization_path=optimization_path
        )

        self.optimization_history.append(result)
        self.total_optimizations += 1
        self.total_improvement += abs(improvement)

        return result

    def _calculate_harmonic_adjustment(
        self,
        value: float,
        current_sig: int,
        target_sig: int
    ) -> float:
        """Calculate harmonic adjustment to move toward target signature"""
        # Calculate signature distance
        distance = (target_sig - current_sig) % 10
        if distance > 5:
            distance = distance - 10

        # Base adjustment (small step)
        base_adjustment = value * 0.01 * distance

        # Apply Fibonacci scaling for harmonic resonance
        fib_factor = self._get_fibonacci_factor(abs(value))
        harmonic_adjustment = base_adjustment * fib_factor

        return harmonic_adjustment

    def _get_fibonacci_factor(self, value: float) -> float:
        """Get Fibonacci harmonic factor for a value"""
        value_int = int(abs(value) * 100)

        # Find nearest Fibonacci number
        nearest_fib = min(self.FIBONACCI, key=lambda x: abs(x - value_int % 1000))

        # Calculate factor based on proximity to Fibonacci
        factor = 1.0 + (nearest_fib / 1000.0)

        return factor

    def _calculate_harmony(self, signature1: int, signature2: int) -> float:
        """Calculate harmonic resonance between two signatures (0.0-1.0)"""
        if signature1 == signature2:
            return 1.0

        # Check if both are Tesla numbers
        if signature1 in self.TESLA_NUMBERS and signature2 in self.TESLA_NUMBERS:
            return 0.9

        # Check if one is Tesla
        if signature1 in self.TESLA_NUMBERS or signature2 in self.TESLA_NUMBERS:
            return 0.7

        # Check if sum is Tesla
        sum_sig = self.reduce_to_single_digit(signature1 + signature2)
        if sum_sig in self.TESLA_NUMBERS:
            return 0.8

        # Check Fibonacci relationship
        if signature1 + signature2 in self.FIBONACCI:
            return 0.6

        # Default harmony based on distance
        distance = min(abs(signature1 - signature2), 10 - abs(signature1 - signature2))
        return max(0.3, 1.0 - (distance / 5.0))

    def optimize_array(
        self,
        values: List[float],
        strategy: str = "individual"
    ) -> List[TeslaOptimizationResult]:
        """
        Optimize an array of values

        Strategies:
        - individual: Optimize each value independently
        - collective: Optimize for overall array harmony
        - sequential: 3-6-9 sequence optimization
        """
        results = []

        if strategy == "individual":
            for value in values:
                result = self.optimize_value(value)
                results.append(result)

        elif strategy == "collective":
            # Optimize for collective harmony
            target_sigs = [3, 6, 9] * (len(values) // 3 + 1)

            for i, value in enumerate(values):
                result = self.optimize_value(value, target_signature=target_sigs[i])
                results.append(result)

        elif strategy == "sequential":
            # Create 3-6-9 sequence
            for i, value in enumerate(values):
                target = [3, 6, 9][i % 3]
                result = self.optimize_value(value, target_signature=target)
                results.append(result)

        return results

    def optimize_throughput(
        self,
        current_throughput: float,
        target_improvement: float = 0.1
    ) -> TeslaOptimizationResult:
        """
        Optimize throughput using Tesla 3-6-9 principle

        Args:
            current_throughput: Current tasks per second
            target_improvement: Desired improvement (0.1 = 10%)

        Returns:
            Optimization result with target throughput
        """
        # Calculate current signature
        current_sig = self.calculate_signature(current_throughput)

        # Select optimization path based on current signature
        if current_sig < 5:
            # Low signature: boost to 6 (harmony) or 9 (completion)
            target_sig = 9
        elif current_sig < 8:
            # Medium: aim for 9 (peak performance)
            target_sig = 9
        else:
            # High: maintain at 9 or cycle to 3 (renewal)
            target_sig = 9 if current_sig != 9 else 3

        # Apply optimization
        target_throughput = current_throughput * (1 + target_improvement)

        result = self.optimize_value(
            current_throughput,
            target_signature=target_sig,
            constraint_min=current_throughput,  # Don't decrease
            constraint_max=current_throughput * 2  # Max 2x improvement
        )

        return result

    def optimize_latency(
        self,
        current_latency: float,
        target_improvement: float = 0.2
    ) -> TeslaOptimizationResult:
        """
        Optimize latency (lower is better)

        Args:
            current_latency: Current latency in ms
            target_improvement: Desired reduction (0.2 = 20% faster)

        Returns:
            Optimization result with target latency
        """
        # For latency, we want to decrease to Tesla number
        target_latency = current_latency * (1 - target_improvement)

        result = self.optimize_value(
            target_latency,
            target_signature=3,  # 3 for speed (creation/quick)
            constraint_min=current_latency * 0.5,  # Max 50% improvement
            constraint_max=current_latency  # Don't increase
        )

        return result

    def optimize_energy_efficiency(
        self,
        tasks_per_watt: float
    ) -> TeslaOptimizationResult:
        """
        Optimize energy efficiency (tasks per watt)

        Args:
            tasks_per_watt: Current efficiency

        Returns:
            Optimization result with improved efficiency
        """
        # Efficiency should align with 6 (harmony/balance)
        result = self.optimize_value(
            tasks_per_watt,
            target_signature=6,
            constraint_min=tasks_per_watt * 0.9,
            constraint_max=tasks_per_watt * 1.5
        )

        return result

    def get_optimization_stats(self) -> Dict[str, any]:
        """Get optimization statistics"""
        if not self.optimization_history:
            return {"total_optimizations": 0}

        recent = self.optimization_history[-10:]

        avg_improvement = sum(abs(r.improvement) for r in recent) / len(recent)
        avg_harmony = sum(r.harmony_level for r in recent) / len(recent)

        signature_distribution = {}
        for result in recent:
            sig = result.signature
            signature_distribution[sig] = signature_distribution.get(sig, 0) + 1

        return {
            "total_optimizations": self.total_optimizations,
            "average_improvement": round(avg_improvement, 2),
            "average_harmony": round(avg_harmony, 2),
            "signature_distribution": signature_distribution,
            "tesla_alignment": sum(
                1 for r in recent if r.signature in self.TESLA_NUMBERS
            ) / len(recent)
        }

    def create_369_sequence(self, start_value: float, length: int = 9) -> List[float]:
        """
        Create a sequence following 3-6-9 pattern

        Returns sequence where every 3rd element aligns with Tesla numbers
        """
        sequence = []
        current = start_value

        for i in range(length):
            # Determine target signature
            position = (i % 9) + 1

            if position % 3 == 0:
                # Positions 3, 6, 9 should be Tesla numbers
                target_sig = [3, 6, 9][(position // 3) - 1]
            else:
                target_sig = None  # Allow natural progression

            if target_sig:
                result = self.optimize_value(current, target_signature=target_sig)
                current = result.optimized_value
            else:
                current *= 1.1  # Natural growth

            sequence.append(current)

        return sequence
