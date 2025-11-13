"""
LUCA 369/370 - Meshtastic Integration Tests
Tests für dezentrales Mesh-Netzwerk

Architekt: Lennart Wuchold
Datum: 11.11.2025
Standard: 369/370
"""

import pytest

from luca.core.info_block_engine import BlockType, InfoBlock

# Try to import Meshtastic components
try:
    from luca.meshtastic.luca_mesh_bridge import (
        LucaMeshBridge,
        create_mesh_enabled_luca,
    )
    from luca.meshtastic.mesh_network import MESHTASTIC_AVAILABLE

    MESH_INTEGRATION_AVAILABLE = True
except (ImportError, Exception):
    # Catch all exceptions including cryptography module issues in CI
    MESH_INTEGRATION_AVAILABLE = False
    MESHTASTIC_AVAILABLE = False
    LucaMeshBridge = None  # Stub
    create_mesh_enabled_luca = None  # Stub

# Skip all tests if mesh not available (CI/CD won't have hardware)
pytestmark = pytest.mark.skipif(
    not MESH_INTEGRATION_AVAILABLE,
    reason="Meshtastic integration not available - skipping mesh tests",
)


class TestMeshtasticBasics:
    """Basic Tests für Meshtastic-Integration"""

    def test_mesh_bridge_initialization(self):
        """Test: Mesh Bridge kann initialisiert werden"""
        bridge = LucaMeshBridge(node_name="LUCA_Test_Node")

        assert bridge is not None
        assert bridge.info_block_engine is not None
        # Mesh kann None sein wenn keine Hardware
        assert bridge.mesh is not None or not MESHTASTIC_AVAILABLE

    def test_create_mesh_enabled_luca(self):
        """Test: Convenience function arbeitet"""
        luca = create_mesh_enabled_luca("Test_Node")

        assert luca is not None
        assert luca.info_block_engine is not None

    def test_lightweight_block_creation(self):
        """Test: Lightweight Blocks für Mesh werden erstellt"""
        bridge = LucaMeshBridge()

        block = bridge.create_lightweight_block(
            block_type=BlockType.FOUNDATION,
            content="LUCA ist ein Bio-inspiriertes KI-System. Es nutzt Fermentation.",
            next_hint="Mehr im nächsten Block",
        )

        assert block is not None
        assert block.block_type == BlockType.FOUNDATION
        assert len(block.content) <= 200  # Max für Mesh
        assert block.has_next_preview == True


class TestBlockCompression:
    """Tests für Block-Kompression (256-byte Meshtastic limit)"""

    def test_block_compression_basic(self):
        """Test: Block wird für Meshtastic komprimiert"""
        bridge = LucaMeshBridge()

        block = InfoBlock(
            content="Dies ist ein Test-Block für Meshtastic. Er muss komprimiert werden.",
            block_type=BlockType.FOUNDATION,
            sentence_count=2,
            has_next_preview=True,
            next_block_hint="Next",
        )

        compressed = bridge._compress_block_for_mesh(block, 0, 3)

        assert compressed is not None
        assert len(compressed) <= 256  # Meshtastic limit
        assert "[LUCA]" in compressed
        assert "[1/3]" in compressed
        assert "[F]" in compressed  # Foundation

    def test_block_compression_truncation(self):
        """Test: Lange Blöcke werden gekürzt"""
        bridge = LucaMeshBridge()

        # Block mit sehr langem Content
        long_content = "x" * 500  # Viel zu lang für Meshtastic

        block = InfoBlock(
            content=long_content,
            block_type=BlockType.BUILDING,
            sentence_count=1,
            has_next_preview=False,
        )

        compressed = bridge._compress_block_for_mesh(block, 1, 4)

        assert len(compressed) <= 256
        assert compressed.endswith("...")  # Truncation indicator

    def test_compression_preserves_header(self):
        """Test: Header-Format wird beibehalten"""
        bridge = LucaMeshBridge()

        block = InfoBlock(
            content="Test content",
            block_type=BlockType.CONNECTION,
            sentence_count=1,
            has_next_preview=False,
        )

        compressed = bridge._compress_block_for_mesh(block, 2, 4)

        # Check header format
        assert compressed.startswith("[LUCA]")
        assert "[3/4]" in compressed  # Index+1
        assert "[C]" in compressed  # Connection


class TestInfoBlockMeshIntegration:
    """Tests für Integration zwischen Info-Blocks und Mesh"""

    def test_process_query_generates_blocks(self):
        """Test: Query-Verarbeitung generiert Info-Blocks"""
        bridge = LucaMeshBridge()

        blocks = bridge.process_query_via_mesh("Was ist LUCA?")

        assert blocks is not None
        assert len(blocks) > 0
        # Should have Foundation + Building + Connection
        assert len(blocks) >= 3

    def test_blocks_have_correct_types(self):
        """Test: Generierte Blocks haben korrekte Types"""
        bridge = LucaMeshBridge()

        blocks = bridge.process_query_via_mesh("Test Query")

        # First should be Foundation
        assert blocks[0].block_type == BlockType.FOUNDATION
        # Last should be Connection
        assert blocks[-1].block_type == BlockType.CONNECTION

    def test_bridge_stats(self):
        """Test: Bridge-Statistiken funktionieren"""
        bridge = LucaMeshBridge()

        stats = bridge.get_bridge_stats()

        assert stats is not None
        assert "info_block_engine" in stats
        assert "mesh_available" in stats
        assert stats["info_block_engine"] == "active"


class TestMeshOfflineMode:
    """Tests für Offline-Funktionalität"""

    def test_bridge_works_without_mesh(self):
        """Test: Bridge funktioniert auch ohne Mesh-Hardware"""
        # Simuliert Szenario ohne physische Hardware
        bridge = LucaMeshBridge()

        # Info-Block-Engine sollte funktionieren
        blocks = bridge.process_query_via_mesh("Test")

        assert blocks is not None
        assert len(blocks) > 0

    def test_lightweight_blocks_without_mesh(self):
        """Test: Lightweight Blocks können ohne Mesh erstellt werden"""
        bridge = LucaMeshBridge()

        block = bridge.create_lightweight_block(
            block_type=BlockType.BUILDING, content="Test content"
        )

        assert block is not None
        assert block.block_type == BlockType.BUILDING


# === PYTEST CONFIGURATION ===

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
