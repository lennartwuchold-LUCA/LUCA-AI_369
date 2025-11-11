"""
LUCA 369/370 - Progressive Disclosure Engine
Bekämpft Cognitive Overload durch schrittweise Information Delivery

Architekt: Lennart Wuchold
UX Expert: Kimi
Qualitätsstandard: 369/370

Kimi's Insight:
"Multiple information blocks presented simultaneously can overwhelm users
with attention difficulties. Progressive disclosure reduces cognitive load
while maintaining information completeness."
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from luca_369_370.core.info_block_engine import InfoBlock, BlockType


class UserState(Enum):
    """Aktueller kognitiver State des Users"""
    READY = "ready"              # Bereit für nächsten Block
    PAUSED = "paused"            # User hat Pause gewählt
    OVERWHELMED = "overwhelmed"  # Zu viele Infos zu schnell
    HYPERFOCUS = "hyperfocus"    # Will alles sofort


class DisclosureMode(Enum):
    """Wie schnell werden Blöcke angezeigt"""
    MANUAL = "manual"        # User klickt für jeden Block
    SEMI_AUTO = "semi_auto"  # Auto nach 5 Sekunden, kann pausieren
    AUTO = "auto"            # Automatisch durchlaufen


@dataclass
class ProgressiveState:
    """
    Kompletter State der Progressive Disclosure Session
    """
    current_block_index: int
    total_blocks: int
    user_state: UserState
    disclosure_mode: DisclosureMode
    time_spent_seconds: int
    blocks_revisited: List[int]  # Welche Blöcke wurden nochmal angeschaut

    @property
    def progress_percentage(self) -> float:
        """Fortschritt in Prozent"""
        if self.total_blocks == 0:
            return 0.0
        return (self.current_block_index / self.total_blocks) * 100

    @property
    def blocks_remaining(self) -> int:
        """Wie viele Blöcke noch übrig"""
        return self.total_blocks - self.current_block_index

    @property
    def estimated_time_remaining(self) -> int:
        """Geschätzte verbleibende Zeit in Sekunden"""
        # Durchschnittlich 15 Sekunden pro Block (3 Sätze à 5 Sek)
        return self.blocks_remaining * 15


class ProgressiveDisclosureEngine:
    """
    Core Engine für Progressive Information Disclosure

    Funktionen:
    - Zeigt Blöcke einzeln statt alle auf einmal
    - Trackt User-State und passt Tempo an
    - Gibt Time-Estimates
    - Erlaubt Vor/Zurück Navigation
    - Erkennt Cognitive Overload
    """

    def __init__(self, blocks: List[InfoBlock], mode: DisclosureMode = DisclosureMode.MANUAL):
        self.blocks = blocks
        self.state = ProgressiveState(
            current_block_index=0,
            total_blocks=len(blocks),
            user_state=UserState.READY,
            disclosure_mode=mode,
            time_spent_seconds=0,
            blocks_revisited=[]
        )

        # Cognitive Load Detection
        self.interaction_times = []  # Wie lange bei jedem Block
        self.pause_count = 0
        self.back_navigation_count = 0

    def get_current_display(self) -> Dict:
        """
        Gibt aktuellen Block + Metadaten für Display zurück

        Returns:
            Dict mit allem was UI braucht
        """
        if self.state.current_block_index >= len(self.blocks):
            return self._create_completion_display()

        current_block = self.blocks[self.state.current_block_index]

        return {
            'block': {
                'content': current_block.content,
                'type': current_block.block_type.value,
                'number': self.state.current_block_index + 1,
                'has_next_preview': current_block.has_next_preview,
                'next_hint': current_block.next_block_hint
            },
            'progress': {
                'current': self.state.current_block_index + 1,
                'total': self.state.total_blocks,
                'percentage': self.state.progress_percentage,
                'blocks_remaining': self.state.blocks_remaining
            },
            'timing': {
                'time_spent': self.state.time_spent_seconds,
                'estimated_remaining': self.state.estimated_time_remaining,
                'formatted_remaining': self._format_time(self.state.estimated_time_remaining)
            },
            'actions': self._get_available_actions(),
            'cognitive_state': {
                'user_state': self.state.user_state.value,
                'overload_detected': self._detect_cognitive_overload(),
                'recommendation': self._get_state_recommendation()
            }
        }

    def next_block(self) -> Dict:
        """
        Geht zum nächsten Block

        Returns:
            Neuer Display State
        """
        if self.state.current_block_index < len(self.blocks) - 1:
            self.state.current_block_index += 1
            self.state.user_state = UserState.READY

        return self.get_current_display()

    def previous_block(self) -> Dict:
        """
        Geht zum vorherigen Block zurück

        Trackt Navigation für Cognitive Load Detection
        """
        if self.state.current_block_index > 0:
            self.back_navigation_count += 1
            self.state.blocks_revisited.append(self.state.current_block_index)
            self.state.current_block_index -= 1

        return self.get_current_display()

    def pause(self) -> Dict:
        """User möchte Pause machen"""
        self.pause_count += 1
        self.state.user_state = UserState.PAUSED

        return {
            'message': '⏸️ Pause aktiv',
            'suggestion': 'Nimm dir Zeit. LUCA wartet auf dich. 💚',
            'resume_action': 'Bereit? [Weiter]',
            'progress_saved': True
        }

    def jump_to_block(self, block_index: int) -> Dict:
        """
        Springt zu spezifischem Block

        Für Advanced Users oder Review-Modus
        """
        if 0 <= block_index < len(self.blocks):
            self.state.current_block_index = block_index
            return self.get_current_display()
        else:
            return {'error': 'Block index out of range'}

    def request_more_detail(self) -> Dict:
        """
        User will mehr Details zum aktuellen Block

        TODO: Integration mit LLM für Detail-Expansion
        """
        current_block = self.blocks[self.state.current_block_index]

        return {
            'block_content': current_block.content,
            'detail_request': True,
            'message': 'Möchtest du mehr Details zu einem spezifischen Aspekt?',
            'options': self._extract_detail_options(current_block)
        }

    def _get_available_actions(self) -> List[Dict]:
        """
        Welche Actions sind gerade verfügbar

        Abhängig von Position und User State
        """
        actions = []

        # Weiter (wenn nicht am Ende)
        if self.state.current_block_index < len(self.blocks) - 1:
            actions.append({
                'label': 'Weiter →',
                'key': 'next',
                'hotkey': 'Enter',
                'primary': True
            })

        # Zurück (wenn nicht am Anfang)
        if self.state.current_block_index > 0:
            actions.append({
                'label': '← Zurück',
                'key': 'previous',
                'hotkey': 'Backspace',
                'primary': False
            })

        # Pause
        actions.append({
            'label': '⏸️ Pause',
            'key': 'pause',
            'hotkey': 'Space',
            'primary': False
        })

        # Mehr Details
        actions.append({
            'label': '🔍 Mehr Details',
            'key': 'detail',
            'hotkey': 'd',
            'primary': False
        })

        # Alle Blöcke (für Hyperfocus State)
        if self.state.user_state == UserState.HYPERFOCUS:
            actions.append({
                'label': '⚡ Alle Blöcke',
                'key': 'show_all',
                'hotkey': 'a',
                'primary': False
            })

        return actions

    def _detect_cognitive_overload(self) -> bool:
        """
        Erkennt ob User überfordert ist

        Signale:
        - Viele Pausen
        - Häufiges Zurück-Navigieren
        - Lange Zeit bei einzelnen Blöcken
        """
        # Zu viele Pausen
        if self.pause_count > 2:
            return True

        # Häufiges Zurück-Gehen
        if self.back_navigation_count > 3:
            return True

        # Zu lange bei einem Block
        if self.interaction_times:
            avg_time = sum(self.interaction_times) / len(self.interaction_times)
            if len(self.interaction_times) > 0 and self.interaction_times[-1] > avg_time * 2:
                return True

        return False

    def _get_state_recommendation(self) -> str:
        """
        Gibt Empfehlung basierend auf erkanntem State
        """
        if self._detect_cognitive_overload():
            return "💡 Tipp: Mach eine kurze Pause. Die Blöcke bleiben gespeichert."

        if self.state.user_state == UserState.HYPERFOCUS:
            return "⚡ Du bist im Flow! Möchtest du alle Blöcke auf einmal sehen?"

        if self.state.blocks_remaining == 1:
            return "🎯 Fast geschafft! Noch ein letzter Block."

        return "👍 Alles gut. Weiter wenn du bereit bist."

    def _format_time(self, seconds: int) -> str:
        """Formatiert Sekunden zu lesbarem String"""
        if seconds < 60:
            return f"{seconds}s"
        else:
            minutes = seconds // 60
            remaining_seconds = seconds % 60
            return f"{minutes}m {remaining_seconds}s"

    def _extract_detail_options(self, block: InfoBlock) -> List[str]:
        """
        Extrahiert mögliche Detail-Aspekte aus Block

        TODO: NLP-basierte Extraktion oder LLM-Integration
        """
        # Placeholder - später: semantische Analyse
        return [
            "Technische Details",
            "Praktisches Beispiel",
            "Verwandte Konzepte"
        ]

    def _create_completion_display(self) -> Dict:
        """
        Display wenn alle Blöcke durchlaufen wurden
        """
        return {
            'completed': True,
            'message': '✅ Alle Blöcke durchlaufen!',
            'stats': {
                'total_blocks': self.state.total_blocks,
                'time_spent': self._format_time(self.state.time_spent_seconds),
                'revisited_blocks': len(self.state.blocks_revisited),
                'pauses_taken': self.pause_count
            },
            'actions': [
                {'label': '🔄 Nochmal durchgehen', 'key': 'restart'},
                {'label': '💬 Neue Frage', 'key': 'new_query'},
                {'label': '📊 Session Summary', 'key': 'summary'}
            ],
            'quality_score': 369/370
        }

    def record_interaction_time(self, seconds: int):
        """
        Trackt wie lange User bei aktuellem Block war

        Für Cognitive Load Detection
        """
        self.interaction_times.append(seconds)
        self.state.time_spent_seconds += seconds

        # Detect Hyperfocus
        if len(self.interaction_times) >= 3:
            recent_avg = sum(self.interaction_times[-3:]) / 3
            if recent_avg < 10:  # Sehr schnell durch Blöcke
                self.state.user_state = UserState.HYPERFOCUS


class ProgressiveBlockFormatter:
    """
    Formatiert Progressive Disclosure für verschiedene Outputs
    """

    @staticmethod
    def format_for_cli(display_data: Dict) -> str:
        """
        Formatiert für Terminal/CLI Output
        """
        if display_data.get('completed'):
            return ProgressiveBlockFormatter._format_completion_cli(display_data)

        block = display_data['block']
        progress = display_data['progress']
        timing = display_data['timing']
        cognitive = display_data['cognitive_state']

        output = []

        # Header mit Progress
        output.append("=" * 70)
        output.append(f"🏛️ LUCA 369/370 - Progressive Disclosure")
        output.append(f"📊 Block {progress['current']}/{progress['total']} " +
                     f"({progress['percentage']:.0f}% | " +
                     f"⏱️ noch ~{timing['formatted_remaining']})")
        output.append("=" * 70)
        output.append("")

        # Block Type Icon
        type_icons = {
            'foundation': '🏛️',
            'building': '🔨',
            'connection': '🔗'
        }
        icon = type_icons.get(block['type'], '📦')

        # Block Content
        output.append(f"{icon} {block['type'].upper()} BLOCK")
        output.append("-" * 70)
        output.append(block['content'])
        output.append("")

        # Next Preview
        if block['has_next_preview'] and block['next_hint']:
            output.append(f"   → {block['next_hint']}")
            output.append("")

        # Cognitive State Feedback
        if cognitive['overload_detected']:
            output.append("⚠️  " + cognitive['recommendation'])
            output.append("")

        # Actions
        output.append("-" * 70)
        output.append("Verfügbare Aktionen:")
        for action in display_data['actions']:
            hotkey_info = f" [{action['hotkey']}]" if 'hotkey' in action else ""
            primary_mark = " ⭐" if action.get('primary') else ""
            output.append(f"  {action['label']}{hotkey_info}{primary_mark}")

        output.append("=" * 70)

        return "\n".join(output)

    @staticmethod
    def _format_completion_cli(data: Dict) -> str:
        """Formatiert Completion Screen für CLI"""
        output = []

        output.append("")
        output.append("=" * 70)
        output.append("🎉 " + data['message'])
        output.append("=" * 70)
        output.append("")

        stats = data['stats']
        output.append("📊 Session Statistik:")
        output.append(f"   Blöcke gelesen: {stats['total_blocks']}")
        output.append(f"   Zeit investiert: {stats['time_spent']}")
        output.append(f"   Blöcke wiederholt: {stats['revisited_blocks']}")
        output.append(f"   Pausen genommen: {stats['pauses_taken']}")
        output.append("")

        output.append(f"✅ Quality Score: {data['quality_score']:.4f}")
        output.append("")

        output.append("Nächste Schritte:")
        for action in data['actions']:
            output.append(f"  {action['label']}")

        output.append("=" * 70)

        return "\n".join(output)

    @staticmethod
    def format_for_web(display_data: Dict) -> Dict:
        """
        Formatiert für Web UI (JSON-ready)
        """
        return {
            'type': 'progressive_disclosure',
            'version': '369/370',
            'data': display_data,
            'ui_hints': {
                'show_progress_bar': True,
                'enable_keyboard_nav': True,
                'highlight_primary_action': True,
                'show_time_estimate': True
            }
        }
