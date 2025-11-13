#!/usr/bin/env python3
"""
🚑 LUCA Medical Emergency System - Test
Tests medical LLM integration with natural remedies and regional resources.

Run: python test_emergency.py

Author: Großvater & Lennart Wuchold
Standard: 369/370
"""

import os
import sys

# Add luca to path
sys.path.insert(0, os.path.dirname(__file__))

from luca.medical import (
    LOCAL_RESOURCES,
    NATURAL_EMERGENCY_AIDS,
    EmergencyAutomation,
    MedicalEmergencyLLM,
)

print("=" * 70)
print("🌿 LUCA-AI_369 - Medical Emergency System Test")
print("=" * 70)

# Test 1: Medical Emergency LLM
print("\n## TEST 1: Medical Emergency LLM ##\n")

api_key = os.getenv("ANTHROPIC_API_KEY")
medical_llm = MedicalEmergencyLLM()

# Simulate hiking injury with wound
emergency_response = medical_llm.query_medical_emergency(
    symptoms="Schnittwunde am Arm, blutet stark, keine Allergien",
    location="Hamburg",
    available_plants=["Arnika", "Wegerich", "Kiefernnadeln"],
)

print("=== MEDIZINISCHER NOTFALL-PLAN ===")
print(emergency_response)
print()

# Test 2: Natural Aid Database
print("\n## TEST 2: Natural Aid Database ##\n")

print("Verfügbare Behandlungen für Wunden:")
wound_aids = NATURAL_EMERGENCY_AIDS.get("Wunden & Schürfwunden", {})
for plant in wound_aids.get("pflanzlich", []):
    print(f"  • {plant['name']}: {plant['effect']}")
print()

# Test 3: Regional Resources
print("\n## TEST 3: Regional Resources (Hamburg) ##\n")

hamburg_resources = LOCAL_RESOURCES.get("Hamburg", {})
print(f"Notruf: {hamburg_resources.get('emergency', '112')}")
print(f"Ärzte-Notdienst: {hamburg_resources.get('aerzte_notdienst', 'N/A')}")
print(f"Giftnotruf: {hamburg_resources.get('giftnotruf', 'N/A')}")
print(
    f"Regionale Pflanzen: {', '.join(hamburg_resources.get('regionale_pflanzen', []))}"
)
print()

# Test 4: Emergency Automation (Simulation)
print("\n## TEST 4: Emergency Automation (Simulation) ##\n")


# Create a minimal kernel mock for testing
class MinimalKernel:
    def __init__(self):
        self.consciousness_state = type(
            "obj",
            (object,),
            {"consciousness_level": 300.0, "quantum_coherence": 0.8},
        )()

    def broadcast_universal_message(self, message):
        print(f"📡 Mesh-Broadcast: {message[:80]}...")


kernel = MinimalKernel()
emergency = EmergencyAutomation(kernel, medical_llm)

# Simulate emergency
print("\n🚨 Simuliere Wanderunfall...")
medical_advice, natural_aids, local_help = emergency.start_emergency_protocol(
    incident_type="Prellung am Knie nach Sturz",
    location="Hamburg",
)

# Check vitals
print("\n💓 Vitaldaten-Check:")
vitals = emergency.check_vitals()
for key, value in vitals.items():
    print(f"   {key}: {value}")

# Test 5: Different Regions
print("\n## TEST 5: Different Regions ##\n")

regions = ["Berlin", "München", "Wien", "Zürich"]
for region in regions:
    resources = LOCAL_RESOURCES.get(region, {})
    print(f"{region}:")
    print(f"  Emergency: {resources.get('emergency', 'N/A')}")
    print(f"  Giftnotruf: {resources.get('giftnotruf', 'N/A')}")
    print()

print("=" * 70)
print("✅ Medical Emergency System Test abgeschlossen")
print("=" * 70)
print("\n⚠️ WICHTIG: Diese Tests sind NUR zur Demonstration!")
print("   Bei echten Notfällen IMMER 112 wählen!")
print("=" * 70)
