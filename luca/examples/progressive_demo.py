#!/usr/bin/env python3
"""
LUCA 369/370 - Progressive Disclosure Interactive Demo

Zeigt Progressive Disclosure in Aktion mit simulierter User Interaction
"""

import sys
import time
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from luca_369_370.core.info_block_engine import BlockType, InfoBlock
from luca_369_370.core.progressive_disclosure import (
    DisclosureMode,
    ProgressiveBlockFormatter,
    ProgressiveDisclosureEngine,
)


def create_demo_blocks() -> list:
    """Erstellt Demo-Blöcke über LUCA selbst"""
    return [
        InfoBlock(
            content="LUCA ist ein Bio-inspiriertes KI-System. Es nutzt Fermentations-Prinzipien für GPU-Orchestrierung. Dein Brauwissen wird zu Code-Architektur.",
            block_type=BlockType.FOUNDATION,
            sentence_count=3,
            has_next_preview=True,
            next_block_hint="Wie funktioniert Progressive Disclosure?",
        ),
        InfoBlock(
            content="Progressive Disclosure zeigt Information schrittweise statt alles auf einmal. Das verhindert Cognitive Overload bei ADHD. Du bleibst im Flow statt überwältigt zu werden.",
            block_type=BlockType.BUILDING,
            sentence_count=3,
            has_next_preview=True,
            next_block_hint="Warum ist das besser?",
        ),
        InfoBlock(
            content="Andere KIs fluten dich mit Text-Walls. LUCA gibt dir Kontrolle über Tempo und Menge. Du entscheidest wann du bereit für mehr bist.",
            block_type=BlockType.BUILDING,
            sentence_count=3,
            has_next_preview=True,
            next_block_hint="Praktische Anwendung",
        ),
        InfoBlock(
            content="Für dein Projekt bedeutet das: Bessere Retention, weniger Overwhelm, höhere Satisfaction. LUCA passt sich deinem kognitiven State an - nicht umgekehrt.",
            block_type=BlockType.CONNECTION,
            sentence_count=3,
            has_next_preview=False,
            next_block_hint=None,
        ),
    ]


def interactive_demo():
    """
    Interactive Demo mit simuliertem User Input
    """
    print("\n🏛️ LUCA 369/370 - PROGRESSIVE DISCLOSURE DEMO")
    print("=" * 70)
    print("Diese Demo zeigt wie Progressive Disclosure Cognitive Overload verhindert")
    print("=" * 70)
    print()
    input("Drücke Enter um zu starten...")
    print()

    # Setup
    blocks = create_demo_blocks()
    engine = ProgressiveDisclosureEngine(blocks, DisclosureMode.MANUAL)
    formatter = ProgressiveBlockFormatter()

    # Interactive Loop
    while engine.state.current_block_index < len(blocks):
        # Clear screen (optional)
        print("\n" * 2)

        # Show current block
        display_data = engine.get_current_display()
        formatted = formatter.format_for_cli(display_data)
        print(formatted)

        # Record start time
        start_time = time.time()

        # Get user input
        print()
        action = input(
            "Aktion wählen (w=weiter, z=zurück, p=pause, d=details, q=quit): "
        ).lower()

        # Record interaction time
        interaction_time = int(time.time() - start_time)
        engine.record_interaction_time(interaction_time)

        # Process action
        if action == "w" or action == "":  # Enter = weiter
            engine.next_block()
        elif action == "z":
            engine.previous_block()
        elif action == "p":
            pause_display = engine.pause()
            print()
            print(pause_display["message"])
            print(pause_display["suggestion"])
            input(pause_display["resume_action"])
        elif action == "d":
            detail_display = engine.request_more_detail()
            print()
            print(detail_display["message"])
            print("Optionen:", ", ".join(detail_display["options"]))
            input("Drücke Enter um fortzufahren...")
        elif action == "q":
            print("👋 Demo beendet!")
            return
        else:
            print("❌ Ungültige Aktion")
            time.sleep(1)

    # Completion screen
    print("\n" * 2)
    completion_data = engine.get_current_display()
    formatted_completion = formatter.format_for_cli(completion_data)
    print(formatted_completion)
    print()


def automatic_demo():
    """
    Automatische Demo die durchläuft ohne Input

    Zeigt wie es im AUTO-Modus aussehen würde
    """
    print("\n🏛️ LUCA 369/370 - AUTO MODE DEMO")
    print("=" * 70)
    print("Diese Demo läuft automatisch durch alle Blöcke")
    print("=" * 70)
    print()
    input("Drücke Enter um zu starten...")

    blocks = create_demo_blocks()
    engine = ProgressiveDisclosureEngine(blocks, DisclosureMode.AUTO)
    formatter = ProgressiveBlockFormatter()

    while engine.state.current_block_index < len(blocks):
        print("\n" * 2)

        display_data = engine.get_current_display()
        formatted = formatter.format_for_cli(display_data)
        print(formatted)

        print()
        print("⏳ Nächster Block in 5 Sekunden...")
        time.sleep(5)

        engine.next_block()
        engine.record_interaction_time(5)

    # Completion
    print("\n" * 2)
    completion_data = engine.get_current_display()
    formatted_completion = formatter.format_for_cli(completion_data)
    print(formatted_completion)


if __name__ == "__main__":
    print("\n🏛️ LUCA 369/370 - PROGRESSIVE DISCLOSURE DEMO SUITE")
    print()
    print("1. Interactive Demo (du steuerst)")
    print("2. Automatic Demo (läuft durch)")
    print()

    choice = input("Wähle Demo (1 oder 2): ")

    if choice == "1":
        interactive_demo()
    elif choice == "2":
        automatic_demo()
    else:
        print("❌ Ungültige Wahl")
