"""
Tests for Medical Emergency System

Author: Großvater & Lennart Wuchold
Standard: 369/370
"""

import pytest

from luca.medical import (
    LOCAL_RESOURCES,
    NATURAL_EMERGENCY_AIDS,
    EmergencyAutomation,
    MedicalEmergencyLLM,
)


class TestNaturalAidDatabase:
    """Test natural aid database structure"""

    def test_natural_aids_structure(self):
        """Test that natural aids database has expected structure"""
        assert "Wunden & Schürfwunden" in NATURAL_EMERGENCY_AIDS
        assert "Insektenstiche & Bisse" in NATURAL_EMERGENCY_AIDS
        assert "Prellungen & Zerrungen" in NATURAL_EMERGENCY_AIDS
        assert "Verbrennungen" in NATURAL_EMERGENCY_AIDS
        assert "Unterkühlung" in NATURAL_EMERGENCY_AIDS

    def test_wound_treatment_has_plants(self):
        """Test wound treatment includes plant remedies"""
        wound_aids = NATURAL_EMERGENCY_AIDS["Wunden & Schürfwunden"]
        assert "pflanzlich" in wound_aids
        assert len(wound_aids["pflanzlich"]) > 0

        # Check first plant has required fields
        plant = wound_aids["pflanzlich"][0]
        assert "name" in plant
        assert "effect" in plant

    def test_local_resources_structure(self):
        """Test local resources have emergency contacts"""
        assert "Hamburg" in LOCAL_RESOURCES
        assert "Berlin" in LOCAL_RESOURCES

        hamburg = LOCAL_RESOURCES["Hamburg"]
        assert "emergency" in hamburg
        assert hamburg["emergency"] == "112"
        assert "giftnotruf" in hamburg
        assert "regionale_pflanzen" in hamburg


class TestMedicalEmergencyLLM:
    """Test Medical Emergency LLM"""

    def test_initialization_without_client(self):
        """Test MedicalEmergencyLLM initializes without Anthropic client"""
        llm = MedicalEmergencyLLM()
        assert llm.medical_history == {}

    def test_fallback_response(self):
        """Test fallback response when LLM unavailable"""
        llm = MedicalEmergencyLLM(anthropic_client=None)
        response = llm.query_medical_emergency(
            symptoms="Test symptom", location="Hamburg", available_plants=["Arnika"]
        )

        assert "NOTFALL-PROTOKOLL" in response
        assert "112" in response
        assert "Hamburg" in response

    def test_get_regional_resources(self):
        """Test getting regional resources"""
        llm = MedicalEmergencyLLM()
        resources = llm.get_regional_resources("Hamburg")

        assert "emergency" in resources
        assert "giftnotruf" in resources
        assert resources["emergency"] == "112"

    def test_identify_available_plants(self):
        """Test plant identification for region"""
        llm = MedicalEmergencyLLM()
        plants = llm.identify_available_plants("Hamburg")

        assert isinstance(plants, list)
        assert len(plants) > 0


class TestEmergencyAutomation:
    """Test Emergency Automation System"""

    def test_initialization(self):
        """Test EmergencyAutomation initialization"""

        # Create minimal kernel mock
        class MockKernel:
            def __init__(self):
                self.consciousness_state = type(
                    "obj", (object,), {"consciousness_level": 300.0}
                )()

        kernel = MockKernel()
        llm = MedicalEmergencyLLM()
        automation = EmergencyAutomation(kernel, llm)

        assert automation.emergency_active is False
        assert automation.vitals["pulse"] is None

    def test_check_vitals(self):
        """Test vital signs checking"""

        class MockKernel:
            def __init__(self):
                self.consciousness_state = type(
                    "obj", (object,), {"consciousness_level": 300.0}
                )()

        kernel = MockKernel()
        llm = MedicalEmergencyLLM()
        automation = EmergencyAutomation(kernel, llm)

        vitals = automation.check_vitals()

        assert "pulse" in vitals
        assert "consciousness" in vitals
        assert "breathing" in vitals
        assert "temperature" in vitals

    def test_identify_regional_plants(self):
        """Test regional plant identification"""

        class MockKernel:
            pass

        kernel = MockKernel()
        llm = MedicalEmergencyLLM()
        automation = EmergencyAutomation(kernel, llm)

        # Test wound-related plants
        plants = automation._identify_regional_plants("Hamburg", "Schnittwunde am Arm")

        assert isinstance(plants, dict)
        assert "Saison" in plants  # Should include season info

    def test_get_local_resources(self):
        """Test getting local resources"""

        class MockKernel:
            pass

        kernel = MockKernel()
        llm = MedicalEmergencyLLM()
        automation = EmergencyAutomation(kernel, llm)

        resources = automation._get_local_resources("Berlin")

        assert "emergency" in resources
        assert resources["emergency"] == "112"


class TestIntegration:
    """Integration tests for medical system"""

    def test_emergency_protocol_simulation(self):
        """Test complete emergency protocol (without actual broadcast)"""

        class MockKernel:
            def __init__(self):
                self.consciousness_state = type(
                    "obj", (object,), {"consciousness_level": 300.0}
                )()

        kernel = MockKernel()
        llm = MedicalEmergencyLLM()
        automation = EmergencyAutomation(kernel, llm)

        # Simulate emergency
        advice, natural_aids, local_help = automation.start_emergency_protocol(
            incident_type="Prellung am Knie", location="Hamburg"
        )

        # Check returns
        assert isinstance(advice, str)
        assert isinstance(natural_aids, dict)
        assert isinstance(local_help, dict)

        # Check emergency was activated
        assert automation.emergency_active is True

        # Check local help has Hamburg resources
        assert local_help["emergency"] == "112"
        assert "040" in local_help["giftnotruf"]  # Hamburg poison control


class TestSafety:
    """Safety and compliance tests"""

    def test_emergency_number_correct(self):
        """Test that all regions have correct emergency number"""
        for region, resources in LOCAL_RESOURCES.items():
            assert "emergency" in resources
            # Germany/Austria/Switzerland use 112 or 144
            assert resources["emergency"] in ["112", "144"]

    def test_all_treatments_have_warnings(self):
        """Test that dangerous treatments have warnings"""
        # Arnika should have warning about open wounds
        wound_aids = NATURAL_EMERGENCY_AIDS["Wunden & Schürfwunden"]
        arnika = next(
            (p for p in wound_aids["pflanzlich"] if p["name"] == "Arnika"), None
        )

        assert arnika is not None
        assert "warning" in arnika
        assert "offene Wunden" in arnika["warning"]

    def test_insect_sting_has_allergy_warning(self):
        """Test insect stings have allergy warning"""
        insect_aids = NATURAL_EMERGENCY_AIDS["Insektenstiche & Bisse"]
        assert "warning" in insect_aids
        assert "112" in insect_aids["warning"]
