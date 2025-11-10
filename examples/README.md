# LUCA Examples

Usage examples for LUCA resource allocator.

## Basic Usage

Simple resource allocation with Monod strategy:

```bash
python basic_usage.py
```

**Demonstrates:**
- Basic Monod allocation
- Neurodiversity-aware allocation (ADHD vs neurotypical)
- Gamma optimization for target quality

## Neurodiversity Comparison

Compare allocation across different neurot types:

```bash
python neurodiversity_comparison.py
```

**Demonstrates:**
- Neurotypical (γ = 1.0)
- ADHD (γ = 2.0)
- Autism (γ = 3.5)
- Energy level adjustments (hyperfocus, normal, brainfog)

## Quick Start

```python
from luca import ResourceAllocator, Workload

# Create allocator
allocator = ResourceAllocator(
    strategy='monod',
    gamma=1.2,  # variance parameter
    total_tokens=10000
)

# Define workloads
workloads = [
    Workload(id="task_1", complexity=0.5, priority=0.8),
    Workload(id="task_2", complexity=0.7, priority=0.6),
]

# Allocate resources
results = allocator.distribute(workloads)

# Check results
for result in results:
    print(f"{result.workload_id}: {result.tokens_allocated} tokens")
```

## Strategies

### Monod Strategy

Based on fermentation kinetics:

```python
allocator = ResourceAllocator(strategy='monod')
```

### Lotka-Volterra Strategy

Based on predator-prey dynamics:

```python
allocator = ResourceAllocator(strategy='lotka_volterra')
```

## Gamma Parameter

Controls variance in optimization:

- **γ = 1.0**: Neurotypical baseline
- **γ = 2.0**: ADHD (faster context switching)
- **γ = 3.5**: Autism (sustained focus)

```python
from luca.neurodiversity import GAMMA_ADHD

allocator = ResourceAllocator(gamma=GAMMA_ADHD.value)
```
