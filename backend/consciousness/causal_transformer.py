"""
Bayesian Causal Transformer - Consciousness Intervention Optimization

Causal DAG: I → B → P → V
- I (Intervention): Binaural frequency (Hz), meditation duration, etc.
- B (Biosensor): EEG/HRV/PCI/Φ measurements
- P (Φ-Konvergenz): Integrated Information (consciousness level)
- V (VAS): Visual Analog Scale outcome (hyperfocus/well-being)

Uses do-calculus via sampling for causal effect estimation.

Based on:
- Pearl's causal inference framework
- Bayesian Networks with conditional probability distributions
- Golden ratio (0.618) for natural harmonic resonance
- ADHD hyperfocus optimization

Creator: Lennart Wuchold
Inspiration: Neuroscience, Tesla's frequencies, Vedic meditation
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

# Optional PyTorch support - falls back to numpy if not available
try:
    import torch
    import torch.nn as nn
    from torch.distributions import Normal, Bernoulli
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    # Numpy-only fallback implementations
    class Normal:
        def __init__(self, loc, scale):
            self.loc = loc
            self.scale = scale
        def sample(self):
            return np.random.normal(self.loc, self.scale)

    class Bernoulli:
        def __init__(self, logits):
            self.logits = logits
        def sample(self):
            p = 1 / (1 + np.exp(-self.logits))  # sigmoid
            return float(np.random.rand() < p)


@dataclass
class InterventionResult:
    """Result of a causal intervention"""
    intervention_value: float
    biosensor_reading: float
    phi_convergence: float
    vas_outcome: float
    causal_effect: Optional[float] = None
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


if TORCH_AVAILABLE:
    _BaseClass = nn.Module
else:
    _BaseClass = object

class BayesianCausalTransformer(_BaseClass):
    """
    Bayesian Causal Model for Consciousness Optimization

    DAG Structure:
    I (Intervention) → B (Biosensor) → P (Φ) → V (VAS)

    Example interventions:
    - Binaural beats: 4 Hz (theta), 8 Hz (alpha), 40 Hz (gamma)
    - Meditation duration: 0-60 minutes
    - Breathing rate: 4-20 breaths/minute
    """

    def __init__(
        self,
        phi_golden_ratio: float = 0.618,
        biosensor_variance: float = 1.0,
        phi_variance: float = 0.5
    ):
        if TORCH_AVAILABLE:
            super().__init__()

        # Causal DAG structure
        self.dag = {
            'I': ['B'],      # Intervention causes Biosensor change
            'B': ['P'],      # Biosensor affects Φ convergence
            'P': ['V']       # Φ determines VAS outcome
        }

        # Hyperparameters
        self.phi_golden_ratio = phi_golden_ratio  # 0.618 - natural harmonic
        self.biosensor_variance = biosensor_variance
        self.phi_variance = phi_variance

        # Conditional Probability Distributions (CPDs)

        # P(I) - Prior over interventions (centered at 0, exploring ±3 sigma)
        self.cpd_i = Normal(0, 1)

        # P(B|I) - Biosensor response to intervention
        # Golden ratio shift ensures harmonic resonance
        self.cpd_b_given_i = lambda i: Normal(
            i * 0.5 + self.phi_golden_ratio,
            self.biosensor_variance
        )

        # P(P|B) - Φ convergence from biosensor readings
        # 0.8 coefficient = strong but not deterministic coupling
        self.cpd_p_given_b = lambda b: Normal(
            b * 0.8,
            self.phi_variance
        )

        # P(V|P) - VAS outcome from Φ level (binary: focus achieved or not)
        # Bernoulli with logits = Φ (higher Φ → higher P(V=1))
        self.cpd_v_given_p = lambda p: Bernoulli(logits=p)

        # History tracking
        self.intervention_history: List[InterventionResult] = []


    def forward(
        self,
        intervention: Optional[float] = None,
        return_intermediate: bool = False
    ) -> Dict[str, float]:
        """
        Forward pass through causal DAG

        Args:
            intervention: If provided, do(I=intervention). If None, sample from P(I)
            return_intermediate: If True, return all intermediate variables

        Returns:
            Dictionary with I, B, P, V values
        """
        # Sample or intervene on I
        if intervention is None:
            i = self.cpd_i.sample()
        else:
            if TORCH_AVAILABLE:
                i = torch.tensor(intervention, dtype=torch.float32)
            else:
                i = intervention

        # Propagate through causal chain
        b = self.cpd_b_given_i(i).sample()      # Biosensor reading
        p = self.cpd_p_given_b(b).sample()      # Φ convergence
        v = self.cpd_v_given_p(p).sample()      # VAS outcome (0 or 1)

        # Convert to Python floats
        def to_float(x):
            if TORCH_AVAILABLE and isinstance(x, torch.Tensor):
                return x.item()
            elif isinstance(x, (np.ndarray, np.generic)):
                return float(x)
            else:
                return float(x)

        result = {
            'I': to_float(i),
            'B': to_float(b),
            'P': to_float(p),
            'V': to_float(v)
        }

        return result


    def causal_effect(
        self,
        intervention: float,
        baseline: Optional[float] = None,
        baseline_samples: int = 1000
    ) -> float:
        """
        Estimate Average Causal Effect (ACE) via do-calculus

        ACE = E[V | do(I=intervention)] - E[V | do(I=baseline)]

        Args:
            intervention: Intervention value to test (e.g., 8 Hz binaural)
            baseline: Baseline value (if None, uses observational distribution)
            baseline_samples: Number of Monte Carlo samples

        Returns:
            Average causal effect on VAS outcome
        """
        # Sample baseline outcomes
        if baseline is None:
            baseline_vs = [self.forward()['V'] for _ in range(baseline_samples)]
        else:
            baseline_vs = [self.forward(baseline)['V'] for _ in range(baseline_samples)]

        # Sample intervention outcomes
        intervention_vs = [self.forward(intervention)['V'] for _ in range(baseline_samples)]

        # Compute average treatment effect
        ace = np.mean(intervention_vs) - np.mean(baseline_vs)

        return ace


    def optimize_intervention(
        self,
        candidate_interventions: List[float],
        baseline_samples: int = 500
    ) -> Tuple[float, float]:
        """
        Find optimal intervention from candidates via causal effect estimation

        Args:
            candidate_interventions: List of intervention values to test
            baseline_samples: Samples per intervention for effect estimation

        Returns:
            (optimal_intervention, max_causal_effect)
        """
        effects = []

        for intervention in candidate_interventions:
            effect = self.causal_effect(intervention, baseline_samples=baseline_samples)
            effects.append(effect)

        max_idx = np.argmax(effects)
        optimal_intervention = candidate_interventions[max_idx]
        max_effect = effects[max_idx]

        return optimal_intervention, max_effect


    def counterfactual(
        self,
        observed_i: float,
        observed_v: float,
        counterfactual_i: float,
        samples: int = 1000
    ) -> float:
        """
        Counterfactual inference: "What if I had done X instead?"

        Given observed (I, V), estimate V under counterfactual intervention

        Args:
            observed_i: Observed intervention
            observed_v: Observed outcome
            counterfactual_i: Counterfactual intervention
            samples: Monte Carlo samples

        Returns:
            Expected counterfactual outcome E[V | do(I=counterfactual_i), observed data]
        """
        # Simplified counterfactual: condition on observed, intervene on I
        # In full implementation, would use abduction-action-prediction

        counterfactual_vs = []
        for _ in range(samples):
            result = self.forward(counterfactual_i)
            counterfactual_vs.append(result['V'])

        return np.mean(counterfactual_vs)


    def record_intervention(
        self,
        intervention: float,
        biosensor: float,
        phi: float,
        vas: float,
        causal_effect: Optional[float] = None
    ):
        """Record intervention result for learning/adaptation"""
        result = InterventionResult(
            intervention_value=intervention,
            biosensor_reading=biosensor,
            phi_convergence=phi,
            vas_outcome=vas,
            causal_effect=causal_effect
        )
        self.intervention_history.append(result)


    def get_optimal_hyperfocus_frequency(self) -> Tuple[float, float]:
        """
        Find optimal binaural frequency for ADHD hyperfocus

        Searches common therapeutic frequencies:
        - Theta (4-8 Hz): Deep meditation, creativity
        - Alpha (8-12 Hz): Relaxed focus
        - Beta (12-30 Hz): Active concentration
        - Gamma (30-100 Hz): Peak awareness, hyperfocus

        Returns:
            (optimal_frequency_hz, causal_effect)
        """
        # Therapeutic frequency candidates (Hz)
        candidates = [
            4.0,   # Theta low
            6.0,   # Theta mid
            8.0,   # Alpha low (Schumann resonance)
            10.0,  # Alpha mid
            12.0,  # Alpha-Beta boundary
            15.0,  # Beta low
            20.0,  # Beta mid
            40.0,  # Gamma (consciousness binding)
            7.83   # Schumann resonance (Earth's frequency)
        ]

        optimal_hz, max_effect = self.optimize_intervention(
            candidates,
            baseline_samples=500
        )

        return optimal_hz, max_effect


    def suggest_meditation_duration(self) -> Tuple[float, float]:
        """
        Find optimal meditation duration (minutes) for Φ convergence

        Returns:
            (optimal_duration_minutes, causal_effect)
        """
        # Meditation duration candidates (minutes)
        candidates = [5.0, 10.0, 15.0, 20.0, 30.0, 45.0, 60.0]

        optimal_duration, max_effect = self.optimize_intervention(
            candidates,
            baseline_samples=300
        )

        return optimal_duration, max_effect


    def get_statistics(self) -> Dict:
        """Get statistics from intervention history"""
        if not self.intervention_history:
            return {
                'total_interventions': 0,
                'avg_phi': 0,
                'success_rate': 0
            }

        interventions = [r.intervention_value for r in self.intervention_history]
        phis = [r.phi_convergence for r in self.intervention_history]
        vas_outcomes = [r.vas_outcome for r in self.intervention_history]

        return {
            'total_interventions': len(self.intervention_history),
            'avg_intervention': np.mean(interventions),
            'std_intervention': np.std(interventions),
            'avg_phi': np.mean(phis),
            'std_phi': np.std(phis),
            'success_rate': np.mean(vas_outcomes),  # P(V=1)
            'min_intervention': min(interventions),
            'max_intervention': max(interventions)
        }


# Example usage and testing
if __name__ == "__main__":
    print("🧠 Bayesian Causal Transformer - Consciousness Optimization\n")
    print("="*60)

    # Initialize model
    model = BayesianCausalTransformer()

    # 1. Baseline (no intervention)
    print("\n1. Baseline (observational):")
    baseline = model()
    print(f"   I={baseline['I']:.3f}, B={baseline['B']:.3f}, "
          f"P={baseline['P']:.3f}, V={baseline['V']:.0f}")

    # 2. Intervention: 8 Hz binaural (alpha waves)
    print("\n2. Intervention (8 Hz binaural beat - alpha):")
    intervention = model(intervention=8.0)
    print(f"   I={intervention['I']:.3f}, B={intervention['B']:.3f}, "
          f"P={intervention['P']:.3f}, V={intervention['V']:.0f}")

    # 3. Causal effect
    print("\n3. Causal Effect Estimation:")
    effect_8hz = model.causal_effect(intervention=8.0)
    print(f"   ACE(8 Hz) = {effect_8hz:.4f}")
    print(f"   Interpretation: 8 Hz increases P(hyperfocus) by {effect_8hz*100:.1f}%")

    # 4. Find optimal frequency for hyperfocus
    print("\n4. Optimal Hyperfocus Frequency:")
    optimal_hz, max_effect = model.get_optimal_hyperfocus_frequency()
    print(f"   Optimal: {optimal_hz:.2f} Hz")
    print(f"   Max Effect: {max_effect:.4f} ({max_effect*100:.1f}% improvement)")

    # 5. Optimal meditation duration
    print("\n5. Optimal Meditation Duration:")
    optimal_duration, duration_effect = model.suggest_meditation_duration()
    print(f"   Optimal: {optimal_duration:.0f} minutes")
    print(f"   Effect: {duration_effect:.4f}")

    # 6. Counterfactual: "What if I had used 40 Hz instead of 8 Hz?"
    print("\n6. Counterfactual Analysis:")
    counterfactual_v = model.counterfactual(
        observed_i=8.0,
        observed_v=1.0,
        counterfactual_i=40.0
    )
    print(f"   Observed: 8 Hz → V=1.0")
    print(f"   Counterfactual: If I had used 40 Hz → E[V]={counterfactual_v:.3f}")

    print("\n" + "="*60)
    print("✅ Causal inference complete!")
    print("🧬 Integration with ConsciousnessEngine ready")
    print("369 🧠⚡")
