"""
HACCP Checkpoint 3: Integration Completeness
Test that all LUCA 370 components integrate correctly

Critical Limit: All integration points function correctly
Priority: HIGH (validates system cohesion)
"""

import sys
import os
import traceback

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def test_integration(test_name: str, test_func) -> bool:
    """Test if an integration point works correctly"""
    try:
        test_func()
        print(f"✅ {test_name}: PASS")
        return True
    except Exception as e:
        print(f"❌ {test_name}: FAIL")
        print(f"   Error: {str(e)}")
        traceback.print_exc()
        return False

def run_checkpoint_3():
    """Run HACCP Checkpoint 3: Integration Completeness"""
    print("=" * 70)
    print("HACCP CHECKPOINT 3: INTEGRATION COMPLETENESS")
    print("=" * 70)
    print()

    results = []

    # Import all modules
    from backend.consciousness.tesla_layers import ConsciousnessEngine
    from backend.consciousness.universal_inclusion_network import UniversalInclusionNetwork, Entity
    from backend.consciousness.dmt_fingerprint import DMT_FingerprintExtractor, DMT_Fingerprint
    from backend.consciousness.meshtastic_crisis_backup import MeshtasticCrisisSystem, MeshtasticNode
    from backend.consciousness.luca_370_integration import LUCA_370_System, PersonalizedAI

    print("--- Core Integration Tests ---")

    # Test 1: LUCA_370_System creates all subsystems
    def test_luca_370_system_creation():
        luca = LUCA_370_System()
        assert hasattr(luca, 'universal_network'), "Missing universal_network"
        assert hasattr(luca, 'fingerprint_extractor'), "Missing fingerprint_extractor"
        assert hasattr(luca, 'crisis_system'), "Missing crisis_system"
        assert hasattr(luca, 'insights_db'), "Missing insights_db"
        assert isinstance(luca.universal_network, UniversalInclusionNetwork)
        assert isinstance(luca.fingerprint_extractor, DMT_FingerprintExtractor)
        assert isinstance(luca.crisis_system, MeshtasticCrisisSystem)

    results.append(test_integration(
        "LUCA_370_System creates all subsystems",
        test_luca_370_system_creation
    ))

    # Test 2: DMT_Fingerprint extraction workflow
    def test_dmt_fingerprint_extraction():
        extractor = DMT_FingerprintExtractor()
        biosensor_data = {
            'eeg': {'alpha_beta_ratio': 1.2, 'theta': 0.4, 'coherence': 0.6},
            'hrv': {'baseline': 65, 'rmssd': 55, 'variability': 0.7},
            'pci': {'emotional_spectrum': 0.6, 'regulation': 0.7},
            'phi': {'baseline': 0.4, 'integration': 0.5}
        }
        fingerprint = extractor.extract('test_user', biosensor_data, consent=True)
        assert isinstance(fingerprint, DMT_Fingerprint)
        assert fingerprint.user_id_hash is not None
        assert len(fingerprint.core) > 0
        assert len(fingerprint.middle) > 0
        assert len(fingerprint.outer) > 0
        assert 0.5 <= fingerprint.personal_phi <= 2.5

    results.append(test_integration(
        "DMT-Fingerprint extraction workflow",
        test_dmt_fingerprint_extraction
    ))

    # Test 3: DMT_Fingerprint integrates with UniversalInclusionNetwork
    def test_fingerprint_network_integration():
        network = UniversalInclusionNetwork()
        extractor = DMT_FingerprintExtractor()

        # Extract fingerprint
        biosensor_data = {
            'eeg': {'alpha_beta_ratio': 1.2},
            'hrv': {'baseline': 65},
            'phi': {'baseline': 0.4}
        }
        fingerprint = extractor.extract('test_user', biosensor_data, consent=True)

        # Add to network as entity
        entity = Entity(
            id=fingerprint.user_id_hash,
            name='TestUser',
            category=fingerprint.primary_category,
            state=0.5,
            biosensor_data={'eeg': 0.5, 'hrv': 0.65, 'phi': 0.4}
        )
        network.add_entity(entity, fingerprint.primary_category)

        # Verify entity was added
        assert network.total_entities > 0
        assert fingerprint.primary_category in network.nodes
        assert len(network.nodes[fingerprint.primary_category]) > 0

    results.append(test_integration(
        "DMT-Fingerprint integrates with UniversalInclusionNetwork",
        test_fingerprint_network_integration
    ))

    # Test 4: Meshtastic accepts DMT_Fingerprint
    def test_meshtastic_fingerprint_integration():
        mesh = MeshtasticCrisisSystem()

        # Add nodes
        node = MeshtasticNode("test_node_001")
        mesh.add_node(node)

        # Create fingerprint
        extractor = DMT_FingerprintExtractor()
        biosensor_data = {
            'eeg': {'alpha_beta_ratio': 1.2},
            'hrv': {'baseline': 65},
            'phi': {'baseline': 0.4}
        }
        fingerprint = extractor.extract('test_user', biosensor_data, consent=True)

        # Preserve via Meshtastic
        status = mesh.preserve_crisis_fingerprint(
            user_id='test_user',
            fingerprint=fingerprint,
            crisis_type='test',
            interventions=[],
            emergency_contacts=[],
            medical_info={},
            location=None
        )

        assert 'mesh nodes' in status.lower()
        assert len(mesh.crisis_registry) > 0

    results.append(test_integration(
        "Meshtastic accepts DMT-Fingerprint",
        test_meshtastic_fingerprint_integration
    ))

    # Test 5: PersonalizedAI uses ConsciousnessEngine
    def test_personalized_ai_consciousness_engine():
        from datetime import datetime

        # Create fingerprint
        extractor = DMT_FingerprintExtractor()
        biosensor_data = {
            'eeg': {'alpha_beta_ratio': 1.2},
            'hrv': {'baseline': 65},
            'phi': {'baseline': 0.4}
        }
        fingerprint = extractor.extract('test_user', biosensor_data, consent=True)

        # Create consciousness engine
        consciousness = ConsciousnessEngine()

        # Create PersonalizedAI
        personal_ai = PersonalizedAI(
            user_id_hash=fingerprint.user_id_hash,
            fingerprint=fingerprint,
            consciousness_engine=consciousness,
            personal_phi=fingerprint.personal_phi,
            intervention_history=[],
            created_at=datetime.now()
        )

        # Process input
        result = personal_ai.process("Test input")

        assert 'thought' in result
        assert result['thought'] is not None
        assert 'personal_phi' in result
        assert result['personal_phi'] == fingerprint.personal_phi

    results.append(test_integration(
        "PersonalizedAI uses ConsciousnessEngine",
        test_personalized_ai_consciousness_engine
    ))

    print()
    print("--- End-to-End Integration Test ---")

    # Test 6: Complete user onboarding workflow
    def test_complete_onboarding_workflow():
        luca = LUCA_370_System()

        # Add Meshtastic node
        node = MeshtasticNode("integration_node_001")
        luca.crisis_system.add_node(node)

        # Onboard user
        biosensor_data = {
            'eeg': {'alpha_beta_ratio': 1.2, 'theta': 0.4, 'coherence': 0.6,
                   'attention_patterns': 0.7},
            'hrv': {'baseline': 65, 'rmssd': 55, 'stress_reactivity': 0.3,
                   'variability': 0.7},
            'pci': {'emotional_spectrum': 0.6, 'regulation': 0.7},
            'phi': {'baseline': 0.4, 'integration': 0.5}
        }

        personal_ai = luca.onboard_user(
            user_id='integration_test_user',
            biosensor_data=biosensor_data,
            consent_processing=True,
            consent_insights=True,
            consent_crisis=True
        )

        # Verify onboarding
        assert personal_ai is not None
        assert isinstance(personal_ai, PersonalizedAI)
        assert luca.users_onboarded == 1
        assert len(luca.personalized_ais) == 1
        assert luca.universal_network.total_entities >= 1
        assert luca.crisis_preservations >= 1

        # Process input through personalized AI
        result = luca.process_user_input('integration_test_user', 'Test input')
        assert result is not None
        assert 'thought' in result

    results.append(test_integration(
        "Complete user onboarding workflow",
        test_complete_onboarding_workflow
    ))

    print()

    # Summary
    print("=" * 70)
    passed = sum(results)
    total = len(results)
    percentage = (passed / total * 100) if total > 0 else 0

    print(f"CHECKPOINT 3 RESULTS: {passed}/{total} integrations successful ({percentage:.1f}%)")

    if passed == total:
        print("✅ CHECKPOINT 3: PASS - All components integrate correctly")
        print("   Safe to proceed to Checkpoint 4 (End-to-End Workflow)")
        return True
    else:
        print("❌ CHECKPOINT 3: FAIL - Some integrations failed")
        print("   CORRECTIVE ACTION REQUIRED:")
        print("   1. Check integration point implementations")
        print("   2. Verify data flows between components")
        print("   3. Review error traces above for specific issues")
        return False

if __name__ == '__main__':
    success = run_checkpoint_3()
    sys.exit(0 if success else 1)
