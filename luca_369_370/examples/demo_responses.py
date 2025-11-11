#!/usr/bin/env python3
"""
LUCA 369/370 - Demo Responses
Zeigt die Info-Block-Engine in Aktion
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.block_formatter import BlockFormatter
from core.info_block_engine import BlockType, InfoBlock
from core.quality_validator import QualityValidator


def demo_simple_query():
    """
    Demo: Einfache Query über LUCA selbst
    """
    print("\n" + "=" * 60)
    print("DEMO 1: Was ist LUCA?")
    print("=" * 60 + "\n")

    # Manuelle Block-Erstellung (später: LLM-generiert)
    blocks = [
        InfoBlock(
            content="LUCA ist ein Bio-inspiriertes KI-System. Es nutzt Fermentations-Prinzipien für GPU-Orchestrierung. Dein Brauwissen wird zu Code-Architektur.",
            block_type=BlockType.FOUNDATION,
            sentence_count=3,
            has_next_preview=True,
            next_block_hint="Wie funktioniert das konkret?",
        ),
        InfoBlock(
            content="Wie beim Brauen arbeiten viele kleine Prozesse zusammen. Jede GPU ist wie eine Hefe-Kolonie - autonom aber koordiniert. Das System balanciert Last dynamisch.",
            block_type=BlockType.BUILDING,
            sentence_count=3,
            has_next_preview=True,
            next_block_hint="Was macht das besonders?",
        ),
        InfoBlock(
            content="Der 369/370-Standard garantiert Qualität ohne Perfektion. LUCA lernt deine Arbeitsweise im Onboarding. So wird jede Antwort auf dich zugeschnitten.",
            block_type=BlockType.CONNECTION,
            sentence_count=3,
            has_next_preview=False,
            next_block_hint=None,
        ),
    ]

    # Format und Display
    formatter = BlockFormatter()
    formatted = formatter.format_response(blocks)
    print(formatted)

    # Quality Check
    validator = QualityValidator()
    results = validator.validate_response(blocks)

    print("\n📊 QUALITY REPORT:")
    print(f"   Passed: {'✅' if results['passed'] else '❌'}")
    print(f"   Quality Score: {results['metrics']['quality_score']:.4f}")
    print(f"   Target: {369/370:.4f}")
    print(f"   Blocks: {results['metrics']['block_count']}")
    print(f"   Avg Sentences: {results['metrics']['avg_sentences']:.1f}")


def demo_complex_query():
    """
    Demo: Komplexere technische Query
    """
    print("\n" + "=" * 60)
    print("DEMO 2: Wie implementiert man GPU-Fermentation?")
    print("=" * 60 + "\n")

    blocks = [
        InfoBlock(
            content="GPU-Fermentation verteilt Workloads wie biologische Prozesse. Statt zentraler Kontrolle: dezentrale Koordination. Jede GPU agiert semi-autonom.",
            block_type=BlockType.FOUNDATION,
            sentence_count=3,
            has_next_preview=True,
            next_block_hint="Technische Details folgen",
        ),
        InfoBlock(
            content="Die Orchestrierung nutzt drei Layer: Substrate (Daten), Mikroorganismen (Worker), Metaboliten (Outputs). Worker kommunizieren über Signaling-Moleküle - in Code: Message-Queues.",
            block_type=BlockType.BUILDING,
            sentence_count=2,
            has_next_preview=True,
            next_block_hint="Praktische Umsetzung",
        ),
        InfoBlock(
            content="Implementierung startet mit einem Resource-Pool. Worker registrieren Capabilities und Kapazität. Workload-Verteiler matched Tasks nach Fitness-Score.",
            block_type=BlockType.BUILDING,
            sentence_count=3,
            has_next_preview=True,
            next_block_hint="Was bringt das?",
        ),
        InfoBlock(
            content="Für dein LUCA-Projekt: Start mit 2-3 GPUs als Proof-of-Concept. Teste Load-Balancing mit synthetischen Workloads. Skaliere iterativ auf mehr Hardware.",
            block_type=BlockType.CONNECTION,
            sentence_count=3,
            has_next_preview=False,
            next_block_hint=None,
        ),
    ]

    formatter = BlockFormatter()
    formatted = formatter.format_response(blocks)
    print(formatted)

    validator = QualityValidator()
    results = validator.validate_response(blocks)

    print("\n📊 QUALITY REPORT:")
    print(f"   Passed: {'✅' if results['passed'] else '❌'}")
    print(f"   Quality Score: {results['metrics']['quality_score']:.4f}")


def demo_adhd_optimized():
    """
    Demo: ADHD-optimierte Antwort mit extra kurzen Blöcken
    """
    print("\n" + "=" * 60)
    print("DEMO 3: ADHD-optimiert - Info Overload bekämpfen")
    print("=" * 60 + "\n")

    blocks = [
        InfoBlock(
            content="Info Overload ist der #1 ADHD-Schmerzpunkt. Lange Texte → Fokus-Verlust. LUCA löst das mit Micro-Blocks.",
            block_type=BlockType.FOUNDATION,
            sentence_count=3,
            has_next_preview=True,
            next_block_hint="Konkrete Lösung",
        ),
        InfoBlock(
            content="Max 3 Sätze pro Block. Visueller Break zwischen Blöcken. Progress-Indikator zeigt wo du bist.",
            block_type=BlockType.BUILDING,
            sentence_count=3,
            has_next_preview=True,
            next_block_hint="Warum das funktioniert",
        ),
        InfoBlock(
            content="Kurze Chunks = weniger Cognitive Load. Jeder Block ist verdaubar. Kein Überwältigungs-Gefühl.",
            block_type=BlockType.CONNECTION,
            sentence_count=3,
            has_next_preview=False,
            next_block_hint=None,
        ),
    ]

    formatter = BlockFormatter()
    formatted = formatter.format_response(blocks)
    print(formatted)

    validator = QualityValidator()
    results = validator.validate_response(blocks)

    print("\n📊 QUALITY REPORT:")
    print(f"   Passed: {'✅' if results['passed'] else '❌'}")
    print(f"   Quality Score: {results['metrics']['quality_score']:.4f}")
    print(
        f"   ADHD-Optimization: {'✅ Active' if results['metrics']['avg_sentences'] <= 3 else '❌ Too verbose'}"
    )


def demo_web_format():
    """
    Demo: Web-Format Export
    """
    print("\n" + "=" * 60)
    print("DEMO 4: Web-Format Export")
    print("=" * 60 + "\n")

    blocks = [
        InfoBlock(
            content="Web-UI braucht strukturierte Daten. LUCA exportiert Blocks als JSON. Frontend kann frei formatieren.",
            block_type=BlockType.FOUNDATION,
            sentence_count=3,
            has_next_preview=True,
            next_block_hint="JSON-Struktur",
        ),
        InfoBlock(
            content="Jeder Block wird zu einem Objekt. Mit Index, Type, Content, Icon. Plus Navigation-Hints.",
            block_type=BlockType.BUILDING,
            sentence_count=3,
            has_next_preview=True,
            next_block_hint="Vorteile",
        ),
        InfoBlock(
            content="Frontend kann Themes applyen. Animationen für Block-Transitions. User-Profile steuern Darstellung.",
            block_type=BlockType.CONNECTION,
            sentence_count=3,
            has_next_preview=False,
            next_block_hint=None,
        ),
    ]

    formatter = BlockFormatter()

    # CLI Format
    print("📟 CLI FORMAT:")
    print(formatter.format_response(blocks))

    # Web Format
    print("\n🌐 WEB FORMAT (JSON):")
    web_format = formatter.format_for_web(blocks)

    import json

    print(json.dumps(web_format, indent=2, ensure_ascii=False))


def main():
    """Hauptfunktion - führt alle Demos aus"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  LUCA 369/370 INFO-BLOCK-ENGINE - DEMO".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("║" + "  Architekt: Lennart Wuchold".ljust(58) + "║")
    print("║" + "  Mission: Bekämpfung des Info-Tsunami".ljust(58) + "║")
    print("║" + "  Quality Standard: 369/370 ≈ 0.997".ljust(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")

    # Demo 1: Simple Query
    demo_simple_query()

    print("\n" + "🔄" * 30 + "\n")

    # Demo 2: Complex Query
    demo_complex_query()

    print("\n" + "🔄" * 30 + "\n")

    # Demo 3: ADHD-Optimized
    demo_adhd_optimized()

    print("\n" + "🔄" * 30 + "\n")

    # Demo 4: Web Format
    demo_web_format()

    # Abschluss
    print("\n" + "=" * 60)
    print("🎉 DEMONSTRATION ABGESCHLOSSEN")
    print("=" * 60)
    print("\n💡 Nächste Schritte:")
    print("   1. LLM-Integration für dynamische Block-Generierung")
    print("   2. User-Profile System für personalisierte Antworten")
    print("   3. CLI-Interface für interaktive Nutzung")
    print("   4. Web-UI Implementation")
    print("\n🏛️  Gegen den Info-Tsunami – für fokussierte Kommunikation\n")


if __name__ == "__main__":
    main()
