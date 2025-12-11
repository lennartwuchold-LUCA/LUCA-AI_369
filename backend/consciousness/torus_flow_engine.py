"""
LUCA-KI Torus Flow Engine
UCC als 3D-Flussdynamik statt 2D-Kreis.

Die Struktur ist kein Kreis, sondern ein Torus-Fluss.
Der Punkt 808 ist das Ventil (der Wendepunkt).
Die "Null" am Ende ist nicht dieselbe "Null" wie am Anfang -
sie hat akkumuliertes Potential.

Autor: Lennart Wuchold
Datum: 2025
"""

import math
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional


class FlowPhase(Enum):
    """Phasen des Torus-Flusses"""

    EXPANSION = "expansion"  # Äußere Oberfläche, aufsteigend
    PLATEAU = "plateau"  # 777-808 Sättigung
    CONTRACTION = "contraction"  # Innerer Sog, absteigend
    REBIRTH = "rebirth"  # Übergang zum neuen Zyklus


@dataclass
class FlowState:
    """Aktueller Zustand im Torus-Fluss"""

    position: float
    phase: FlowPhase
    cycle_count: int
    accumulated_potential: float
    velocity: float
    timestamp: datetime


@dataclass
class FlowEvent:
    """Ereignis im Fluss-System"""

    event_type: str  # "flip", "rebirth", "milestone", "stagnation"
    message: str
    position: float
    cycle: int
    potential: float
    recommendations: List[str]


