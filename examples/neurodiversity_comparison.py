"""
Neurodiversity Comparison Example

Demonstrates how gamma parameter adapts allocation for different neurot types
"""

from luca import ResourceAllocator, Workload
from luca.neurodiversity import (
    NeurodiversityParameter,
    Neurotype,
    GAMMA_NEUROTYPICAL,
    GAMMA_ADHD,
    GAMMA_AUTISM
)

print("=" * 70)
print("Neurodiversity Parameter Comparison")
print("=" * 70)

# Create workload
workload = [
    Workload(
        id="complex_task",
        complexity=0.7,
        priority=0.8
    )
]

# Test different neurotypes
neurotypes = [
    ("Neurotypical", GAMMA_NEUROTYPICAL),
    ("ADHD", GAMMA_ADHD),
    ("Autism", GAMMA_AUTISM),
]

results = {}

for name, gamma_param in neurotypes:
    allocator = ResourceAllocator(
        strategy='monod',
        gamma=gamma_param.value,
        total_tokens=10000
    )

    result = allocator.distribute(workload)[0]
    results[name] = result

    print(f"\n{name} (γ = {gamma_param.value}):")
    print(f"  Description: {gamma_param.description}")
    print(f"  Tokens allocated: {result.tokens_allocated}")
    print(f"  Estimated quality: {result.estimated_quality:.2%}")

# Compare ADHD vs Neurotypical
print("\n" + "=" * 70)
print("ADHD vs Neurotypical Comparison")
print("=" * 70)

adhd_tokens = results["ADHD"].tokens_allocated
neuro_tokens = results["Neurotypical"].tokens_allocated
diff_percentage = ((adhd_tokens / neuro_tokens) - 1) * 100

print(f"\nADHD receives {diff_percentage:+.1f}% tokens vs Neurotypical")
print(f"This reflects: Faster saturation (quicker context switching)")

# Energy level adjustments
print("\n" + "=" * 70)
print("Energy Level Adjustments (ADHD User)")
print("=" * 70)

adhd_gamma = GAMMA_ADHD

energy_levels = ['hyperfocus', 'normal', 'brainfog']

for energy in energy_levels:
    adjusted_gamma = adhd_gamma.adjust_for_energy(energy)

    allocator = ResourceAllocator(
        strategy='monod',
        gamma=adjusted_gamma,
        total_tokens=10000
    )

    result = allocator.distribute(workload)[0]

    print(f"\n{energy.upper()}:")
    print(f"  Adjusted γ: {adjusted_gamma:.2f}")
    print(f"  Tokens: {result.tokens_allocated}")
    print(f"  Quality: {result.estimated_quality:.2%}")
