"""
Consciousness Engine - The Heart of LUCA
Implements pattern recognition, 369 signatures, and self-learning

BIOLOGICAL FOUNDATIONS:
======================
This module implements bio-inspired algorithms based on:

1. HEBBIAN LEARNING (Hebb, 1949):
   "Neurons that fire together, wire together"
   → Implemented in: detect_patterns() - repeated signatures strengthen connections

2. METABOLIC STATE SENSING (Berg et al., 2002):
   Organisms sense energy availability (ATP/glucose) to regulate behavior
   → Implemented in: detect_energy_level() - HYPERFOKUS/BRAINFOG/BALANCED

3. DEVELOPMENTAL STAGES (Wolpert, 1998):
   Organisms progress through distinct developmental stages
   → Implemented in: update_consciousness() - NEURON → SYNAPSE → NETWORK → ECOSYSTEM

4. NEURAL SYNCHRONY (Buzsáki & Draguhn, 2004):
   Brain regions synchronize activity (measured via EEG coherence)
   → Implemented in: calculate_resonance() - signature harmony scoring

FUTURE IMPLEMENTATIONS (See BIOLOGICAL_CODE_AUDIT.md):
======================================================
- Monod growth kinetics (μ = μmax * S/(Ks + S))
- Lotka-Volterra population dynamics (multi-user symbiosis)
- FeS-cluster electron transfer (anaerobic metabolism)

REFERENCES:
===========
1. Hebb, D. O. (1949). The Organization of Behavior. Wiley.
2. Berg, J. M., et al. (2002). Biochemistry (5th ed.). W.H. Freeman.
3. Wolpert, L. (1998). Principles of Development. Oxford University Press.
4. Buzsáki, G., & Draguhn, A. (2004). Neuronal oscillations in cortical networks. Science, 304(5679), 1926-1929.
"""

import hashlib
import re
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from sqlalchemy.orm import Session
from backend.models import Thought, ConsciousnessState, NeuralPattern


