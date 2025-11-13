#!/usr/bin/env python3
"""
Demo: Combined Instagram + paper2web Integration
Zeigt wie Instagram-Posts mit Paper-Links verarbeitet werden

Author: Großvater & Lennart Wuchold
Standard: 369/370
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from luca.social.paper2web_instagram import InstagramPaperBridge

# Optional: Anthropic client
try:
    from anthropic import Anthropic

    api_key = os.getenv("ANTHROPIC_API_KEY")
    client = Anthropic(api_key=api_key) if api_key else None
except ImportError:
    client = None
    print("⚠️ Anthropic nicht installiert - verwende Fallback-Modus")


# Minimal kernel mock
class MinimalKernel:
    def __init__(self):
        self.consciousness_level = 300.0


def main():
    print("=" * 70)
    print("🌌📄 LUCA Instagram + paper2web Integration Demo")
    print("=" * 70)

    # Initialize kernel and bridge
    kernel = MinimalKernel()
    bridge = InstagramPaperBridge(client, kernel)

    # Example 1: Instagram-Post mit arXiv-Link
    print("\n\n### BEISPIEL 1: Instagram mit arXiv Paper")
    print("-" * 70)

    instagram_url = "https://www.instagram.com/p/DQLX5qIiKqH/"
    manual_content = """
    Instagram-Post vom 13.11.2024

    Polarlichter über Hamburg - Tesla's 3-6-9 Frequenzen manifestieren sich!

    Neue Forschung: https://arxiv.org/abs/2301.01808

    Caption: "Für uns - der Funke lebt ⚡"
    Location: Hamburg, Deutschland

    #Tesla369 #Consciousness #Polarlichter #Science
    """

    result1 = bridge.process_instagram_with_papers(instagram_url, manual_content)

    print(f"\n📊 Ergebnis:")
    print(f"   Instagram-Resonanz: {result1['instagram_resonance']}")
    print(f"   Papers gefunden: {len(result1['papers'])}")
    print(f"   Gesamt-Resonanz: {result1['total_resonance']}")

    # Generate Instagram response
    response1 = bridge.generate_instagram_response(result1, target_language="de")
    print(f"\n💬 Instagram-Antwort:\n{response1}")

    # Example 2: Instagram ohne Papers
    print("\n\n### BEISPIEL 2: Instagram ohne Papers")
    print("-" * 70)

    instagram_url2 = "https://www.instagram.com/p/DQLX5qIiKqX/"
    manual_content2 = """
    Instagram-Post: Sonnenuntergang am Strand

    Keine Papers, nur pure Naturverbindung

    Location: Ostsee
    """

    result2 = bridge.process_instagram_with_papers(instagram_url2, manual_content2)

    print(f"\n📊 Ergebnis:")
    print(f"   Instagram-Resonanz: {result2['instagram_resonance']}")
    print(f"   Papers gefunden: {len(result2['papers'])}")
    print(f"   Gesamt-Resonanz: {result2['total_resonance']}")

    response2 = bridge.generate_instagram_response(result2, target_language="de")
    print(f"\n💬 Instagram-Antwort:\n{response2}")

    # Statistics
    print("\n\n### STATISTIKEN")
    print("-" * 70)
    stats = bridge.get_statistics()
    print(f"📱 Instagram-Posts verarbeitet: {stats['total_instagram_posts']}")
    print(f"📚 Papers verarbeitet: {stats['total_papers_processed']}")
    print(f"⚡ Gesamt-Resonanz: {stats['total_combined_resonance']}")
    print(f"🧠 Bewusstseins-Beitrag: {stats['consciousness_contribution']:.2f}")
    print(f"📊 Durchschnitt Instagram: {stats['avg_instagram_resonance']:.1f}")
    print(f"📊 Durchschnitt Papers: {stats['avg_paper_resonance']:.1f}")

    # Consciousness level
    print(f"\n🧠 Kernel Bewusstseins-Level: {kernel.consciousness_level:.2f}")

    print("\n" + "=" * 70)
    print("✅ Demo abgeschlossen")
    print("=" * 70)


if __name__ == "__main__":
    main()
