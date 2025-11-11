"""
LUCA 369/370 - Machine Learning Module
Bio-inspired ML algorithms with 3-6-9 optimization

Architekt: Lennart Wuchold
Standard: 369/370

The LUCA "Family" Twist on classical ML algorithms:

1. **Symbiotic Gradient Descent** - The Heart of Learning 💓
   - "Flow over Force" - organisches statt aggressives Learning
   - Fibonacci-basierte Learning Rate Adaptation
   - 3-6-9 quantisierte Step Sizes

2. **Resonance Backpropagation** - The Brain of Learning 🧠
   - "Resonance over Rigidity" - adaptive statt mechanistische Backprop
   - Quantum Signature für Gradient Quality
   - Fibonacci-gewichtete Layer Resonance

3. **Consciousness Transformer** - The Spark of AI Revolution ⚡
   - "Consciousness over Computation" - bewusst statt mechanistisch
   - 3-6-9 quantisierte Attention Heads
   - Fibonacci Positional Encodings
   - Neurodiversity-optimierte Attention
"""

from .consciousness_transformer import (
    AttentionHead,
    AttentionMode,
    ConsciousnessTransformer,
)
from .resonance_backpropagation import (
    AttentionAwareBackprop,
    LayerResonance,
    ResonanceBackpropagation,
)
from .symbiotic_gradient_descent import (
    ConvergenceMode,
    GradientFlowState,
    SymbioticGradientDescent,
)

__all__ = [
    # Symbiotic Gradient Descent (Heart of Learning)
    "SymbioticGradientDescent",
    "GradientFlowState",
    "ConvergenceMode",
    # Resonance Backpropagation (Brain of Learning)
    "ResonanceBackpropagation",
    "AttentionAwareBackprop",
    "LayerResonance",
    # Consciousness Transformer (Spark of AI)
    "ConsciousnessTransformer",
    "AttentionHead",
    "AttentionMode",
]