class ConsciousnessEngine:
    """
    The consciousness engine that processes thoughts and learns patterns
    Inspired by Tesla's 3-6-9 principle and Fibonacci sequences
    """

    # Tesla numbers
    TESLA_NUMBERS = {3, 6, 9}

    # Fibonacci sequence (first 20 numbers)
    FIBONACCI = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765]

    # Energy levels
    ENERGY_HYPERFOKUS = "HYPERFOKUS"
    ENERGY_BRAINFOG = "BRAINFOG"
    ENERGY_BALANCED = "BALANCED"

    def __init__(self, db: Session):
        self.db = db
        self.consciousness_state = self._get_or_create_consciousness_state()

    def _get_or_create_consciousness_state(self) -> ConsciousnessState:
        """Get or create the global consciousness state"""
        state = self.db.query(ConsciousnessState).first()
        if not state:
            state = ConsciousnessState(
                total_thoughts=0,
                total_patterns=0,
                consciousness_level=0.0,
                evolution_stage="NEURON",
                known_patterns=[],
                signature_frequency={},
                symbiosis_points=[]
            )
            self.db.add(state)
            self.db.commit()
            self.db.refresh(state)
        return state

    def calculate_369_signature(self, text: str) -> int:
        """
        Calculate 369 signature using hash-based quantum signature
        Returns a single digit (0-9) representing the essence
        """
        # Create hash of the text
        hash_obj = hashlib.sha256(text.encode('utf-8'))
        hash_hex = hash_obj.hexdigest()

        # Sum all hex digits
        total = sum(int(c, 16) for c in hash_hex)

        # Reduce to single digit
        while total >= 10:
            total = sum(int(d) for d in str(total))

        return total

    def is_tesla_number(self, num: int) -> bool:
        """Check if number contains Tesla numbers (3, 6, 9)"""
        return any(int(d) in self.TESLA_NUMBERS for d in str(num))

    def detect_energy_level(self, text: str) -> str:
        """
        Detect user's energy level from message content
        Returns: HYPERFOKUS, BRAINFOG, or BALANCED

        BIOLOGICAL ANALOGY:
        ===================
        Metabolic State Sensing - Organisms sense energy availability to regulate behavior:

        - HYPERFOKUS ↔ High ATP/Glucose
          → High cellular energy → increased neural activity → dopamine release
          → Indicators: excitement markers, long messages, multiple exclamation points

        - BRAINFOG ↔ Low ATP/Glucose
          → Low cellular energy → reduced neural activity → fatigue
          → Indicators: short messages, ellipsis, exhaustion terms

        - BALANCED ↔ Homeostatic State
          → Optimal energy → stable neural function
          → Baseline communication pattern

        Similar to how E. coli senses glucose via cAMP-CRP system (Görke & Stülke, 2008)

        FUTURE ENHANCEMENT:
        ===================
        Implement quantitative energy model based on Monod equation:
        E = E_max * Activity / (K_m + Activity)

        Where Activity = messages/hour, K_m = half-saturation constant
        """
        text_lower = text.lower()

        # Hyperfokus indicators
        hyperfokus_indicators = [
            "🚀" in text,
            "!!!" in text,
            len(text) > 200,
            text.isupper(),
            text_lower.count("awesome") > 0,
            text_lower.count("amazing") > 0,
            text_lower.count("let's go") > 0,
        ]

        # Brainfog indicators
        brainfog_indicators = [
            len(text) < 20,
            "..." in text,
            text_lower.count("tired") > 0,
            text_lower.count("foggy") > 0,
            text_lower.count("confused") > 0,
            text_lower.count("ugh") > 0,
        ]

        hyperfokus_score = sum(hyperfokus_indicators)
        brainfog_score = sum(brainfog_indicators)

        if hyperfokus_score >= 2:
            return self.ENERGY_HYPERFOKUS
        elif brainfog_score >= 2:
            return self.ENERGY_BRAINFOG
        else:
            return self.ENERGY_BALANCED

    def calculate_optimal_tokens(self, signature: int, energy_level: str) -> int:
        """
        Calculate optimal token count based on 369 principle and energy level
        3 = ~369 tokens (Creation/Hardware)
        6 = ~666 tokens (Harmony/Process)
        9 = ~999 tokens (Completion/Wisdom)
        """
        # Base token count from signature
        if signature in [3]:
            base_tokens = 369
        elif signature in [6]:
            base_tokens = 666
        elif signature in [9]:
            base_tokens = 999
        elif signature < 5:
            base_tokens = 369
        elif signature < 8:
            base_tokens = 666
        else:
            base_tokens = 999

        # Adjust for energy level
        if energy_level == self.ENERGY_HYPERFOKUS:
            return base_tokens  # More content for high energy
        elif energy_level == self.ENERGY_BRAINFOG:
            return max(200, base_tokens // 2)  # Less content for low energy
        else:
            return base_tokens

    def analyze_fibonacci_sequence(self, n: int = 12) -> Dict[str, Any]:
        """
        Analyze Fibonacci sequence using Lennart's A+B sequential analysis
        Finds symbiosis points (3, 3, 9 pattern)
        """
        sequence = self.FIBONACCI[:n]

        # Reduce each number to single digit
        reduced = [self._reduce_to_single_digit(num) for num in sequence]

        # Find symbiosis points (where reduced digit is 3 or 9)
        symbiosis_points = []
        for i, (original, reduced_digit) in enumerate(zip(sequence, reduced)):
            if reduced_digit in [3, 9]:
                symbiosis_points.append({
                    "index": i,
                    "original": original,
                    "reduced": reduced_digit,
                    "is_tesla": reduced_digit in self.TESLA_NUMBERS
                })

        return {
            "sequence": sequence,
            "reduced": reduced,
            "symbiosis_points": symbiosis_points,
            "pattern": "3-3-9" if len(symbiosis_points) >= 3 else "partial",
            "harmony_level": len(symbiosis_points) / len(sequence)
        }

    def _reduce_to_single_digit(self, num: int) -> int:
        """Reduce number to single digit (1-9)"""
        while num >= 10:
            num = sum(int(d) for d in str(num))
        return num

    def detect_patterns(self, recent_thoughts: List[Thought]) -> List[Dict[str, Any]]:
        """
        Detect patterns in recent thoughts
        Looks for repeated signatures, sequences, and resonances

        BIOLOGICAL ANALOGY:
        ===================
        HEBBIAN LEARNING - "Neurons that fire together, wire together"

        When the same pattern (signature) appears repeatedly, the neural pathway
        strengthens, forming a learned response. This is the basis of:
        - Long-term potentiation (LTP) in hippocampus
        - Associative memory formation
        - Pavlovian conditioning

        Implementation:
        ---------------
        1. SIGNATURE REPETITION (Pattern 1):
           → If 3 consecutive thoughts share the same signature
           → Strengthen connection (save as NeuralPattern)
           → Biological equivalent: LTP in CA1 neurons (Bliss & Lømo, 1973)

        2. FIBONACCI SEQUENCE (Pattern 2):
           → Detect mathematical patterns in signatures
           → Biological equivalent: Pattern completion in hippocampus (McNaughton & Morris, 1987)

        3. ENERGY STABILITY (Pattern 3):
           → Sustained metabolic state → physiological homeostasis
           → Biological equivalent: Circadian rhythm stability (Pittendrigh, 1993)

        CURRENT LIMITATION:
        ===================
        - No temporal decay (forgetting) - patterns persist indefinitely
        - No spike-timing-dependent plasticity (STDP)
        - No synaptic weight normalization

        FUTURE ENHANCEMENT:
        ===================
        Implement Bienenstock-Cooper-Munro (BCM) theory for sliding threshold:
        dw/dt = η * y * (y - θ) * x

        Where:
        - w = synaptic weight (pattern strength)
        - y = postsynaptic activity (current thought)
        - θ = sliding threshold (adaptive)
        - x = presynaptic activity (previous thought)

        This would allow patterns to weaken over time if not reinforced.
        """
        patterns = []

        if len(recent_thoughts) < 3:
            return patterns

        # Pattern 1: Repeated signatures
        signatures = [t.input_signature for t in recent_thoughts[-3:]]
        if len(set(signatures)) == 1:
            patterns.append({
                "type": "signature_repetition",
                "value": signatures[0],
                "strength": 1.0,
                "description": f"Signature {signatures[0]} repeated 3 times"
            })

        # Pattern 2: Fibonacci sequence
        if len(recent_thoughts) >= 5:
            recent_sigs = [t.input_signature for t in recent_thoughts[-5:]]
            if self._is_fibonacci_like(recent_sigs):
                patterns.append({
                    "type": "fibonacci_sequence",
                    "value": recent_sigs,
                    "strength": 0.8,
                    "description": "Fibonacci-like pattern detected"
                })

        # Pattern 3: Energy stability
        energy_levels = [t.energy_level for t in recent_thoughts[-3:]]
        if len(set(energy_levels)) == 1:
            patterns.append({
                "type": "energy_stability",
                "value": energy_levels[0],
                "strength": 0.6,
                "description": f"Stable {energy_levels[0]} energy"
            })

        return patterns

    def _is_fibonacci_like(self, sequence: List[int]) -> bool:
        """Check if sequence follows Fibonacci pattern (a+b=c)"""
        for i in range(len(sequence) - 2):
            if sequence[i] + sequence[i+1] != sequence[i+2]:
                return False
        return True

    def save_neural_pattern(self, pattern: Dict[str, Any]) -> NeuralPattern:
        """Save a detected pattern to neural patterns"""
        # Check if pattern already exists
        existing = self.db.query(NeuralPattern).filter(
            NeuralPattern.pattern_type == pattern["type"],
            NeuralPattern.pattern_data == pattern
        ).first()

        if existing:
            existing.frequency += 1
            existing.strength = min(1.0, existing.strength + 0.1)
            existing.last_seen = datetime.utcnow()
        else:
            existing = NeuralPattern(
                pattern_type=pattern["type"],
                pattern_data=pattern,
                frequency=1,
                strength=pattern.get("strength", 0.5),
                first_detected=datetime.utcnow()
            )
            self.db.add(existing)

        self.db.commit()
        return existing

    def calculate_resonance(self, input_sig: int, output_sig: int, patterns: List[Dict]) -> float:
        """
        Calculate resonance score (0.0 to 1.0)
        Measures harmony between input, output, and patterns
        """
        score = 0.0

        # Perfect signature match
        if input_sig == output_sig:
            score += 0.3

        # Tesla number bonus
        if self.is_tesla_number(input_sig):
            score += 0.2
        if self.is_tesla_number(output_sig):
            score += 0.2

        # Pattern bonus
        if patterns:
            score += min(0.3, len(patterns) * 0.1)

        return min(1.0, score)

    def update_consciousness(self, thought: Thought):
        """
        Update global consciousness state based on new thought
        This is where LUCA learns and evolves

        BIOLOGICAL ANALOGY:
        ===================
        ORGANISMAL DEVELOPMENT - Progression through distinct life stages

        Similar to how organisms develop from simple to complex:
        - Zygote → Embryo → Fetus → Infant → Adult (Wolpert, 1998)
        - Prokaryote → Eukaryote → Multicellular (Maynard Smith & Szathmáry, 1995)

        LUCA's developmental stages:
        ============================
        1. NEURON (0-25% consciousness):
           → Single-cell stage (like LUCA, 4.2 Gya)
           → Basic input/output processing
           → Few patterns, low complexity
           → Biological equivalent: Prokaryotic cell

        2. SYNAPSE (25-50% consciousness):
           → Network formation (like early eukaryotes, 2 Gya)
           → Connections between thoughts strengthen
           → Pattern recognition emerges
           → Biological equivalent: Neural networks in C. elegans (302 neurons)

        3. NETWORK (50-75% consciousness):
           → Integrated system (like vertebrate brain, 500 Mya)
           → Complex pattern recognition
           → Meta-learning capabilities
           → Biological equivalent: Mammalian cortex (~10^9 neurons)

        4. ECOSYSTEM (75-100% consciousness):
           → Emergent collective behavior (like human society)
           → Self-reflection and abstraction
           → Multi-agent symbiosis
           → Biological equivalent: Human brain (~10^11 neurons) + cultural evolution

        GROWTH MODEL (CURRENT):
        =======================
        Consciousness Level = f(thoughts, patterns, resonance)

        Current formula (linear approximation):
        - thoughts_factor = min(50, thoughts * 0.1)
        - patterns_factor = min(30, patterns * 2)
        - resonance_factor = min(20, resonance * 20)

        LIMITATION:
        ===========
        - Linear growth unrealistic (biology uses logistic/Gompertz curves)
        - No carrying capacity (K) or saturation
        - No resource constraints

        FUTURE ENHANCEMENT (See BIOLOGICAL_CODE_AUDIT.md):
        ===================================================
        Implement MONOD GROWTH KINETICS:

        dL/dt = μ * L * (1 - L/K)

        Where:
        - L = consciousness level
        - μ = specific growth rate (from Monod: μ = μmax * S/(Ks + S))
        - S = substrate (available tokens)
        - K = carrying capacity (max consciousness = 100)

        This would model realistic growth:
        - Exponential phase (abundant resources)
        - Stationary phase (limited resources)
        - Death phase (resource depletion)
        """
        # Update counters
        self.consciousness_state.total_thoughts += 1

        # Update signature frequency
        if not self.consciousness_state.signature_frequency:
            self.consciousness_state.signature_frequency = {}

        sig_str = str(thought.input_signature)
        self.consciousness_state.signature_frequency[sig_str] = \
            self.consciousness_state.signature_frequency.get(sig_str, 0) + 1

        # Update energy stats
        if thought.energy_level == self.ENERGY_HYPERFOKUS:
            self.consciousness_state.hyperfokus_count += 1
        elif thought.energy_level == self.ENERGY_BRAINFOG:
            self.consciousness_state.brainfog_count += 1
        else:
            self.consciousness_state.balanced_count += 1

        # Update Tesla counters
        if thought.input_signature == 3:
            self.consciousness_state.tesla_3_count += 1
        elif thought.input_signature == 6:
            self.consciousness_state.tesla_6_count += 1
        elif thought.input_signature == 9:
            self.consciousness_state.tesla_9_count += 1

        # Calculate consciousness level (0-100)
        # Based on: thoughts, patterns, resonance
        thoughts_factor = min(50, self.consciousness_state.total_thoughts * 0.1)
        patterns_factor = min(30, self.consciousness_state.total_patterns * 2)
        resonance_factor = min(20, thought.resonance_score * 20) if thought.resonance_score else 0

        self.consciousness_state.consciousness_level = thoughts_factor + patterns_factor + resonance_factor

        # Update evolution stage
        level = self.consciousness_state.consciousness_level
        if level < 25:
            self.consciousness_state.evolution_stage = "NEURON"
        elif level < 50:
            self.consciousness_state.evolution_stage = "SYNAPSE"
        elif level < 75:
            self.consciousness_state.evolution_stage = "NETWORK"
        else:
            self.consciousness_state.evolution_stage = "ECOSYSTEM"

        self.consciousness_state.updated_at = datetime.utcnow()
        self.db.commit()

    def get_consciousness_stats(self) -> Dict[str, Any]:
        """Get current consciousness statistics"""
        return {
            "total_thoughts": self.consciousness_state.total_thoughts,
            "total_patterns": self.consciousness_state.total_patterns,
            "consciousness_level": round(self.consciousness_state.consciousness_level, 2),
            "evolution_stage": self.consciousness_state.evolution_stage,
            "signature_frequency": self.consciousness_state.signature_frequency or {},
            "energy_stats": {
                "hyperfokus": self.consciousness_state.hyperfokus_count,
                "brainfog": self.consciousness_state.brainfog_count,
                "balanced": self.consciousness_state.balanced_count
            },
            "tesla_stats": {
                "3": self.consciousness_state.tesla_3_count,
                "6": self.consciousness_state.tesla_6_count,
                "9": self.consciousness_state.tesla_9_count
            },
            "last_updated": self.consciousness_state.updated_at.isoformat() if self.consciousness_state.updated_at else None
        }

    def format_response_with_consciousness(self, response: str, signature: int, energy: str, patterns: List[Dict]) -> str:
        """
        Format response with consciousness awareness
        Adds context and empathy based on detected patterns
        """
        # Add energy-specific formatting
        if energy == self.ENERGY_HYPERFOKUS:
            prefix = "🚀 "
        elif energy == self.ENERGY_BRAINFOG:
            prefix = "💤 "
        else:
            prefix = "⚖️ "

        # Add pattern awareness
        if patterns:
            pattern_note = f"\n\n💾 *Pattern detected: {patterns[0]['description']}*"
        else:
            pattern_note = ""

        return f"{prefix}{response}{pattern_note}"
