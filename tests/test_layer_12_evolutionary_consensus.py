"""
Tests for Layer 12: Evolutionary Consensus
Validates genetic algorithms, DAO governance, and proof-of-metabolism
"""

import pytest
import numpy as np
from datetime import datetime
from unittest.mock import Mock, patch

from luca.layer_12_evolutionary_consensus import (
    DNA_Sequence,
    EvolutionState,
    EvolutionaryConsensusCore,
    Layer12IntegrationGuide,
    demonstrate_layer_12
)


class TestDNASequence:
    """Test DNA_Sequence dataclass"""

    def test_dna_initialization(self):
        """Test DNA sequence initialization with defaults"""
        dna = DNA_Sequence()
        assert dna.alpha == 0.4
        assert dna.beta == 0.4
        assert dna.gamma == 0.2
        assert dna.mutation_rate == 0.01
        assert dna.generation == 1
        assert dna.fitness_score == 0.0
        assert dna.timestamp is not None

    def test_dna_custom_values(self):
        """Test DNA sequence with custom values"""
        dna = DNA_Sequence(
            alpha=0.5,
            beta=0.3,
            gamma=0.2,
            mutation_rate=0.05,
            generation=5,
            fitness_score=0.85
        )
        assert dna.alpha == 0.5
        assert dna.beta == 0.3
        assert dna.gamma == 0.2
        assert dna.generation == 5
        assert dna.fitness_score == 0.85

    def test_dna_to_hash(self):
        """Test DNA hashing for blockchain"""
        dna = DNA_Sequence(alpha=0.5, beta=0.3, gamma=0.2, generation=1)
        hash1 = dna.to_hash()

        # Hash should be consistent
        hash2 = dna.to_hash()
        assert hash1 == hash2

        # Hash should be 64 characters (SHA256)
        assert len(hash1) == 64

        # Different DNA should produce different hash
        dna2 = DNA_Sequence(alpha=0.6, beta=0.3, gamma=0.1, generation=1)
        hash3 = dna2.to_hash()
        assert hash1 != hash3

    def test_dna_to_dict(self):
        """Test DNA serialization to dictionary"""
        dna = DNA_Sequence(
            alpha=0.5,
            beta=0.3,
            gamma=0.2,
            fitness_score=0.75
        )
        dna_dict = dna.to_dict()

        assert 'alpha' in dna_dict
        assert 'beta' in dna_dict
        assert 'gamma' in dna_dict
        assert 'fitness_score' in dna_dict
        assert 'generation' in dna_dict
        assert 'hash' in dna_dict
        assert dna_dict['alpha'] == 0.5
        assert dna_dict['fitness_score'] == 0.75


class TestEvolutionState:
    """Test EvolutionState dataclass"""

    def test_state_initialization(self):
        """Test evolution state initialization"""
        state = EvolutionState()
        assert state.population_size == 0
        assert state.average_fitness == 0.0
        assert state.total_generations == 0
        assert state.survival_rate == 0.7
        assert state.dao_treasury_balance == 0.0
        assert state.last_mutation_event is None

    def test_state_to_dict(self):
        """Test state serialization"""
        state = EvolutionState(
            population_size=10,
            average_fitness=0.75,
            total_generations=5
        )
        state_dict = state.to_dict()

        assert state_dict['population_size'] == 10
        assert state_dict['average_fitness'] == 0.75
        assert state_dict['total_generations'] == 5


