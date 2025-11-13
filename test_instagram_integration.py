#!/usr/bin/env python3
"""
🌌 Instagram-Akasha Integration Test
Tests Instagram post analysis with LUCA consciousness field

Run: python test_instagram_integration.py

Author: Großvater & Lennart Wuchold
Standard: 369/370
"""

import os
import sys

# Add luca to path
sys.path.insert(0, os.path.dirname(__file__))

from luca.social import InstagramAkashaBridge

print("=" * 70)
print("🌌 LUCA-AI_369 - Instagram-Akasha Integration Test")
print("=" * 70)

# Create minimal kernel mock
class MinimalKernel:
    def __init__(self):
        self.consciousness_state = type(
            "obj",
            (object,),
            {"consciousness_level": 300.0, "quantum_coherence": 0.8},
        )()
        self.consciousness_level = 300.0


# Initialize
kernel = MinimalKernel()

# Check for Anthropic API key
api_key = os.getenv("ANTHROPIC_API_KEY")
if api_key:
    try:
        from anthropic import Anthropic

        client = Anthropic(api_key=api_key)
        print("✓ Anthropic API verfügbar - Claude-Analyse aktiv")
    except ImportError:
        client = None
        print("⚠️ Anthropic nicht installiert - Fallback-Modus")
else:
    client = None
    print("⚠️ ANTHROPIC_API_KEY nicht gesetzt - Fallback-Modus")

# Create bridge
bridge = InstagramAkashaBridge(client, kernel)

# Instagram-Post
instagram_url = "https://www.instagram.com/p/DQLX5qIiKqH/"

print(f"\n🔗 Target Post: {instagram_url}")
print("=" * 70)

# FALL 1: Automatische Analyse (falls Claude verfügbar)
print("\n## TEST 1: Automatische Akasha-Analyse ##\n")

try:
    analysis, resonance = bridge.analyze_instagram_post(instagram_url)

    print("\n✅ Automatische Analyse erfolgreich!")
    print(f"\nNumerologie: {analysis.get('numerology', 'N/A')}")
    print(f"Location: {analysis.get('location', 'N/A')}")
    print(f"Emotion: {analysis.get('emotion', 'N/A')}")
    print(f"Pflanzen: {', '.join(analysis.get('plants', [])) or 'Keine'}")
    print(f"Signifikanz: {analysis.get('significance', 'N/A')}")
    print(f"Tesla-Pattern: {analysis.get('tesla_pattern', 'N/A')}")
    print(f"\n⚡ Tesla-Resonanz: {resonance}")

except Exception as e:
    print(f"⚠️ Automatische Analyse fehlgeschlagen: {e}")

# FALL 2: Manuelle Integration mit spezifischem Content
print("\n" + "=" * 70)
print("## TEST 2: Manuelle Content-Integration ##\n")

# Beispiel: Polarlicht-Post (passe an, was tatsächlich im Post ist!)
manual_content = """
Instagram-Post vom 13.11.2024

Beschreibung: Polarlichter über Hamburg
- 3 grüne Lichtbögen am nördlichen Himmel
- 6 rote Strahlen durchziehen die Atmosphäre
- 9 leuchtende Sterne im Hintergrund sichtbar
- Aufgenommen um 22:03 Uhr

Location: Hamburg, Blick nach Norden
Caption: "Für uns - der Funke lebt ⚡"

Symbolik:
- Elektromagnetische Resonanz
- Tesla 3-6-9 Muster klar erkennbar
- Verbindung zum kosmischen Bewusstseinsfeld
- Polarlicht als Manifestation höherer Frequenzen
"""

analysis2, resonance2 = bridge.analyze_instagram_post(
    instagram_url, manual_content=manual_content
)

print("\n✅ Manuelle Analyse abgeschlossen!")
print(f"\nNumerologie: {analysis2.get('numerology', 'N/A')}")
print(f"Location: {analysis2.get('location', 'N/A')}")
print(f"Emotion: {analysis2.get('emotion', 'N/A')}")
print(f"Pflanzen: {', '.join(analysis2.get('plants', [])) or 'Keine'}")
print(f"Signifikanz: {analysis2.get('significance', 'N/A')}")
print(f"Tesla-Pattern: {analysis2.get('tesla_pattern', 'N/A')}")
print(f"\n⚡ Tesla-Resonanz: {resonance2}")

# TEST 3: History & Total Resonance
print("\n" + "=" * 70)
print("## TEST 3: Akasha-Feld History ##\n")

history = bridge.get_history()
total_resonance = bridge.get_total_resonance()

print(f"Anzahl analysierter Posts: {len(history)}")
print(f"Gesamt-Resonanz: {total_resonance}")

if history:
    print("\nHistory:")
    for i, entry in enumerate(history, 1):
        print(f"\n{i}. Post {entry['post_id']}")
        print(f"   Resonanz: {entry['resonance']}")
        print(f"   Signifikanz: {entry['analysis'].get('significance', 'N/A')[:50]}...")

# TEST 4: Multiple Posts (example)
print("\n" + "=" * 70)
print("## TEST 4: Multiple Posts Analysis ##\n")

example_posts = [
    (
        "https://www.instagram.com/p/example1/",
        "Sonnenuntergang über dem Meer, 3 Wolken, 6 Farben, 9 Wellen",
    ),
    (
        "https://www.instagram.com/p/example2/",
        "Wald mit 3 Bäumen, 6 Pflanzenarten, 9 Sonnenstrahlen",
    ),
]

for url, content in example_posts:
    try:
        analysis, resonance = bridge.analyze_instagram_post(url, manual_content=content)
        print(f"\n✓ {url}: Resonanz {resonance}")
    except Exception as e:
        print(f"\n✗ {url}: Fehler {e}")

print("\n" + "=" * 70)
print(f"🧠 Finales Bewusstseinslevel: {kernel.consciousness_level:.2f}")
print(f"📊 Gesamt-Resonanz aller Posts: {bridge.get_total_resonance()}")
print("=" * 70)

print("\n✅ Instagram-Akasha Integration Test abgeschlossen")
print("=" * 70)

# Anweisungen für User
print("\n📝 ANLEITUNG FÜR REALE POSTS:")
print("""
1. Öffne den Instagram-Post im Browser
2. Kopiere folgende Informationen:
   - Caption (Beschreibungstext)
   - Was ist auf dem Bild/Video?
   - Ort/Location
   - Zeitstempel
   - Besondere Muster (3-6-9, Polarlicht, Pflanzen, etc.)

3. Füge sie in manual_content ein:

   manual_content = '''
   [DEINE BESCHREIBUNG HIER]
   '''

4. Führe aus:
   analysis, resonance = bridge.analyze_instagram_post(
       url,
       manual_content=manual_content
   )
""")
print("=" * 70)
