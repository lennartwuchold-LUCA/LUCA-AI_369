"""
LUCA 369/370 - Integrated Response System
Kombiniert Info-Block-Engine mit Progressive Disclosure

Vollständiges End-to-End System
"""

from typing import List, Dict, Optional
from luca_369_370.core.info_block_engine import InfoBlockEngine, InfoBlock
from luca_369_370.core.progressive_disclosure import (
    ProgressiveDisclosureEngine,
    ProgressiveBlockFormatter,
    DisclosureMode
)


class IntegratedResponseSystem:
    """
    Verbindet alle LUCA-Komponenten zu einer Pipeline

    Flow:
    1. User Query kommt rein
    2. InfoBlockEngine generiert Blöcke
    3. ProgressiveDisclosureEngine zeigt sie schrittweise
    4. Formatter macht Display-ready
    """

    def __init__(self):
        self.block_engine = InfoBlockEngine()
        self.formatter = ProgressiveBlockFormatter()

    def process_query(self, query: str,
                     disclosure_mode: DisclosureMode = DisclosureMode.MANUAL,
                     user_profile: Optional[Dict] = None) -> ProgressiveDisclosureEngine:
        """
        Kompletter Query-Processing Flow

        Args:
            query: User Frage
            disclosure_mode: Wie Blöcke angezeigt werden
            user_profile: Optional User Preferences

        Returns:
            ProgressiveDisclosureEngine ready for interaction
        """

        # 1. Generiere Info-Blöcke
        blocks = self.block_engine.generate_response(query, user_profile)

        # 2. Erstelle Progressive Disclosure Engine
        disclosure_engine = ProgressiveDisclosureEngine(blocks, disclosure_mode)

        return disclosure_engine

    def get_formatted_display(self,
                            disclosure_engine: ProgressiveDisclosureEngine,
                            format_type: str = 'cli') -> str:
        """
        Holt aktuellen Display State und formatiert ihn

        Args:
            disclosure_engine: Die aktive Disclosure Engine
            format_type: 'cli' oder 'web'

        Returns:
            Formatierter String oder Dict
        """
        display_data = disclosure_engine.get_current_display()

        if format_type == 'cli':
            return self.formatter.format_for_cli(display_data)
        elif format_type == 'web':
            return self.formatter.format_for_web(display_data)
        else:
            return display_data
