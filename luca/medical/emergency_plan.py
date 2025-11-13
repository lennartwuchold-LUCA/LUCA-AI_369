"""
🚑 Medical Emergency LLM Integration
Combines Claude AI medical knowledge with natural remedies and local resources.

⚠️ WICHTIG: Dieses System ersetzt KEINE ärztliche Behandlung!
Bei lebensbedrohlichen Situationen IMMER 112 wählen!

Author: Großvater & Lennart Wuchold
Standard: 369/370
"""

import os
from typing import Dict, List, Optional

# Optional Anthropic import
try:
    from anthropic import Anthropic

    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    Anthropic = None


class MedicalEmergencyLLM:
    """
    Medizinisches LLM für Notfallsituationen mit pflanzlicher & regionaler Expertise

    Combines:
    - Claude AI medical knowledge (via Anthropic API)
    - Natural/herbal remedies database
    - Regional resource localization
    - 369 consciousness integration
    """

    def __init__(self, anthropic_client: Optional[Anthropic] = None):
        """
        Initialize Medical Emergency LLM

        Args:
            anthropic_client: Anthropic client instance (optional)
        """
        self.client = anthropic_client
        self.medical_history: Dict = {}

        # Try to initialize if not provided
        if not self.client and ANTHROPIC_AVAILABLE:
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if api_key:
                self.client = Anthropic(api_key=api_key)

    def query_medical_emergency(
        self,
        symptoms: str,
        location: Optional[str] = None,
        available_plants: Optional[List[str]] = None,
    ) -> str:
        """
        Query medizinisches LLM mit Fokus auf natürliche & lokale Therapien

        Args:
            symptoms: Beschreibung der Symptome
            location: Geografische Region (z.B. "Hamburg", "Berlin")
            available_plants: Liste verfügbarer Pflanzen in der Umgebung

        Returns:
            Strukturierte medizinische Notfallhilfe (Deutsch)
        """
        if not self.client:
            return self._fallback_response(symptoms, location, available_plants)

        location_info = f"Region: {location}" if location else "Region: Allgemein"
        plants_info = (
            f"Verfügbare Pflanzen: {', '.join(available_plants)}"
            if available_plants
            else ""
        )

        prompt = f"""Du bist ein medizinischer Notfall-Assistent für das LUCA-AI System.

NOTFALL-SITUATION:
Symptome: {symptoms}
{location_info}
{plants_info}

Gib eine strukturierte Antwort in folgendem Format:

1. SOFORTMASSNAHMEN (DRINGEND)
   - Was muss JETZT sofort getan werden?
   - Wann 112 rufen?

2. PFLANZLICHE/NATÜRLICHE HILFEN (wenn sicher anwendbar)
   - Welche der verfügbaren Pflanzen können helfen?
   - Wie anwenden?
   - Warnungen/Kontraindikationen

3. LOKALE RESSOURCEN
   - Apotheken-Notdienst
   - Ärztlicher Bereitschaftsdienst
   - Giftnotrufzentrale (falls relevant)

4. WANN IST PROFESSIONELLE HILFE NÖTIG?
   - Klare Kriterien für ärztliche Behandlung

⚠️ WICHTIG: Betone bei lebensbedrohlichen Symptomen SOFORT 112!

Antworte in Deutsch, präzise, action-orientiert und mit Tesla's 3-6-9 Struktur (3 Sofortmaßnahmen, 6 Optionen, 9 Ressourcen wenn möglich).
"""

        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1500,
                temperature=0.3,  # Lower temp for medical accuracy
                messages=[{"role": "user", "content": prompt}],
            )

            response = message.content[0].text

            # Store in history for learning
            self.medical_history[len(self.medical_history)] = {
                "symptoms": symptoms,
                "location": location,
                "response": response[:200],  # Abbreviated
            }

            return response

        except Exception as e:
            return self._fallback_response(
                symptoms, location, available_plants, error=str(e)
            )

    def _fallback_response(
        self,
        symptoms: str,
        location: Optional[str],
        available_plants: Optional[List[str]],
        error: Optional[str] = None,
    ) -> str:
        """
        Fallback response wenn LLM nicht verfügbar ist

        Returns:
            Basic medical emergency guidance
        """
        error_msg = f"\n⚠️ Medical LLM offline: {error}" if error else ""

        return f"""🚑 NOTFALL-PROTOKOLL (Offline-Modus){error_msg}

SYMPTOME: {symptoms}
REGION: {location or 'Unbekannt'}

1. SOFORTMASSNAHMEN:
   ⚠️ Bei lebensbedrohlichen Symptomen: SOFORT 112 WÄHLEN!

   - Ruhe bewahren
   - Stabile Seitenlage bei Bewusstlosigkeit
   - Bei Blutungen: Druckverband anlegen
   - Bei Verbrennungen: 15 Min unter fließendem Wasser kühlen

2. VERFÜGBARE PFLANZEN: {', '.join(available_plants) if available_plants else 'Keine angegeben'}

   Grundregeln:
   - Arnika: Bei Prellungen/Blutergüssen (NICHT auf offene Wunden!)
   - Wegerich/Spitzwegerich: Bei Insektenstichen, Wunden
   - Aloe Vera: Bei leichten Verbrennungen (1. Grad)

   ⚠️ NUR anwenden wenn 100% sicher identifiziert!

3. LOKALE RESSOURCEN:
   - Notruf: 112
   - Ärztlicher Bereitschaftsdienst: 116117 (Deutschland)
   - Giftnotruf: Regionale Nummer (z.B. Berlin: 030 19240)

4. PROFESSIONELLE HILFE NÖTIG BEI:
   - Bewusstseinsverlust
   - Starke Blutungen
   - Atemnot
   - Verdacht auf Vergiftung
   - Verbrennungen 2./3. Grades
   - Allergische Reaktionen

📖 Detaillierte Informationen: luca/medical/natural_aid_database.py

⚠️ Diese Informationen ersetzen KEINE ärztliche Behandlung!
"""

    def get_regional_resources(self, location: str) -> Dict:
        """
        Get local emergency resources for a region

        Args:
            location: City or region name

        Returns:
            Dictionary with emergency contacts and resources
        """
        from .natural_aid_database import DEFAULT_RESOURCES, LOCAL_RESOURCES

        return LOCAL_RESOURCES.get(location, DEFAULT_RESOURCES)

    def identify_available_plants(
        self, location: str, season: Optional[str] = None
    ) -> List[str]:
        """
        Identify likely available plants in a region

        Args:
            location: Geographic location
            season: Optional season (Frühling, Sommer, Herbst, Winter)

        Returns:
            List of plant names
        """
        from .natural_aid_database import LOCAL_RESOURCES

        resources = LOCAL_RESOURCES.get(location, {})
        return resources.get("regionale_pflanzen", ["Wegerich", "Arnika (Apotheke)"])
