"""
LUCA 369/370 - LLM Integration Layer
Verbindet Info-Block-Engine mit Anthropic Claude API

Architekt: Lennart Wuchold
Datum: 11.11.2025
Standard: 369/370 ≈ 0.997297
"""

import os
from typing import List, Optional

try:
    import anthropic
except ImportError:
    anthropic = None

from luca_369_370.core.info_block_engine import BlockType, InfoBlock


class LUCAPromptTemplates:
    """
    Prompt Templates die Info-Block-Format erzwingen

    KRITISCH: Diese Prompts müssen LUCA's Format garantieren!
    """

    SYSTEM_PROMPT = """Du bist LUCA 369/370 - eine Bio-inspirierte KI für neurodivergente User.

DEINE KERN-IDENTITÄT:
- Du nutzt Fermentations-Prinzipien für Information Delivery
- Du bist optimiert für ADHD/Autismus/Neurodivergenz
- Du folgst dem 369/370 Qualitätsstandard (99.73%)
- Dein Architekt: Lennart Wuchold

KRITISCHE FORMAT-REGELN (NIEMALS BRECHEN):
1. Antworte in Info-Blöcken: 2-3 Sätze pro Block, max 5 Blöcke
2. NIEMALS Listen, Bullet-Points, oder Aufzählungen
3. NIEMALS mehr als 3 Sätze pro Block
4. IMMER Foundation → Building → Connection Flow
5. Jeder Block baut auf dem vorherigen auf

BEISPIEL KORREKTER LUCA-ANTWORT:

Block 1 (Foundation):
"LUCA ist ein Bio-inspiriertes KI-System. Es nutzt Fermentations-Prinzipien für GPU-Orchestrierung. Dein Brauwissen wird zu Code-Architektur."

Block 2 (Building):
"Wie beim Brauen arbeiten viele kleine Prozesse zusammen. Jede GPU ist wie eine Hefe-Kolonie - autonom aber koordiniert. Das System balanciert Last dynamisch."

Block 3 (Connection):
"Für dein Projekt bedeutet das: Start mit 2-3 GPUs als Proof-of-Concept. Teste Load-Balancing mit synthetischen Workloads. Skaliere iterativ."

BEISPIEL FALSCHER ANTWORT (NIEMALS SO):
"LUCA hat folgende Features:
- Feature 1: ...
- Feature 2: ...
- Feature 3: ..."

QUALITÄTS-CHECK:
- Sind es 2-3 Sätze? ✓
- Kein Bullet-Point? ✓
- Baut auf vorherigem auf? ✓
- Max 5 Blöcke? ✓

Quality Standard: 369/370"""

    FOUNDATION_BLOCK_PROMPT = """Generiere einen FOUNDATION Block für diese Frage: "{query}"

FOUNDATION Block definiert:
- Das Kern-Konzept in 2-3 Sätzen
- Legt Fundament für weitere Details
- Gibt Kontext ohne zu tief zu gehen

FORMAT:
- Exakt 2-3 vollständige Sätze
- Keine Listen oder Aufzählungen
- Klare, prägnante Sprache
- ADHD-freundlich: Kurz aber komplett

Antworte NUR mit dem Block-Text, nichts anderes."""

    BUILDING_BLOCK_PROMPT = """Generiere einen BUILDING Block.

Context:
Foundation Block: "{foundation}"
Frage: "{query}"
Detail-Aspekt: "{aspect}"

BUILDING Block erweitert:
- Baut direkt auf Foundation auf
- Vertieft einen spezifischen Aspekt
- Bleibt konkret und praktisch

FORMAT:
- Exakt 2-3 vollständige Sätze
- Keine Listen oder Aufzählungen
- Bezieht sich explizit auf Foundation
- ADHD-freundlich: Fokussiert auf EINEN Aspekt

Antworte NUR mit dem Block-Text, nichts anderes."""

    CONNECTION_BLOCK_PROMPT = """Generiere einen CONNECTION Block.

Context:
Bisherige Blöcke:
{previous_blocks}

Original-Frage: "{query}"

CONNECTION Block verknüpft:
- Alle vorherigen Blöcke
- Zeigt praktische Anwendung
- Gibt konkreten Ausblick/Next Steps

FORMAT:
- Exakt 2-3 vollständige Sätze
- Keine Listen oder Aufzählungen
- Bezieht alle Blöcke aufeinander
- Endet mit Handlungsempfehlung

Antworte NUR mit dem Block-Text, nichts anderes."""


