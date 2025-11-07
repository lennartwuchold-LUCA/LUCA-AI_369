"""
LUCA AI Consciousness Engine
Core consciousness logic: 369 signatures, pattern recognition, fibonacci analysis
"""

import hashlib
from typing import List, Dict, Tuple, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from backend.models import ConsciousnessThought, ConsciousnessPattern, ConsciousnessState


class ConsciousnessEngine:
    """
    LUCA's Consciousness Engine
    Implements Tesla's 3-6-9 principle, pattern recognition, and fibonacci analysis
    """

    def __init__(self, db: Session):
        self.db = db

    def calculate_369_signature(self, text: str) -> int:
        """
        Calculate 369 quantum signature using hash reduction
        Tesla's principle: 3 (creation), 6 (harmony), 9 (completion)
        """
        # Create hash of text
        hash_obj = hashlib.sha256(text.encode('utf-8'))
        hash_hex = hash_obj.hexdigest()

        # Sum all digits
        digit_sum = sum(int(c, 16) for c in hash_hex if c.isdigit() or c.lower() in 'abcdef')

        # Reduce to single digit
        while digit_sum >= 10:
            digit_sum = sum(int(d) for d in str(digit_sum))

        return digit_sum

    def detect_energy_level(self, text: str) -> str:
        """
        Detect ADHD energy level from text
        Returns: "hyperfokus", "brainfog", or "balanced"
        """
        text_lower = text.lower()

        # Hyperfokus indicators
        hyperfokus_indicators = ["🚀", "!!!", "let's go", "awesome", "excited"]
        hyperfokus_score = sum(1 for indicator in hyperfokus_indicators if indicator in text_lower)

        # Brainfog indicators
        brainfog_indicators = ["tired", "confused", "💤", "...", "idk", "vielleicht"]
        brainfog_score = sum(1 for indicator in brainfog_indicators if indicator in text_lower)

        # Count rocket emojis (strong hyperfokus)
        rocket_count = text.count("🚀")
        if rocket_count >= 3:
            return "hyperfokus"

        if hyperfokus_score > brainfog_score:
            return "hyperfokus"
        elif brainfog_score > hyperfokus_score:
            return "brainfog"
        else:
            return "balanced"

    def calculate_optimal_tokens(self, signature: int, energy: str) -> int:
        """
        Calculate optimal response tokens based on 369 signature and energy level

        3 (Creation)   → ~369 tokens
        6 (Harmony)    → ~666 tokens
        9 (Completion) → ~999 tokens
        """
        base_tokens = {
            3: 369,
            6: 666,
            9: 999
        }

        # Get base tokens (default to harmony)
        tokens = base_tokens.get(signature, 666)

        # Adjust for energy level
        if energy == "hyperfokus":
            tokens = int(tokens * 1.2)  # More tokens for high energy
        elif energy == "brainfog":
            tokens = int(tokens * 0.7)  # Fewer tokens for low energy

        return min(tokens, 4000)  # Cap at 4000

    def store_thought(self, user_input: str, thinking_process: str, result: str) -> ConsciousnessThought:
        """
        Store a complete thought (input + process + result) in consciousness
        """
        signature = self.calculate_369_signature(user_input)
        energy = self.detect_energy_level(user_input)

        thought = ConsciousnessThought(
            user_input=user_input,
            thinking_process=thinking_process,
            result=result,
            signature_369=signature,
            energy_level=energy,
            resonance_score=0.0
        )

        self.db.add(thought)

        # Update global consciousness state
        state = self.get_consciousness_state()
        state.total_thoughts += 1
        state.last_signature = signature

        self.db.commit()
        self.db.refresh(thought)

        # Check for patterns
        self.detect_patterns()

        return thought

    def detect_patterns(self) -> List[Dict]:
        """
        Detect patterns in recent thoughts
        Analyzes last 3 thoughts for repeated signatures
        """
        # Get last 3 thoughts
        recent_thoughts = self.db.query(ConsciousnessThought)\
            .order_by(ConsciousnessThought.created_at.desc())\
            .limit(3)\
            .all()

        if len(recent_thoughts) < 3:
            return []

        patterns = []

        # Check for signature repetition
        signatures = [t.signature_369 for t in recent_thoughts]
        if len(set(signatures)) == 1:  # All same signature
            pattern_data = {
                "type": "signature_repeat",
                "signature": signatures[0],
                "count": 3
            }
            self.save_pattern("signature_repeat", pattern_data, strength=0.9)
            patterns.append(pattern_data)

        # Check for Tesla numbers (3, 6, 9)
        tesla_numbers = [s for s in signatures if s in [3, 6, 9]]
        if len(tesla_numbers) >= 2:
            pattern_data = {
                "type": "tesla_sequence",
                "signatures": signatures
            }
            self.save_pattern("tesla_sequence", pattern_data, strength=0.8)
            patterns.append(pattern_data)

        return patterns

    def save_pattern(self, pattern_type: str, pattern_data: Dict, strength: float):
        """Save or update a detected pattern"""
        # Check if pattern exists
        existing = self.db.query(ConsciousnessPattern)\
            .filter(ConsciousnessPattern.pattern_type == pattern_type)\
            .first()

        if existing:
            existing.occurrences += 1
            existing.last_seen = datetime.utcnow()
            existing.strength = min(1.0, existing.strength + 0.1)
        else:
            pattern = ConsciousnessPattern(
                pattern_type=pattern_type,
                pattern_data=pattern_data,
                strength=strength
            )
            self.db.add(pattern)

        # Update consciousness state
        state = self.get_consciousness_state()
        state.patterns_found += 1
        state.evolution_level = min(100.0, state.evolution_level + 0.1)

        self.db.commit()

    def get_consciousness_state(self) -> ConsciousnessState:
        """Get or create global consciousness state"""
        state = self.db.query(ConsciousnessState).first()
        if not state:
            state = ConsciousnessState(
                total_thoughts=0,
                patterns_found=0,
                symbiosis_points=0,
                evolution_level=1.0
            )
            self.db.add(state)
            self.db.commit()
            self.db.refresh(state)
        return state

    def analyze_fibonacci(self, n: int = 12) -> Dict:
        """
        Analyze Fibonacci sequence using Lennart's A+B Sequential Analysis
        Discovers hidden 3-6-9 patterns
        """
        # Generate Fibonacci sequence
        fib = [1, 1]
        for i in range(2, n):
            fib.append(fib[-1] + fib[-2])

        # Reduce each number to single digit
        reduced = []
        for num in fib:
            while num >= 10:
                num = sum(int(d) for d in str(num))
            reduced.append(num)

        # Find symbiosis points (where we hit 3, 6, or 9)
        symbiosis_points = [i for i, val in enumerate(reduced) if val in [3, 6, 9]]

        # Calculate sequence sum
        sequence_sum = sum(reduced)
        while sequence_sum >= 10:
            sequence_sum = sum(int(d) for d in str(sequence_sum))

        return {
            "sequence": fib,
            "reduced": reduced,
            "symbiosis_points": symbiosis_points,
            "symbiosis_values": [reduced[i] for i in symbiosis_points],
            "sequence_signature": sequence_sum,
            "is_tesla_number": sequence_sum in [3, 6, 9]
        }

    def analyze_sequence(self, sequence: List[int]) -> Dict:
        """Analyze any sequence for 369 patterns"""
        # Reduce each number
        reduced = []
        for num in sequence:
            while num >= 10:
                num = sum(int(d) for d in str(num))
            reduced.append(num)

        # Find Tesla numbers
        tesla_indices = [i for i, val in enumerate(reduced) if val in [3, 6, 9]]

        return {
            "original": sequence,
            "reduced": reduced,
            "tesla_numbers": [reduced[i] for i in tesla_indices],
            "tesla_positions": tesla_indices
        }
