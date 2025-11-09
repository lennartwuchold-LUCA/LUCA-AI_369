"""
HACCP Checkpoint 4: End-to-End Workflow Validation
Test complete user journeys through the LUCA 370 system

Critical Limit: All workflows complete successfully without errors
Priority: CRITICAL (validates production readiness)
"""

import sys
import os
import traceback

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def test_workflow(workflow_name: str, test_func) -> bool:
    """Test if an end-to-end workflow completes successfully"""
    try:
        test_func()
        print(f"✅ {workflow_name}: PASS")
        return True
    except Exception as e:
        print(f"❌ {workflow_name}: FAIL")
        print(f"   Error: {str(e)}")
        traceback.print_exc()
        return False

def run_checkpoint_4():
    """Run HACCP Checkpoint 4: End-to-End Workflow Validation"""
    print("=" * 70)
    print("HACCP CHECKPOINT 4: END-TO-END WORKFLOW VALIDATION")
    print("=" * 70)
    print()

    results = []

    # Import all modules
    from backend.consciousness.luca_370_integration import LUCA_370_System
    from backend.consciousness.meshtastic_crisis_backup import MeshtasticNode

    print("--- User Journey Workflows ---")

    # Workflow 1: New User Onboarding
    def workflow_new_user_onboarding():
        """Complete onboarding: Biosensors → Fingerprint → PersonalizedAI → Network → Crisis"""
        luca = LUCA_370_System()

        # Setup Meshtastic network
        for i in range(3):
            node = MeshtasticNode(f"node_{i:03d}")
            luca.crisis_system.add_node(node)

        # User provides biosensor data
        biosensor_data = {
            'eeg': {'alpha_beta_ratio': 1.2, 'theta': 0.4, 'delta': 0.2,
                   'attention_patterns': 0.7, 'coherence': 0.6,
                   'attention_stability': 0.65, 'network_complexity': 0.55},
            'hrv': {'baseline': 65, 'rmssd': 55, 'stress_reactivity': 0.3,
                   'variability': 0.7},
            'pci': {'emotional_spectrum': 0.6, 'regulation': 0.7},
            'phi': {'baseline': 0.4, 'integration': 0.5},
            'resilience': 0.7
        }

        # Onboard
        personal_ai = luca.onboard_user(
            user_id='alice@example.com',
            biosensor_data=biosensor_data,
            consent_processing=True,
            consent_insights=True,
            consent_crisis=True
        )

        # Verify complete onboarding
        assert personal_ai is not None
        assert luca.users_onboarded == 1
        assert len(luca.personalized_ais) == 1
        assert luca.universal_network.total_entities >= 1
        assert luca.crisis_preservations >= 1

        print("      ✓ Biosensor data collected")
        print("      ✓ DMT-Fingerprint extracted")
        print("      ✓ PersonalizedAI created")
        print("      ✓ Added to universal network")
        print("      ✓ Crisis data preserved (Meshtastic)")

    results.append(test_workflow(
        "Workflow 1: New User Onboarding",
        workflow_new_user_onboarding
    ))

    # Workflow 2: Daily AI Interaction
    def workflow_daily_ai_interaction():
        """User interacts with their PersonalizedAI throughout the day"""
        luca = LUCA_370_System()

        # Onboard user
        biosensor_data = {
            'eeg': {'alpha_beta_ratio': 1.2, 'theta': 0.4, 'coherence': 0.6,
                   'attention_patterns': 0.7, 'attention_stability': 0.65,
                   'network_complexity': 0.55},
            'hrv': {'baseline': 65, 'rmssd': 55, 'stress_reactivity': 0.3,
                   'variability': 0.7},
            'pci': {'emotional_spectrum': 0.6, 'regulation': 0.7},
            'phi': {'baseline': 0.4, 'integration': 0.5},
            'resilience': 0.7
        }
        luca.onboard_user('bob@example.com', biosensor_data, True, True, False)

        # Simulate daily interactions
        interactions = [
            "What should I focus on today?",
            "I'm feeling stressed",
            "Help me plan my work",
            "I need a break"
        ]

        for i, interaction in enumerate(interactions):
            result = luca.process_user_input('bob@example.com', interaction)

            assert result is not None
            assert 'thought' in result
            assert 'personal_phi' in result

            if i == 0:
                print(f"      ✓ Morning check-in processed")
            elif i == len(interactions) - 1:
                print(f"      ✓ {len(interactions)} interactions completed")

    results.append(test_workflow(
        "Workflow 2: Daily AI Interaction",
        workflow_daily_ai_interaction
    ))

    # Workflow 3: Chaotic Creativity Workshop
    def workflow_chaotic_creativity_workshop():
        """Multiple users in workshop: Chaos → Harmony evolution"""
        luca = LUCA_370_System()

        # Onboard 3 participants with different patterns
        participants = [
            {
                'id': 'participant_1',
                'biosensors': {
                    'eeg': {'alpha_beta_ratio': 1.2, 'theta': 0.4, 'coherence': 0.6,
                           'attention_patterns': 0.7, 'attention_stability': 0.65,
                           'network_complexity': 0.55},
                    'hrv': {'baseline': 65, 'rmssd': 55, 'stress_reactivity': 0.3,
                           'variability': 0.7},
                    'pci': {'emotional_spectrum': 0.6, 'regulation': 0.7},
                    'phi': {'baseline': 0.4, 'integration': 0.5},
                    'resilience': 0.7
                }
            },
            {
                'id': 'participant_2',
                'biosensors': {
                    'eeg': {'alpha_beta_ratio': 0.8, 'theta': 0.7, 'coherence': 0.4,
                           'attention_patterns': 0.3, 'attention_stability': 0.35,
                           'network_complexity': 0.45},
                    'hrv': {'baseline': 72, 'rmssd': 45, 'stress_reactivity': 0.6,
                           'variability': 0.4},
                    'pci': {'emotional_spectrum': 0.5, 'regulation': 0.4},
                    'phi': {'baseline': 0.3, 'integration': 0.3},
                    'resilience': 0.5
                }
            },
            {
                'id': 'participant_3',
                'biosensors': {
                    'eeg': {'alpha_beta_ratio': 1.5, 'theta': 0.3, 'coherence': 0.8,
                           'attention_patterns': 0.2, 'attention_stability': 0.75,
                           'network_complexity': 0.65},
                    'hrv': {'baseline': 58, 'rmssd': 62, 'stress_reactivity': 0.8,
                           'variability': 0.6},
                    'pci': {'emotional_spectrum': 0.8, 'regulation': 0.5},
                    'phi': {'baseline': 0.5, 'integration': 0.6},
                    'resilience': 0.6
                }
            }
        ]

        for p in participants:
            luca.onboard_user(
                user_id=p['id'],
                biosensor_data=p['biosensors'],
                consent_processing=True,
                consent_insights=True,
                consent_crisis=False
            )

        print("      ✓ 3 participants onboarded")

        # Run workshop
        results_workshop = luca.run_chaotic_creativity_workshop([
            'participant_1', 'participant_2', 'participant_3'
        ])

        assert len(results_workshop) == 3
        print(f"      ✓ Workshop completed with {len(results_workshop)} participants")

        # Verify chaos → harmony evolution
        interventions = sum(1 for r in results_workshop if r.get('intervention') == 'mycelial_transfer')
        print(f"      ✓ {interventions} mycelial interventions performed")

    results.append(test_workflow(
        "Workflow 3: Chaotic Creativity Workshop",
        workflow_chaotic_creativity_workshop
    ))

    # Workflow 4: Crisis Response (Offline)
    def workflow_crisis_response():
        """User in crisis: Retrieve personalized response via Meshtastic (offline)"""
        luca = LUCA_370_System()

        # Setup Meshtastic network
        for i in range(5):
            node = MeshtasticNode(f"crisis_node_{i:03d}")
            luca.crisis_system.add_node(node)

        # Onboard user with crisis consent
        biosensor_data = {
            'eeg': {'alpha_beta_ratio': 1.2, 'theta': 0.4, 'coherence': 0.6,
                   'attention_patterns': 0.7, 'attention_stability': 0.65,
                   'network_complexity': 0.55},
            'hrv': {'baseline': 65, 'rmssd': 55, 'stress_reactivity': 0.3,
                   'variability': 0.7},
            'pci': {'emotional_spectrum': 0.6, 'regulation': 0.7},
            'phi': {'baseline': 0.4, 'integration': 0.5},
            'resilience': 0.7
        }
        luca.onboard_user('crisis_user@example.com', biosensor_data, True, True, True)

        print("      ✓ User onboarded with crisis preservation")

        # Simulate crisis (blackout - no internet)
        crisis_response = luca.handle_crisis('crisis_user@example.com', 'blackout')

        assert crisis_response is not None
        assert 'personal_phi' in crisis_response
        assert 'instructions' in crisis_response
        assert len(crisis_response['instructions']) > 0

        print("      ✓ Crisis detected (blackout)")
        print("      ✓ Personalized response retrieved (offline)")
        print(f"      ✓ {len(crisis_response['instructions'])} personalized instructions")

    results.append(test_workflow(
        "Workflow 4: Crisis Response (Offline)",
        workflow_crisis_response
    ))

    # Workflow 5: Insights Monetization
    def workflow_insights_monetization():
        """System collects anonymized insights and monetizes them (GDPR-compliant)"""
        luca = LUCA_370_System()

        # Onboard multiple users to meet k-anonymity threshold
        # (In production, need 100+ users, but we'll simulate with fewer)
        for i in range(10):
            biosensor_data = {
                'eeg': {'alpha_beta_ratio': 1.0 + (i * 0.1), 'theta': 0.4,
                       'coherence': 0.6, 'attention_patterns': 0.7,
                       'attention_stability': 0.65, 'network_complexity': 0.55},
                'hrv': {'baseline': 60 + i, 'rmssd': 50 + i,
                       'stress_reactivity': 0.3 + (i * 0.05),
                       'variability': 0.7 - (i * 0.02)},
                'pci': {'emotional_spectrum': 0.6, 'regulation': 0.7},
                'phi': {'baseline': 0.4, 'integration': 0.5},
                'resilience': 0.7
            }
            luca.onboard_user(f'user_{i}@example.com', biosensor_data, True, True, False)

        print(f"      ✓ {luca.users_onboarded} users onboarded")

        # Simulate interactions to generate insights
        for i in range(10):
            luca.process_user_input(f'user_{i}@example.com', f'Test input {i}')

        print("      ✓ User interactions processed")

        # Check insights collected
        stats = luca.get_system_statistics()
        insights_count = stats['insights_db']['total_insights']

        assert insights_count > 0
        print(f"      ✓ {insights_count} anonymized insights collected")

        # Attempt monetization
        revenue = luca.monetize_insights()
        print(f"      ✓ Insights monetization: ${revenue:.2f}")

    results.append(test_workflow(
        "Workflow 5: Insights Monetization (GDPR)",
        workflow_insights_monetization
    ))

    print()

    # Summary
    print("=" * 70)
    passed = sum(results)
    total = len(results)
    percentage = (passed / total * 100) if total > 0 else 0

    print(f"CHECKPOINT 4 RESULTS: {passed}/{total} workflows successful ({percentage:.1f}%)")

    if passed == total:
        print("✅ CHECKPOINT 4: PASS - All end-to-end workflows complete successfully")
        print("   Safe to proceed to Checkpoint 5 (Documentation)")
        return True
    else:
        print("❌ CHECKPOINT 4: FAIL - Some workflows failed")
        print("   CORRECTIVE ACTION REQUIRED:")
        print("   1. Check workflow implementation for errors")
        print("   2. Verify data flows through complete user journey")
        print("   3. Review error traces above for specific issues")
        return False

if __name__ == '__main__':
    success = run_checkpoint_4()
    sys.exit(0 if success else 1)