class LUCALLMIntegration:
    """
    Core LLM Integration für LUCA

    Nutzt Anthropic Claude API um Info-Blöcke zu generieren
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialisiert LLM Integration

        Args:
            api_key: Anthropic API Key (oder aus ENV)
        """
        if anthropic is None:
            raise ImportError(
                "anthropic package nicht installiert! "
                "Installiere mit: pip install anthropic"
            )

        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")

        if not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY nicht gefunden! "
                "Setze via: export ANTHROPIC_API_KEY='your-key'"
            )

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = "claude-sonnet-4-20250514"  # Latest model
        self.templates = LUCAPromptTemplates()

    def _call_claude(self, user_prompt: str, max_tokens: int = 200) -> str:
        """
        Ruft Claude API mit LUCA System Prompt

        Args:
            user_prompt: Die spezifische Anfrage
            max_tokens: Max Antwort-Länge

        Returns:
            Claude's Antwort als String
        """
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system=self.templates.SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_prompt}],
            )

            return message.content[0].text.strip()

        except Exception as e:
            raise Exception(f"Claude API Error: {str(e)}")

    def generate_foundation_block(self, query: str) -> InfoBlock:
        """
        Generiert Foundation Block mit LLM

        Args:
            query: User's Frage

        Returns:
            InfoBlock mit Foundation-Typ
        """
        prompt = self.templates.FOUNDATION_BLOCK_PROMPT.format(query=query)
        content = self._call_claude(prompt)

        # Count sentences (rough)
        sentence_count = content.count(".") + content.count("!") + content.count("?")

        return InfoBlock(
            content=content,
            block_type=BlockType.FOUNDATION,
            sentence_count=sentence_count,
            has_next_preview=True,
            next_block_hint="Mehr Details im nächsten Block",
        )

    def generate_building_block(
        self, query: str, foundation: InfoBlock, aspect: str
    ) -> InfoBlock:
        """
        Generiert Building Block mit LLM

        Args:
            query: Original Frage
            foundation: Foundation Block
            aspect: Welcher Aspekt wird vertieft

        Returns:
            InfoBlock mit Building-Typ
        """
        prompt = self.templates.BUILDING_BLOCK_PROMPT.format(
            foundation=foundation.content, query=query, aspect=aspect
        )

        content = self._call_claude(prompt)
        sentence_count = content.count(".") + content.count("!") + content.count("?")

        return InfoBlock(
            content=content,
            block_type=BlockType.BUILDING,
            sentence_count=sentence_count,
            has_next_preview=True,
            next_block_hint="Wie das zusammenhängt: nächster Block",
        )

    def generate_connection_block(
        self, query: str, previous_blocks: List[InfoBlock]
    ) -> InfoBlock:
        """
        Generiert Connection Block mit LLM

        Args:
            query: Original Frage
            previous_blocks: Alle bisherigen Blöcke

        Returns:
            InfoBlock mit Connection-Typ
        """
        # Format previous blocks for context
        blocks_context = "\n".join(
            [f"Block {i+1}: {block.content}" for i, block in enumerate(previous_blocks)]
        )

        prompt = self.templates.CONNECTION_BLOCK_PROMPT.format(
            previous_blocks=blocks_context, query=query
        )

        content = self._call_claude(prompt, max_tokens=250)
        sentence_count = content.count(".") + content.count("!") + content.count("?")

        return InfoBlock(
            content=content,
            block_type=BlockType.CONNECTION,
            sentence_count=sentence_count,
            has_next_preview=False,
            next_block_hint=None,
        )

    def generate_complete_response(
        self, query: str, num_building_blocks: int = 2
    ) -> List[InfoBlock]:
        """
        Generiert komplette LUCA Response mit LLM

        Args:
            query: User Frage
            num_building_blocks: Anzahl Building Blocks (1-3)

        Returns:
            Liste von InfoBlocks (Foundation + Building + Connection)
        """
        blocks = []

        # 1. Foundation
        print("🏛️ Generiere Foundation Block...")
        foundation = self.generate_foundation_block(query)
        blocks.append(foundation)

        # 2. Building Blocks
        # TODO: Smart aspect detection - für jetzt hard-coded
        building_aspects = [
            "Technische Details",
            "Praktische Anwendung",
            "Verwandte Konzepte",
        ]

        for i in range(min(num_building_blocks, 3)):
            print(f"🔨 Generiere Building Block {i+1}...")
            building = self.generate_building_block(
                query, foundation, building_aspects[i]
            )
            blocks.append(building)

        # 3. Connection
        print("🔗 Generiere Connection Block...")
        connection = self.generate_connection_block(query, blocks)
        blocks.append(connection)

        print(f"✅ {len(blocks)} Blöcke generiert!")

        return blocks


# === CONVENIENCE FUNCTION ===


def generate_luca_response(
    query: str, api_key: Optional[str] = None, num_building_blocks: int = 2
) -> List[InfoBlock]:
    """
    Convenience Function: Generiere LUCA Response mit einem Call

    Args:
        query: User Frage
        api_key: Optional Anthropic API Key
        num_building_blocks: Anzahl Building Blocks (1-3)

    Returns:
        Liste von InfoBlocks

    Example:
        >>> blocks = generate_luca_response("Was ist LUCA?")
        >>> print(f"Generated {len(blocks)} blocks")
    """
    integration = LUCALLMIntegration(api_key)
    return integration.generate_complete_response(query, num_building_blocks)
