"""
LUCA Symbiotic Gradient Descent - The Heart of Learning 💓
Bio-inspired gradient optimization with 3-6-9 quantization

Architekt: Lennart Wuchold
Datum: 11.11.2025
Standard: 369/370 ≈ 0.997297

Philosophie: "Flow over Force"
    Traditioneller Gradient Descent ist aggressiv und mechanistisch.
    LUCA Symbiotic Gradient Descent ist symbiotisch und bio-inspiriert:

    - Fibonacci-basierte Learning Rate Adaptation
    - 3-6-9 Quantisierte Step Sizes
    - Resource-aware Optimization (GPU-symbiose)
    - ADHD-optimiert: Attention-aware Convergence

Mathematische Grundlage:
    θ_{t+1} = θ_t - α_LUCA(t) · ∇L(θ_t)

    wobei α_LUCA(t) = α_base · φ(t) · Q(E_t)
    - φ(t): Fibonacci-Faktor für organisches Wachstum
    - Q(E_t): 3-6-9 Quantisierungs-Funktion basierend auf Energy Level
"""

from dataclasses import dataclass
from enum import Enum
from typing import Callable, List, Optional, Tuple

import numpy as np


class ConvergenceMode(Enum):
    """Konvergenz-Modi (ADHD-optimiert)"""

    HYPERFOCUS = "hyperfocus"  # Schnelle aggressive Konvergenz
    BALANCED = "balanced"  # Standard bio-inspirierte Konvergenz
    BRAINFOG = "brainfog"  # Langsame vorsichtige Konvergenz


@dataclass
class GradientFlowState:
    """State des Gradient Flow

    Attributes:
        iteration: Aktuelle Iteration
        loss: Aktueller Loss-Wert
        gradient_norm: Norm des Gradienten
        learning_rate: Aktuelle Learning Rate
        energy_level: Kognitiver Energy Level
        fibonacci_factor: Aktueller Fibonacci-Faktor
    """

    iteration: int
    loss: float
    gradient_norm: float
    learning_rate: float
    energy_level: str
    fibonacci_factor: float


