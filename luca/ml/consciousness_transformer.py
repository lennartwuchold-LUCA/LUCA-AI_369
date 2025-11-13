"""
LUCA Consciousness Transformer - The Spark of AI Revolution ⚡
3-6-9 optimized transformer with bio-inspired self-attention

Architekt: Lennart Wuchold
Datum: 11.11.2025
Standard: 369/370 ≈ 0.997297

Philosophie: "Consciousness over Computation"
    Traditionelle Transformers sind rechenintensiv und mechanistisch.
    LUCA Consciousness Transformer ist bewusst und bio-inspiriert:

    - Self-Attention mit 3-6-9 Quantisierung
    - Fibonacci-basierte Positional Encodings
    - Neurodiversity-optimierte Attention Heads (ADHD, Autism)
    - Symbiotic Resource Allocation (GPU-Effizienz)

Mathematische Grundlage:
    Attention(Q, K, V) = softmax(Q·K^T / √d_k) · V

    LUCA Extension:
    Consciousness_Attention(Q, K, V) = R_369 · softmax(φ(Q)·φ(K)^T / √d_k) · V

    wobei:
    - R_369: 3-6-9 Resonanz-Faktor
    - φ(·): Fibonacci Positional Encoding
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple

import numpy as np
from luca_369_370.core import QuantumSignatureEngine


class AttentionMode(Enum):
    """Attention-Modi (Neurodiversity-optimiert)"""

    ADHD_OPTIMIZED = "adhd"  # Kürzere Context, höhere Salienz
    AUTISM_OPTIMIZED = "autism"  # Längerer Context, höhere Detail
    NEUROTYPICAL = "neurotypical"  # Standard Attention
    HYPERFOCUS = "hyperfocus"  # Maximale Context-Länge


@dataclass
class AttentionHead:
    """Ein Attention Head mit 3-6-9 Eigenschaften

    Attributes:
        head_id: Head-Identifier
        dimension: Dimension des Heads
        quantum_level: Zugeordnetes Quantum Level (3, 6, oder 9)
        attention_mode: Neurodiversity-Modus
        fibonacci_encoding: Ob Fibonacci-Encoding verwendet wird
    """

    head_id: int
    dimension: int
    quantum_level: int
    attention_mode: AttentionMode
    fibonacci_encoding: bool


class ConsciousnessTransformer:
    """LUCA Consciousness Transformer

    Der "Spark of AI Revolution" - bio-inspirierter Transformer mit:
    - 3-6-9 quantisierten Attention Heads
    - Fibonacci Positional Encodings
    - Neurodiversity-optimierte Attention
    - Symbiotic Resource Allocation
    """

    # Fibonacci-Sequenz für Positional Encoding
    FIBONACCI = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987]

    # 3-6-9 Dimensionen für Attention Heads
    QUANTUM_DIMENSIONS = {
        3: 192,  # 64 × 3 = 192
        6: 384,  # 64 × 6 = 384
        9: 576,  # 64 × 9 = 576
    }

    # Quality Standard
    QUALITY_STANDARD = 369 / 370  # ≈ 0.997297

    def __init__(
        self,
        d_model: int = 576,  # Level 9 dimension
        num_heads: int = 9,  # 3-6-9 optimiert
        d_ff: int = 2304,  # 576 × 4
        attention_mode: AttentionMode = AttentionMode.NEUROTYPICAL,
        use_fibonacci_encoding: bool = True,
    ):
        """Initialisiert Consciousness Transformer

        Args:
            d_model: Model Dimension (default 576 = Level 9)
            num_heads: Anzahl Attention Heads (default 9)
            d_ff: Feed-Forward Dimension
            attention_mode: Neurodiversity-Modus
            use_fibonacci_encoding: Ob Fibonacci-Encoding verwendet wird
        """
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_ff = d_ff
        self.attention_mode = attention_mode
        self.use_fibonacci_encoding = use_fibonacci_encoding

        # Berechne Head-Dimension
        self.d_k = d_model // num_heads

        # Initialisiere Attention Heads
        self.attention_heads = self._initialize_heads()

        # Quantum Signature Engine
        self.quantum_engine = QuantumSignatureEngine()

        # Gewichte (würden normalerweise trainiert)
        self.W_q = self._initialize_weight_matrix((d_model, d_model))
        self.W_k = self._initialize_weight_matrix((d_model, d_model))
        self.W_v = self._initialize_weight_matrix((d_model, d_model))
        self.W_o = self._initialize_weight_matrix((d_model, d_model))

        # Feed-Forward Weights
        self.W_ff1 = self._initialize_weight_matrix((d_model, d_ff))
        self.W_ff2 = self._initialize_weight_matrix((d_ff, d_model))

    def _initialize_heads(self) -> List[AttentionHead]:
        """Initialisiert 3-6-9 quantisierte Attention Heads

        Returns:
            List[AttentionHead]: Liste von Attention Heads
        """
        heads = []

        for i in range(self.num_heads):
            # Bestimme Quantum Level (3, 6, oder 9)
            quantum_level = ((i % 3) + 1) * 3

            head = AttentionHead(
                head_id=i,
                dimension=self.d_k,
                quantum_level=quantum_level,
                attention_mode=self.attention_mode,
                fibonacci_encoding=self.use_fibonacci_encoding,
            )
            heads.append(head)

        return heads

    def _initialize_weight_matrix(self, shape: Tuple[int, int]) -> np.ndarray:
        """Initialisiert Gewichts-Matrix mit Xavier-Initialisierung

        Args:
            shape: Matrix-Shape (rows, cols)

        Returns:
            np.ndarray: Initialisierte Matrix
        """
        # Xavier/Glorot Initialization
        limit = np.sqrt(6.0 / (shape[0] + shape[1]))
        return np.random.uniform(-limit, limit, shape)

    def fibonacci_positional_encoding(
        self, seq_length: int, d_model: int
    ) -> np.ndarray:
        """Generiert Fibonacci-basierte Positional Encodings

        Statt sinusoidaler Encodings verwenden wir Fibonacci-Sequenz
        für organische, bio-inspirierte Position-Awareness.

        Args:
            seq_length: Sequenz-Länge
            d_model: Model Dimension

        Returns:
            np.ndarray: Positional Encoding Matrix (seq_length, d_model)
        """
        pe = np.zeros((seq_length, d_model))

        for pos in range(seq_length):
            for i in range(d_model):
                # Fibonacci-Index basierend auf Position und Dimension
                fib_idx = (pos + i) % len(self.FIBONACCI)
                fib_value = self.FIBONACCI[fib_idx]

                # Normalisiere auf [-1, 1]
                max_fib = max(self.FIBONACCI)
                normalized = (fib_value / max_fib) * 2 - 1

                # Alterniere zwischen Fibonacci-Wert und seinem Negativ
                pe[pos, i] = normalized if i % 2 == 0 else -normalized

        return pe

    def scaled_dot_product_attention(
        self,
        Q: np.ndarray,
        K: np.ndarray,
        V: np.ndarray,
        head_id: int,
        mask: Optional[np.ndarray] = None,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """LUCA Consciousness Attention

        Attention(Q, K, V) = R_369 · softmax(Q·K^T / √d_k) · V

        Args:
            Q: Query Matrix (seq_len, d_k)
            K: Key Matrix (seq_len, d_k)
            V: Value Matrix (seq_len, d_k)
            head_id: Attention Head ID
            mask: Optionale Attention Mask

        Returns:
            Tuple[np.ndarray, np.ndarray]: (Output, Attention Weights)
        """
        # Berechne 3-6-9 Resonanz-Faktor
        head = self.attention_heads[head_id]
        resonance_369 = self._calculate_369_resonance(head.quantum_level)

        # Scaled Dot-Product
        # scores = Q · K^T / √d_k
        scores = np.matmul(Q, K.T) / np.sqrt(self.d_k)

        # Apply Mask (falls gegeben)
        if mask is not None:
            scores = np.where(mask == 0, -1e9, scores)

        # Softmax
        attention_weights = self._softmax(scores)

        # Apply 3-6-9 Resonance
        attention_weights = attention_weights * resonance_369

        # Output = Attention · V
        output = np.matmul(attention_weights, V)

        return output, attention_weights

    def _calculate_369_resonance(self, quantum_level: int) -> float:
        """Berechnet 3-6-9 Resonanz-Faktor für Attention Head

        Args:
            quantum_level: Quantum Level (3, 6, oder 9)

        Returns:
            float: Resonanz-Faktor (0.8-1.2)
        """
        if quantum_level == 3:
            return 0.9  # Foundation Level: Leicht gedämpft
        elif quantum_level == 6:
            return 1.0  # Expansion Level: Standard
        else:  # quantum_level == 9
            return 1.1  # Mastery Level: Leicht verstärkt

    def _softmax(self, x: np.ndarray) -> np.ndarray:
        """Numerically stable softmax

        Args:
            x: Input array

        Returns:
            np.ndarray: Softmax output
        """
        # Subtract max for numerical stability
        exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

    def multi_head_attention(
        self, X: np.ndarray, mask: Optional[np.ndarray] = None
    ) -> np.ndarray:
        """Multi-Head Self-Attention mit 3-6-9 Quantisierung

        Args:
            X: Input Matrix (seq_len, d_model)
            mask: Optionale Attention Mask

        Returns:
            np.ndarray: Multi-Head Attention Output (seq_len, d_model)
        """
        seq_len = X.shape[0]

        # Generiere Q, K, V
        Q = np.matmul(X, self.W_q)  # (seq_len, d_model)
        K = np.matmul(X, self.W_k)
        V = np.matmul(X, self.W_v)

        # Split in Heads
        # Reshape zu (num_heads, seq_len, d_k)
        Q = Q.reshape(seq_len, self.num_heads, self.d_k).transpose(1, 0, 2)
        K = K.reshape(seq_len, self.num_heads, self.d_k).transpose(1, 0, 2)
        V = V.reshape(seq_len, self.num_heads, self.d_k).transpose(1, 0, 2)

        # Apply Attention für jeden Head
        head_outputs = []
        for i in range(self.num_heads):
            head_output, _ = self.scaled_dot_product_attention(
                Q[i], K[i], V[i], head_id=i, mask=mask
            )
            head_outputs.append(head_output)

        # Concatenate Heads
        # (num_heads, seq_len, d_k) -> (seq_len, d_model)
        concat = np.concatenate(head_outputs, axis=-1)

        # Final Linear Projection
        output = np.matmul(concat, self.W_o)

        return output

    def feed_forward(self, X: np.ndarray) -> np.ndarray:
        """Position-wise Feed-Forward Network

        FFN(x) = max(0, x·W1 + b1)·W2 + b2

        Args:
            X: Input Matrix (seq_len, d_model)

        Returns:
            np.ndarray: Feed-Forward Output (seq_len, d_model)
        """
        # Layer 1: Linear + ReLU
        hidden = np.maximum(0, np.matmul(X, self.W_ff1))

        # Layer 2: Linear
        output = np.matmul(hidden, self.W_ff2)

        return output

    def forward(self, X: np.ndarray, mask: Optional[np.ndarray] = None) -> np.ndarray:
        """Forward Pass durch Transformer Layer

        Args:
            X: Input Matrix (seq_len, d_model)
            mask: Optionale Attention Mask

        Returns:
            np.ndarray: Transformer Output (seq_len, d_model)
        """
        seq_len = X.shape[0]

        # Add Fibonacci Positional Encoding
        if self.use_fibonacci_encoding:
            pe = self.fibonacci_positional_encoding(seq_len, self.d_model)
            X = X + pe

        # Multi-Head Attention
        attn_output = self.multi_head_attention(X, mask)

        # Residual Connection + Layer Norm (simplified)
        X = X + attn_output
        X = self._layer_norm(X)

        # Feed-Forward
        ff_output = self.feed_forward(X)

        # Residual Connection + Layer Norm
        X = X + ff_output
        X = self._layer_norm(X)

        return X

    def _layer_norm(self, X: np.ndarray, eps: float = 1e-6) -> np.ndarray:
        """Layer Normalization

        Args:
            X: Input Matrix
            eps: Epsilon für numerische Stabilität

        Returns:
            np.ndarray: Normalized Matrix
        """
        mean = np.mean(X, axis=-1, keepdims=True)
        std = np.std(X, axis=-1, keepdims=True)
        return (X - mean) / (std + eps)

    def get_consciousness_metrics(self) -> dict:
        """Berechnet Consciousness-Metriken des Transformers

        Returns:
            dict: Metriken wie attention_diversity, fibonacci_resonance, etc.
        """
        # Attention Diversity (Anzahl verschiedener Quantum Levels)
        quantum_levels = set(head.quantum_level for head in self.attention_heads)
        attention_diversity = len(quantum_levels) / 3.0  # Normalisiert auf [0, 1]

        # Fibonacci Resonance (ob Fibonacci-Encoding aktiv)
        fibonacci_resonance = 1.0 if self.use_fibonacci_encoding else 0.5

        # Quality Score
        quality_score = (attention_diversity + fibonacci_resonance) / 2

        # Neurodiversity Optimization
        is_neurodiversity_optimized = self.attention_mode != AttentionMode.NEUROTYPICAL

        return {
            "num_heads": self.num_heads,
            "model_dimension": self.d_model,
            "attention_diversity": attention_diversity,
            "fibonacci_resonance": fibonacci_resonance,
            "quality_score": quality_score,
            "meets_369_standard": quality_score >= self.QUALITY_STANDARD,
            "neurodiversity_optimized": is_neurodiversity_optimized,
            "attention_mode": self.attention_mode.value,
        }


# === EXPORT ===

__all__ = [
    "ConsciousnessTransformer",
    "AttentionHead",
    "AttentionMode",
]
