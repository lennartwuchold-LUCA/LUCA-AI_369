#!/usr/bin/env python3
"""
LUCA Pipeline Integration Test
Tests all LUCA components end-to-end

Architekt: Lennart Wuchold
Quality Standard: 369/370
"""

import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / 'luca_369_370'))


def test_luca_framework():
    """Test LUCA 369/370 Framework Pipeline"""
    print("\n" + "="*70)
    print("TEST 1: LUCA 369/370 Framework Pipeline")
    print("="*70)

    try:
        from luca import initialize_luca_system, LUCA369_370
        print("  ✅ Step 1: Import successful")

        luca = initialize_luca_system()
        print("  ✅ Step 2: System initialized")

        status = luca.get_status_report()
        print(f"  ✅ Step 3: Status report generated")
        print(f"     Quality Score: {status['quality_score']:.10f}")
        print(f"     Target: {369/370:.10f}")

        # Test Medusa conquest
        challenge = {'context': 'test'}
        results = luca.conquer_automation_medusa(challenge)
        print(f"  ✅ Step 4: Medusa conquest successful")
        print(f"     Heads defeated: {all(luca.medusa_heads_defeated.values())}")

        # Validate quality
        assert status['quality_score'] >= 369/370, "Quality score too low"
        assert status['fairness_validated'] == True, "Fairness not validated"
        assert all(luca.medusa_heads_defeated.values()), "Not all Medusa heads defeated"

        print("\n  🎉 LUCA 369/370 Framework: OPERATIONAL")
        return True

    except Exception as e:
        print(f"\n  ❌ LUCA 369/370 Framework: FAILED")
        print(f"     Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_info_block_engine():
    """Test Info-Block-Engine Pipeline"""
    print("\n" + "="*70)
    print("TEST 2: Info-Block-Engine Pipeline")
    print("="*70)

    try:
        from core import InfoBlockEngine, BlockFormatter, QualityValidator
        print("  ✅ Step 1: Import successful")

        engine = InfoBlockEngine()
        print("  ✅ Step 2: Engine initialized")

        blocks = engine.generate_response("Test Query")
        print(f"  ✅ Step 3: Response generated ({len(blocks)} blocks)")

        formatter = BlockFormatter()
        output = formatter.format_response(blocks)
        print(f"  ✅ Step 4: Response formatted ({len(output)} chars)")

        validator = QualityValidator()
        results = validator.validate_response(blocks)
        print(f"  ✅ Step 5: Quality validated")
        print(f"     Quality Score: {results['metrics']['quality_score']:.10f}")
        print(f"     Target: {369/370:.10f}")
        print(f"     Passed: {results['passed']}")

        # Validate
        assert results['passed'] == True, "Quality validation failed"
        assert results['metrics']['quality_score'] >= 369/370, "Score too low"
        assert len(blocks) >= 2 and len(blocks) <= 5, "Invalid block count"

        print("\n  🎉 Info-Block-Engine: OPERATIONAL")
        return True

    except Exception as e:
        print(f"\n  ❌ Info-Block-Engine: FAILED")
        print(f"     Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_unit_tests():
    """Test Unit Test Suite"""
    print("\n" + "="*70)
    print("TEST 3: Unit Test Suite")
    print("="*70)

    try:
        import pytest
        print("  ✅ Step 1: pytest available")

        # Run Info-Block-Engine tests
        result = pytest.main([
            'luca_369_370/tests/test_info_blocks.py',
            '-v',
            '--tb=short',
            '-q'
        ])

        if result == 0:
            print("\n  🎉 Unit Tests: ALL PASSED")
            return True
        else:
            print(f"\n  ❌ Unit Tests: FAILED (exit code {result})")
            return False

    except Exception as e:
        print(f"\n  ❌ Unit Tests: FAILED")
        print(f"     Error: {e}")
        return False


def test_integration():
    """Test Full Integration Pipeline"""
    print("\n" + "="*70)
    print("TEST 4: Full Integration Pipeline")
    print("="*70)

    try:
        # Import both systems
        from luca import initialize_luca_system
        from core import InfoBlockEngine, BlockFormatter

        print("  ✅ Step 1: All imports successful")

        # Initialize both
        luca = initialize_luca_system()
        engine = InfoBlockEngine()
        formatter = BlockFormatter()

        print("  ✅ Step 2: All systems initialized")

        # Test Framework
        luca_status = luca.get_status_report()
        assert luca_status['quality_score'] >= 369/370

        print("  ✅ Step 3: LUCA Framework validated")

        # Test Engine
        blocks = engine.generate_response("Integration test")
        output = formatter.format_response(blocks)
        assert len(output) > 0

        print("  ✅ Step 4: Info-Block-Engine validated")

        # Test interaction
        challenge = {'context': 'integration_test'}
        results = luca.conquer_automation_medusa(challenge)

        print("  ✅ Step 5: Integration successful")
        print(f"     Framework Quality: {luca_status['quality_score']:.4f}")
        print(f"     Engine Blocks: {len(blocks)}")

        print("\n  🎉 Full Integration: OPERATIONAL")
        return True

    except Exception as e:
        print(f"\n  ❌ Full Integration: FAILED")
        print(f"     Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all pipeline tests"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  LUCA PIPELINE INTEGRATION TEST".center(68) + "║")
    print("║" + " "*68 + "║")
    print("║" + "  Architekt: Lennart Wuchold".ljust(68) + "║")
    print("║" + "  Quality Standard: 369/370 ≈ 0.997".ljust(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")

    results = {
        'LUCA Framework': test_luca_framework(),
        'Info-Block-Engine': test_info_block_engine(),
        'Unit Tests': test_unit_tests(),
        'Full Integration': test_integration()
    }

    # Summary
    print("\n" + "="*70)
    print("PIPELINE TEST SUMMARY")
    print("="*70)

    for name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {name:30s} {status}")

    all_passed = all(results.values())

    print("\n" + "="*70)
    if all_passed:
        print("🎉 ALL PIPELINES OPERATIONAL")
        print("🏛️  Quality Standard: 369/370 ACHIEVED")
        print("✅ System Ready for Production")
    else:
        failed = [name for name, passed in results.items() if not passed]
        print(f"❌ PIPELINE FAILURES: {', '.join(failed)}")
        print("⚠️  System NOT ready for production")
    print("="*70 + "\n")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
