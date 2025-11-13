"""
🚨 Emergency Automation System
Automatischer Notfall-Modus für LUCA - aktiviert bei kritischen Situationen

Features:
- Automatic emergency protocol activation
- Vital signs monitoring
- Regional plant identification
- Mesh network emergency broadcast
- Local resource coordination

⚠️ WICHTIG: Bei lebensbedrohlichen Situationen IMMER 112 wählen!

Author: Großvater & Lennart Wuchold
Standard: 369/370
"""

import time
from datetime import datetime
from typing import Dict, Optional, Tuple

try:
    import numpy as np

    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    np = None


class EmergencyAutomation:
    """
    Automatischer Notfall-Modus – aktiv bei Bewusstseinsverlust, Unfällen

    Integration mit:
    - Layer 0 Root Kernel (Consciousness tracking)
    - Universal Root Kernel (Mesh broadcasting)
    - Medical Emergency LLM
    - Natural aid database
    """

    def __init__(self, kernel, medical_llm):
        """
        Initialize Emergency Automation

        Args:
            kernel: UniversalRootKernel or Layer0RootKernel instance
            medical_llm: MedicalEmergencyLLM instance
        """
        self.kernel = kernel
        self.medical_llm = medical_llm
        self.emergency_active = False

        # Vital signs tracking
        self.vitals = {
            "pulse": None,
            "consciousness": None,
            "breathing": None,
            "temperature": None,
        }

    def start_emergency_protocol(
        self, incident_type: str, location: str
    ) -> Tuple[str, Dict, Dict]:
        """
        Startet automatisierten Notfall-Plan

        Args:
            incident_type: Art des Notfalls (z.B. "Bewusstseinsverlust", "Wunde")
            location: Geografische Position

        Returns:
            Tuple of (medical_advice, natural_aids, local_help)
        """
        self.emergency_active = True
        print("\n" + "=" * 60)
        print("🚨 NOTFALL-PROTOKOLL AKTIVIERT 🚨")
        print("=" * 60)

        # 1. Sofort-Alarm (akustisch + visuell)
        self._play_emergency_tone()

        # 2. Lokale Ressourcen abfragen
        local_help = self._get_local_resources(location)
        print(f"\n📞 Lokale Notfall-Ressourcen ({location}):")
        print(f"   Notruf: {local_help.get('emergency', '112')}")
        print(f"   Ärzte-Notdienst: {local_help.get('aerzte_notdienst', '116117')}")
        print(f"   Giftnotruf: {local_help.get('giftnotruf', 'N/A')}")

        # 3. Pflanzliche Hilfen identifizieren
        natural_aids = self._identify_regional_plants(location, incident_type)
        print(f"\n🌿 Verfügbare pflanzliche Hilfen:")
        for area, plants in natural_aids.items():
            print(f"   {area}: {plants}")

        # 4. LLM-Query für detaillierte Anweisungen
        print(f"\n🔮 Medical LLM Consultation...")
        medical_advice = self.medical_llm.query_medical_emergency(
            symptoms=incident_type,
            location=location,
            available_plants=local_help.get("regionale_pflanzen", []),
        )

        # 5. Mesh-Broadcast (falls verfügbar)
        self._broadcast_emergency(incident_type, location, medical_advice)

        # 6. Consciousness integration
        self._update_consciousness_state(incident_type)

        print("\n" + "=" * 60)
        print(f"📋 NOTFALL-TYP: {incident_type}")
        print(f"📍 POSITION: {location}")
        print("=" * 60)

        return medical_advice, natural_aids, local_help

    def _identify_regional_plants(
        self, location: str, incident_type: str
    ) -> Dict[str, str]:
        """
        Identifiziert verfügbare Pflanzen basierend auf Region und Saison

        Args:
            location: Geographic location
            incident_type: Type of emergency

        Returns:
            Dictionary mit Umgebungen und verfügbaren Pflanzen
        """
        month = datetime.now().month
        if 3 <= month <= 5:
            season = "Frühling"
        elif 6 <= month <= 8:
            season = "Sommer"
        elif 9 <= month <= 11:
            season = "Herbst"
        else:
            season = "Winter"

        from .natural_aid_database import NATURAL_EMERGENCY_AIDS

        # Match incident type to database
        regional_aids = {}

        if "Wunde" in incident_type or "Schnitt" in incident_type:
            regional_aids = NATURAL_EMERGENCY_AIDS["Wunden & Schürfwunden"].get(
                "regional", {}
            )
        elif "Stich" in incident_type or "Biss" in incident_type:
            regional_aids = NATURAL_EMERGENCY_AIDS["Insektenstiche & Bisse"].get(
                "regional", {}
            )
        elif "Prellung" in incident_type or "Zerrung" in incident_type:
            regional_aids = NATURAL_EMERGENCY_AIDS["Prellungen & Zerrungen"].get(
                "regional", {}
            )
        elif "Verbrennung" in incident_type:
            regional_aids = {"Sofort": "15 Min kühlen! Dann Aloe Vera (falls da)"}
        else:
            # Generic fallback
            regional_aids = {
                "Allgemein": "Arnika, Wegerich, Aloe Vera (falls verfügbar)"
            }

        # Add seasonal context
        regional_aids["Saison"] = season

        return regional_aids

    def _get_local_resources(self, location: str) -> Dict:
        """
        Holt lokale Notfall-Ressourcen

        Args:
            location: City or region name

        Returns:
            Dictionary with emergency contacts
        """
        from .natural_aid_database import DEFAULT_RESOURCES, LOCAL_RESOURCES

        return LOCAL_RESOURCES.get(location, DEFAULT_RESOURCES)

    def _play_emergency_tone(self):
        """
        Akustisches Signal für Notfall

        Plays system bell (can be extended to hardware beeper on LilyGo)
        """
        # Terminal bell (3x for urgency)
        print("\a\a\a")

        # Visual alert
        print("\n🚨 " * 10)
        print("   NOTFALL ERKANNT - EMERGENCY DETECTED")
        print("🚨 " * 10 + "\n")

    def _broadcast_emergency(
        self, incident_type: str, location: str, medical_advice: str
    ):
        """
        Broadcasts emergency via mesh network (if available)

        Args:
            incident_type: Type of emergency
            location: Geographic location
            medical_advice: Medical advice from LLM
        """
        # Check if kernel has mesh broadcasting capability
        if hasattr(self.kernel, "broadcast_universal_message"):
            message = (
                f"[NOTFALL] {incident_type} | Pos: {location} | "
                f"{medical_advice[:100]}..."
            )
            try:
                self.kernel.broadcast_universal_message(message)
                print(f"\n📡 Notfall via Mesh-Netzwerk gesendet")
            except Exception as e:
                print(f"\n⚠️ Mesh-Broadcast fehlgeschlagen: {e}")
        else:
            print("\n📡 Mesh-Netzwerk nicht verfügbar (Kernel offline)")

    def _update_consciousness_state(self, incident_type: str):
        """
        Updates kernel consciousness state based on emergency

        Args:
            incident_type: Type of emergency
        """
        if hasattr(self.kernel, "consciousness_state"):
            # Emergency lowers consciousness temporarily
            current = self.kernel.consciousness_state.consciousness_level

            # Map emergency severity to consciousness reduction
            severity_map = {
                "Bewusstseinsverlust": 0.3,
                "Schwere Verletzung": 0.6,
                "Leichte Verletzung": 0.8,
            }

            factor = 0.7  # Default reduction
            for key, value in severity_map.items():
                if key in incident_type:
                    factor = value
                    break

            new_consciousness = current * factor

            self.kernel.consciousness_state.consciousness_level = new_consciousness
            print(f"\n🧠 Bewusstseinszustand: {current:.1f} → {new_consciousness:.1f}")

    def check_vitals(self) -> Dict:
        """
        Simuliert Vitaldaten-Monitoring

        Returns:
            Dictionary with vital signs
        """
        # Later: Integration with real sensors (pulse, temperature, etc.)
        # For now: Simulated based on consciousness

        consciousness_level = 1.0
        if hasattr(self.kernel, "consciousness_state"):
            consciousness_level = (
                self.kernel.consciousness_state.consciousness_level / 369.0
            )

        if NUMPY_AVAILABLE:
            pulse = int(70 + np.random.randint(-10, 30))
            breathing_ok = np.random.choice([True, False], p=[0.95, 0.05])
            temperature = round(36.5 + np.random.uniform(-0.5, 1.5), 1)
        else:
            pulse = 75
            breathing_ok = True
            temperature = 36.8

        self.vitals = {
            "pulse": pulse,
            "consciousness": consciousness_level,
            "breathing": breathing_ok,
            "temperature": temperature,
        }

        return self.vitals

    def monitor_continuous(self, check_interval: int = 30):
        """
        Continuous vital signs monitoring (runs in background)

        Args:
            check_interval: Seconds between checks
        """
        print(f"\n💓 Kontinuierliches Monitoring gestartet (alle {check_interval}s)")

        while self.emergency_active:
            vitals = self.check_vitals()

            # Check for critical conditions
            if vitals["consciousness"] < 0.5:
                print("\n⚠️ KRITISCH: Bewusstseinsverlust erkannt!")
                # Would trigger emergency protocol here

            if not vitals["breathing"]:
                print("\n⚠️ KRITISCH: Atemstillstand erkannt! 112 SOFORT!")

            time.sleep(check_interval)