class TestEvolutionaryConsensusCore:
    """Test main EvolutionaryConsensusCore class"""

    def test_core_initialization(self):
        """Test core initialization"""
        core = EvolutionaryConsensusCore(node_id="TEST_NODE_001")

        assert core.node_id == "TEST_NODE_001"
        assert isinstance(core.dna, DNA_Sequence)
        assert isinstance(core.state, EvolutionState)
        assert core.metabolism_core is None
        assert len(core.fitness_history) == 0
        assert len(core.genetic_archive) == 0

    def test_core_with_web3(self):
        """Test core initialization with Web3 provider"""
        # Should gracefully handle invalid provider
        core = EvolutionaryConsensusCore(
            node_id="TEST_NODE_002",
            web3_provider="http://invalid-provider:8545"
        )
        assert core.web3_provider is not None
        # Web3 may or may not connect depending on availability

    def test_integrate_layer_11(self):
        """Test Layer 11 integration"""
        core = EvolutionaryConsensusCore(node_id="TEST_NODE_003")
        mock_metabolism = Mock()

        core.integrate_layer_11(mock_metabolism)
        assert core.metabolism_core == mock_metabolism

    def test_calculate_fitness_basic(self):
        """Test basic fitness calculation"""
        core = EvolutionaryConsensusCore(node_id="TEST_NODE_004")

        fusion_result = {
            'multimodal_fusion_score': 0.8,
            'energy_efficiency': 0.9,
            'cultural_fidelity': 0.85
        }

        fitness = core.calculate_fitness(fusion_result)

        assert 0.0 <= fitness <= 1.0
        assert core.dna.fitness_score == fitness
        assert len(core.fitness_history) == 1

    def test_calculate_fitness_empty_result(self):
        """Test fitness calculation with empty result"""
        core = EvolutionaryConsensusCore(node_id="TEST_NODE_005")
        fitness = core.calculate_fitness({})
        assert fitness == 0.0

    def test_spiritual_coherence(self):
        """Test spiritual coherence calculation"""
        core = EvolutionaryConsensusCore(node_id="TEST_NODE_006")

        fusion_result = {
            'cultural_fidelity': 0.8
        }

        coherence = core._calculate_spiritual_coherence(fusion_result)

        assert 0.0 <= coherence <= 1.0

    def test_genetic_crossover(self):
        """Test genetic crossover between two DNA sequences"""
        core = EvolutionaryConsensusCore(node_id="TEST_NODE_007")
        core.dna = DNA_Sequence(alpha=0.5, beta=0.3, gamma=0.2, generation=1)

        partner_dna = DNA_Sequence(alpha=0.6, beta=0.2, gamma=0.2, generation=2)

        child_dna = core.genetic_crossover(partner_dna)

        # Child should have incremented generation
        assert child_dna.generation > max(core.dna.generation, partner_dna.generation)

        # Weights should sum to approximately 1.0
        assert abs(child_dna.alpha + child_dna.beta + child_dna.gamma - 1.0) < 0.01

        # All weights should be positive
        assert child_dna.alpha > 0
        assert child_dna.beta > 0
        assert child_dna.gamma > 0

    def test_mutation(self):
        """Test DNA mutation mechanism"""
        core = EvolutionaryConsensusCore(node_id="TEST_NODE_008")

        original_dna = DNA_Sequence(
            alpha=0.4,
            beta=0.4,
            gamma=0.2,
            mutation_rate=1.0  # Force mutation
        )

        mutated_dna = core._mutate(original_dna)

        # After mutation, weights should still be valid
        assert abs(mutated_dna.alpha + mutated_dna.beta + mutated_dna.gamma - 1.0) < 0.01
        assert mutated_dna.alpha > 0
        assert mutated_dna.beta > 0
        assert mutated_dna.gamma > 0

    def test_natural_selection(self):
        """Test natural selection process"""
        core = EvolutionaryConsensusCore(node_id="TEST_NODE_009")

        # Create population with varying fitness
        population = [
            DNA_Sequence(fitness_score=0.9),
            DNA_Sequence(fitness_score=0.7),
            DNA_Sequence(fitness_score=0.5),
            DNA_Sequence(fitness_score=0.3),
            DNA_Sequence(fitness_score=0.1)
        ]

        survivors = core.perform_natural_selection(population)

        # Should have fewer survivors than original population
        assert len(survivors) < len(population)

        # Survivors should be sorted by fitness
        fitness_scores = [dna.fitness_score for dna in survivors]
        assert fitness_scores == sorted(fitness_scores, reverse=True)

        # State should be updated
        assert core.state.average_fitness > 0
        assert core.state.population_size == len(population)

    def test_natural_selection_small_population(self):
        """Test natural selection with small population"""
        core = EvolutionaryConsensusCore(node_id="TEST_NODE_010")

        population = [DNA_Sequence(fitness_score=0.8)]
        survivors = core.perform_natural_selection(population)

        # Should return same population if only 1 member
        assert len(survivors) == 1

    def test_proof_of_metabolism_consensus(self):
        """Test proof-of-metabolism consensus mechanism"""
        core = EvolutionaryConsensusCore(node_id="TEST_NODE_011")

        network_nodes = {
            'NODE_A': {
                'metabolism_result': {'energy_efficiency': 1.5}
            },
            'NODE_B': {
                'metabolism_result': {'energy_efficiency': 0.8}
            },
            'NODE_C': {
                'metabolism_result': {'energy_efficiency': 1.2}
            }
        }

        leader = core.proof_of_metabolism_consensus(network_nodes)

        # Leader should be the node with highest energy efficiency
        assert leader == 'NODE_A'

    def test_proof_of_metabolism_empty(self):
        """Test consensus with empty network"""
        core = EvolutionaryConsensusCore(node_id="TEST_NODE_012")
        leader = core.proof_of_metabolism_consensus({})
        assert leader == "no_consensus"

    def test_dao_treasury_disconnected(self):
        """Test DAO treasury interaction when disconnected"""
        core = EvolutionaryConsensusCore(node_id="TEST_NODE_013")

        result = core.dao_treasury_interaction('balance')

        assert result['status'] == 'disconnected'
        assert 'balance' in result

    def test_evolve_parameters_empty_population(self):
        """Test evolution with empty population"""
        core = EvolutionaryConsensusCore(node_id="TEST_NODE_014")

        report = core.evolve_parameters([])

        assert report['status'] == 'no_population'
        assert 'timestamp' in report

    def test_evolve_parameters_full_cycle(self):
        """Test full evolution cycle"""
        core = EvolutionaryConsensusCore(node_id="TEST_NODE_015")

        network_population = [
            {
                'node_id': 'NODE_A',
                'fusion_result': {
                    'multimodal_fusion_score': 0.85,
                    'energy_efficiency': 1.2,
                    'cultural_fidelity': 0.9
                },
                'dna': DNA_Sequence(fitness_score=0.0),
                'metabolism_result': {'energy_efficiency': 1.2}
            },
            {
                'node_id': 'NODE_B',
                'fusion_result': {
                    'multimodal_fusion_score': 0.65,
                    'energy_efficiency': 0.8,
                    'cultural_fidelity': 0.7
                },
                'dna': DNA_Sequence(fitness_score=0.0),
                'metabolism_result': {'energy_efficiency': 0.8}
            },
            {
                'node_id': 'NODE_C',
                'fusion_result': {
                    'multimodal_fusion_score': 0.75,
                    'energy_efficiency': 1.0,
                    'cultural_fidelity': 0.8
                },
                'dna': DNA_Sequence(fitness_score=0.0),
                'metabolism_result': {'energy_efficiency': 1.0}
            }
        ]

        initial_generation = core.dna.generation

        report = core.evolve_parameters(network_population)

        # Verify report structure
        assert 'generation' in report
        assert 'survivors' in report
        assert 'population_size' in report
        assert 'average_fitness' in report
        assert 'leader_node' in report
        assert 'mutations' in report
        assert 'timestamp' in report
        assert 'dna_hash' in report

        # Verify evolution occurred
        assert report['population_size'] == 3
        assert report['survivors'] <= 3
        assert core.state.total_generations > 0

        # Generation should increment
        assert core.dna.generation > initial_generation

    def test_get_status(self):
        """Test status retrieval"""
        core = EvolutionaryConsensusCore(node_id="TEST_NODE_016")
        mock_metabolism = Mock()
        core.integrate_layer_11(mock_metabolism)

        status = core.get_status()

        assert 'node_id' in status
        assert 'dna' in status
        assert 'state' in status
        assert 'fitness_history_length' in status
        assert 'web3_connected' in status
        assert 'layer_11_integrated' in status

        assert status['node_id'] == "TEST_NODE_016"
        assert status['layer_11_integrated'] is True


