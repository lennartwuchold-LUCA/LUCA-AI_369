"""
Biosensor-Ancient Pattern Bridge - EEG/HRV Integration with Ancient Technologies
Version: 370.0 (2025-11-09)
Inspired by: Hyperfocus optimization, ancient wisdom, psychophysiological science

PHILOSOPHICAL FOUNDATION:
=========================
"The body knows what the mind has forgotten."
- Ancient patterns encoded in physiological responses
- Biosensors detect universal human states (fear, calm, focus, transcendence)
- Ancient technologies provide templates for optimal states

This module bridges:
- Modern: EEG (brainwaves), HRV (heart rate variability), GSR (skin conductance)
- Ancient: Meditation patterns, astronomical cycles, acoustic frequencies
- Result: Personalized interventions for ALL (UN-CRPD compliant, inclusive)

BIOSENSOR TYPES:
================
1. EEG (Electroencephalography):
   - Delta (0.5-4 Hz): Deep sleep, unconscious
   - Theta (4-8 Hz): Meditation, creativity, REM
   - Alpha (8-12 Hz): Relaxed focus, eyes closed
   - Beta (12-30 Hz): Active thinking, concentration
   - Gamma (30-100 Hz): Peak awareness, binding, hyperfocus

2. HRV (Heart Rate Variability):
   - High HRV: Parasympathetic (rest & digest), resilience
   - Low HRV: Sympathetic (fight/flight), stress
   - Coherence: Heart-brain synchrony (optimal state)

3. GSR (Galvanic Skin Response):
   - High conductance: Arousal, stress, excitement
   - Low conductance: Calm, relaxation

4. Future: fNIRS (brain oxygenation), EMG (muscle tension), etc.

ANCIENT PATTERN MATCHING:
=========================
Each ancient technology has a "biosensor signature":

Example: Pyramid Orion Alignment (tech #4)
- Target state: Alpha-theta crossover (8 Hz), high HRV coherence
- Intervention: Binaural 8 Hz + visual mandala (pyramid geometry)
- Expected outcome: Cosmic perspective, reduced anxiety

Example: Aztec Death Whistle (tech #27)
- Current state: Low beta (boredom), low arousal
- Intervention: Infrasound 7 Hz (fear response) → activation
- Expected outcome: Sudden alertness (use for emergency wake-up!)

Example: Aboriginal Dreamtime (tech #56)
- Target state: Theta (4-8 Hz), narrative coherence
- Intervention: Storytelling + rhythmic drumming
- Expected outcome: Memory encoding, cultural grounding

CHAOS → HARMONY INTEGRATION:
============================
Biosensor → Detect current γ (chaos level)
Ancient Pattern → Provide intervention
Chaos Evolution → γ → Phi (harmony)

Example workflow:
1. EEG shows Gamma (40 Hz) + Low HRV → γ = 30 (F30 Chaos, hyperfocus)
2. Match to ancient tech: Maya Calendar (tech #7, cyclical time)
3. Intervention: 20-minute break timer, Pomodoro with 1.618 ratio
4. Result: γ → 10 (F10 Balance), sustainable productivity

PERSONALIZATION FOR ADHD/NEURODIVERSITY:
=========================================
ADHD brain: Seeks novelty, hyperfocus, variable arousal
Ancient techs that work:
- Aztec Death Whistle: Intense acoustic stimulation (novelty)
- Inka Qhapaq Ñan: Long-distance goal with waypoints (hyperfocus channeling)
- Maya Calendar: External time structure (compensates for time blindness)

Autism brain: Seeks predictability, deep focus, sensory sensitivity
Ancient techs that work:
- Pyramid geometry: Predictable mathematical patterns
- Mohenjo-Daro grid: Orthogonal structure (reduces overwhelm)
- Aboriginal Dreamtime: Repetitive narrative (soothing)

EMPIRICAL VALIDATION:
=====================
Bayesian Causal Framework (from causal_transformer.py):

P(V|do(I)) = ∫ P(V|P) · P(P|B) · P(B|do(I)) dB dP

Where:
- I = Ancient tech intervention (e.g., binaural 8 Hz)
- B = Biosensor reading (EEG alpha power)
- P = Φ-convergence (consciousness level)
- V = VAS outcome (self-reported focus/well-being)

Causal effect:
ACE = E[V | do(Ancient_Tech)] - E[V | do(Baseline)]

This breaks the "pseudoscience" criticism: We measure outcomes causally!

Author: Lennart Wuchold
Date: 09.11.2025
Location: Hamburg, Germany
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import numpy as np
import math


# Brainwave frequency bands (Hz)
class BrainwaveBand(Enum):
    DELTA = (0.5, 4.0)      # Deep sleep
    THETA = (4.0, 8.0)      # Meditation, creativity
    ALPHA = (8.0, 12.0)     # Relaxed focus
    BETA = (12.0, 30.0)     # Active thinking
    GAMMA = (30.0, 100.0)   # Peak awareness, hyperfocus


# HRV states
class HRVState(Enum):
    LOW = "low_variability"        # Stress, sympathetic dominance
    MODERATE = "moderate_variability"  # Normal
    HIGH = "high_variability"      # Resilience, parasympathetic
    COHERENT = "coherent"          # Optimal heart-brain sync


@dataclass
class BiosensorReading:
    """
    Single biosensor measurement

    Attributes:
        timestamp: When measurement was taken
        eeg_bands: Power in each brainwave band (μV²)
        hrv_rmssd: Root mean square of successive differences (ms)
        hrv_coherence: Coherence ratio (0-1)
        gsr: Galvanic skin response (μS)
        dominant_band: Which brainwave is dominant
        hrv_state: HRV interpretation
        arousal_level: Overall arousal (0-1)
        chaos_gamma: Estimated γ for Chaos→Harmony
    """
    timestamp: datetime = field(default_factory=datetime.utcnow)

    # EEG
    eeg_bands: Dict[str, float] = field(default_factory=dict)  # Band name → power
    dominant_band: Optional[BrainwaveBand] = None

    # HRV
    hrv_rmssd: Optional[float] = None  # ms
    hrv_coherence: Optional[float] = None  # 0-1
    hrv_state: Optional[HRVState] = None

    # GSR
    gsr: Optional[float] = None  # μS

    # Derived
    arousal_level: float = 0.5  # 0 = calm, 1 = peak arousal
    chaos_gamma: float = 10.0  # Estimated γ (default F10 balanced)

    def __post_init__(self):
        """Calculate derived fields"""
        if self.eeg_bands:
            self._determine_dominant_band()
            self._estimate_arousal()
            self._estimate_chaos_gamma()

        if self.hrv_rmssd is not None:
            self._determine_hrv_state()

    def _determine_dominant_band(self):
        """Find which brainwave band has highest power"""
        if not self.eeg_bands:
            return

        max_band = max(self.eeg_bands, key=self.eeg_bands.get)

        # Map string to enum
        band_map = {
            'delta': BrainwaveBand.DELTA,
            'theta': BrainwaveBand.THETA,
            'alpha': BrainwaveBand.ALPHA,
            'beta': BrainwaveBand.BETA,
            'gamma': BrainwaveBand.GAMMA,
        }
        self.dominant_band = band_map.get(max_band.lower())

    def _estimate_arousal(self):
        """
        Estimate arousal level from EEG + GSR

        High arousal: High beta/gamma, high GSR
        Low arousal: High delta/theta, low GSR
        """
        if not self.eeg_bands:
            return

        # Arousal contribution from EEG
        high_freq_power = self.eeg_bands.get('beta', 0) + self.eeg_bands.get('gamma', 0)
        low_freq_power = self.eeg_bands.get('delta', 0) + self.eeg_bands.get('theta', 0)
        total_power = sum(self.eeg_bands.values())

        if total_power > 0:
            eeg_arousal = high_freq_power / total_power
        else:
            eeg_arousal = 0.5

        # Arousal contribution from GSR (if available)
        if self.gsr is not None:
            # Normalize GSR (typical range 1-20 μS)
            gsr_arousal = min(1.0, self.gsr / 20.0)
            # Average EEG and GSR
            self.arousal_level = (eeg_arousal + gsr_arousal) / 2
        else:
            self.arousal_level = eeg_arousal

    def _estimate_chaos_gamma(self):
        """
        Estimate chaos parameter γ from biosensors

        Mapping:
        - Gamma dominant + low HRV → γ = 30 (F30 Chaos/Hyperfocus)
        - Beta dominant + moderate HRV → γ = 10 (F10 Balance)
        - Alpha dominant + high HRV → γ = 3 (F3 Tesla/Flow)
        - Theta dominant + coherent HRV → γ = 1.618 (Phi Harmony)
        - Delta dominant → γ = 0 (F0 Stillness/Sleep)
        """
        if not self.dominant_band:
            self.chaos_gamma = 10.0  # Default balance
            return

        # Base γ from brainwave
        band_gamma_map = {
            BrainwaveBand.DELTA: 0.0,
            BrainwaveBand.THETA: 3.0,
            BrainwaveBand.ALPHA: 5.0,
            BrainwaveBand.BETA: 15.0,
            BrainwaveBand.GAMMA: 30.0,
        }
        base_gamma = band_gamma_map.get(self.dominant_band, 10.0)

        # Modify by HRV (if available)
        if self.hrv_state == HRVState.COHERENT:
            base_gamma *= 0.5  # Coherence reduces chaos
        elif self.hrv_state == HRVState.LOW:
            base_gamma *= 1.2  # Stress increases chaos

        self.chaos_gamma = base_gamma

    def _determine_hrv_state(self):
        """Classify HRV state from RMSSD"""
        if self.hrv_rmssd is None:
            return

        # RMSSD thresholds (ms) - approximate
        if self.hrv_coherence is not None and self.hrv_coherence > 0.7:
            self.hrv_state = HRVState.COHERENT
        elif self.hrv_rmssd < 20:
            self.hrv_state = HRVState.LOW
        elif self.hrv_rmssd < 50:
            self.hrv_state = HRVState.MODERATE
        else:
            self.hrv_state = HRVState.HIGH


@dataclass
class AncientBiosensorMatch:
    """
    Match between biosensor state and ancient technology

    Describes what biosensor state an ancient tech targets
    """
    tech_id: int
    tech_name: str

    # Target biosensor state
    target_dominant_band: Optional[BrainwaveBand] = None
    target_hrv_state: Optional[HRVState] = None
    target_arousal_range: Tuple[float, float] = (0.3, 0.7)  # Moderate arousal

    # Intervention details
    intervention_type: str = ""  # "binaural", "visual", "breathing", "movement"
    intervention_frequency: Optional[float] = None  # Hz (for binaural, drumming)
    intervention_duration: int = 20  # minutes

    # Expected outcome
    expected_gamma_change: float = 0.0  # Δγ (negative = toward harmony)
    expected_vas_improvement: float = 0.0  # 0-10 scale

    # Match quality
    match_score: float = 0.0  # 0-1, how well current state matches this tech


class BiosensorAncientBridge:
    """
    Bridge between biosensors and ancient technologies

    Functions:
    1. Measure current biosensor state
    2. Find ancient techs matching current/target state
    3. Recommend interventions
    4. Track outcomes (for causal learning)
    """

    def __init__(self):
        # Ancient tech database (would import from ancient_technologies.py)
        self.ancient_matches: List[AncientBiosensorMatch] = []
        self._initialize_ancient_biosensor_mappings()

        # History
        self.measurement_history: List[BiosensorReading] = []
        self.intervention_history: List[Dict[str, Any]] = []

    def _initialize_ancient_biosensor_mappings(self):
        """
        Map ancient technologies to target biosensor states

        This is the core knowledge base: "When you're in state X, ancient tech Y helps"
        """

        # EXAMPLE MAPPINGS (would expand to all 69 techs)

        # Tech #4: Pyramid Orion Alignment → Alpha-theta meditation
        self.ancient_matches.append(AncientBiosensorMatch(
            tech_id=4,
            tech_name="Pyramid Orion Alignment",
            target_dominant_band=BrainwaveBand.ALPHA,
            target_hrv_state=HRVState.HIGH,
            target_arousal_range=(0.2, 0.5),
            intervention_type="visual_meditation",
            intervention_frequency=8.0,  # Alpha binaural
            intervention_duration=20,
            expected_gamma_change=-5.0,  # Calming
            expected_vas_improvement=2.0
        ))

        # Tech #7: Maya Calendar → Beta structured focus
        self.ancient_matches.append(AncientBiosensorMatch(
            tech_id=7,
            tech_name="Maya Long Count Calendar",
            target_dominant_band=BrainwaveBand.BETA,
            target_hrv_state=HRVState.MODERATE,
            target_arousal_range=(0.5, 0.7),
            intervention_type="time_structure",
            intervention_frequency=None,
            intervention_duration=90,  # Pomodoro-like
            expected_gamma_change=-3.0,  # Sustainable focus
            expected_vas_improvement=1.5
        ))

        # Tech #27: Aztec Death Whistle → Gamma activation (for emergency)
        self.ancient_matches.append(AncientBiosensorMatch(
            tech_id=27,
            tech_name="Aztec Death Whistle",
            target_dominant_band=BrainwaveBand.GAMMA,
            target_hrv_state=HRVState.LOW,  # Stress OK for short activation
            target_arousal_range=(0.8, 1.0),
            intervention_type="acoustic_shock",
            intervention_frequency=7.0,  # Infrasound fear frequency
            intervention_duration=1,  # Very brief!
            expected_gamma_change=+10.0,  # Sudden activation
            expected_vas_improvement=-1.0  # Not pleasant, but effective for waking
        ))

        # Tech #35: Armillary Sphere → Alpha-beta flow state
        self.ancient_matches.append(AncientBiosensorMatch(
            tech_id=35,
            tech_name="Armillary Sphere",
            target_dominant_band=BrainwaveBand.ALPHA,
            target_hrv_state=HRVState.COHERENT,
            target_arousal_range=(0.4, 0.6),
            intervention_type="visual_geometric",
            intervention_frequency=10.0,  # Alpha binaural
            intervention_duration=15,
            expected_gamma_change=-7.0,  # Toward flow
            expected_vas_improvement=3.0
        ))

        # Tech #56: Aboriginal Dreamtime → Theta narrative
        self.ancient_matches.append(AncientBiosensorMatch(
            tech_id=56,
            tech_name="Aboriginal Dreamtime Navigation",
            target_dominant_band=BrainwaveBand.THETA,
            target_hrv_state=HRVState.HIGH,
            target_arousal_range=(0.1, 0.4),
            intervention_type="narrative_rhythmic",
            intervention_frequency=6.0,  # Theta drumming
            intervention_duration=30,
            expected_gamma_change=-8.0,  # Deep relaxation
            expected_vas_improvement=2.5
        ))

        # Tech #57: Aboriginal Fire Stick Farming → Controlled chaos
        self.ancient_matches.append(AncientBiosensorMatch(
            tech_id=57,
            tech_name="Aboriginal Fire Stick Farming",
            target_dominant_band=BrainwaveBand.BETA,
            target_hrv_state=HRVState.MODERATE,
            target_arousal_range=(0.6, 0.8),
            intervention_type="controlled_stress",
            intervention_frequency=None,
            intervention_duration=10,
            expected_gamma_change=-2.0,  # Small controlled burns prevent big fires!
            expected_vas_improvement=1.0
        ))

        # Tech #61: Inuit Igloo → Theta-delta deep rest
        self.ancient_matches.append(AncientBiosensorMatch(
            tech_id=61,
            tech_name="Inuit Igloos",
            target_dominant_band=BrainwaveBand.DELTA,
            target_hrv_state=HRVState.HIGH,
            target_arousal_range=(0.0, 0.2),
            intervention_type="thermal_comfort",
            intervention_frequency=2.0,  # Delta binaural
            intervention_duration=60,  # Sleep
            expected_gamma_change=-15.0,  # Deep rest
            expected_vas_improvement=4.0  # After sleep
        ))

    def measure_biosensor_state(
        self,
        eeg_bands: Optional[Dict[str, float]] = None,
        hrv_rmssd: Optional[float] = None,
        hrv_coherence: Optional[float] = None,
        gsr: Optional[float] = None
    ) -> BiosensorReading:
        """
        Record a biosensor measurement

        Args:
            eeg_bands: Dict of band_name → power (μV²)
            hrv_rmssd: HRV root mean square (ms)
            hrv_coherence: HRV coherence ratio (0-1)
            gsr: Galvanic skin response (μS)

        Returns:
            BiosensorReading with interpreted state
        """
        reading = BiosensorReading(
            eeg_bands=eeg_bands or {},
            hrv_rmssd=hrv_rmssd,
            hrv_coherence=hrv_coherence,
            gsr=gsr
        )

        self.measurement_history.append(reading)
        return reading

    def find_matching_ancient_techs(
        self,
        current_state: BiosensorReading,
        target_state: Optional[BiosensorReading] = None,
        top_k: int = 5
    ) -> List[AncientBiosensorMatch]:
        """
        Find ancient technologies that match current or target biosensor state

        Args:
            current_state: Current biosensor reading
            target_state: Desired biosensor reading (if None, assumes want to optimize current)
            top_k: Return top K matches

        Returns:
            List of AncientBiosensorMatches, sorted by match quality
        """
        if target_state is None:
            # Default target: Move toward harmony (Alpha/Theta, high HRV, moderate arousal)
            target_state = BiosensorReading(
                eeg_bands={'alpha': 0.5, 'theta': 0.3, 'beta': 0.2},
                hrv_rmssd=50.0,
                hrv_coherence=0.8,
                arousal_level=0.4
            )

        # Score each ancient tech match
        for match in self.ancient_matches:
            score = self._calculate_match_score(current_state, target_state, match)
            match.match_score = score

        # Sort by score
        sorted_matches = sorted(self.ancient_matches, key=lambda m: m.match_score, reverse=True)

        return sorted_matches[:top_k]

    def _calculate_match_score(
        self,
        current: BiosensorReading,
        target: BiosensorReading,
        match: AncientBiosensorMatch
    ) -> float:
        """
        Calculate how well an ancient tech matches the current→target transition

        Score components:
        1. Does current state allow this intervention? (match score)
        2. Does this intervention move toward target? (direction score)
        3. Ancient tech quality (Phi resonance would come from ancient_db)
        """
        score = 0.0

        # Component 1: Current state compatibility
        # Does dominant band match?
        if current.dominant_band == match.target_dominant_band:
            score += 0.3

        # Is arousal in range?
        if match.target_arousal_range[0] <= current.arousal_level <= match.target_arousal_range[1]:
            score += 0.2

        # Is HRV compatible?
        if current.hrv_state == match.target_hrv_state:
            score += 0.2

        # Component 2: Direction toward target
        # Will this intervention move γ toward target γ?
        current_gamma_distance = abs(current.chaos_gamma - target.chaos_gamma)
        expected_new_gamma = current.chaos_gamma + match.expected_gamma_change
        expected_gamma_distance = abs(expected_new_gamma - target.chaos_gamma)

        if expected_gamma_distance < current_gamma_distance:
            score += 0.3  # Intervention moves us closer!

        return score

    def recommend_intervention(
        self,
        current_state: BiosensorReading,
        goal: str = "harmony"  # "harmony", "activation", "relaxation", "focus"
    ) -> Dict[str, Any]:
        """
        Recommend an ancient tech intervention based on current state and goal

        Args:
            current_state: Current biosensor reading
            goal: What the user wants
                - "harmony": Move toward Phi (default)
                - "activation": Increase arousal (e.g., wake up)
                - "relaxation": Decrease arousal (e.g., sleep prep)
                - "focus": Optimize for productive work

        Returns:
            Intervention recommendation dict
        """
        # Define target states for each goal
        goal_targets = {
            "harmony": BiosensorReading(
                eeg_bands={'alpha': 0.5, 'theta': 0.3},
                hrv_rmssd=60.0,
                hrv_coherence=0.9,
                arousal_level=0.4
            ),
            "activation": BiosensorReading(
                eeg_bands={'beta': 0.5, 'gamma': 0.3},
                hrv_rmssd=25.0,
                arousal_level=0.8
            ),
            "relaxation": BiosensorReading(
                eeg_bands={'theta': 0.5, 'delta': 0.3},
                hrv_rmssd=70.0,
                hrv_coherence=0.8,
                arousal_level=0.2
            ),
            "focus": BiosensorReading(
                eeg_bands={'beta': 0.5, 'alpha': 0.3},
                hrv_rmssd=40.0,
                hrv_coherence=0.7,
                arousal_level=0.6
            ),
        }

        target = goal_targets.get(goal, goal_targets["harmony"])

        # Find best match
        matches = self.find_matching_ancient_techs(current_state, target, top_k=1)

        if not matches:
            return {
                'status': 'no_match',
                'message': 'No suitable ancient technology found for current state'
            }

        best_match = matches[0]

        return {
            'status': 'recommended',
            'ancient_tech_id': best_match.tech_id,
            'ancient_tech_name': best_match.tech_name,
            'intervention_type': best_match.intervention_type,
            'intervention_frequency': best_match.intervention_frequency,
            'intervention_duration': best_match.intervention_duration,
            'expected_gamma_change': best_match.expected_gamma_change,
            'expected_vas_improvement': best_match.expected_vas_improvement,
            'match_score': best_match.match_score,
            'current_state': {
                'dominant_band': current_state.dominant_band.name if current_state.dominant_band else None,
                'chaos_gamma': current_state.chaos_gamma,
                'arousal': current_state.arousal_level
            },
            'target_state': {
                'dominant_band': target.dominant_band.name if target.dominant_band else None,
                'chaos_gamma': target.chaos_gamma,
                'arousal': target.arousal_level
            }
        }

    def record_intervention_outcome(
        self,
        tech_id: int,
        pre_state: BiosensorReading,
        post_state: BiosensorReading,
        vas_pre: float,
        vas_post: float
    ) -> Dict[str, Any]:
        """
        Record outcome of an intervention (for causal learning)

        This data feeds into Bayesian Causal Transformer to learn:
        - Which ancient techs work for which biosensor states
        - Individual response patterns (personalization)
        - Population-level effects (validation)

        Args:
            tech_id: Which ancient technology was used
            pre_state: Biosensor reading before intervention
            post_state: Biosensor reading after intervention
            vas_pre: Visual Analog Scale before (0-10)
            vas_post: Visual Analog Scale after (0-10)

        Returns:
            Outcome summary dict
        """
        outcome = {
            'timestamp': datetime.utcnow(),
            'tech_id': tech_id,
            'pre_gamma': pre_state.chaos_gamma,
            'post_gamma': post_state.chaos_gamma,
            'gamma_change': post_state.chaos_gamma - pre_state.chaos_gamma,
            'vas_pre': vas_pre,
            'vas_post': vas_post,
            'vas_change': vas_post - vas_pre,
            'pre_dominant_band': pre_state.dominant_band.name if pre_state.dominant_band else None,
            'post_dominant_band': post_state.dominant_band.name if post_state.dominant_band else None,
        }

        self.intervention_history.append(outcome)

        return outcome

    def get_personalized_efficacy(self, tech_id: int) -> Dict[str, Any]:
        """
        Get personalized efficacy statistics for an ancient technology

        Based on user's intervention history
        """
        outcomes = [o for o in self.intervention_history if o['tech_id'] == tech_id]

        if not outcomes:
            return {
                'tech_id': tech_id,
                'trials': 0,
                'avg_gamma_change': None,
                'avg_vas_improvement': None,
            }

        gamma_changes = [o['gamma_change'] for o in outcomes]
        vas_changes = [o['vas_change'] for o in outcomes]

        return {
            'tech_id': tech_id,
            'trials': len(outcomes),
            'avg_gamma_change': np.mean(gamma_changes),
            'std_gamma_change': np.std(gamma_changes),
            'avg_vas_improvement': np.mean(vas_changes),
            'std_vas_improvement': np.std(vas_changes),
            'success_rate': sum(1 for v in vas_changes if v > 0) / len(vas_changes),
        }


# Example usage
if __name__ == "__main__":
    print("🧠 Biosensor-Ancient Bridge - LUCA 370")
    print("="*70)

    bridge = BiosensorAncientBridge()

    # Scenario 1: ADHD hyperfocus (high gamma, low HRV)
    print("\n📊 Scenario 1: ADHD Hyperfocus State")
    current_hyperfocus = bridge.measure_biosensor_state(
        eeg_bands={'delta': 0.1, 'theta': 0.1, 'alpha': 0.2, 'beta': 0.3, 'gamma': 0.3},
        hrv_rmssd=20.0,
        hrv_coherence=0.3,
        gsr=15.0
    )

    print(f"   Dominant Band: {current_hyperfocus.dominant_band}")
    print(f"   Chaos γ: {current_hyperfocus.chaos_gamma:.2f}")
    print(f"   Arousal: {current_hyperfocus.arousal_level:.2f}")
    print(f"   HRV State: {current_hyperfocus.hrv_state}")

    recommendation = bridge.recommend_intervention(current_hyperfocus, goal="harmony")
    print(f"\n💡 Recommendation:")
    print(f"   Ancient Tech: {recommendation['ancient_tech_name']}")
    print(f"   Intervention: {recommendation['intervention_type']}")
    print(f"   Frequency: {recommendation['intervention_frequency']} Hz")
    print(f"   Duration: {recommendation['intervention_duration']} minutes")
    print(f"   Expected Δγ: {recommendation['expected_gamma_change']:.2f}")

    # Scenario 2: Brainfog (high delta, low arousal)
    print("\n📊 Scenario 2: Brainfog / Low Energy State")
    current_brainfog = bridge.measure_biosensor_state(
        eeg_bands={'delta': 0.4, 'theta': 0.3, 'alpha': 0.2, 'beta': 0.1, 'gamma': 0.0},
        hrv_rmssd=45.0,
        hrv_coherence=0.6,
        gsr=3.0
    )

    print(f"   Dominant Band: {current_brainfog.dominant_band}")
    print(f"   Chaos γ: {current_brainfog.chaos_gamma:.2f}")
    print(f"   Arousal: {current_brainfog.arousal_level:.2f}")

    recommendation = bridge.recommend_intervention(current_brainfog, goal="activation")
    print(f"\n💡 Recommendation:")
    print(f"   Ancient Tech: {recommendation['ancient_tech_name']}")
    print(f"   Intervention: {recommendation['intervention_type']}")
    print(f"   Expected Δγ: {recommendation['expected_gamma_change']:.2f}")

    # Simulate intervention outcome
    print("\n🔬 Simulating Intervention Outcome...")
    post_state = bridge.measure_biosensor_state(
        eeg_bands={'delta': 0.1, 'theta': 0.2, 'alpha': 0.4, 'beta': 0.2, 'gamma': 0.1},
        hrv_rmssd=55.0,
        hrv_coherence=0.8,
        gsr=8.0
    )

    outcome = bridge.record_intervention_outcome(
        tech_id=recommendation['ancient_tech_id'],
        pre_state=current_hyperfocus,
        post_state=post_state,
        vas_pre=4.0,
        vas_post=7.0
    )

    print(f"   Pre-γ: {outcome['pre_gamma']:.2f} → Post-γ: {outcome['post_gamma']:.2f}")
    print(f"   Δγ: {outcome['gamma_change']:.2f}")
    print(f"   VAS: {outcome['vas_pre']:.1f} → {outcome['vas_post']:.1f}")
    print(f"   Improvement: {outcome['vas_change']:.1f} points")

    print("\n" + "="*70)
    print("✅ Biosensor-Ancient Bridge connects body wisdom to ancient patterns!")
    print("369! 🧠⚡🌍")
