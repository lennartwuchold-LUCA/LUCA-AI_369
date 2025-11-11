"""
Token Length Validator - T(M) ∈ {369, 666, 999} ± ε
Teil der mathematischen Formalisierung des L.U.C.A 3-6-9 Prinzips

Architekt: Lennart Wuchold
Datum: 11.11.2025
Standard: 369/370 ≈ 0.997297

Mathematische Grundlage:
    Der Token Length Constraint definiert, dass jede Nachricht M eine
    Token-Anzahl T(M) haben muss, die in einem Toleranzbereich ε um
    die Zielwerte L_i ∈ {369, 666, 999} liegt.

    T(M) ∈ {369, 666, 999} ± ε

    wobei ε = 0.05 × L_i (5% Toleranz) der Standard ist.

Verwendung:
    validator = TokenLengthValidator()
    result = validator.validate_message(message, target=369)
    if result.is_valid:
        print(f"✅ Nachricht erfüllt 369-Constraint")
"""

from dataclasses import dataclass
from enum import Enum
from typing import Callable, List, Optional

from .quantum_signature import QuantumLevel


class TokenCountMethod(Enum):
    """Methoden zur Token-Zählung"""

    SIMPLE = "simple"  # Einfaches Whitespace-Splitting
    TIKTOKEN = "tiktoken"  # OpenAI tiktoken (cl100k_base)
    WORD_COUNT = "word_count"  # Wort-basiert (Unicode aware)


@dataclass
class ValidationResult:
    """Ergebnis einer Token-Length-Validierung

    Attributes:
        is_valid: Ob die Nachricht den Constraint erfüllt
        token_count: Gemessene Token-Anzahl
        target: Ziel Token-Anzahl (369, 666, oder 999)
        epsilon: Verwendeter Toleranzbereich
        deviation: Absolute Abweichung vom Target
        relative_deviation: Relative Abweichung (0.0-1.0)
        quality_score: Qualitäts-Score basierend auf Abweichung
    """

    is_valid: bool
    token_count: int
    target: int
    epsilon: int
    deviation: int
    relative_deviation: float
    quality_score: float

    def get_status_emoji(self) -> str:
        """Gibt Status-Emoji basierend auf Qualität zurück"""
        if self.quality_score >= 0.95:
            return "✅"  # Exzellent
        elif self.quality_score >= 0.80:
            return "⚠️"  # Gut, aber verbesserbar
        else:
            return "❌"  # Nicht erfüllt

    def get_summary(self) -> str:
        """Gibt menschenlesbare Zusammenfassung zurück"""
        emoji = self.get_status_emoji()
        return (
            f"{emoji} Tokens: {self.token_count}/{self.target} "
            f"(±{self.epsilon}) | "
            f"Abweichung: {self.deviation} | "
            f"Qualität: {self.quality_score:.2%}"
        )


