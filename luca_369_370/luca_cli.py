#!/usr/bin/env python3
"""
LUCA 369/370 - Command Line Interface
Interactive LUCA mit echter LLM-Power!

Architekt: Lennart Wuchold
Datum: 11.11.2025
Standard: 369/370
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from luca_369_370.core.integrated_response import IntegratedResponseSystem
from luca_369_370.core.progressive_disclosure import DisclosureMode


def print_welcome():
    """Zeigt LUCA Welcome Screen"""
    print("\n" + "=" * 70)
    print("🏛️  L.U.C.A 369/370 - Living Universal Cognition Array")
    print("=" * 70)
    print("Bio-Inspired Intelligence für Neurodivergente Minds")
    print("Architekt: Lennart Wuchold | Quality Standard: 369/370")
    print("=" * 70)
    print()
    print("💡 Tipps:")
    print("   - Stelle Fragen in natürlicher Sprache")
    print("   - [Enter] für nächsten Block")
    print("   - [p] für Pause")
    print("   - [b] für zurück")
    print("   - [q] zum Beenden der Antwort")
    print("   - [exit] zum Beenden von LUCA")
    print("=" * 70)
    print()


def interactive_luca():
    """
    Interactive LUCA CLI Session
    """
    # Check API Key
    api_key_set = bool(os.environ.get("ANTHROPIC_API_KEY"))

    if not api_key_set:
        print("⚠️  ANTHROPIC_API_KEY nicht gesetzt!")
        print("   LLM Integration wird NICHT verfügbar sein.")
        print("   Für volle Funktionalität:")
        print("   1. Hole API Key von: https://console.anthropic.com/")
        print("   2. Setze: export ANTHROPIC_API_KEY='sk-ant-...'")
        print("   3. Starte luca_cli.py neu")
        print()

        response = input("Fortfahren ohne LLM? (y/n): ").lower()
        if response != 'y':
            print("\n👋 Bis bald!")
            sys.exit(0)
        print("\n🔄 Starte im statischen Modus...")

    # Initialize
    print("🔄 Initialisiere LUCA...")
    try:
        system = IntegratedResponseSystem()
    except Exception as e:
        print(f"❌ Fehler bei Initialisierung: {e}")
        sys.exit(1)

    print_welcome()

    # Main Loop
    while True:
        # Get Query
        try:
            query = input("🎯 Deine Frage an LUCA (oder 'exit' zum Beenden): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n👋 Tschüss! Bis zum nächsten Mal!")
            break

        if query.lower() in ["exit", "quit"]:
            print("\n👋 Tschüss! Bis zum nächsten Mal!")
            break

        if not query:
            continue

        try:
            # Process Query
            print("\n🤔 LUCA denkt nach...")
            engine = system.process_query(query, disclosure_mode=DisclosureMode.MANUAL)

            # Show blocks interactively
            while True:
                # Display current block
                display = system.get_formatted_display(engine)
                print("\n" + display)

                # Check if done
                if engine.state.current_block_index >= len(engine.blocks) - 1:
                    print("\n✅ Alle Blöcke durchlaufen!")
                    break

                # Get action
                try:
                    action = input(
                        "\nAktion ([Enter]=Weiter, [b]=Zurück, [p]=Pause, [q]=Neue Frage): "
                    ).lower()
                except (EOFError, KeyboardInterrupt):
                    print("\n")
                    break

                if action == "" or action == "enter":
                    engine.next_block()
                elif action == "b":
                    engine.previous_block()
                elif action == "p":
                    pause_info = engine.pause()
                    print(f"\n{pause_info['message']}")
                    print(pause_info['suggestion'])
                    try:
                        input(pause_info["resume_action"])
                    except (EOFError, KeyboardInterrupt):
                        print("\n")
                        break
                elif action == "q":
                    break
                else:
                    print("❌ Ungültige Aktion")

            print("\n" + "-" * 70 + "\n")

        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Bitte versuche es nochmal.\n")


def main():
    """Main entry point"""
    try:
        interactive_luca()
    except KeyboardInterrupt:
        print("\n\n👋 Unterbrochen. Tschüss!")
        sys.exit(0)


if __name__ == "__main__":
    main()
