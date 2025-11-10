"""
Basic LUCA Usage Example

Demonstrates resource allocation using Monod kinetics
"""

from luca import ResourceAllocator, Workload

# Example 1: Simple allocation with Monod strategy
print("=" * 60)
print("Example 1: Basic Monod Allocation")
print("=" * 60)

allocator = ResourceAllocator(
    strategy='monod',
    gamma=1.2,  # Slightly above neurotypical baseline
    total_tokens=10000
)

workloads = [
    Workload(id="task_1", complexity=0.3, priority=0.8),
    Workload(id="task_2", complexity=0.7, priority=0.5),
    Workload(id="task_3", complexity=0.5, priority=0.9),
]

results = allocator.distribute(workloads)

for result in results:
    print(f"\n{result.workload_id}:")
    print(f"  Tokens allocated: {result.tokens_allocated}")
    print(f"  Estimated quality: {result.estimated_quality:.2%}")
    print(f"  Gamma applied: {result.gamma_applied:.2f}")

# Get statistics
stats = allocator.get_statistics(results)
print(f"\nOverall Statistics:")
print(f"  Utilization: {stats['utilization']:.2%}")
print(f"  Average quality: {stats['average_quality']:.2%}")
print(f"  Min quality: {stats['min_quality']:.2%}")

# Example 2: Neurodiversity-aware allocation
print("\n" + "=" * 60)
print("Example 2: Neurodiversity-Aware Allocation")
print("=" * 60)

# ADHD user (gamma = 2.0) vs neurotypical (gamma = 1.0)
adhd_allocator = ResourceAllocator(strategy='monod', gamma=2.0)
neurotypical_allocator = ResourceAllocator(strategy='monod', gamma=1.0)

workload = [Workload(id="task", complexity=0.5, priority=0.7)]

adhd_result = adhd_allocator.distribute(workload)[0]
neuro_result = neurotypical_allocator.distribute(workload)[0]

print(f"\nADHD user (γ=2.0):")
print(f"  Tokens: {adhd_result.tokens_allocated}")
print(f"  Quality: {adhd_result.estimated_quality:.2%}")

print(f"\nNeurotypical user (γ=1.0):")
print(f"  Tokens: {neuro_result.tokens_allocated}")
print(f"  Quality: {neuro_result.estimated_quality:.2%}")

print(f"\nDifference: {adhd_result.tokens_allocated - neuro_result.tokens_allocated} tokens")
print(f"ADHD user gets {(adhd_result.tokens_allocated / neuro_result.tokens_allocated - 1) * 100:.1f}% more tokens")

# Example 3: Optimize gamma for target quality
print("\n" + "=" * 60)
print("Example 3: Gamma Optimization")
print("=" * 60)

allocator = ResourceAllocator(strategy='monod')

test_workloads = [
    Workload(id=f"task_{i}", complexity=0.5, priority=0.6)
    for i in range(5)
]

optimal_gamma = allocator.optimize_gamma(
    workloads=test_workloads,
    target_quality=0.8
)

print(f"\nOptimal gamma for 80% quality target: {optimal_gamma:.2f}")

# Test with optimal gamma
optimized_allocator = ResourceAllocator(strategy='monod', gamma=optimal_gamma)
optimized_results = optimized_allocator.distribute(test_workloads)
avg_quality = sum(r.estimated_quality for r in optimized_results) / len(optimized_results)

print(f"Achieved quality: {avg_quality:.2%}")
