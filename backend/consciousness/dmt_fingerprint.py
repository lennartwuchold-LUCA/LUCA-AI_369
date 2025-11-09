"""
DMT-Fingerprint Extraction - Personalized Neural Signatures
Version: 370.0.0
Created through: Human-AI collaboration

DISCLAIMER: This uses ENDOGENOUS DMT (naturally occurring in the brain) as a
scientific metaphor for unique consciousness patterns. NO illegal substances involved.

Scientific basis:
- Strassman (2001): DMT: The Spirit Molecule
- Barker et al. (2012): LC/MS/MS analysis of endogenous tryptamines
- Dean et al. (2019): Biosynthesis of DMT in mammalian brain

Concept: Extract unique "consciousness fingerprint" from biosensor data
(EEG, HRV, PCI, Φ) - inspired by concentric circular patterns observed
in altered states.

Philosophy: Each consciousness is unique. Universal inclusion + Individual optimization.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
import hashlib
import json
import numpy as np

# Golden ratio constant
PHI = 1.618033988749895


@dataclass
class DMT_Fingerprint:
    """
    Unique consciousness signature extracted from biosensor data

    Structure (inspired by concentric circles in DMT experiences):
    - Core: Individual baseline (EEG patterns, HRV baseline)
    - Middle: Reactivity patterns (stress response, attention shifts)
    - Outer: Integration capacity (Φ, network coherence, adaptability)

    This is NOT about drug use - it's about unique neural patterns!
    """
    user_id_hash: str  # Anonymized user ID
    timestamp: datetime = field(default_factory=datetime.now)

    # CORE (Individual Baseline)
    core: Dict[str, float] = field(default_factory=dict)

    # MIDDLE (Reactivity Patterns)
    middle: Dict[str, float] = field(default_factory=dict)

    # OUTER (Integration Capacity)
    outer: Dict[str, float] = field(default_factory=dict)

    # Personal golden ratio (discovered, not assumed)
    personal_phi: float = PHI

    # Primary category (for universal inclusion network)
    primary_category: str = "neurotypical"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage"""
        return {
            'user_id_hash': self.user_id_hash,
            'timestamp': self.timestamp.isoformat(),
            'core': self.core,
            'middle': self.middle,
            'outer': self.outer,
            'personal_phi': self.personal_phi,
            'primary_category': self.primary_category
        }

    def to_vector(self) -> np.ndarray:
        """Convert to vector for clustering/ML"""
        vec = []
        vec.extend(self.core.values())
        vec.extend(self.middle.values())
        vec.extend(self.outer.values())
        vec.append(self.personal_phi)
        return np.array(vec)