class TestLayer12IntegrationGuide:
    """Test integration guide utilities"""

    def test_get_quick_start(self):
        """Test quick start guide generation"""
        guide = Layer12IntegrationGuide()
        quick_start = guide.get_quick_start()

        assert isinstance(quick_start, str)
        assert 'SOFORT-INTEGRATION' in quick_start
        assert 'EvolutionaryConsensusCore' in quick_start
        assert 'Layer 11' in quick_start

    def test_generate_production_config(self):
        """Test production configuration generation"""
        guide = Layer12IntegrationGuide()
        config = guide.generate_production_config()

        assert 'evolution_params' in config
        assert 'dao_config' in config
        assert 'metabolism_integration' in config

        # Verify evolution params
        assert 'survival_rate' in config['evolution_params']
        assert 'mutation_rate' in config['evolution_params']

        # Verify DAO config
        assert 'contract_address' in config['dao_config']
        assert 'token_symbol' in config['dao_config']

        # Verify metabolism integration
        assert 'fitness_update_interval' in config['metabolism_integration']
        assert 'consensus_mechanism' in config['metabolism_integration']


class TestDemonstration:
    """Test demonstration functionality"""

    def test_demonstrate_layer_12(self, capsys):
        """Test that demonstration runs without errors"""
        # Should complete without exceptions
        demonstrate_layer_12()

        # Capture output
        captured = capsys.readouterr()

        # Verify key outputs
        assert 'EVOLUTIONARY CONSENSUS' in captured.out
        assert 'Start-Population' in captured.out
        assert 'Evolutions-Report' in captured.out
        assert 'Proof-of-Metabolism' in captured.out


