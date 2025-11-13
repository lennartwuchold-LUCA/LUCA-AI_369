"""
LUCA 369/370 - Integrated Response System
NOW with REAL LLM Integration!

Kombiniert Info-Block-Engine mit Progressive Disclosure und LLM

Architekt: Lennart Wuchold
Datum: 11.11.2025
Standard: 369/370
"""

from typing import Dict, List, Optional

from luca.core.info_block_engine import InfoBlock, InfoBlockEngine
from luca.core.progressive_disclosure import (
    DisclosureMode,
    ProgressiveBlockFormatter,
    ProgressiveDisclosureEngine,
)

# LLM Integration (optional)
try:
    from luca.core.llm_integration import LUCALLMIntegration

    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False


class IntegratedResponseSystem:
    """
    Complete LUCA Pipeline mit LLM Integration

    Flow:
    1. User Query → LLM Integration (wenn verfügbar)
    2. LLM generates Info-Blocks
    3. Progressive Disclosure wraps them
    4. Formatter makes display-ready
    """

    def __init__(self, api_key: Optional[str] = None, use_llm: bool = True):
        """
        Initialize with optional LLM Integration

        Args:
            api_key: Optional Anthropic API Key
            use_llm: Whether to use LLM (requires anthropic package + API key)
        """
        self.use_llm = use_llm and LLM_AVAILABLE

        if self.use_llm:
            try:
                self.llm = LUCALLMIntegration(api_key)
                print("✅ LLM Integration active (Anthropic Claude)")
            except (ValueError, ImportError) as e:
                print(f"⚠️  LLM nicht verfügbar: {e}")
                print("   Fallback auf statische Blöcke")
                self.use_llm = False
                self.block_engine = InfoBlockEngine()
        else:
            self.block_engine = InfoBlockEngine()

        self.formatter = ProgressiveBlockFormatter()

    def process_query(
        self,
        query: str,
        disclosure_mode: DisclosureMode = DisclosureMode.MANUAL,
        user_profile: Optional[Dict] = None,
        num_building_blocks: int = 2,
    ) -> ProgressiveDisclosureEngine:
        """
        Complete Query Processing mit LLM

        Args:
            query: User Frage
            disclosure_mode: Wie Blöcke angezeigt werden
            user_profile: Optional User Preferences
            num_building_blocks: Anzahl Building Blocks (1-3, nur für LLM)

        Returns:
            ProgressiveDisclosureEngine ready for interaction
        """

        print(f"\n🏛️ LUCA 369/370 verarbeitet: '{query}'")
        print("=" * 60)

        # 1. Generiere Info-Blöcke
        if self.use_llm:
            # Mit LLM Integration
            blocks = self.llm.generate_complete_response(query, num_building_blocks)
        else:
            # Fallback auf statische Engine
            blocks = self.block_engine.generate_response(query, user_profile)

        # 2. Erstelle Progressive Disclosure Engine
        disclosure_engine = ProgressiveDisclosureEngine(blocks, disclosure_mode)

        print("✅ Response bereit!")
        print("=" * 60)

        return disclosure_engine

    def get_formatted_display(
        self, disclosure_engine: ProgressiveDisclosureEngine, format_type: str = "cli"
    ) -> str:
        """
        Holt aktuellen Display State und formatiert ihn

        Args:
            disclosure_engine: Die aktive Disclosure Engine
            format_type: 'cli' oder 'web'

        Returns:
            Formatierter String oder Dict
        """
        display_data = disclosure_engine.get_current_display()

        if format_type == "cli":
            return self.formatter.format_for_cli(display_data)
        elif format_type == "web":
            return self.formatter.format_for_web(display_data)
        else:
            return display_data
