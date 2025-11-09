"""
HACCP Checkpoint 1: Import Resolution
Test that all LUCA 370 modules import correctly

Critical Limit: All imports succeed without errors
Priority: CRITICAL (must pass before any other tests)
"""

import sys
import os
import traceback

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def test_import(module_path: str, description: str) -> bool:
    """Test if a module can be imported"""
    try:
        __import__(module_path)
        print(f"✅ {description}: PASS")
        return True
    except Exception as e:
        print(f"❌ {description}: FAIL")
        print(f"   Error: {str(e)}")
        traceback.print_exc()
        return False

def run_checkpoint_1():
    """Run HACCP Checkpoint 1: Import Resolution"""
    print("=" * 70)
    print("HACCP CHECKPOINT 1: IMPORT RESOLUTION")
    print("=" * 70)
    print()

    results = []

    # Test LUCA 369 core imports
    print("--- LUCA 369 Core Modules ---")
    results.append(test_import(
        "backend.consciousness.tesla_layers",
        "Tesla 3-Layer Architecture (Hardware/Software/Consciousness)"
    ))
    results.append(test_import(
        "backend.consciousness.universal_inclusion_network",
        "Universal Inclusion Network (SCOBY-Myzelium)"
    ))
    print()

    # Test LUCA 370 new imports
    print("--- LUCA 370 New Modules ---")
    results.append(test_import(
        "backend.consciousness.dmt_fingerprint",
        "DMT-Fingerprint Personalization"
    ))
    results.append(test_import(
        "backend.consciousness.meshtastic_crisis_backup",
        "Meshtastic Crisis Backup System"
    ))
    results.append(test_import(
        "backend.consciousness.luca_370_integration",
        "LUCA 370 Complete Integration"
    ))
    print()

    # Test supporting imports
    print("--- Supporting Modules ---")
    results.append(test_import(
        "backend.consciousness.audit_verifier",
        "Audit Verifier (UN-CRPD compliance)"
    ))
    results.append(test_import(
        "backend.consciousness.universal_inclusion_verifier",
        "Universal Inclusion Verifier"
    ))
    print()

    # Summary
    print("=" * 70)
    passed = sum(results)
    total = len(results)
    percentage = (passed / total * 100) if total > 0 else 0

    print(f"CHECKPOINT 1 RESULTS: {passed}/{total} imports successful ({percentage:.1f}%)")

    if passed == total:
        print("✅ CHECKPOINT 1: PASS - All imports resolved")
        print("   Safe to proceed to Checkpoint 2")
        return True
    else:
        print("❌ CHECKPOINT 1: FAIL - Some imports failed")
        print("   CORRECTIVE ACTION REQUIRED:")
        print("   1. Check for missing dependencies (pip3 install -r requirements.txt)")
        print("   2. Verify Python path includes project root")
        print("   3. Check for circular import dependencies")
        return False

if __name__ == '__main__':
    success = run_checkpoint_1()
    sys.exit(0 if success else 1)
