"""
LUCA 369/370 - Block Formatter
Formatiert Info-Blöcke für optimale Lesbarkeit

ADHD-Optimiert:
- Visuelle Breaks
- Klare Struktur
- Progress-Indikatoren
"""

from typing import Dict, List

from .info_block_engine import BlockType, InfoBlock


class BlockFormatter:
    """
    Formatiert Info-Blöcke für Terminal/CLI und später Web-UI
    """

    def __init__(self, style: str = "minimal"):
        self.style = style
        self.block_icons = {
            BlockType.FOUNDATION: "🏛️",
            BlockType.BUILDING: "🔨",
            BlockType.CONNECTION: "🔗",
        }

    def format_response(self, blocks: List[InfoBlock]) -> str:
        """
        Formatiert komplette Response mit visuellen Breaks

        Args:
            blocks: Liste von InfoBlocks

        Returns:
            Formatierter String ready for display
        """
        output = []
        total_blocks = len(blocks)

        # Header
        output.append("=" * 60)
        output.append("🎯 LUCA 369/370 Response")
        output.append("=" * 60)
        output.append("")

        # Blocks
        for idx, block in enumerate(blocks, 1):
            formatted_block = self._format_single_block(block, idx, total_blocks)
            output.append(formatted_block)
            output.append("")  # Visual break

            # Progress indicator
            if idx < total_blocks:
                output.append(f"   ↓ ({idx}/{total_blocks})")
                output.append("")

        # Footer
        output.append("=" * 60)
        output.append("✅ Response complete | Quality: 369/370")
        output.append("=" * 60)

        return "\n".join(output)

    def _format_single_block(self, block: InfoBlock, index: int, total: int) -> str:
        """Formatiert einen einzelnen Block"""

        icon = self.block_icons.get(block.block_type, "📦")
        type_name = block.block_type.value.upper()

        lines = [
            f"{icon} Block {index}/{total} - {type_name}",
            "-" * 60,
            f"{block.content}",
        ]

        if block.has_next_preview and block.next_block_hint:
            lines.append("")
            lines.append(f"   → {block.next_block_hint}")

        return "\n".join(lines)

    def format_for_web(self, blocks: List[InfoBlock]) -> Dict:
        """
        Formatiert für Web-UI (JSON-ready)

        Returns:
            Dict mit strukturierten Block-Daten
        """
        return {
            "blocks": [
                {
                    "index": idx,
                    "type": block.block_type.value,
                    "content": block.content,
                    "icon": self.block_icons.get(block.block_type, "📦"),
                    "has_next": block.has_next_preview,
                    "next_hint": block.next_block_hint,
                }
                for idx, block in enumerate(blocks, 1)
            ],
            "total_blocks": len(blocks),
            "quality_score": 369 / 370,
        }