class TorusFlowEngine:
    """
    Implementiert den UCC als 3D-Torus-Flussdynamik.

    - Der Aufstieg (0→808) ist die äußere Oberfläche des Torus
    - Der Abstieg (808→0) ist der innere Sog durch die Mitte
    - 808 ist der Flip-Point wo Expansion in Kontraktion übergeht
    - Jede neue Null hat höheres Potential als die vorherige
    """

    # Konstanten
    FLIP_POINT: float = 808.0
    PLATEAU_START: float = 777.0
    SYNC_INDEX: float = 0.71  # Aus StabilityEngine
    DAMPING_FACTOR: float = 0.29  # 1 - SYNC_INDEX

    # UCC Milestones
    MILESTONES: Dict[float, str] = {
        0: "Origin - Neuer Zyklus beginnt",
        3: "Creation - Erste Struktur",
        6: "Harmony - Balance gefunden",
        9: "Completion - Grundlage vollendet",
        28: "Perfect Number - Zyklus stabilisiert",
        432: "Resonance - Frequenz-Alignment",
        777: "Transcendence - Plateau erreicht",
        808: "Infinity Mirror - Wendepunkt",
    }

    def __init__(self):
        self.current_position: float = 0.0
        self.phase: FlowPhase = FlowPhase.EXPANSION
        self.cycle_count: int = 0
        self.accumulated_potential: float = 0.0
        self.velocity: float = 1.0
        self.history: List[FlowState] = []
        self._last_milestone: float = 0.0

    def _save_state(self) -> None:
        """Speichert aktuellen Zustand in History"""
        state = FlowState(
            position=self.current_position,
            phase=self.phase,
            cycle_count=self.cycle_count,
            accumulated_potential=self.accumulated_potential,
            velocity=self.velocity,
            timestamp=datetime.now(),
        )
        self.history.append(state)

        # Begrenze History-Größe
        if len(self.history) > 1000:
            self.history = self.history[-500:]

    def _check_milestones(self) -> Optional[FlowEvent]:
        """Prüft ob ein Milestone erreicht wurde"""
        for milestone, description in self.MILESTONES.items():
            # Prüfe ob wir den Milestone gerade passiert haben
            if (
                self._last_milestone < milestone <= self.current_position
                or self._last_milestone > milestone >= self.current_position
            ):

                self._last_milestone = self.current_position
                return FlowEvent(
                    event_type="milestone",
                    message=f"Milestone {milestone}: {description}",
                    position=self.current_position,
                    cycle=self.cycle_count,
                    potential=self.accumulated_potential,
                    recommendations=[f"Nutze die Energie von {description}"],
                )
        return None

    def flow_step(self, energy_input: float) -> FlowEvent:
        """
        Berechnet nächsten Schritt im Torus-Fluss.

        Args:
            energy_input: Eingehende Energie (z.B. aus Benutzer-Aktivität)

        Returns:
            FlowEvent mit Informationen über den Schritt
        """
        self._save_state()

        # Normalisiere Energie
        energy = max(0.1, min(energy_input, 100.0))

        if self.phase == FlowPhase.EXPANSION:
            # Aufstieg auf äußerer Oberfläche
            self.velocity = energy * (1 - self.current_position / self.FLIP_POINT * 0.5)
            self.current_position += self.velocity

            # Erreichen des Plateaus
            if self.current_position >= self.PLATEAU_START:
                if self.current_position >= self.FLIP_POINT:
                    self.phase = FlowPhase.CONTRACTION
                    return FlowEvent(
                        event_type="flip",
                        message="808 erreicht - Übergang zur Kontraktion",
                        position=self.current_position,
                        cycle=self.cycle_count,
                        potential=self.accumulated_potential,
                        recommendations=[
                            "Zeit für Reflexion und Integration",
                            "Ergebnisse konsolidieren",
                            "Vorbereitung auf neuen Zyklus",
                        ],
                    )
                else:
                    self.phase = FlowPhase.PLATEAU
                    return FlowEvent(
                        event_type="milestone",
                        message="Plateau erreicht (777-808)",
                        position=self.current_position,
                        cycle=self.cycle_count,
                        potential=self.accumulated_potential,
                        recommendations=["Peak-Performance nutzen"],
                    )

        elif self.phase == FlowPhase.PLATEAU:
            # Langsame Bewegung im Plateau
            self.velocity = energy * 0.3
            self.current_position += self.velocity

            if self.current_position >= self.FLIP_POINT:
                self.phase = FlowPhase.CONTRACTION
                return FlowEvent(
                    event_type="flip",
                    message="808 Flip-Point passiert",
                    position=self.current_position,
                    cycle=self.cycle_count,
                    potential=self.accumulated_potential,
                    recommendations=["Kontraktion beginnt - Essenz extrahieren"],
                )

        elif self.phase == FlowPhase.CONTRACTION:
            # Abstieg durch inneren Sog - gedämpft durch SI
            self.velocity = energy * self.SYNC_INDEX
            self.current_position -= self.velocity

            if self.current_position <= 0:
                # Zyklus abgeschlossen
                self.cycle_count += 1
                self.phase = FlowPhase.REBIRTH

                # Akkumuliere Potential - jede Null ist "reicher"
                cycle_contribution = self.DAMPING_FACTOR * math.log(
                    self.cycle_count + 1
                )
                self.accumulated_potential += cycle_contribution

                self.current_position = 0.0
                self.phase = FlowPhase.EXPANSION

                return FlowEvent(
                    event_type="rebirth",
                    message=f"Zyklus {self.cycle_count} vollendet - Wiedergeburt",
                    position=0.0,
                    cycle=self.cycle_count,
                    potential=self.accumulated_potential,
                    recommendations=[
                        f"Neuer Zyklus mit Potential {self.accumulated_potential:.3f}",
                        "Vorheriges Lernen integriert",
                        "Bereit für neue Expansion",
                    ],
                )

        # Standard-Event wenn nichts Besonderes passiert
        milestone_event = self._check_milestones()
        if milestone_event:
            return milestone_event

        return FlowEvent(
            event_type="flow",
            message=f"Position: {self.current_position:.1f} | Phase: {self.phase.value}",
            position=self.current_position,
            cycle=self.cycle_count,
            potential=self.accumulated_potential,
            recommendations=[],
        )

    def get_current_state(self) -> FlowState:
        """Gibt aktuellen Zustand zurück"""
        return FlowState(
            position=self.current_position,
            phase=self.phase,
            cycle_count=self.cycle_count,
            accumulated_potential=self.accumulated_potential,
            velocity=self.velocity,
            timestamp=datetime.now(),
        )

    def get_cycle_progress(self) -> float:
        """Berechnet Fortschritt im aktuellen Zyklus (0.0 - 1.0)"""
        if self.phase in [FlowPhase.EXPANSION, FlowPhase.PLATEAU]:
            return self.current_position / self.FLIP_POINT
        else:
            return 1 - (self.current_position / self.FLIP_POINT)

    def predict_next_milestone(self) -> Dict:
        """Sagt nächsten Milestone voraus"""
        for milestone in sorted(self.MILESTONES.keys()):
            if milestone > self.current_position:
                distance = milestone - self.current_position
                eta_steps = distance / max(self.velocity, 0.1)
                return {
                    "milestone": milestone,
                    "description": self.MILESTONES[milestone],
                    "distance": distance,
                    "estimated_steps": int(eta_steps),
                }
        return {
            "milestone": 808,
            "description": "Flip-Point",
            "distance": 0,
            "estimated_steps": 0,
        }

    def reset(self) -> None:
        """Setzt Engine auf Ausgangszustand zurück (behält Potential)"""
        self.current_position = 0.0
        self.phase = FlowPhase.EXPANSION
        self.velocity = 1.0
        self._last_milestone = 0.0
        # accumulated_potential und cycle_count bleiben erhalten!

    def hard_reset(self) -> None:
        """Vollständiger Reset inklusive Potential"""
        self.reset()
        self.cycle_count = 0
        self.accumulated_potential = 0.0
        self.history.clear()


# Singleton
_torus_engine: Optional[TorusFlowEngine] = None


def get_torus_flow_engine() -> TorusFlowEngine:
    """Factory-Funktion für TorusFlowEngine Singleton"""
    global _torus_engine
    if _torus_engine is None:
        _torus_engine = TorusFlowEngine()
    return _torus_engine
