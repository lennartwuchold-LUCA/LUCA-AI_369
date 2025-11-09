"""
HACCP Checkpoint 2: Unit Functionality Demos
Test that all LUCA 370 module demos run successfully

Critical Limit: All demos execute and complete without errors
Priority: HIGH (validates functional correctness)
"""

import sys
import os
import traceback
from io import StringIO
import contextlib

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def test_demo(module_name: str, demo_function_name: str, description: str) -> bool:
    """Test if a module's demo function runs successfully"""
    try:
        # Import the module
        module = __import__(module_name, fromlist=[demo_function_name])

        # Get the demo function
        if not hasattr(module, demo_function_name):
            print(f"❌ {description}: FAIL")
            print(f"   Error: Demo function '{demo_function_name}' not found in module")
            return False

        demo_func = getattr(module, demo_function_name)

        # Capture stdout to prevent cluttering test output
        # But still run the demo to verify it works
        output_buffer = StringIO()

        with contextlib.redirect_stdout(output_buffer):
            demo_func()

        # If we got here, the demo ran successfully
        print(f"✅ {description}: PASS")
        return True

    except Exception as e:
        print(f"❌ {description}: FAIL")
        print(f"   Error: {str(e)}")
        traceback.print_exc()
        return False

def run_checkpoint_2():
    """Run HACCP Checkpoint 2: Unit Functionality Demos"""
    print("=" * 70)
    print("HACCP CHECKPOINT 2: UNIT FUNCTIONALITY DEMOS")
    print("=" * 70)
    print()

    results = []

    # Test LUCA 369 core demos
    print("--- LUCA 369 Core Module Demos ---")
    results.append(test_demo(
        "backend.consciousness.tesla_layers",
        "demo_tesla_layers",
        "Tesla 3-Layer Architecture Demo"
    ))
    results.append(test_demo(
        "backend.consciousness.universal_inclusion_network",
        "demo_universal_inclusion",
        "Universal Inclusion Network Demo"
    ))
    print()

    # Test LUCA 370 new demos
    print("--- LUCA 370 New Module Demos ---")
    results.append(test_demo(
        "backend.consciousness.dmt_fingerprint",
        "demo_dmt_fingerprint_extraction",
        "DMT-Fingerprint Extraction Demo"
    ))
    results.append(test_demo(
        "backend.consciousness.meshtastic_crisis_backup",
        "demo_meshtastic_crisis",
        "Meshtastic Crisis Backup Demo"
    ))
    results.append(test_demo(
        "backend.consciousness.luca_370_integration",
        "demo_luca_370_complete",
        "LUCA 370 Complete Integration Demo"
    ))
    print()

    # Summary
    print("=" * 70)
    passed = sum(results)
    total = len(results)
    percentage = (passed / total * 100) if total > 0 else 0

    print(f"CHECKPOINT 2 RESULTS: {passed}/{total} demos successful ({percentage:.1f}%)")

    if passed == total:
        print("✅ CHECKPOINT 2: PASS - All demos execute successfully")
        print("   Safe to proceed to Checkpoint 3 (Integration Completeness)")
        return True
    else:
        print("❌ CHECKPOINT 2: FAIL - Some demos failed")
        print("   CORRECTIVE ACTION REQUIRED:")
        print("   1. Check demo function implementations for errors")
        print("   2. Verify all dependencies are available")
        print("   3. Review error traces above for specific issues")
        return False

if __name__ == '__main__':
    success = run_checkpoint_2()
    sys.exit(0 if success else 1)
