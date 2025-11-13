"""
LUCA 369/370 - Progressive Disclosure Tests
"""

import pytest

from luca.core.info_block_engine import BlockType, InfoBlock
from luca.core.progressive_disclosure import (
    DisclosureMode,
    ProgressiveDisclosureEngine,
    UserState,
)


class TestProgressiveDisclosureEngine:
    """Tests für Progressive Disclosure Engine"""

    def create_test_blocks(self) -> list:
        """Helper: Erstellt Test-Blöcke"""
        return [
            InfoBlock("Block 1", BlockType.FOUNDATION, 2),
            InfoBlock("Block 2", BlockType.BUILDING, 2),
            InfoBlock("Block 3", BlockType.CONNECTION, 2),
        ]

    def test_engine_initialization(self):
        """Test: Engine initialisiert korrekt"""
        blocks = self.create_test_blocks()
        engine = ProgressiveDisclosureEngine(blocks)

        assert engine.state.current_block_index == 0
        assert engine.state.total_blocks == 3
        assert engine.state.user_state == UserState.READY

    def test_next_block_navigation(self):
        """Test: Vorwärts-Navigation funktioniert"""
        blocks = self.create_test_blocks()
        engine = ProgressiveDisclosureEngine(blocks)

        # Start bei Block 0
        assert engine.state.current_block_index == 0

        # Gehe zu Block 1
        engine.next_block()
        assert engine.state.current_block_index == 1

        # Gehe zu Block 2
        engine.next_block()
        assert engine.state.current_block_index == 2

        # Versuche über Ende hinaus
        engine.next_block()
        assert engine.state.current_block_index == 2  # Bleibt bei letztem

    def test_previous_block_navigation(self):
        """Test: Rückwärts-Navigation funktioniert"""
        blocks = self.create_test_blocks()
        engine = ProgressiveDisclosureEngine(blocks)

        # Gehe vorwärts
        engine.next_block()
        engine.next_block()
        assert engine.state.current_block_index == 2

        # Gehe zurück
        engine.previous_block()
        assert engine.state.current_block_index == 1
        assert engine.back_navigation_count == 1

    def test_progress_calculation(self):
        """Test: Progress wird korrekt berechnet"""
        blocks = self.create_test_blocks()
        engine = ProgressiveDisclosureEngine(blocks)

        # Bei Block 0
        assert engine.state.progress_percentage == 0.0
        assert engine.state.blocks_remaining == 3

        # Bei Block 1
        engine.next_block()
        assert engine.state.progress_percentage == pytest.approx(33.33, 0.1)
        assert engine.state.blocks_remaining == 2

        # Bei Block 2
        engine.next_block()
        assert engine.state.progress_percentage == pytest.approx(66.66, 0.1)
        assert engine.state.blocks_remaining == 1

    def test_time_estimation(self):
        """Test: Zeitschätzung ist korrekt"""
        blocks = self.create_test_blocks()
        engine = ProgressiveDisclosureEngine(blocks)

        # 3 Blöcke * 15 Sek = 45 Sek
        assert engine.state.estimated_time_remaining == 45

        engine.next_block()
        # 2 Blöcke * 15 Sek = 30 Sek
        assert engine.state.estimated_time_remaining == 30

    def test_pause_functionality(self):
        """Test: Pause funktioniert"""
        blocks = self.create_test_blocks()
        engine = ProgressiveDisclosureEngine(blocks)

        pause_result = engine.pause()

        assert engine.state.user_state == UserState.PAUSED
        assert engine.pause_count == 1
        assert pause_result["progress_saved"] == True

    def test_cognitive_overload_detection(self):
        """Test: Cognitive Overload wird erkannt"""
        blocks = self.create_test_blocks()
        engine = ProgressiveDisclosureEngine(blocks)

        # Simuliere zu viele Pausen
        engine.pause()
        engine.pause()
        engine.pause()

        assert engine._detect_cognitive_overload() == True

    def test_hyperfocus_detection(self):
        """Test: Hyperfocus wird erkannt"""
        blocks = self.create_test_blocks()
        engine = ProgressiveDisclosureEngine(blocks)

        # Simuliere sehr schnelle Interaktionen
        engine.record_interaction_time(5)
        engine.record_interaction_time(6)
        engine.record_interaction_time(5)

        assert engine.state.user_state == UserState.HYPERFOCUS

    def test_display_data_structure(self):
        """Test: Display Data hat korrekte Struktur"""
        blocks = self.create_test_blocks()
        engine = ProgressiveDisclosureEngine(blocks)

        display = engine.get_current_display()

        assert "block" in display
        assert "progress" in display
        assert "timing" in display
        assert "actions" in display
        assert "cognitive_state" in display

        # Check sub-structures
        assert "content" in display["block"]
        assert "current" in display["progress"]
        assert "estimated_remaining" in display["timing"]

    def test_completion_state(self):
        """Test: Completion State wird korrekt erreicht"""
        blocks = self.create_test_blocks()
        engine = ProgressiveDisclosureEngine(blocks)

        # Gehe durch alle Blöcke
        # Block 0 -> Block 1
        engine.next_block()
        # Block 1 -> Block 2 (last block)
        engine.next_block()

        # We're now at the last block (index 2)
        # To see completion, we need to manually set to past the end
        engine.state.current_block_index = len(blocks)

        display = engine.get_current_display()

        assert display.get("completed") == True
        assert "stats" in display
        assert display["stats"]["total_blocks"] == 3

    def test_jump_to_block(self):
        """Test: Jump to specific block works"""
        blocks = self.create_test_blocks()
        engine = ProgressiveDisclosureEngine(blocks)

        # Jump to block 2
        result = engine.jump_to_block(2)
        assert engine.state.current_block_index == 2
        assert "block" in result

        # Try invalid jump
        result = engine.jump_to_block(10)
        assert "error" in result

    def test_request_more_detail(self):
        """Test: Request more detail functionality"""
        blocks = self.create_test_blocks()
        engine = ProgressiveDisclosureEngine(blocks)

        detail_result = engine.request_more_detail()

        assert "detail_request" in detail_result
        assert detail_result["detail_request"] == True
        assert "options" in detail_result
        assert len(detail_result["options"]) > 0

    def test_interaction_time_tracking(self):
        """Test: Interaction time is tracked correctly"""
        blocks = self.create_test_blocks()
        engine = ProgressiveDisclosureEngine(blocks)

        engine.record_interaction_time(10)
        engine.record_interaction_time(15)

        assert len(engine.interaction_times) == 2
        assert engine.state.time_spent_seconds == 25

    def test_blocks_revisited_tracking(self):
        """Test: Blocks revisited are tracked"""
        blocks = self.create_test_blocks()
        engine = ProgressiveDisclosureEngine(blocks)

        engine.next_block()
        engine.next_block()
        engine.previous_block()

        assert len(engine.state.blocks_revisited) == 1
        assert 2 in engine.state.blocks_revisited

    def test_available_actions_at_start(self):
        """Test: Available actions at start are correct"""
        blocks = self.create_test_blocks()
        engine = ProgressiveDisclosureEngine(blocks)

        display = engine.get_current_display()
        actions = display["actions"]

        # Should have next, pause, detail but not previous
        action_keys = [a["key"] for a in actions]
        assert "next" in action_keys
        assert "pause" in action_keys
        assert "detail" in action_keys
        assert "previous" not in action_keys

    def test_available_actions_at_middle(self):
        """Test: Available actions in middle include both nav"""
        blocks = self.create_test_blocks()
        engine = ProgressiveDisclosureEngine(blocks)
        engine.next_block()

        display = engine.get_current_display()
        actions = display["actions"]

        action_keys = [a["key"] for a in actions]
        assert "next" in action_keys
        assert "previous" in action_keys

    def test_hyperfocus_adds_show_all_action(self):
        """Test: Hyperfocus state adds show_all action"""
        blocks = self.create_test_blocks()
        engine = ProgressiveDisclosureEngine(blocks)

        # Trigger hyperfocus
        engine.record_interaction_time(5)
        engine.record_interaction_time(6)
        engine.record_interaction_time(5)

        display = engine.get_current_display()
        actions = display["actions"]
        action_keys = [a["key"] for a in actions]

        assert "show_all" in action_keys


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