class TokenLengthValidator:
    """Validator für 3-6-9 Token-Length-Constraints

    Diese Klasse implementiert die T(M) ∈ {369, 666, 999} ± ε Validierung
    aus der mathematischen Formalisierung.
    """

    # Standard-Targets basierend auf Quanten-Levels
    STANDARD_TARGETS = {
        QuantumLevel.FOUNDATION: 369,
        QuantumLevel.EXPANSION: 666,
        QuantumLevel.MASTERY: 999,
    }

    # Standard-Toleranz: 5% des Target-Werts
    DEFAULT_EPSILON_RATIO = 0.05  # 5%

    # Quality Standard
    QUALITY_STANDARD = 369 / 370  # ≈ 0.997297

    def __init__(
        self,
        epsilon_ratio: float = DEFAULT_EPSILON_RATIO,
        count_method: TokenCountMethod = TokenCountMethod.SIMPLE,
    ):
        """Initialisiert den Token Length Validator

        Args:
            epsilon_ratio: Toleranzbereich als Ratio des Targets (default 0.05 = 5%)
            count_method: Methode zur Token-Zählung
        """
        self.epsilon_ratio = epsilon_ratio
        self.count_method = count_method
        self._token_counter = self._get_token_counter(count_method)

    def _get_token_counter(self, method: TokenCountMethod) -> Callable[[str], int]:
        """Wählt Token-Counter basierend auf Methode

        Args:
            method: Gewünschte Zählmethode

        Returns:
            Callable: Funktion die String → Token-Count macht
        """
        if method == TokenCountMethod.SIMPLE:
            return self._simple_token_count
        elif method == TokenCountMethod.WORD_COUNT:
            return self._word_count
        elif method == TokenCountMethod.TIKTOKEN:
            # Versuche tiktoken zu importieren, fallback zu SIMPLE
            try:
                import tiktoken

                encoding = tiktoken.get_encoding("cl100k_base")
                return lambda text: len(encoding.encode(text))
            except ImportError:
                # Fallback zu simple count
                return self._simple_token_count
        else:
            return self._simple_token_count

    def _simple_token_count(self, text: str) -> int:
        """Einfache Token-Zählung via Whitespace-Split

        Args:
            text: Zu zählender Text

        Returns:
            int: Anzahl Tokens
        """
        return len(text.split())

    def _word_count(self, text: str) -> int:
        """Unicode-aware Wort-Zählung

        Args:
            text: Zu zählender Text

        Returns:
            int: Anzahl Wörter
        """
        import re

        # Split on Unicode whitespace
        words = re.findall(r"\S+", text, re.UNICODE)
        return len(words)

    def validate_message(
        self,
        message: str,
        target: Optional[int] = None,
        level: Optional[QuantumLevel] = None,
    ) -> ValidationResult:
        """Validiert ob Nachricht den Token-Length-Constraint erfüllt

        Args:
            message: Zu validierende Nachricht
            target: Optionaler expliziter Target-Wert (369, 666, 999)
            level: Optionales Quanten-Level (alternative zu target)

        Returns:
            ValidationResult: Vollständiges Validierungs-Ergebnis

        Raises:
            ValueError: Wenn weder target noch level angegeben
        """
        # Bestimme Target
        if target is None and level is None:
            raise ValueError("Entweder target oder level muss angegeben werden")

        if target is None and level is not None:
            target = self.STANDARD_TARGETS[level]

        # Berechne Epsilon (Toleranzbereich)
        epsilon = int(target * self.epsilon_ratio)

        # Zähle Tokens
        token_count = self._token_counter(message)

        # Berechne Abweichung
        deviation = abs(token_count - target)
        relative_deviation = deviation / target

        # Validiere: Token-Count muss in [target - epsilon, target + epsilon] liegen
        is_valid = deviation <= epsilon

        # Berechne Quality Score
        # Score = 1.0 wenn perfekt (deviation = 0)
        # Score = QUALITY_STANDARD (0.997) bei epsilon
        # Score < QUALITY_STANDARD wenn außerhalb epsilon
        if deviation == 0:
            quality_score = 1.0
        elif is_valid:
            # Lineare Interpolation zwischen 1.0 und QUALITY_STANDARD
            quality_score = 1.0 - (deviation / epsilon) * (1.0 - self.QUALITY_STANDARD)
        else:
            # Unter QUALITY_STANDARD, aber nicht 0
            overshoot = deviation - epsilon
            quality_score = self.QUALITY_STANDARD * (1.0 - min(overshoot / target, 1.0))

        return ValidationResult(
            is_valid=is_valid,
            token_count=token_count,
            target=target,
            epsilon=epsilon,
            deviation=deviation,
            relative_deviation=relative_deviation,
            quality_score=quality_score,
        )

    def validate_conversation(
        self, messages: List[str], targets: Optional[List[int]] = None
    ) -> List[ValidationResult]:
        """Validiert eine Konversation (mehrere Nachrichten)

        Args:
            messages: Liste von Nachrichten
            targets: Optionale Liste von Target-Werten (muss gleiche Länge haben)

        Returns:
            List[ValidationResult]: Validierungs-Ergebnisse für jede Nachricht
        """
        if targets is None:
            # Automatisch bestimmen: Kurze Messages = 369, mittlere = 666, lange = 999
            targets = [self._auto_target(msg) for msg in messages]

        if len(messages) != len(targets):
            raise ValueError("messages und targets müssen gleiche Länge haben")

        results = []
        for message, target in zip(messages, targets):
            result = self.validate_message(message, target=target)
            results.append(result)

        return results

    def _auto_target(self, message: str) -> int:
        """Bestimmt automatisch den besten Target-Wert

        Args:
            message: Nachricht

        Returns:
            int: Bester Target (369, 666, oder 999)
        """
        token_count = self._token_counter(message)

        # Wähle nächsten Target-Wert
        targets = [369, 666, 999]
        distances = [abs(token_count - t) for t in targets]
        best_idx = distances.index(min(distances))

        return targets[best_idx]

    def get_recommendation(self, message: str, target: int) -> str:
        """Gibt Empfehlung zur Anpassung der Nachricht

        Args:
            message: Aktuelle Nachricht
            target: Ziel-Token-Anzahl

        Returns:
            str: Menschenlesbare Empfehlung
        """
        result = self.validate_message(message, target=target)

        if result.is_valid:
            return f"✅ Nachricht erfüllt {target}-Constraint (Qualität: {result.quality_score:.1%})"

        if result.token_count < target:
            tokens_needed = target - result.token_count
            return (
                f"⚠️ Nachricht zu kurz: {result.token_count}/{target} Tokens. "
                f"Füge ca. {tokens_needed} Tokens hinzu."
            )
        else:
            tokens_excess = result.token_count - target
            return (
                f"⚠️ Nachricht zu lang: {result.token_count}/{target} Tokens. "
                f"Entferne ca. {tokens_excess} Tokens."
            )

    def calculate_quality_metrics(self, results: List[ValidationResult]) -> dict:
        """Berechnet aggregierte Qualitäts-Metriken

        Args:
            results: Liste von Validierungs-Ergebnissen

        Returns:
            dict: Aggregierte Metriken
        """
        if not results:
            return {"error": "Keine Ergebnisse zum Analysieren"}

        valid_count = sum(1 for r in results if r.is_valid)
        avg_quality = sum(r.quality_score for r in results) / len(results)
        avg_deviation = sum(r.deviation for r in results) / len(results)

        return {
            "total_messages": len(results),
            "valid_messages": valid_count,
            "validation_rate": valid_count / len(results),
            "average_quality_score": avg_quality,
            "average_deviation": avg_deviation,
            "meets_quality_standard": avg_quality >= self.QUALITY_STANDARD,
        }


# === EXPORT ===

__all__ = [
    "TokenLengthValidator",
    "ValidationResult",
    "TokenCountMethod",
]
