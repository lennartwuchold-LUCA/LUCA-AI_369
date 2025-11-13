"""
🌿 LUCA Medical Emergency Module
Combines medical LLM knowledge with natural/herbal remedies and regional resources.

Author: Großvater & Lennart Wuchold
Standard: 369/370
"""

try:
    from .emergency_automation import EmergencyAutomation
    from .emergency_plan import MedicalEmergencyLLM
    from .natural_aid_database import LOCAL_RESOURCES, NATURAL_EMERGENCY_AIDS

    _MEDICAL_AVAILABLE = True
except ImportError:
    MedicalEmergencyLLM = None
    EmergencyAutomation = None
    NATURAL_EMERGENCY_AIDS = None
    LOCAL_RESOURCES = None
    _MEDICAL_AVAILABLE = False

__all__ = [
    "MedicalEmergencyLLM",
    "EmergencyAutomation",
    "NATURAL_EMERGENCY_AIDS",
    "LOCAL_RESOURCES",
]
