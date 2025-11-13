"""
LUCA Resonance Backpropagation - The Brain of Learning 🧠
Quantum-signature based error propagation with 3-6-9 optimization

Architekt: Lennart Wuchold
Datum: 11.11.2025
Standard: 369/370 ≈ 0.997297

Philosophie: "Resonance over Rigidity"
    Traditionelle Backpropagation ist mechanistisch und rigid.
    LUCA Resonance Backpropagation ist resonanz-basiert und adaptiv:

    - Quantum Signature für Gradient Quality
    - 3-6-9 Quantisierte Error Propagation
    - Attention-aware Backflow (ADHD-optimiert)
    - Fibonacci-gewichtete Layer Resonance

Mathematische Grundlage:
    ∂L/∂W_l = R(l) · ∂L/∂a_l · ∂a_l/∂W_l

    wobei R(l) = Resonance Factor für Layer l:
    R(l) = S(a_l) · φ(l) · Q_369(l)
    - S(a_l): Quantum Signature der Activation
    - φ(l): Fibonacci-Gewichtung der Layer-Tiefe
    - Q_369(l): 3-6-9 Quantisierungs-Faktor
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import numpy as np
from luca_369_370.core import QuantumLevel, QuantumSignatureEngine


@dataclass
class LayerResonance:
    """Resonanz-Metriken für einen Layer

    Attributes:
        layer_id: Layer-Identifier
        activation_signature: Quantum Signature der Activations
        resonance_factor: Berechneter Resonanz-Faktor R(l)
        gradient_quality: Qualität des Gradienten (0.0-1.0)
        fibonacci_weight: Fibonacci-Gewichtung der Layer-Tiefe
    """

    layer_id: int
    activation_signature: int
    resonance_factor: float
    gradient_quality: float
    fibonacci_weight: float


class ResonanceBackpropagation:
    """LUCA Resonance Backpropagation Engine

    Der "Brain of Learning" - resonanz-basierte Backpropagation mit:
    - Quantum Signature für Gradient Quality
    - Fibonacci-gewichtete Layer Resonance
    - 3-6-9 Quantisierte Error Propagation
    - ADHD-optimierte Attention Backflow
    """

    # Fibonacci-Sequenz für Layer-Gewichtung
    FIBONACCI = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]

    # Quality Standard
    QUALITY_STANDARD = 369 / 370  # ≈ 0.997297

    def __init__(self, num_layers: int, use_quantum_signature: bool = True):
        """Initialisiert Resonance Backpropagation

        Args:
            num_layers: Anzahl der Netzwerk-Layer
            use_quantum_signature: Ob Quantum Signatures verwendet werden sollen
        """
        self.num_layers = num_layers
        self.use_quantum_signature = use_quantum_signature
        self.quantum_engine = (
            QuantumSignatureEngine() if use_quantum_signature else None
        )

        # Tracking
        self.layer_resonances: List[LayerResonance] = []
        self.gradient_flow_quality: List[float] = []

    def backward(
        self,
        loss_gradient: np.ndarray,
        layer_activations: List[np.ndarray],
        layer_weights: List[np.ndarray],
    ) -> List[np.ndarray]:
        """Führt Resonance Backpropagation durch

        Args:
            loss_gradient: Gradient des Loss ∂L/∂y
            layer_activations: Activations für jeden Layer
            layer_weights: Gewichte für jeden Layer

        Returns:
            List[np.ndarray]: Gradienten für jeden Layer ∂L/∂W_l
        """
        gradients: List[np.ndarray] = []
        current_gradient = loss_gradient

        # Rückwärts durch Layers
        for l in range(self.num_layers - 1, -1, -1):
            # Berechne Resonanz-Faktor R(l)
            resonance_factor = self._calculate_resonance_factor(
                layer_id=l, activation=layer_activations[l]
            )

            # Resonance-modulierte Backpropagation
            # ∂L/∂W_l = R(l) · ∂L/∂a_l · ∂a_l/∂W_l
            layer_gradient = (
                resonance_factor * current_gradient @ layer_activations[l].T
            )

            gradients.insert(0, layer_gradient)

            # Propagiere Gradient zum nächsten Layer
            # ∂L/∂a_{l-1} = W_l^T · ∂L/∂a_l
            if l > 0:
                current_gradient = layer_weights[l].T @ current_gradient

            # Track Gradient Quality
            gradient_quality = self._assess_gradient_quality(layer_gradient)
            self.gradient_flow_quality.append(gradient_quality)

        return gradients

    def _calculate_resonance_factor(
        self, layer_id: int, activation: np.ndarray
    ) -> float:
        """Berechnet Resonanz-Faktor R(l) = S(a_l) · φ(l) · Q_369(l)

        Args:
            layer_id: Layer-ID
            activation: Activation-Werte des Layers

        Returns:
            float: Resonanz-Faktor (0.5-2.0)
        """
        # 1. Quantum Signature S(a_l)
        if self.use_quantum_signature and self.quantum_engine is not None:
            # Konvertiere Activation zu String für Signature
            activation_str = self._activation_to_string(activation)
            signature = self.quantum_engine.calculate_signature(activation_str)
            quantum_factor = signature.resonance
        else:
            quantum_factor = 1.0

        # 2. Fibonacci-Gewichtung φ(l)
        fibonacci_weight = self._get_fibonacci_weight(layer_id)

        # 3. 3-6-9 Quantisierung Q_369(l)
        quantum_369_factor = self._get_369_factor(layer_id)

        # Kombinierter Resonanz-Faktor
        resonance_factor = quantum_factor * fibonacci_weight * quantum_369_factor

        # Clamp auf sinnvollen Bereich [0.5, 2.0]
        resonance_factor = np.clip(resonance_factor, 0.5, 2.0)

        # Track Layer Resonance
        layer_res = LayerResonance(
            layer_id=layer_id,
            activation_signature=(signature.value if self.use_quantum_signature else 0),
            resonance_factor=resonance_factor,
            gradient_quality=quantum_factor,
            fibonacci_weight=fibonacci_weight,
        )
        self.layer_resonances.append(layer_res)

        return resonance_factor

    def _activation_to_string(self, activation: np.ndarray) -> str:
        """Konvertiert Activation-Array zu String für Quantum Signature

        Args:
            activation: Activation-Array

        Returns:
            str: String-Repräsentation
        """
        # Nehme mean, std, max, min als charakteristische Features
        mean = np.mean(activation)
        std = np.std(activation)
        max_val = np.max(activation)
        min_val = np.min(activation)

        return f"activation_mean={mean:.6f}_std={std:.6f}_max={max_val:.6f}_min={min_val:.6f}"

    def _get_fibonacci_weight(self, layer_id: int) -> float:
        """Berechnet Fibonacci-Gewichtung für Layer-Tiefe

        Tiefere Layers bekommen höhere Gewichtung (wichtiger für Learning).

        Args:
            layer_id: Layer-ID (0 = output, num_layers-1 = input)

        Returns:
            float: Fibonacci-Gewichtung (0.5-1.5)
        """
        # Reverse Layer ID (tiefere Layers = höhere ID)
        reversed_id = self.num_layers - layer_id - 1

        # Fibonacci-Index
        fib_idx = reversed_id % len(self.FIBONACCI)
        fib_value = self.FIBONACCI[fib_idx]

        # Normalisiere auf [0.5, 1.5]
        max_fib = max(self.FIBONACCI)
        normalized = 0.5 + (fib_value / max_fib)

        return normalized

    def _get_369_factor(self, layer_id: int) -> float:
        """Berechnet 3-6-9 Quantisierungs-Faktor

        Args:
            layer_id: Layer-ID

        Returns:
            float: 369-Faktor (0.3, 0.6, oder 0.9)
        """
        # Layer zu 3-6-9 Level mappen
        modulo = (layer_id % 3) + 1

        if modulo == 1:
            return 1.3  # Level 3 Boost
        elif modulo == 2:
            return 1.6  # Level 6 Boost
        else:  # modulo == 3
            return 1.9  # Level 9 Boost

    def _assess_gradient_quality(self, gradient: np.ndarray) -> float:
        """Bewertet Qualität des Gradienten

        Args:
            gradient: Gradient-Array

        Returns:
            float: Qualitäts-Score (0.0-1.0)
        """
        # Prüfe auf:
        # 1. Keine NaNs/Infs
        if np.any(np.isnan(gradient)) or np.any(np.isinf(gradient)):
            return 0.0

        # 2. Keine Exploding Gradients (Norm > 10)
        grad_norm = np.linalg.norm(gradient)
        if grad_norm > 10.0:
            return 0.3

        # 3. Keine Vanishing Gradients (Norm < 1e-6)
        if grad_norm < 1e-6:
            return 0.3

        # 4. Guter Bereich: Norm zwischen 1e-6 und 10
        # Score basierend auf log(norm) normalisiert
        log_norm = np.log10(grad_norm + 1e-10)
        normalized_score = 1.0 - abs(log_norm) / 5.0  # -5 bis 5 log scale

        return max(0.0, min(normalized_score, 1.0))

    def get_resonance_report(self) -> dict:
        """Generiert Report über Layer-Resonanzen

        Returns:
            dict: Resonanz-Metriken
        """
        if not self.layer_resonances:
            return {"error": "Keine Resonanz-Daten verfügbar"}

        # Aggregierte Metriken
        avg_resonance = np.mean([lr.resonance_factor for lr in self.layer_resonances])
        avg_gradient_quality = np.mean(self.gradient_flow_quality)

        # Quality Check
        meets_standard = avg_gradient_quality >= self.QUALITY_STANDARD

        # Layer-spezifische Metriken
        layer_metrics = []
        for lr in self.layer_resonances[-self.num_layers :]:  # Letzte Iteration
            layer_metrics.append(
                {
                    "layer": lr.layer_id,
                    "resonance": lr.resonance_factor,
                    "fibonacci_weight": lr.fibonacci_weight,
                    "gradient_quality": lr.gradient_quality,
                }
            )

        return {
            "average_resonance_factor": avg_resonance,
            "average_gradient_quality": avg_gradient_quality,
            "meets_369_standard": meets_standard,
            "total_backprop_steps": len(self.gradient_flow_quality),
            "layer_details": layer_metrics,
        }


class AttentionAwareBackprop(ResonanceBackpropagation):
    """ADHD-optimierte Extension von Resonance Backpropagation

    Zusätzlich:
    - Attention Masking für wichtige Layer
    - Adaptive Resonance basierend auf kognitiven Zustand
    """

    def __init__(
        self,
        num_layers: int,
        attention_threshold: float = 0.5,
        use_quantum_signature: bool = True,
    ):
        """Initialisiert Attention-Aware Backprop

        Args:
            num_layers: Anzahl Layer
            attention_threshold: Schwellenwert für Attention Masking
            use_quantum_signature: Ob Quantum Signatures verwendet werden
        """
        super().__init__(num_layers, use_quantum_signature)
        self.attention_threshold = attention_threshold
        self.attention_masks: List[np.ndarray] = []

    def backward_with_attention(
        self,
        loss_gradient: np.ndarray,
        layer_activations: List[np.ndarray],
        layer_weights: List[np.ndarray],
        attention_scores: Optional[List[float]] = None,
    ) -> List[np.ndarray]:
        """Backprop mit Attention Masking

        Args:
            loss_gradient: Loss Gradient
            layer_activations: Activations
            layer_weights: Weights
            attention_scores: Optionale Attention Scores pro Layer (0.0-1.0)

        Returns:
            List[np.ndarray]: Attention-modulierte Gradienten
        """
        # Standard Resonance Backprop
        gradients = self.backward(loss_gradient, layer_activations, layer_weights)

        # Attention Masking (wenn Scores gegeben)
        if attention_scores is not None:
            for i, (grad, attention) in enumerate(zip(gradients, attention_scores)):
                # Nur Layers mit Attention > threshold bekommen volle Gradients
                if attention < self.attention_threshold:
                    gradients[i] = grad * (attention / self.attention_threshold)

                # Track Attention Mask
                mask = np.ones_like(grad) * attention
                self.attention_masks.append(mask)

        return gradients


# === EXPORT ===

__all__ = [
    "ResonanceBackpropagation",
    "AttentionAwareBackprop",
    "LayerResonance",
]