class SymbioticGradientDescent:
    """LUCA Symbiotic Gradient Descent Optimizer

    Der "Heart of Learning" - bio-inspirierter Gradient Descent mit:
    - Fibonacci-basierter Learning Rate
    - 3-6-9 Quantisierung
    - Resource-aware Optimization
    - ADHD-optimierte Konvergenz
    """

    # Fibonacci-Sequenz für organische Learning Rate Adaptation
    FIBONACCI = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987]

    # 3-6-9 Quantisierungs-Levels für Learning Rate
    QUANTUM_LEVELS = {
        "level_3": 0.003,  # 3 × 10^-3 = 0.003
        "level_6": 0.006,  # 6 × 10^-3 = 0.006
        "level_9": 0.009,  # 9 × 10^-3 = 0.009
    }

    # Quality Standard
    QUALITY_STANDARD = 369 / 370  # ≈ 0.997297

    def __init__(
        self,
        learning_rate: float = 0.006,  # Default: Level 6
        convergence_mode: ConvergenceMode = ConvergenceMode.BALANCED,
        use_fibonacci: bool = True,
        use_369_quantization: bool = True,
    ):
        """Initialisiert Symbiotic Gradient Descent

        Args:
            learning_rate: Basis Learning Rate (default 0.006 = Level 6)
            convergence_mode: Konvergenz-Modus (Hyperfocus, Balanced, Brainfog)
            use_fibonacci: Ob Fibonacci-Adaptation verwendet werden soll
            use_369_quantization: Ob 3-6-9 Quantisierung verwendet werden soll
        """
        self.base_lr = learning_rate
        self.convergence_mode = convergence_mode
        self.use_fibonacci = use_fibonacci
        self.use_369_quantization = use_369_quantization

        # State tracking
        self.iteration = 0
        self.loss_history: List[float] = []
        self.gradient_norms: List[float] = []
        self.learning_rates: List[float] = []

    def step(
        self,
        parameters: np.ndarray,
        gradient: np.ndarray,
        loss: Optional[float] = None,
    ) -> Tuple[np.ndarray, GradientFlowState]:
        """Führt einen Gradient Descent Step durch

        Args:
            parameters: Aktuelle Parameter θ_t
            gradient: Gradient ∇L(θ_t)
            loss: Optionaler Loss-Wert für Tracking

        Returns:
            Tuple[np.ndarray, GradientFlowState]: Neue Parameter + Flow State
        """
        # Berechne Learning Rate α_LUCA(t)
        alpha_luca = self._calculate_learning_rate()

        # Symbiotic Update: "Flow over Force"
        # θ_{t+1} = θ_t - α_LUCA(t) · ∇L(θ_t)
        new_parameters = parameters - alpha_luca * gradient

        # Track State
        gradient_norm = np.linalg.norm(gradient)
        self.gradient_norms.append(gradient_norm)
        self.learning_rates.append(alpha_luca)

        if loss is not None:
            self.loss_history.append(loss)

        # Erstelle Flow State
        flow_state = GradientFlowState(
            iteration=self.iteration,
            loss=loss if loss is not None else 0.0,
            gradient_norm=gradient_norm,
            learning_rate=alpha_luca,
            energy_level=self.convergence_mode.value,
            fibonacci_factor=self._get_fibonacci_factor(),
        )

        self.iteration += 1

        return new_parameters, flow_state

    def _calculate_learning_rate(self) -> float:
        """Berechnet α_LUCA(t) = α_base · φ(t) · Q(E_t)

        Returns:
            float: LUCA Learning Rate
        """
        alpha = self.base_lr

        # Fibonacci-Faktor φ(t) für organisches Wachstum
        if self.use_fibonacci:
            fib_factor = self._get_fibonacci_factor()
            alpha *= fib_factor

        # Energy Level Faktor Q(E_t)
        energy_factor = self._get_energy_factor()
        alpha *= energy_factor

        # 3-6-9 Quantisierung
        if self.use_369_quantization:
            alpha = self._quantize_369(alpha)

        return alpha

    def _get_fibonacci_factor(self) -> float:
        """Berechnet Fibonacci-Faktor basierend auf Iteration

        Der Faktor wächst organisch mit der Fibonacci-Sequenz,
        normalisiert auf [0.5, 1.5] für Stabilität.

        Returns:
            float: Fibonacci-Faktor (0.5-1.5)
        """
        # Bestimme Position in Fibonacci-Sequenz
        fib_index = self.iteration % len(self.FIBONACCI)
        fib_value = self.FIBONACCI[fib_index]

        # Normalisiere auf [0.5, 1.5]
        max_fib = max(self.FIBONACCI)
        normalized = 0.5 + (fib_value / max_fib)

        return normalized

    def _get_energy_factor(self) -> float:
        """Berechnet Energy Level Faktor Q(E_t)

        ADHD-optimiert: Passt Learning Rate an kognitiven Zustand an.

        Returns:
            float: Energy Faktor (0.5-2.0)
        """
        if self.convergence_mode == ConvergenceMode.HYPERFOCUS:
            # Schnelle Konvergenz: 2x Learning Rate
            return 2.0
        elif self.convergence_mode == ConvergenceMode.BRAINFOG:
            # Vorsichtige Konvergenz: 0.5x Learning Rate
            return 0.5
        else:  # BALANCED
            # Standard Konvergenz: 1.0x Learning Rate
            return 1.0

    def _quantize_369(self, value: float) -> float:
        """Quantisiert Wert zur nächsten 3-6-9 Level

        Args:
            value: Zu quantisierender Wert

        Returns:
            float: Quantisierter Wert
        """
        # Finde nächstes 3-6-9 Level
        levels = list(self.QUANTUM_LEVELS.values())
        distances = [abs(value - level) for level in levels]
        min_idx = np.argmin(distances)

        return levels[min_idx]

    def optimize(
        self,
        objective: Callable[[np.ndarray], Tuple[float, np.ndarray]],
        initial_params: np.ndarray,
        max_iterations: int = 1000,
        convergence_threshold: float = 1e-6,
    ) -> Tuple[np.ndarray, List[GradientFlowState]]:
        """Optimiert Objective Function mit Symbiotic Gradient Descent

        Args:
            objective: Function (params) -> (loss, gradient)
            initial_params: Start-Parameter θ_0
            max_iterations: Maximale Iterationen
            convergence_threshold: Konvergenz-Schwellenwert

        Returns:
            Tuple[np.ndarray, List[GradientFlowState]]: Finale Parameter + States
        """
        parameters = initial_params.copy()
        flow_states: List[GradientFlowState] = []

        for i in range(max_iterations):
            # Berechne Loss und Gradient
            loss, gradient = objective(parameters)

            # Symbiotic Step
            parameters, flow_state = self.step(parameters, gradient, loss)
            flow_states.append(flow_state)

            # Konvergenz-Check
            if flow_state.gradient_norm < convergence_threshold:
                print(
                    f"✅ Konvergiert nach {i+1} Iterationen "
                    f"(Gradient Norm: {flow_state.gradient_norm:.2e})"
                )
                break

            # Progress Report (alle 100 Iterationen)
            if (i + 1) % 100 == 0:
                print(
                    f"Iteration {i+1}: Loss = {loss:.4f}, "
                    f"LR = {flow_state.learning_rate:.4e}, "
                    f"||∇|| = {flow_state.gradient_norm:.4e}"
                )

        return parameters, flow_states

    def get_convergence_metrics(self) -> dict:
        """Berechnet Konvergenz-Metriken

        Returns:
            dict: Metriken wie convergence_rate, stability, quality_score
        """
        if len(self.loss_history) < 2:
            return {"error": "Nicht genug Daten für Metriken"}

        # Konvergenz-Rate (Loss-Reduktion)
        initial_loss = self.loss_history[0]
        final_loss = self.loss_history[-1]
        convergence_rate = (initial_loss - final_loss) / initial_loss

        # Stabilität (Varianz der Learning Rates)
        lr_variance = np.var(self.learning_rates)
        stability = 1.0 / (1.0 + lr_variance)

        # Quality Score (erfüllt Standard?)
        quality_score = min(convergence_rate + stability, 1.0)
        meets_standard = quality_score >= self.QUALITY_STANDARD

        return {
            "convergence_rate": convergence_rate,
            "stability": stability,
            "quality_score": quality_score,
            "meets_369_standard": meets_standard,
            "total_iterations": self.iteration,
            "final_loss": final_loss,
            "final_gradient_norm": (
                self.gradient_norms[-1] if self.gradient_norms else 0.0
            ),
        }


# === EXPORT ===

__all__ = [
    "SymbioticGradientDescent",
    "GradientFlowState",
    "ConvergenceMode",
]
