"""
LUCA 369/370 - Info-Block-Engine
Bekämpft den Informations-Tsunami durch modulare, aufbauende Antworten

Architekt: Lennart Wuchold
Standard: 369/370
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class BlockType(Enum):
    """Die drei Arten von Info-Blöcken"""
    FOUNDATION = "foundation"      # Basis-Konzept
    BUILDING = "building"          # Darauf aufbauend
    CONNECTION = "connection"      # Verknüpfung/Anwendung


@dataclass
class InfoBlock:
    """
    Ein einzelner Info-Block nach LUCA-Standard

    Qualitätskriterien:
    - Max 3 Sätze
    - Klarer Block-Typ
    - Referenz zum vorherigen Block
    - Preview für nächsten Block (optional)
    """
    content: str
    block_type: BlockType
    sentence_count: int
    has_next_preview: bool = False
    next_block_hint: Optional[str] = None

    def validate_quality(self) -> bool:
        """Validiert gegen 369/370 Standard"""
        sentences = self.content.count('.') + self.content.count('!') + self.content.count('?')
        return sentences <= 3 and len(self.content) > 0


class InfoBlockEngine:
    """
    Kern-Engine für Info-Block-Generierung

    Athene's Weisheit: Präzision über Vollständigkeit
    """

    def __init__(self):
        self.max_blocks_per_response = 5
        self.max_sentences_per_block = 3
        self.quality_threshold = 369/370  # 0.997

    def create_foundation_block(self, core_concept: str) -> InfoBlock:
        """
        Block 1: Das Fundament

        Funktion:
        - Definiert das Kern-Konzept
        - Gibt Kontext
        - Verspricht mehr Details

        Args:
            core_concept: Das zentrale Konzept der Antwort

        Returns:
            InfoBlock mit Foundation-Typ
        """
        # TODO: Hier kommt die LLM-Integration oder Template-Logic
        # Für jetzt: Struktureller Platzhalter

        return InfoBlock(
            content=f"Foundation: {core_concept}",
            block_type=BlockType.FOUNDATION,
            sentence_count=2,
            has_next_preview=True,
            next_block_hint="Mehr dazu im nächsten Block"
        )

    def create_building_block(self, foundation: InfoBlock, detail_aspect: str) -> InfoBlock:
        """
        Block 2-4: Aufbauend

        Funktion:
        - Baut auf Foundation auf
        - Fügt einen Detail-Aspekt hinzu
        - Verweist zurück zum Fundament

        Args:
            foundation: Der Foundation-Block
            detail_aspect: Welcher Aspekt wird vertieft

        Returns:
            InfoBlock mit Building-Typ
        """

        return InfoBlock(
            content=f"Building on foundation: {detail_aspect}",
            block_type=BlockType.BUILDING,
            sentence_count=3,
            has_next_preview=True,
            next_block_hint="Wie das zusammenhängt: nächster Block"
        )

    def create_connection_block(self, previous_blocks: List[InfoBlock],
                               application: str) -> InfoBlock:
        """
        Block 5: Die Verbindung

        Funktion:
        - Verknüpft alle vorherigen Blöcke
        - Zeigt praktische Anwendung
        - Gibt optionalen Ausblick

        Args:
            previous_blocks: Alle bisherigen Blöcke
            application: Praktische Anwendung/Relevanz

        Returns:
            InfoBlock mit Connection-Typ
        """

        return InfoBlock(
            content=f"Connection to application: {application}",
            block_type=BlockType.CONNECTION,
            sentence_count=3,
            has_next_preview=False,  # Letzter Block
            next_block_hint=None
        )

    def generate_response(self, query: str,
                         user_profile: Optional[Dict] = None) -> List[InfoBlock]:
        """
        Haupt-Methode: Generiert komplette Block-Antwort

        Args:
            query: Die User-Frage
            user_profile: Optional - User-Präferenzen aus Onboarding

        Returns:
            Liste von InfoBlocks (max 5)

        Quality-Check:
            - Jeder Block validated
            - Gesamt-Score >= 369/370
        """

        blocks = []

        # 1. Analysiere Query (Placeholder - hier später LLM-Integration)
        core_concept = self._extract_core_concept(query)
        detail_aspects = self._identify_detail_aspects(query, user_profile)
        application = self._determine_application(query, user_profile)

        # 2. Baue Blocks
        foundation = self.create_foundation_block(core_concept)
        blocks.append(foundation)

        # 3. Building Blocks (1-3 Stück je nach Komplexität)
        for aspect in detail_aspects[:3]:  # Max 3 Building Blocks
            building = self.create_building_block(foundation, aspect)
            blocks.append(building)

        # 4. Connection Block
        connection = self.create_connection_block(blocks, application)
        blocks.append(connection)

        # 5. Quality Validation
        if not self._validate_response_quality(blocks):
            raise QualityException("Response does not meet 369/370 standard")

        return blocks

    def _extract_core_concept(self, query: str) -> str:
        """
        Extrahiert das Kern-Konzept aus der Query

        TODO:
        - Integration mit LLM für semantische Analyse
        - Oder: Pattern-Matching für häufige Queries
        """
        # Placeholder Implementation
        return f"Core concept from: {query[:50]}"

    def _identify_detail_aspects(self, query: str,
                                 user_profile: Optional[Dict]) -> List[str]:
        """
        Identifiziert welche Detail-Aspekte relevant sind

        Berücksichtigt:
        - Query-Komplexität
        - User-Profile (falls vorhanden)
        - 369/370 Limit (max 3 Aspekte)
        """
        # Placeholder - später: LLM oder Heuristik
        return ["Aspect 1", "Aspect 2", "Aspect 3"]

    def _determine_application(self, query: str,
                              user_profile: Optional[Dict]) -> str:
        """
        Bestimmt die praktische Anwendung/Relevanz

        Nutzt User-Profile um Kontext zu geben:
        - Coder → Code-Beispiel
        - Writer → Writing-Anwendung
        - Learner → Lern-Kontext
        """
        if user_profile and 'main_use' in user_profile:
            return f"Application for {user_profile['main_use']}"
        return "General application"

    def _validate_response_quality(self, blocks: List[InfoBlock]) -> bool:
        """
        Validiert gesamte Response gegen 369/370 Standard

        Kriterien:
        - Max 5 Blöcke
        - Jeder Block max 3 Sätze
        - Foundation → Building → Connection Flow
        - Quality Score >= 0.997
        """
        if len(blocks) > self.max_blocks_per_response:
            return False

        # Validiere jeden Block
        valid_blocks = sum(1 for block in blocks if block.validate_quality())
        quality_score = valid_blocks / len(blocks) if blocks else 0

        # Check Flow
        has_foundation = any(b.block_type == BlockType.FOUNDATION for b in blocks)
        has_connection = any(b.block_type == BlockType.CONNECTION for b in blocks)

        return (quality_score >= self.quality_threshold and
                has_foundation and
                has_connection)


class QualityException(Exception):
    """Exception für 369/370 Qualitätsverletzungen"""
    pass