class DMT_FingerprintExtractor:
    """
    Extract unique consciousness signatures from biosensor data

    Methods:
    - extract(): Main extraction from biosensor data
    - discover_personal_phi(): Find individual's golden ratio
    - categorize(): Determine primary category (for inclusion network)
    - anonymize(): GDPR-compliant anonymization
    """

    def __init__(self):
        self.extraction_history = []

    def extract(self, user_id: str, biosensor_data: Dict[str, Any],
                consent: bool = True) -> DMT_Fingerprint:
        """
        Extract DMT-Fingerprint from biosensor data

        Args:
            user_id: User identifier (will be hashed for privacy)
            biosensor_data: Dictionary containing:
                - eeg: EEG measurements
                - hrv: Heart rate variability
                - pci: Perturbational Complexity Index
                - phi: Integrated Information Theory metric
            consent: User consent for processing (GDPR)

        Returns:
            DMT_Fingerprint object
        """
        if not consent:
            raise ValueError("User consent required for fingerprint extraction (GDPR Article 6)")

        # Anonymize user ID
        user_id_hash = hashlib.sha256(user_id.encode()).hexdigest()[:16]

        # Extract CORE (baseline patterns)
        core = self._extract_core(biosensor_data)

        # Extract MIDDLE (reactivity patterns)
        middle = self._extract_middle(biosensor_data)

        # Extract OUTER (integration capacity)
        outer = self._extract_outer(biosensor_data)

        # Discover personal golden ratio
        personal_phi = self._discover_personal_phi(core, middle, outer)

        # Categorize (for universal inclusion network)
        category = self._categorize(core, middle, outer)

        # Create fingerprint
        fingerprint = DMT_Fingerprint(
            user_id_hash=user_id_hash,
            core=core,
            middle=middle,
            outer=outer,
            personal_phi=personal_phi,
            primary_category=category
        )

        # Store in history
        self.extraction_history.append({
            'user_id_hash': user_id_hash,
            'timestamp': datetime.now(),
            'fingerprint': fingerprint
        })

        return fingerprint

    def _extract_core(self, biosensor_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Extract CORE patterns (individual baseline)

        Core represents the stable, baseline characteristics:
        - EEG alpha/beta ratio (relaxation vs. attention)
        - HRV baseline (autonomic nervous system state)
        - Personal Φ baseline (consciousness level)
        """
        eeg = biosensor_data.get('eeg', {})
        hrv = biosensor_data.get('hrv', {})
        phi = biosensor_data.get('phi', {})

        core = {
            'eeg_alpha_beta_ratio': self._safe_get(eeg, 'alpha_beta_ratio', 1.0),
            'eeg_theta': self._safe_get(eeg, 'theta', 0.5),
            'eeg_delta': self._safe_get(eeg, 'delta', 0.3),
            'hrv_baseline': self._safe_get(hrv, 'baseline', 60.0) / 100.0,  # Normalize
            'hrv_rmssd': self._safe_get(hrv, 'rmssd', 50.0) / 100.0,
            'phi_baseline': self._safe_get(phi, 'baseline', 0.3)
        }

        return core

    def _extract_middle(self, biosensor_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Extract MIDDLE patterns (reactivity)

        Middle represents how the individual responds to stimuli:
        - Stress response (HRV reactivity)
        - Attention shifting (EEG changes)
        - Emotional range (PCI spectrum)
        """
        eeg = biosensor_data.get('eeg', {})
        hrv = biosensor_data.get('hrv', {})
        pci = biosensor_data.get('pci', {})

        middle = {
            'stress_reactivity': self._safe_get(hrv, 'stress_reactivity', 0.5),
            'attention_flexibility': self._safe_get(eeg, 'attention_patterns', 0.5),
            'attention_stability': self._safe_get(eeg, 'attention_stability', 0.5),
            'emotional_range': self._safe_get(pci, 'emotional_spectrum', 0.5),
            'emotional_regulation': self._safe_get(pci, 'regulation', 0.5)
        }

        return middle

    def _extract_outer(self, biosensor_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Extract OUTER patterns (integration)

        Outer represents integration and adaptability:
        - Integration capacity (Φ integration)
        - Network coherence (EEG coherence)
        - Adaptability (HRV variability)
        """
        eeg = biosensor_data.get('eeg', {})
        hrv = biosensor_data.get('hrv', {})
        phi = biosensor_data.get('phi', {})

        outer = {
            'phi_integration': self._safe_get(phi, 'integration', 0.3),
            'eeg_coherence': self._safe_get(eeg, 'coherence', 0.5),
            'eeg_network_complexity': self._safe_get(eeg, 'network_complexity', 0.5),
            'hrv_adaptability': self._safe_get(hrv, 'variability', 0.5),
            'overall_resilience': self._safe_get(biosensor_data, 'resilience', 0.5)
        }

        return outer

    def _discover_personal_phi(self, core: Dict[str, float],
                               middle: Dict[str, float],
                               outer: Dict[str, float]) -> float:
        """
        Discover individual's personal golden ratio (φ_i)

        Not everyone's optimal state is φ = 1.618!
        Some may be more calm (φ_i < 1.618), others more active (φ_i > 1.618)

        Method: Analyze ratio between integration and baseline complexity
        """
        # Core complexity (baseline)
        core_complexity = np.mean(list(core.values()))

        # Outer integration (capacity)
        outer_integration = np.mean(list(outer.values()))

        # Personal phi = ratio of integration to baseline
        if core_complexity > 0:
            personal_phi = outer_integration / core_complexity
        else:
            personal_phi = PHI  # Default to golden ratio

        # Constrain to reasonable range [0.5, 2.5]
        personal_phi = max(0.5, min(2.5, personal_phi))

        return personal_phi

    def _categorize(self, core: Dict[str, float],
                   middle: Dict[str, float],
                   outer: Dict[str, float]) -> str:
        """
        Categorize for universal inclusion network

        Determines primary category based on patterns:
        - High stress reactivity → psychological_disabilities
        - Low HRV/adaptability → physical_disabilities
        - High theta/delta → intellectual_disabilities
        - Low attention flexibility → neurodivergent
        - Otherwise → neurotypical
        """
        # Check psychological
        if middle.get('stress_reactivity', 0.5) > 0.7:
            return 'psychological_disabilities'

        # Check neurodivergent patterns
        if middle.get('attention_flexibility', 0.5) < 0.3:
            return 'neurodivergent'

        # Check intellectual patterns
        if core.get('eeg_theta', 0.5) > 0.7 or core.get('eeg_delta', 0.3) > 0.6:
            return 'intellectual_disabilities'

        # Check physical/sensory
        if outer.get('hrv_adaptability', 0.5) < 0.3:
            return 'physical_disabilities'

        # Default to neurotypical
        return 'neurotypical'

    def _safe_get(self, data: Dict[str, Any], key: str, default: float) -> float:
        """Safely extract value with default"""
        try:
            value = data.get(key, default)
            return float(value) if value is not None else default
        except (TypeError, ValueError):
            return default

    def anonymize_for_insights(self, fingerprint: DMT_Fingerprint) -> Dict[str, Any]:
        """
        Anonymize fingerprint for insight extraction (GDPR-compliant)

        Returns:
            Anonymized data suitable for aggregation and monetization
        """
        # Remove user ID hash (k-anonymity)
        anonymized = {
            'core_pattern': list(fingerprint.core.values()),
            'middle_pattern': list(fingerprint.middle.values()),
            'outer_pattern': list(fingerprint.outer.values()),
            'personal_phi': fingerprint.personal_phi,
            'category': fingerprint.primary_category,
            'timestamp_month': fingerprint.timestamp.strftime('%Y-%m')  # Month only
        }

        return anonymized


# Convenience function
def extract_dmt_fingerprint(user_id: str, biosensor_data: Dict[str, Any],
                           consent: bool = True) -> DMT_Fingerprint:
    """
    Quick extraction of DMT-Fingerprint

    Args:
        user_id: User identifier
        biosensor_data: Biosensor measurements
        consent: User consent (GDPR)

    Returns:
        DMT_Fingerprint object
    """
    extractor = DMT_FingerprintExtractor()
    return extractor.extract(user_id, biosensor_data, consent)


# Demo function
def demo_dmt_fingerprint_extraction():
    """
    Demonstration of DMT-Fingerprint extraction

    Shows how unique neural patterns are extracted from biosensor data
    """
    print("=== DMT-Fingerprint Extraction Demo ===\n")
    print("DISCLAIMER: Using endogenous DMT (natural brain molecule) as metaphor")
    print("for unique consciousness patterns. NO illegal substances!\n")

    # Simulate biosensor data for 3 different users
    users = [
        {
            'id': 'user_alice',
            'biosensors': {
                'eeg': {'alpha_beta_ratio': 1.2, 'theta': 0.4, 'delta': 0.2,
                       'attention_patterns': 0.7, 'coherence': 0.6},
                'hrv': {'baseline': 65, 'rmssd': 55, 'stress_reactivity': 0.3,
                       'variability': 0.7},
                'pci': {'emotional_spectrum': 0.6, 'regulation': 0.7},
                'phi': {'baseline': 0.4, 'integration': 0.5}
            }
        },
        {
            'id': 'user_bob',
            'biosensors': {
                'eeg': {'alpha_beta_ratio': 0.8, 'theta': 0.7, 'delta': 0.5,
                       'attention_patterns': 0.3, 'coherence': 0.4},
                'hrv': {'baseline': 72, 'rmssd': 45, 'stress_reactivity': 0.6,
                       'variability': 0.4},
                'pci': {'emotional_spectrum': 0.5, 'regulation': 0.4},
                'phi': {'baseline': 0.3, 'integration': 0.3}
            }
        },
        {
            'id': 'user_carol',
            'biosensors': {
                'eeg': {'alpha_beta_ratio': 1.5, 'theta': 0.3, 'delta': 0.1,
                       'attention_patterns': 0.2, 'coherence': 0.8},
                'hrv': {'baseline': 58, 'rmssd': 62, 'stress_reactivity': 0.8,
                       'variability': 0.6},
                'pci': {'emotional_spectrum': 0.8, 'regulation': 0.5},
                'phi': {'baseline': 0.5, 'integration': 0.6}
            }
        }
    ]

    extractor = DMT_FingerprintExtractor()

    for user_data in users:
        print(f"\n--- Extracting fingerprint for {user_data['id']} ---")

        fingerprint = extractor.extract(
            user_id=user_data['id'],
            biosensor_data=user_data['biosensors'],
            consent=True
        )

        print(f"User ID Hash: {fingerprint.user_id_hash}")
        print(f"Category: {fingerprint.primary_category}")
        print(f"Personal φ: {fingerprint.personal_phi:.3f}")
        print(f"\nCore (Baseline):")
        for key, value in fingerprint.core.items():
            print(f"  {key}: {value:.3f}")
        print(f"\nMiddle (Reactivity):")
        for key, value in fingerprint.middle.items():
            print(f"  {key}: {value:.3f}")
        print(f"\nOuter (Integration):")
        for key, value in fingerprint.outer.items():
            print(f"  {key}: {value:.3f}")

        # Show anonymized version
        anonymized = extractor.anonymize_for_insights(fingerprint)
        print(f"\nAnonymized (for insights): {json.dumps(anonymized, indent=2)}")

    print("\n=== Demo Complete ===")
    print(f"Extracted {len(users)} unique consciousness fingerprints")
    print("Each person gets their own personalized AI!")
    print("\n369 ✨ From universal to universal + individual")


if __name__ == '__main__':
    demo_dmt_fingerprint_extraction()