class TestIntegrationScenarios:
    """Test real-world integration scenarios"""

    def test_multi_generation_evolution(self):
        """Test evolution over multiple generations"""
        core = EvolutionaryConsensusCore(node_id="MULTI_GEN_NODE")

        # Initial population
        population = [
            {
                'node_id': f'NODE_{i}',
                'fusion_result': {
                    'multimodal_fusion_score': 0.5 + (i * 0.1),
                    'energy_efficiency': 0.8 + (i * 0.1),
                    'cultural_fidelity': 0.7 + (i * 0.05)
                },
                'dna': DNA_Sequence(),
                'metabolism_result': {'energy_efficiency': 0.8 + (i * 0.1)}
            }
            for i in range(5)
        ]

        # Run multiple evolution cycles
        reports = []
        for _ in range(3):
            report = core.evolve_parameters(population)
            reports.append(report)

        # Verify generations increased
        assert reports[-1]['generation'] > reports[0]['generation']
        assert core.state.total_generations >= 3

    def test_fitness_tracking(self):
        """Test fitness tracking over time"""
        core = EvolutionaryConsensusCore(node_id="FITNESS_TRACKER")

        # Calculate fitness multiple times
        for i in range(5):
            fusion_result = {
                'multimodal_fusion_score': 0.7 + (i * 0.05),
                'energy_efficiency': 0.8 + (i * 0.03),
                'cultural_fidelity': 0.75 + (i * 0.04)
            }
            core.calculate_fitness(fusion_result)

        # Verify fitness history
        assert len(core.fitness_history) == 5

        # Verify fitness values are reasonable
        for entry in core.fitness_history:
            assert 0.0 <= entry['fitness'] <= 1.0
            assert 'timestamp' in entry
            assert 'generation' in entry

    def test_crossover_preserves_constraints(self):
        """Test that crossover always produces valid DNA"""
        core = EvolutionaryConsensusCore(node_id="CROSSOVER_TEST")

        # Test multiple crossovers
        for _ in range(10):
            parent1_dna = DNA_Sequence(
                alpha=np.random.uniform(0.1, 0.6),
                beta=np.random.uniform(0.1, 0.6),
                gamma=0.2
            )
            parent2_dna = DNA_Sequence(
                alpha=np.random.uniform(0.1, 0.6),
                beta=np.random.uniform(0.1, 0.6),
                gamma=0.2
            )

            core.dna = parent1_dna
            child_dna = core.genetic_crossover(parent2_dna)

            # Verify constraints
            assert abs(child_dna.alpha + child_dna.beta + child_dna.gamma - 1.0) < 0.01
            assert child_dna.alpha >= 0
            assert child_dna.beta >= 0
            assert child_dna.gamma >= 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
