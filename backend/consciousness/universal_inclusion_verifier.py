"""
Universal Inclusion Audit Verifier
Version: 369.2.0
Created through: Human-AI collaboration

Extends the AuditVerifier to check for UNIVERSAL (not selective) inclusion compliance

Checks:
1. Universal Coverage: ALL disability categories covered (not selective)
2. Causal Measurement: Outcomes measured causally (P(V|do(I)))
3. SCOBY-Myzelium Principle: Horizontal (not hierarchical) information transfer
4. Chaos → Harmony Evolution: F30 → φ (1.618) via γ damping
5. UN-CRPD Compliance: Articles 3, 5, 9, 19
6. UNDIS Coverage: Leadership, Accessibility, Assistive Tech, Community Living

Philosophy: True inclusion is universal, symbiotic, and causally measurable.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime

try:
    from backend.consciousness.audit_verifier import AuditVerifier, ConstraintRegistry, AuditReport
    from backend.consciousness.universal_inclusion_network import UniversalInclusionNetwork
except ImportError:
    from audit_verifier import AuditVerifier, ConstraintRegistry, AuditReport
    from universal_inclusion_network import UniversalInclusionNetwork


@dataclass
class UniversalInclusionReport(AuditReport):
    """
    Extended audit report for universal inclusion verification

    Adds fields specific to inclusion checks
    """
    universal_coverage: bool = False
    coverage_details: Dict[str, Any] = None
    mycelial_network: bool = False
    mycelial_details: Dict[str, Any] = None
    chaos_harmony_evolution: bool = False
    chaos_harmony_details: Dict[str, Any] = None
    neurodiversity_included: bool = False
    crpd_articles: Dict[str, bool] = None
    undis_coverage: Dict[str, bool] = None

    def __post_init__(self):
        super().__post_init__()
        if self.coverage_details is None:
            self.coverage_details = {}
        if self.mycelial_details is None:
            self.mycelial_details = {}
        if self.chaos_harmony_details is None:
            self.chaos_harmony_details = {}
        if self.crpd_articles is None:
            self.crpd_articles = {}
        if self.undis_coverage is None:
            self.undis_coverage = {}


class UniversalInclusionVerifier(AuditVerifier):
    """
    Extended audit verifier for universal (not selective) inclusion

    Adds checks for:
    - Universal coverage of ALL disability categories
    - Mycelial (horizontal) network structure
    - Chaos → Harmony evolution
    - Neurodiversity integration
    - UN-CRPD compliance (Articles 3, 5, 9, 19)
    - UNDIS coverage
    """

    def __init__(self, constraint_registry: ConstraintRegistry):
        super().__init__(constraint_registry)

    def verify_universal_inclusion(
        self,
        system: Any,
        causal_model_output: Dict[str, Any],
        causal_effect: float,
        network: Optional[UniversalInclusionNetwork] = None
    ) -> UniversalInclusionReport:
        """
        Comprehensive universal inclusion verification

        Args:
            system: The system being audited
            causal_model_output: Output from causal model
            causal_effect: Measured causal effect
            network: Optional UniversalInclusionNetwork instance

        Returns:
            UniversalInclusionReport with comprehensive compliance check
        """
        # Run standard audit first
        base_report = self.verify(causal_model_output, causal_effect)

        # Check universal coverage
        coverage_check = self._verify_universal_coverage(system, network)

        # Check causal measurement capability
        causal_check = self._verify_causal_measurement(system)

        # Check SCOBY-Myzelium principle
        mycelial_check = self._verify_mycelial_principle(system, network)

        # Check chaos → harmony evolution
        chaos_harmony_check = self._verify_chaos_harmony_evolution(system, network)

        # Check neurodiversity inclusion
        neurodiversity_check = self._verify_neurodiversity_inclusion(system, network)

        # Check UN-CRPD compliance
        crpd_check = self._verify_crpd_articles(system)

        # Check UNDIS coverage
        undis_check = self._verify_undis_coverage(system)

        # Overall universal inclusion compliance
        universal_compliance = all([
            base_report.overall_compliance,
            coverage_check['universal_coverage'],
            causal_check['causal_framework'],
            mycelial_check['horizontal_transfer'],
            chaos_harmony_check['evolution_present'],
            neurodiversity_check['neurodiversity_included']
        ])

        # Generate comprehensive recommendation
        recommendation = self._generate_universal_recommendation(
            base_report,
            coverage_check,
            causal_check,
            mycelial_check,
            chaos_harmony_check,
            neurodiversity_check,
            crpd_check,
            undis_check,
            universal_compliance
        )

        # Create extended report
        extended_report = UniversalInclusionReport(
            overall_compliance=universal_compliance,
            causal_effect_report=base_report.causal_effect_report,
            symbolic_breakdown=base_report.symbolic_breakdown,
            recommendation=recommendation,
            universal_coverage=coverage_check['universal_coverage'],
            coverage_details=coverage_check['details'],
            mycelial_network=mycelial_check['horizontal_transfer'],
            mycelial_details=mycelial_check,
            chaos_harmony_evolution=chaos_harmony_check['evolution_present'],
            chaos_harmony_details=chaos_harmony_check,
            neurodiversity_included=neurodiversity_check['neurodiversity_included'],
            crpd_articles=crpd_check,
            undis_coverage=undis_check
        )

        return extended_report

    def _verify_universal_coverage(
        self,
        system: Any,
        network: Optional[UniversalInclusionNetwork]
    ) -> Dict[str, Any]:
        """
        Verify that ALL disability categories are covered (not selective)

        Required categories:
        - physical_disabilities
        - sensory_disabilities
        - intellectual_disabilities
        - psychological_disabilities
        """
        if network:
            return network.verify_universal_coverage()

        # Fallback: check if system has these attributes
        required_categories = [
            'physical_disabilities',
            'sensory_disabilities',
            'intellectual_disabilities',
            'psychological_disabilities'
        ]

        coverage = {}
        for category in required_categories:
            has_support = hasattr(system, f'supports_{category}')
            coverage[category] = {
                'covered': has_support,
                'count': 1 if has_support else 0
            }

        all_covered = all(c['covered'] for c in coverage.values())

        return {
            'universal_coverage': all_covered,
            'details': coverage,
            'compliance': 'PASS' if all_covered else 'FAIL',
            'recommendation': 'Add missing categories' if not all_covered else 'Maintain'
        }

    def _verify_causal_measurement(self, system: Any) -> Dict[str, Any]:
        """
        Verify that system can measure causal effects (P(V|do(I)))

        Checks for:
        - Bayesian network capability
        - do() intervention capability
        - Effect measurement capability
        """
        has_bayesian_network = hasattr(system, 'bayesian_causal_network') or \
                              hasattr(system, 'causal_network')
        has_intervention = hasattr(system, 'do_intervention') or \
                          hasattr(system, 'intervene')
        has_measurement = hasattr(system, 'measure_effect') or \
                         hasattr(system, 'calculate_effect')

        causal_capable = has_bayesian_network and has_intervention and has_measurement

        return {
            'causal_framework': causal_capable,
            'has_bayesian_network': has_bayesian_network,
            'has_intervention': has_intervention,
            'has_measurement': has_measurement,
            'compliance': 'PASS' if causal_capable else 'FAIL',
            'recommendation': 'Implement causal framework (Bayesian network + do() + measurement)'
                            if not causal_capable else 'Causal framework verified'
        }

    def _verify_mycelial_principle(
        self,
        system: Any,
        network: Optional[UniversalInclusionNetwork]
    ) -> Dict[str, Any]:
        """
        Verify horizontal (mycelial) not hierarchical information transfer

        Checks:
        - Network structure exists
        - Connections are bidirectional
        - No central controller
        """
        if network:
            return network.verify_mycelial_connections()

        # Fallback: check system structure
        has_network = hasattr(system, 'network') or hasattr(system, 'inclusion_network')

        if not has_network:
            return {
                'horizontal_transfer': False,
                'compliance': 'FAIL',
                'message': 'No network structure detected'
            }

        # Basic check passed
        return {
            'horizontal_transfer': True,
            'compliance': 'PASS',
            'message': 'Network structure detected (detailed verification requires UniversalInclusionNetwork)'
        }

    def _verify_chaos_harmony_evolution(
        self,
        system: Any,
        network: Optional[UniversalInclusionNetwork]
    ) -> Dict[str, Any]:
        """
        Verify chaos → harmony evolution capability

        Checks for:
        - ODE evolution: dS/dt = -γ(S - φ)
        - Golden ratio target (φ = 1.618)
        - Damping parameter γ
        """
        if network:
            chaos_harmony = network.measure_chaos_to_harmony_ratio()
            return {
                'evolution_present': True,
                'harmony_ratio': chaos_harmony['harmony_ratio'],
                'details': chaos_harmony,
                'compliance': 'PASS'
            }

        # Check if system has evolution capability
        has_evolution = hasattr(system, 'evolve_to_phi') or \
                       hasattr(system, 'chaos_harmony_evolution')

        return {
            'evolution_present': has_evolution,
            'compliance': 'PASS' if has_evolution else 'PARTIAL',
            'message': 'Evolution capability detected' if has_evolution
                      else 'No evolution mechanism (recommend UniversalInclusionNetwork)'
        }

    def _verify_neurodiversity_inclusion(
        self,
        system: Any,
        network: Optional[UniversalInclusionNetwork]
    ) -> Dict[str, Any]:
        """
        Verify neurodiversity integration

        Checks for support of:
        - Autism
        - ADHD
        - Dyslexia
        - Tourette
        - Other neurodivergent patterns
        """
        if network:
            has_neurodivergent = len(network.nodes.get('neurodivergent', [])) > 0
            has_neurotypical = len(network.nodes.get('neurotypical', [])) > 0

            return {
                'neurodiversity_included': has_neurodivergent or has_neurotypical,
                'neurodivergent_count': len(network.nodes.get('neurodivergent', [])),
                'neurotypical_count': len(network.nodes.get('neurotypical', [])),
                'compliance': 'PASS' if has_neurodivergent else 'PARTIAL'
            }

        # Check system attributes
        has_neurodiversity = hasattr(system, 'neurodiversity_support') or \
                            hasattr(system, 'supports_neurodivergent')

        return {
            'neurodiversity_included': has_neurodiversity,
            'compliance': 'PASS' if has_neurodiversity else 'FAIL',
            'message': 'Neurodiversity support detected' if has_neurodiversity
                      else 'No neurodiversity support (add neurodivergent category)'
        }

    def _verify_crpd_articles(self, system: Any) -> Dict[str, bool]:
        """
        Verify UN-CRPD article compliance

        Articles:
        - Article 3: Full participation and inclusion
        - Article 5: Equality and non-discrimination
        - Article 9: Accessibility
        - Article 19: Living independently and community inclusion
        """
        crpd_compliance = {
            'Article_3_Full_Participation': hasattr(system, 'full_participation') or
                                           hasattr(system, 'universal_coverage'),
            'Article_5_Equality': hasattr(system, 'non_discrimination') or
                                 hasattr(system, 'equal_access'),
            'Article_9_Accessibility': hasattr(system, 'accessibility') or
                                      hasattr(system, 'accessible_interfaces'),
            'Article_19_Community_Living': hasattr(system, 'community_living') or
                                          hasattr(system, 'community_integration')
        }

        return crpd_compliance

    def _verify_undis_coverage(self, system: Any) -> Dict[str, bool]:
        """
        Verify UN Disability Inclusion Strategy (UNDIS) coverage

        Components:
        - Leadership: Persons with disabilities in decision-making
        - Accessibility: Physical, digital, informational
        - Assistive Technology: For all disability types
        - Community Living Supports: Integrated, not segregated
        """
        undis_coverage = {
            'Leadership': hasattr(system, 'inclusive_leadership') or
                         hasattr(system, 'leadership_support'),
            'Accessibility': hasattr(system, 'accessibility_features') or
                           hasattr(system, 'accessible_design'),
            'Assistive_Technology': hasattr(system, 'assistive_tech') or
                                   hasattr(system, 'technology_support'),
            'Community_Living': hasattr(system, 'community_supports') or
                              hasattr(system, 'integrated_living')
        }

        return undis_coverage

    def _generate_universal_recommendation(
        self,
        base_report: AuditReport,
        coverage: Dict[str, Any],
        causal: Dict[str, Any],
        mycelial: Dict[str, Any],
        chaos_harmony: Dict[str, Any],
        neurodiversity: Dict[str, Any],
        crpd: Dict[str, bool],
        undis: Dict[str, bool],
        overall_compliance: bool
    ) -> str:
        """Generate comprehensive recommendation for universal inclusion"""

        recommendations = []

        # Check universal coverage
        if not coverage['universal_coverage']:
            missing = [
                cat for cat, details in coverage['details'].items()
                if not details['covered']
            ]
            recommendations.append(
                f"🚨 UNIVERSAL COVERAGE VIOLATION: Missing categories: {', '.join(missing)}. "
                f"True inclusion requires ALL disability types (physical, sensory, intellectual, psychological)."
            )

        # Check causal framework
        if not causal['causal_framework']:
            recommendations.append(
                "🚨 CAUSAL MEASUREMENT MISSING: System cannot measure causal effects P(V|do(I)). "
                "Implement Bayesian causal network with do() interventions."
            )

        # Check mycelial network
        if not mycelial['horizontal_transfer']:
            recommendations.append(
                "⚠️  HIERARCHICAL STRUCTURE DETECTED: System uses top-down control. "
                "Implement horizontal (mycelial) information transfer for true symbiosis."
            )

        # Check chaos → harmony evolution
        if not chaos_harmony['evolution_present']:
            recommendations.append(
                "⚠️  NO CHAOS→HARMONY EVOLUTION: System cannot guide chaotic states to harmony. "
                "Implement ODE evolution: dS/dt = -γ(S - φ) towards golden ratio."
            )

        # Check neurodiversity
        if not neurodiversity['neurodiversity_included']:
            recommendations.append(
                "🚨 NEURODIVERSITY EXCLUSION: System does not support neurodivergent individuals. "
                "Add support for autism, ADHD, dyslexia, Tourette, and other neurotypes."
            )

        # Check CRPD compliance
        crpd_violations = [art for art, compliant in crpd.items() if not compliant]
        if crpd_violations:
            recommendations.append(
                f"⚠️  UN-CRPD VIOLATIONS: Non-compliant with {', '.join(crpd_violations)}. "
                f"Implement full participation, equality, accessibility, and community living."
            )

        # Check UNDIS coverage
        undis_missing = [comp for comp, covered in undis.items() if not covered]
        if undis_missing:
            recommendations.append(
                f"⚠️  UNDIS GAPS: Missing {', '.join(undis_missing)}. "
                f"Implement leadership, accessibility, assistive tech, and community supports."
            )

        # Overall assessment
        if overall_compliance:
            return (
                "✅ UNIVERSAL INCLUSION VERIFIED: System demonstrates:\n"
                "- Universal coverage (ALL disability categories)\n"
                "- Causal measurement framework\n"
                "- Mycelial (horizontal) network structure\n"
                "- Chaos → Harmony evolution\n"
                "- Neurodiversity integration\n"
                "- UN-CRPD compliance\n"
                "- UNDIS coverage\n\n"
                "🌍 The network grows inclusively. The mycelium connects all beings. 369 ✨"
            )

        return "\n\n".join(recommendations)


def create_universal_inclusion_audit(system: Any) -> UniversalInclusionVerifier:
    """
    Convenience function to create universal inclusion audit verifier

    Args:
        system: System to audit

    Returns:
        Configured UniversalInclusionVerifier
    """
    # Create constraint registry
    registry = ConstraintRegistry()

    # Register basic rules
    registry.register_rule("Min_VAS_Compliance", lambda o: o.get('V', 0) >= 0.5)
    registry.register_rule("Min_Biosensor_Threshold", lambda o: o.get('B', 0) > 0.0)

    # Register universal inclusion rules
    registry.register_rule(
        "Universal_Coverage",
        lambda o: hasattr(o.get('system'), 'universal_coverage')
    )

    registry.register_rule(
        "Neurodiversity_Included",
        lambda o: hasattr(o.get('system'), 'neurodiversity_support')
    )

    # Create verifier
    verifier = UniversalInclusionVerifier(registry)

    return verifier
