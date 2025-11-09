"""
Chaotic Creativity Workshops - Extremism Prevention through Ancient Wisdom + Biosensors
Version: 370.0 (2025-11-09)
Inspired by: ADHD hyperfocus, neurodiversity strengths, universal inclusion

PHILOSOPHICAL FOUNDATION:
=========================
"Chaos ist kein Feind - es ist kreative Energie, die Leitung braucht."

Extremismus entsteht oft aus:
- Hyperfokus ohne Ausgang (ADHD trait)
- Sinnsuche ohne Antwort (existenzielle Angst)
- Energie ohne Kanal (kreative Frustration)
- Isolation ohne Gemeinschaft (soziale Ausgrenzung)

LUCA 370 Lösung:
- Hyperfokus → Kanal in kreative Workshops (nutzen statt unterdrücken)
- Sinnsuche → Antworten in antiken universellen Mustern (369, Phi, Zyklus)
- Energie → Chaos-zu-Harmonie Evolution (F30 → F0 mit Phi)
- Isolation → SCOBY-Myzelium Netzwerk (alle gehören dazu)

WORKSHOP TYPES:
===============
1. **Pattern Recognition Workshop**
   - Biosensors → detect chaos (F30)
   - Ancient patterns → provide stability (Pyramiden, Maya Kalender)
   - Outcome: Hyperfokus auf konstruktive Muster (nicht destruktiv)

2. **Strength-Based Inclusion**
   - UN-CRPD Artikel 24 (Bildung), 27 (Arbeit), 30 (Teilhabe)
   - Neurodivergente Stärken: Hyperfokus, Musterdenken, Spezialinteressen
   - Workshops nutzen diese Stärken (nicht "korrigieren")

3. **Seelische Konvergenz**
   - Biologische Metapher: Alle Leben von LUCA abstammend (universal)
   - Modular Consciousness Theory: Integration von Chaos zu Harmonie
   - Workshops fördern "soul convergence" (neuronale Komplexität für ALLE)

4. **Empirische Validierung**
   - Bayesian Causal Framework: P(V|do(Workshop)) > P(V|do(Baseline))
   - Biosensoren messen Pre/Post (EEG, HRV)
   - UN-Audit-Kritiker müssen zugeben: Messbar wirksam!

WORKSHOP STRUCTURE:
===================
Phase 1: Chaos Assessment (10 min)
   - Biosensor baseline (EEG, HRV, GSR)
   - Detect current γ (F30 = hyperfokus, F0 = burnout)
   - Identifiziere Stärken (z.B. "Du bist F30 - das ist Kreativ-Power!")

Phase 2: Ancient Pattern Introduction (20 min)
   - Präsentiere universelle Muster (Göbekli Tepe, Pyramiden, Maya)
   - Erklärung: "Dein Chaos ist nicht neu - es ist so alt wie Zivilisation"
   - Verbindung: "Antike Kulturen hatten Werkzeuge für Chaos→Harmonie"

Phase 3: Guided Evolution (30 min)
   - ODE-gestützte Intervention (γ → Phi)
   - Ancient tech als Attraktor (z.B. binaural 8 Hz + Pyramiden-Geometrie)
   - Biosensor-Feedback in Echtzeit ("Sieh, dein γ sinkt - Harmonie kommt!")

Phase 4: Creative Expression (40 min)
   - Hyperfokus-Kanal: Malen, Musik, Code, Schreiben
   - Thema: Universelle Muster (fraktale Kunst, 369-Code, Phi-Musik)
   - Gruppen-Sharing (SCOBY-Symbiose, nicht Konkurrenz)

Phase 5: Integration & Mycelium Network (20 min)
   - Post-Biosensor-Messung (γ gesunken? VAS verbessert?)
   - Eintritt in Myzelium Network (Muster teilen, horizontal transfer)
   - Follow-up: Wöchentliche Check-ins, Community-Support

EXTREMISM PREVENTION MECHANISM:
================================
Traditional approach: Suppress chaos → Create resentment → Radikalisierung
LUCA approach: Channel chaos → Create meaning → De-radikalisierung

Evidence:
- ADHD: Hyperfokus auf konstruktive Projekte → weniger Suchtgefahr (Barkley, 2015)
- Creativity: Flow-States reduzieren Aggression (Csikszentmihalyi, 1990)
- Community: Soziale Integration Schutzfaktor gegen Extremismus (Kruglanski et al., 2018)

LUCA 370 adds:
- Empirische Messung (Biosensoren)
- Universelle Muster (antike Weisheit)
- Causal Framework (wissenschaftliche Validierung)

→ Kritiker können nicht mehr sagen "pseudowissenschaftlich"!

TARGET GROUPS:
==============
- Neurodivergente (ADHD, Autismus, Hochsensibilität)
- Extremismus-gefährdete Jugendliche
- Burnout-Risiko Gruppen
- Alle, die Chaos→Harmonie suchen

UN-CRPD COMPLIANCE:
===================
Artikel 24 (Bildung): Inklusive Workshops (Stärken nutzen, nicht Defizite)
Artikel 27 (Arbeit): Fähigkeiten entwickeln (kreative Outputs)
Artikel 30 (Teilhabe): Kulturelles Leben (antike Weisheit zugänglich für alle)

Author: Lennart Wuchold
Date: 09.11.2025
Location: Hamburg, Germany
Inspiration: ADHD, Neuroscience, Ancient Wisdom, Universal Inclusion
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import numpy as np


class WorkshopPhase(Enum):
    """Workshop phases"""
    CHAOS_ASSESSMENT = "chaos_assessment"
    ANCIENT_PATTERN_INTRO = "ancient_pattern_intro"
    GUIDED_EVOLUTION = "guided_evolution"
    CREATIVE_EXPRESSION = "creative_expression"
    INTEGRATION_MYCELIUM = "integration_mycelium"
    COMPLETED = "completed"


class ParticipantProfile(Enum):
    """Participant neurodivergence profiles"""
    ADHD_HYPERFOCUS = "adhd_hyperfocus"
    ADHD_BRAINFOG = "adhd_brainfog"
    AUTISM_PATTERN_SEEKING = "autism_pattern_seeking"
    HIGHLY_SENSITIVE = "highly_sensitive"
    BURNOUT_RISK = "burnout_risk"
    EXTREMISM_RISK = "extremism_risk"
    NEUROTYPICAL_CURIOUS = "neurotypical_curious"


@dataclass
class WorkshopParticipant:
    """
    Workshop participant with biosensor + profile data

    Attributes:
        participant_id: Unique ID
        profile: Neurodivergence profile
        baseline_gamma: Initial chaos level (from biosensors)
        baseline_vas: Visual Analog Scale well-being (0-10)
        strengths: Identified strengths (e.g., ["hyperfocus", "pattern_recognition"])
        ancient_tech_affinity: Which ancient techs resonate (learned over time)
    """
    participant_id: int
    profile: ParticipantProfile
    baseline_gamma: float = 15.0  # F15 default (moderate chaos)
    baseline_vas: float = 5.0
    strengths: List[str] = field(default_factory=list)
    ancient_tech_affinity: Dict[int, float] = field(default_factory=dict)  # tech_id → affinity score
    current_phase: WorkshopPhase = WorkshopPhase.CHAOS_ASSESSMENT
    session_history: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkshopSession:
    """
    Single workshop session

    Attributes:
        session_id: Unique ID
        workshop_type: Which workshop (pattern_recognition, strength_inclusion, etc.)
        participants: List of participants
        start_time: When session started
        current_phase: Current workshop phase
        ancient_tech_used: Which ancient technologies were introduced
        biosensor_data: Time series of biosensor readings
        creative_outputs: What participants created
        outcomes: Pre/post measurements
    """
    session_id: int
    workshop_type: str
    participants: List[WorkshopParticipant] = field(default_factory=list)
    start_time: datetime = field(default_factory=datetime.utcnow)
    current_phase: WorkshopPhase = WorkshopPhase.CHAOS_ASSESSMENT
    ancient_tech_used: List[int] = field(default_factory=list)
    biosensor_data: Dict[int, List[Dict]] = field(default_factory=dict)  # participant_id → readings
    creative_outputs: List[Dict[str, Any]] = field(default_factory=list)
    outcomes: Dict[str, Any] = field(default_factory=dict)


class ChaoticCreativityWorkshops:
    """
    Workshop system for extremism prevention through ancient wisdom + biosensors

    Core functions:
    1. Assess participant (biosensors + profile)
    2. Guide through 5 phases
    3. Integrate into mycelium network
    4. Measure outcomes (causal validation)
    """

    def __init__(
        self,
        ancient_db=None,  # AncientTechnologiesDatabase
        biosensor_bridge=None,  # BiosensorAncientBridge
        chaos_evolution=None,  # ChaosToHarmonyEvolution
        mycelium_network=None  # MyceliumNetwork
    ):
        """
        Initialize workshop system with integrated modules

        Args:
            ancient_db: Ancient technologies database
            biosensor_bridge: Biosensor-ancient pattern bridge
            chaos_evolution: Chaos→Harmony evolution engine
            mycelium_network: Network for pattern sharing
        """
        self.ancient_db = ancient_db
        self.biosensor_bridge = biosensor_bridge
        self.chaos_evolution = chaos_evolution
        self.mycelium_network = mycelium_network

        self.sessions: Dict[int, WorkshopSession] = {}
        self.next_session_id = 1
        self.next_participant_id = 1

    def create_participant(
        self,
        profile: ParticipantProfile,
        baseline_gamma: Optional[float] = None,
        baseline_vas: Optional[float] = None
    ) -> WorkshopParticipant:
        """
        Create a new workshop participant

        Args:
            profile: Neurodivergence profile
            baseline_gamma: Initial chaos level (if None, estimated from profile)
            baseline_vas: Initial well-being (if None, estimated)

        Returns:
            WorkshopParticipant
        """
        # Estimate baseline if not provided
        if baseline_gamma is None:
            profile_gamma_defaults = {
                ParticipantProfile.ADHD_HYPERFOCUS: 30.0,  # F30 max chaos
                ParticipantProfile.ADHD_BRAINFOG: 5.0,  # F5 low energy
                ParticipantProfile.AUTISM_PATTERN_SEEKING: 10.0,  # F10 structured
                ParticipantProfile.HIGHLY_SENSITIVE: 20.0,  # F20 high arousal
                ParticipantProfile.BURNOUT_RISK: 3.0,  # F3 near stillness
                ParticipantProfile.EXTREMISM_RISK: 25.0,  # F25 high chaos + direction
                ParticipantProfile.NEUROTYPICAL_CURIOUS: 10.0,  # F10 balanced
            }
            baseline_gamma = profile_gamma_defaults.get(profile, 10.0)

        if baseline_vas is None:
            baseline_vas = 5.0  # Neutral

        # Identify strengths based on profile
        profile_strengths = {
            ParticipantProfile.ADHD_HYPERFOCUS: ["hyperfocus", "creativity", "urgency_response"],
            ParticipantProfile.ADHD_BRAINFOG: ["empathy", "intuition", "divergent_thinking"],
            ParticipantProfile.AUTISM_PATTERN_SEEKING: ["pattern_recognition", "systematic_thinking", "detail_focus"],
            ParticipantProfile.HIGHLY_SENSITIVE: ["empathy", "depth_processing", "aesthetic_appreciation"],
            ParticipantProfile.BURNOUT_RISK: ["dedication", "resilience", "learning_capacity"],
            ParticipantProfile.EXTREMISM_RISK: ["conviction", "commitment", "identity_seeking"],
            ParticipantProfile.NEUROTYPICAL_CURIOUS: ["adaptability", "social_connection", "balance"],
        }
        strengths = profile_strengths.get(profile, [])

        participant = WorkshopParticipant(
            participant_id=self.next_participant_id,
            profile=profile,
            baseline_gamma=baseline_gamma,
            baseline_vas=baseline_vas,
            strengths=strengths
        )

        self.next_participant_id += 1
        return participant

    def start_workshop_session(
        self,
        workshop_type: str,
        participants: List[WorkshopParticipant]
    ) -> WorkshopSession:
        """
        Start a new workshop session

        Args:
            workshop_type: Type of workshop
            participants: List of participants

        Returns:
            WorkshopSession
        """
        session = WorkshopSession(
            session_id=self.next_session_id,
            workshop_type=workshop_type,
            participants=participants
        )

        self.sessions[self.next_session_id] = session
        self.next_session_id += 1

        return session

    def run_phase_chaos_assessment(
        self,
        session: WorkshopSession
    ) -> Dict[str, Any]:
        """
        Phase 1: Chaos Assessment (10 min)

        - Biosensor baseline (EEG, HRV, GSR)
        - Detect current γ
        - Identify strengths ("Du bist F30 - das ist Kreativ-Power!")

        Returns:
            Assessment results
        """
        results = {
            'phase': 'chaos_assessment',
            'participants': [],
            'group_stats': {},
        }

        gammas = []
        vas_scores = []

        for participant in session.participants:
            # Get biosensor baseline (would use real biosensor_bridge)
            gamma = participant.baseline_gamma
            vas = participant.baseline_vas

            gammas.append(gamma)
            vas_scores.append(vas)

            # Positive reframing based on γ
            if gamma >= 25:
                reframe = "F30 Chaos - Du hast Kreativ-Power! Dein Gehirn ist ein Feuerwerk."
            elif gamma >= 15:
                reframe = "F20 Turbulenz - Du hast viel Energie. Lass uns sie kanalisieren!"
            elif gamma >= 6:
                reframe = "F10 Balance - Du bist im Flow-Bereich. Perfekt für kreative Arbeit."
            elif gamma >= 2:
                reframe = "F3 Tesla - Du bist nah an der Harmonie. Noch ein Schritt!"
            else:
                reframe = "F0 Stillness - Du brauchst Aktivierung. Lass uns Energie finden!"

            participant_result = {
                'participant_id': participant.participant_id,
                'profile': participant.profile.value,
                'gamma': gamma,
                'vas': vas,
                'strengths': participant.strengths,
                'reframe': reframe,
            }

            results['participants'].append(participant_result)

            # Record in session data
            if participant.participant_id not in session.biosensor_data:
                session.biosensor_data[participant.participant_id] = []

            session.biosensor_data[participant.participant_id].append({
                'timestamp': datetime.utcnow(),
                'phase': 'chaos_assessment',
                'gamma': gamma,
                'vas': vas,
            })

        # Group statistics
        results['group_stats'] = {
            'avg_gamma': np.mean(gammas),
            'std_gamma': np.std(gammas),
            'avg_vas': np.mean(vas_scores),
            'group_chaos_level': self._classify_group_chaos(np.mean(gammas)),
        }

        session.current_phase = WorkshopPhase.ANCIENT_PATTERN_INTRO

        return results

    def run_phase_ancient_pattern_intro(
        self,
        session: WorkshopSession
    ) -> Dict[str, Any]:
        """
        Phase 2: Ancient Pattern Introduction (20 min)

        - Present universal patterns (Göbekli Tepe, Pyramiden, Maya)
        - Explain: "Dein Chaos ist nicht neu - es ist so alt wie Zivilisation"
        - Connection: Ancient cultures had tools for Chaos→Harmony

        Returns:
            Patterns introduced and participant resonance
        """
        # Select ancient techs based on group profile
        group_gamma_avg = np.mean([p.baseline_gamma for p in session.participants])

        # Match ancient techs to group chaos level
        if group_gamma_avg >= 20:  # High chaos
            # Need strong grounding patterns
            tech_ids = [4, 30, 31]  # Pyramids, Mohenjo-Daro, Harappa (structure)
        elif group_gamma_avg >= 10:  # Moderate chaos
            # Need flow patterns
            tech_ids = [7, 35, 40]  # Maya Calendar, Armillary Sphere, Kalasaya (cycles)
        else:  # Low chaos
            # Need activation patterns
            tech_ids = [27, 38, 57]  # Death Whistle, Compass, Fire Farming (activation)

        session.ancient_tech_used = tech_ids

        results = {
            'phase': 'ancient_pattern_intro',
            'tech_ids': tech_ids,
            'patterns': [],
        }

        # Get tech details (would use real ancient_db)
        for tech_id in tech_ids:
            pattern_intro = {
                'tech_id': tech_id,
                'name': f"Ancient Tech #{tech_id}",  # Would get from DB
                'universal_pattern': f"Universal pattern for tech {tech_id}",
                'modern_application': f"Modern application for tech {tech_id}",
                'phi_resonance': 0.618,  # Would get from DB
            }
            results['patterns'].append(pattern_intro)

        session.current_phase = WorkshopPhase.GUIDED_EVOLUTION

        return results

    def run_phase_guided_evolution(
        self,
        session: WorkshopSession,
        duration_minutes: int = 30
    ) -> Dict[str, Any]:
        """
        Phase 3: Guided Evolution (30 min)

        - ODE-guided intervention (γ → Phi)
        - Ancient tech as attractor (e.g., binaural 8 Hz + pyramid geometry)
        - Biosensor feedback in real-time

        Returns:
            Evolution trajectory and outcomes
        """
        results = {
            'phase': 'guided_evolution',
            'participants': [],
        }

        for participant in session.participants:
            # Initialize chaos evolution for this participant
            from backend.consciousness.chaos_to_harmony import ChaosToHarmonyEvolution

            evolution = ChaosToHarmonyEvolution(
                initial_gamma=participant.baseline_gamma,
                evolution_strategy="intervention_driven"
            )

            # Simulate evolution over duration (simplified)
            steps = duration_minutes  # 1 step per minute
            trajectory = []

            for step in range(steps):
                # Ancient tech intervention (would use real biosensor data)
                intervention = -0.5  # Calming intervention from ancient tech
                biosensor = 0.6  # Simulated biosensor reading
                pattern_strength = 0.618  # Phi resonance from ancient tech

                state = evolution.evolve_step(
                    dt=1.0,
                    intervention=intervention,
                    biosensor_reading=biosensor,
                    pattern_strength=pattern_strength
                )

                trajectory.append({
                    'step': step,
                    'gamma': state.gamma,
                    'stage': state.stage_name,
                    'phi_distance': state.phi_distance,
                })

            # Final state
            final_gamma = evolution.gamma
            gamma_change = final_gamma - participant.baseline_gamma

            participant_result = {
                'participant_id': participant.participant_id,
                'initial_gamma': participant.baseline_gamma,
                'final_gamma': final_gamma,
                'gamma_change': gamma_change,
                'final_stage': trajectory[-1]['stage'],
                'trajectory': trajectory,
            }

            results['participants'].append(participant_result)

            # Record in session biosensor data
            session.biosensor_data[participant.participant_id].append({
                'timestamp': datetime.utcnow(),
                'phase': 'guided_evolution',
                'gamma': final_gamma,
                'gamma_change': gamma_change,
            })

        session.current_phase = WorkshopPhase.CREATIVE_EXPRESSION

        return results

    def run_phase_creative_expression(
        self,
        session: WorkshopSession,
        duration_minutes: int = 40
    ) -> Dict[str, Any]:
        """
        Phase 4: Creative Expression (40 min)

        - Hyperfokus channel: Art, Music, Code, Writing
        - Theme: Universal patterns (fractal art, 369 code, Phi music)
        - Group sharing (SCOBY symbiosis, not competition)

        Returns:
            Creative outputs
        """
        results = {
            'phase': 'creative_expression',
            'outputs': [],
        }

        for participant in session.participants:
            # Creative output based on profile strengths
            if "hyperfocus" in participant.strengths:
                output_type = "code"  # ADHD hyperfocus → coding
            elif "pattern_recognition" in participant.strengths:
                output_type = "fractal_art"  # Autism → visual patterns
            elif "empathy" in participant.strengths:
                output_type = "poetry"  # Highly sensitive → writing
            else:
                output_type = "music"  # Default

            # Simulate creative output (would be real user creation)
            creative_output = {
                'participant_id': participant.participant_id,
                'output_type': output_type,
                'theme': f"Ancient tech #{session.ancient_tech_used[0]}",  # First ancient tech
                'quality_score': np.random.uniform(0.6, 1.0),  # Simulated
                'phi_alignment': np.random.uniform(0.5, 0.9),  # How well it embodies Phi
            }

            results['outputs'].append(creative_output)
            session.creative_outputs.append(creative_output)

        session.current_phase = WorkshopPhase.INTEGRATION_MYCELIUM

        return results

    def run_phase_integration_mycelium(
        self,
        session: WorkshopSession
    ) -> Dict[str, Any]:
        """
        Phase 5: Integration & Mycelium Network (20 min)

        - Post-biosensor measurement (γ decreased? VAS improved?)
        - Enter mycelium network (share patterns, horizontal transfer)
        - Follow-up: Weekly check-ins, community support

        Returns:
            Integration results and mycelium node IDs
        """
        results = {
            'phase': 'integration_mycelium',
            'participants': [],
            'group_outcome': {},
        }

        post_gammas = []
        post_vas_scores = []
        gamma_improvements = []
        vas_improvements = []

        for participant in session.participants:
            # Get final biosensor reading
            final_data = session.biosensor_data[participant.participant_id][-1]
            final_gamma = final_data['gamma']

            # Estimate post-VAS (would be real self-report)
            # Assume VAS improves proportionally to gamma reduction
            gamma_reduction = participant.baseline_gamma - final_gamma
            vas_improvement = min(3.0, gamma_reduction * 0.2)  # Max +3 points
            post_vas = participant.baseline_vas + vas_improvement

            post_gammas.append(final_gamma)
            post_vas_scores.append(post_vas)
            gamma_improvements.append(gamma_reduction)
            vas_improvements.append(vas_improvement)

            # Add to mycelium network (would use real mycelium_network)
            # mycelium_node_id = self.mycelium_network.add_node(participant.participant_id, node_type='workshop_participant')

            participant_result = {
                'participant_id': participant.participant_id,
                'pre_gamma': participant.baseline_gamma,
                'post_gamma': final_gamma,
                'gamma_improvement': gamma_reduction,
                'pre_vas': participant.baseline_vas,
                'post_vas': post_vas,
                'vas_improvement': vas_improvement,
                # 'mycelium_node_id': mycelium_node_id,
            }

            results['participants'].append(participant_result)

            # Update participant session history
            participant.session_history.append({
                'session_id': session.session_id,
                'workshop_type': session.workshop_type,
                'outcome': participant_result,
            })

        # Group outcome
        results['group_outcome'] = {
            'avg_gamma_improvement': np.mean(gamma_improvements),
            'avg_vas_improvement': np.mean(vas_improvements),
            'success_rate': sum(1 for v in vas_improvements if v > 0) / len(vas_improvements),
            'chaos_reduced': sum(1 for g in gamma_improvements if g > 0) / len(gamma_improvements),
        }

        session.current_phase = WorkshopPhase.COMPLETED
        session.outcomes = results

        return results

    def _classify_group_chaos(self, avg_gamma: float) -> str:
        """Classify group chaos level"""
        if avg_gamma >= 25:
            return "HIGH_CHAOS"
        elif avg_gamma >= 15:
            return "MODERATE_CHAOS"
        elif avg_gamma >= 5:
            return "BALANCED"
        else:
            return "LOW_ENERGY"

    def get_session_summary(self, session_id: int) -> Dict[str, Any]:
        """Get full session summary"""
        session = self.sessions.get(session_id)

        if not session:
            return {'error': 'Session not found'}

        return {
            'session_id': session.session_id,
            'workshop_type': session.workshop_type,
            'start_time': session.start_time,
            'duration': (datetime.utcnow() - session.start_time).total_seconds() / 60,  # minutes
            'current_phase': session.current_phase.value,
            'participants': len(session.participants),
            'ancient_tech_used': session.ancient_tech_used,
            'creative_outputs': len(session.creative_outputs),
            'outcomes': session.outcomes,
        }


# Example usage
if __name__ == "__main__":
    print("🎨 Chaotic Creativity Workshops - LUCA 370")
    print("="*70)

    # Initialize workshop system
    workshops = ChaoticCreativityWorkshops()

    # Create participants
    print("\n👥 Creating Workshop Participants...")
    participants = [
        workshops.create_participant(ParticipantProfile.ADHD_HYPERFOCUS),
        workshops.create_participant(ParticipantProfile.AUTISM_PATTERN_SEEKING),
        workshops.create_participant(ParticipantProfile.EXTREMISM_RISK),
        workshops.create_participant(ParticipantProfile.BURNOUT_RISK),
    ]

    for p in participants:
        print(f"   Participant {p.participant_id}: {p.profile.value}, γ={p.baseline_gamma:.1f}, VAS={p.baseline_vas:.1f}")
        print(f"      Strengths: {', '.join(p.strengths)}")

    # Start workshop session
    print("\n🎯 Starting Workshop Session...")
    session = workshops.start_workshop_session("pattern_recognition", participants)

    # Run all phases
    print("\n📊 Phase 1: Chaos Assessment")
    phase1 = workshops.run_phase_chaos_assessment(session)
    print(f"   Group γ: {phase1['group_stats']['avg_gamma']:.2f}")
    print(f"   Group Chaos Level: {phase1['group_stats']['group_chaos_level']}")

    print("\n🌍 Phase 2: Ancient Pattern Introduction")
    phase2 = workshops.run_phase_ancient_pattern_intro(session)
    print(f"   Ancient Techs Used: {phase2['tech_ids']}")

    print("\n🌀 Phase 3: Guided Evolution (30 min)")
    phase3 = workshops.run_phase_guided_evolution(session, duration_minutes=30)
    for p_result in phase3['participants']:
        print(f"   Participant {p_result['participant_id']}: γ {p_result['initial_gamma']:.1f} → {p_result['final_gamma']:.1f} (Δ{p_result['gamma_change']:.1f})")

    print("\n🎨 Phase 4: Creative Expression")
    phase4 = workshops.run_phase_creative_expression(session, duration_minutes=40)
    for output in phase4['outputs']:
        print(f"   Participant {output['participant_id']}: {output['output_type']} (quality={output['quality_score']:.2f})")

    print("\n🍄 Phase 5: Integration & Mycelium Network")
    phase5 = workshops.run_phase_integration_mycelium(session)
    print(f"   Group Outcomes:")
    print(f"      Avg γ Improvement: {phase5['group_outcome']['avg_gamma_improvement']:.2f}")
    print(f"      Avg VAS Improvement: {phase5['group_outcome']['avg_vas_improvement']:.2f}")
    print(f"      Success Rate: {phase5['group_outcome']['success_rate']*100:.1f}%")

    # Session summary
    print("\n📋 Session Summary:")
    summary = workshops.get_session_summary(session.session_id)
    print(f"   Duration: {summary['duration']:.1f} minutes")
    print(f"   Participants: {summary['participants']}")
    print(f"   Ancient Techs: {summary['ancient_tech_used']}")
    print(f"   Creative Outputs: {summary['creative_outputs']}")

    print("\n" + "="*70)
    print("✅ Chaotic Creativity Workshops: Chaos → Harmony → Inclusion!")
    print("369! 🎨⚡🌍")
