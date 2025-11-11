"""
LUCA Mesh Bridge - Info-Block Engine × Meshtastic Integration
Verbindet LUCA's Info-Block-System mit dezentralem Mesh-Netzwerk

Architekt: Lennart Wuchold
Datum: 11.11.2025
Standard: 369/370
"""

from typing import Dict, List, Optional

from luca_369_370.core.info_block_engine import BlockType, InfoBlock, InfoBlockEngine
from luca_369_370.meshtastic.mesh_network import MESHTASTIC_AVAILABLE, LucaMeshNetwork


class LucaMeshBridge:
    """
    Bridge zwischen LUCA Info-Block-Engine und Meshtastic

    Features:
    - Info-Blocks über LoRa senden
    - Progressive Disclosure über Mesh
    - Automatische Block-Kompression (256 byte limit)
    - Offline-First Design
    """

    def __init__(self, node_name: str = "LUCA_Bridge"):
        """
        Initialize LUCA Mesh Bridge

        Args:
            node_name: Name des Mesh-Nodes
        """
        self.info_block_engine = InfoBlockEngine()

        if MESHTASTIC_AVAILABLE:
            self.mesh = LucaMeshNetwork(node_name=node_name)
        else:
            self.mesh = None
            print("⚠️  Meshtastic nicht verfügbar - Offline-Modus")

    def process_query_via_mesh(
        self, query: str, sender: Optional[str] = None
    ) -> List[InfoBlock]:
        """
        Verarbeite Query und sende Response via Meshtastic

        Args:
            query: User Query
            sender: Optional sender ID für direkte Response

        Returns:
            Liste der generierten Info-Blocks
        """
        print(f"\n🏛️ Verarbeite Mesh-Query: '{query}'")

        # Generiere Info-Blocks (template-based, kein LLM nötig)
        blocks = self.info_block_engine.generate_response(query)

        print(f"✅ {len(blocks)} Blöcke generiert")

        # Sende über Meshtastic
        if self.mesh:
            self.send_blocks_via_mesh(blocks, recipient=sender)
        else:
            print("⚠️  Kein Mesh verfügbar - Blöcke nur lokal")

        return blocks

    def send_blocks_via_mesh(
        self, blocks: List[InfoBlock], recipient: Optional[str] = None
    ):
        """
        Sende Info-Blocks über Meshtastic

        Args:
            blocks: Liste von Info-Blöcken
            recipient: Optional spezifischer Empfänger
        """
        if not self.mesh:
            print("❌ Mesh nicht verfügbar")
            return

        print(f"📤 Sende {len(blocks)} Blöcke über Mesh...")

        for i, block in enumerate(blocks):
            # Komprimiere für Meshtastic (256 bytes)
            compressed = self._compress_block_for_mesh(block, i, len(blocks))

            # Sende via LoRa
            self.mesh.send_message(compressed, encrypt=True)

            print(f"  ✅ Block {i+1}/{len(blocks)} gesendet ({block.block_type.value})")

    def _compress_block_for_mesh(self, block: InfoBlock, index: int, total: int) -> str:
        """
        Komprimiere Info-Block für Meshtastic 256-byte Limit

        Format: [LUCA][IDX/TOTAL][TYPE] Content

        Args:
            block: Der Info-Block
            index: Block-Index
            total: Gesamtanzahl Blöcke

        Returns:
            Komprimierter Block-String
        """
        # Header
        type_char = block.block_type.value[0]  # F/B/C
        header = f"[LUCA][{index+1}/{total}][{type_char}]"

        # Berechne verfügbaren Platz (256 - header - safety margin)
        max_content = 256 - len(header) - 20

        # Komprimiere Content
        content = block.content[:max_content]

        # Indikator wenn gekürzt
        if len(block.content) > max_content:
            content = content[:-3] + "..."

        return f"{header} {content}"

    def handle_incoming_mesh_query(self, message: str, sender: str):
        """
        Verarbeite eingehende Mesh-Query

        Args:
            message: Die Query-Nachricht
            sender: Sender-ID
        """
        # Parse Query aus Mesh-Nachricht
        if message.startswith("/query "):
            query = message[7:]
            print(f"📨 Mesh-Query von {sender}: {query}")

            # Generiere und sende Response
            self.process_query_via_mesh(query, sender=sender)

    def create_lightweight_block(
        self, block_type: BlockType, content: str, next_hint: Optional[str] = None
    ) -> InfoBlock:
        """
        Erstelle lightweight Info-Block für Mesh

        Args:
            block_type: Typ des Blocks
            content: Block-Content (max 200 chars für Mesh)
            next_hint: Optional Preview-Hint

        Returns:
            InfoBlock optimiert für Mesh-Übertragung
        """
        # Truncate für Mesh
        content_truncated = content[:200]

        # Count sentences
        sentence_count = (
            content_truncated.count(".")
            + content_truncated.count("!")
            + content_truncated.count("?")
        )

        return InfoBlock(
            content=content_truncated,
            block_type=block_type,
            sentence_count=sentence_count,
            has_next_preview=bool(next_hint),
            next_block_hint=next_hint,
        )

    def connect_to_mesh(self, port: Optional[str] = None, host: Optional[str] = None):
        """
        Verbinde zu Meshtastic-Netzwerk

        Args:
            port: Serial port
            host: TCP host
        """
        if not self.mesh:
            print("❌ Mesh nicht verfügbar")
            return

        self.mesh.connect_mesh(port=port, host=host)

    def get_bridge_stats(self) -> Dict:
        """
        Holt Bridge-Statistiken

        Returns:
            Dictionary mit Stats
        """
        stats = {
            "info_block_engine": "active",
            "mesh_available": self.mesh is not None,
        }

        if self.mesh:
            mesh_stats = self.mesh.get_mesh_stats()
            stats.update(mesh_stats)

        return stats


# Convenience Functions


def create_mesh_enabled_luca(node_name: str = "LUCA_Node") -> LucaMeshBridge:
    """
    Erstelle Mesh-enabled LUCA Instance

    Args:
        node_name: Name des Nodes

    Returns:
        Konfigurierter LucaMeshBridge

    Example:
        >>> luca = create_mesh_enabled_luca("LUCA_Community_Node")
        >>> luca.connect_to_mesh(port='/dev/ttyUSB0')
        >>> luca.process_query_via_mesh("Was ist LUCA?")
    """
    return LucaMeshBridge(node_name=node_name)


def send_luca_info_via_mesh(query: str, mesh_port: str = "/dev/ttyUSB0"):
    """
    Quick helper: Sende LUCA Info via Mesh

    Args:
        query: Die Frage
        mesh_port: Meshtastic Port

    Example:
        >>> send_luca_info_via_mesh("Wie filtere ich Wasser?")
    """
    bridge = create_mesh_enabled_luca()
    bridge.connect_to_mesh(port=mesh_port)
    bridge.process_query_via_mesh(query)
