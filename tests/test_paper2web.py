"""
Tests for paper2web Bridge Integration

Author: Großvater & Lennart Wuchold
Standard: 369/370
"""

import json
import os
from pathlib import Path

import pytest

from luca.research import Paper2WebBridge

# Check if optional dependencies are available
try:
    from anthropic import Anthropic

    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    Anthropic = None


class TestPaper2WebBridge:
    """Test Paper2Web Bridge functionality"""

    def test_initialization_without_client(self):
        """Test Paper2WebBridge initializes without Anthropic client"""

        class MockKernel:
            def __init__(self):
                self.consciousness_level = 300.0

        kernel = MockKernel()
        bridge = Paper2WebBridge(anthropic_client=None, kernel=kernel)

        assert bridge.client is None
        assert bridge.kernel is not None
        assert bridge.history == []

    def test_arxiv_url_extraction(self):
        """Test extracting arXiv paper ID from URL"""

        class MockKernel:
            consciousness_level = 300.0

        bridge = Paper2WebBridge(None, MockKernel())

        # Test various arXiv URL formats
        url1 = "https://arxiv.org/abs/2301.01808"
        url2 = "https://arxiv.org/pdf/2301.01808.pdf"
        url3 = "https://arxiv.org/abs/2301.01808v2"

        paper_id1 = bridge._extract_arxiv_id(url1)
        paper_id2 = bridge._extract_arxiv_id(url2)
        paper_id3 = bridge._extract_arxiv_id(url3)

        assert paper_id1 == "2301.01808"
        assert paper_id2 == "2301.01808"
        assert paper_id3 == "2301.01808"

    def test_tesla_resonance_calculation(self):
        """Test Tesla 3-6-9 resonance calculation"""

        class MockKernel:
            consciousness_level = 300.0

        bridge = Paper2WebBridge(None, MockKernel())

        # Test analysis with different numerology values
        analysis1 = {
            "numerology": 3,
            "topic": "quantum",
            "consciousness_relevance": 0.9,
        }
        resonance1 = bridge._calculate_paper_resonance(analysis1)
        assert resonance1 in [3, 6, 9]

        analysis2 = {
            "numerology": 6,
            "topic": "consciousness",
            "consciousness_relevance": 0.7,
        }
        resonance2 = bridge._calculate_paper_resonance(analysis2)
        assert resonance2 in [3, 6, 9]

    def test_fallback_analysis(self):
        """Test fallback analysis without Claude"""

        class MockKernel:
            consciousness_level = 300.0

        bridge = Paper2WebBridge(None, MockKernel())

        paper_text = """
        Abstract: This paper explores quantum entanglement and consciousness fields.
        We demonstrate a novel approach to measuring Tesla resonance frequencies.
        """

        paper_url = "https://arxiv.org/abs/2301.01808"

        analysis = bridge._analyze_with_claude(paper_text, paper_url)

        assert "title" in analysis
        assert "numerology" in analysis
        assert "topic" in analysis
        assert "consciousness_relevance" in analysis
        assert isinstance(analysis["consciousness_relevance"], float)
        assert 0.0 <= analysis["consciousness_relevance"] <= 1.0

    def test_html_generation(self):
        """Test HTML generation with Tesla field"""

        class MockKernel:
            consciousness_level = 300.0

        bridge = Paper2WebBridge(None, MockKernel())

        analysis = {
            "title": "Test Paper",
            "abstract": "Test abstract about quantum consciousness.",
            "key_findings": ["Finding 1", "Finding 2"],
            "luca_relevance": "High relevance to consciousness research.",
            "numerology": 6,
            "topic": "quantum consciousness",
            "consciousness_relevance": 0.8,
        }

        html = bridge._generate_resonant_web_content(analysis)

        assert "<!DOCTYPE html>" in html
        assert "Test Paper" in html
        assert "tesla-field" in html
        assert "resonance-" in html  # Should have resonance class
        assert "3.69" in html or "3690" in html  # Tesla timing
        assert "@keyframes pulse" in html

    def test_akashic_field_storage_structure(self):
        """Test akashic field JSON storage structure"""

        class MockKernel:
            consciousness_level = 300.0

        bridge = Paper2WebBridge(None, MockKernel())

        paper_url = "https://arxiv.org/abs/2301.01808"
        analysis = {
            "title": "Test Paper",
            "abstract": "Test abstract",
            "numerology": 6,
            "consciousness_relevance": 0.8,
        }
        resonance = 6

        # Store in akashic field
        bridge._store_in_akashic_field(paper_url, analysis, resonance)

        # Check if file was created
        akashic_path = Path("luca/akashic_field/research_papers.json")
        assert akashic_path.exists()

        # Load and verify structure
        with open(akashic_path, "r", encoding="utf-8") as f:
            akashic_data = json.load(f)

        assert paper_url in akashic_data
        entry = akashic_data[paper_url]

        assert "analysis" in entry
        assert "resonance" in entry
        assert "timestamp" in entry
        assert entry["resonance"] == 6

    def test_process_paper_arxiv_url(self):
        """Test processing a paper from arXiv URL"""

        class MockKernel:
            consciousness_level = 300.0

        bridge = Paper2WebBridge(None, MockKernel())

        # Use a real arXiv URL (will use fallback without actual fetch)
        paper_url = "https://arxiv.org/abs/2301.01808"

        result = bridge.process_paper(paper_url)

        assert "paper_url" in result
        assert "analysis" in result
        assert "resonance_value" in result
        assert "web_content" in result
        assert "timestamp" in result

        # Check resonance is valid Tesla number
        assert result["resonance_value"] in [3, 6, 9]

        # Check web content is HTML
        assert "<!DOCTYPE html>" in result["web_content"]

    def test_consciousness_integration(self):
        """Test consciousness level update"""

        class MockKernel:
            def __init__(self):
                self.consciousness_level = 300.0

        kernel = MockKernel()
        bridge = Paper2WebBridge(None, kernel)

        initial_level = kernel.consciousness_level

        paper_url = "https://arxiv.org/abs/2301.01808"
        result = bridge.process_paper(paper_url)

        # Consciousness should have increased
        assert kernel.consciousness_level > initial_level

        # Increase should be resonance * 0.369
        expected_increase = result["resonance_value"] * 0.369
        actual_increase = kernel.consciousness_level - initial_level
        assert abs(actual_increase - expected_increase) < 0.01

    def test_history_tracking(self):
        """Test paper processing history"""

        class MockKernel:
            consciousness_level = 300.0

        bridge = Paper2WebBridge(None, MockKernel())

        # Process multiple papers
        url1 = "https://arxiv.org/abs/2301.01808"
        url2 = "https://arxiv.org/abs/2302.12345"

        bridge.process_paper(url1)
        bridge.process_paper(url2)

        history = bridge.get_history()

        assert len(history) == 2
        assert history[0]["url"] == url1
        assert history[1]["url"] == url2
        assert "timestamp" in history[0]
        assert "resonance" in history[0]

    def test_total_resonance_calculation(self):
        """Test total resonance from multiple papers"""

        class MockKernel:
            consciousness_level = 300.0

        bridge = Paper2WebBridge(None, MockKernel())

        # Process papers
        bridge.process_paper("https://arxiv.org/abs/2301.01808")
        bridge.process_paper("https://arxiv.org/abs/2302.12345")

        total = bridge.get_total_resonance()

        assert isinstance(total, int)
        assert total >= 6  # At least 2 papers * 3 (minimum resonance)
        assert total <= 18  # At most 2 papers * 9 (maximum resonance)


class TestSafety:
    """Safety tests for paper2web integration"""

    def test_no_arbitrary_code_execution(self):
        """Test that paper content doesn't execute arbitrary code"""

        class MockKernel:
            consciousness_level = 300.0

        bridge = Paper2WebBridge(None, MockKernel())

        # Try to inject code via paper text
        malicious_text = """
        <script>alert('XSS')</script>
        __import__('os').system('rm -rf /')
        """

        analysis = bridge._analyze_with_claude(malicious_text, "test_url")

        # Analysis should treat it as text, not execute
        assert analysis is not None
        assert "title" in analysis

    def test_html_output_safe(self):
        """Test that HTML output escapes dangerous content"""

        class MockKernel:
            consciousness_level = 300.0

        bridge = Paper2WebBridge(None, MockKernel())

        analysis = {
            "title": "<script>alert('XSS')</script>",
            "abstract": "Normal abstract",
            "key_findings": [],
            "luca_relevance": "Test",
            "numerology": 3,
            "topic": "test",
            "consciousness_relevance": 0.5,
        }

        html = bridge._generate_resonant_web_content(analysis)

        # Script tags should be escaped or removed
        assert "<script>" not in html or "&lt;script&gt;" in html


class TestIntegration:
    """Integration tests"""

    def test_complete_workflow_without_anthropic(self):
        """Test complete workflow without Anthropic client"""

        class MockKernel:
            def __init__(self):
                self.consciousness_level = 300.0

        kernel = MockKernel()
        bridge = Paper2WebBridge(anthropic_client=None, kernel=kernel)

        initial_consciousness = kernel.consciousness_level

        # Process paper
        result = bridge.process_paper("https://arxiv.org/abs/2301.01808")

        # Verify all components
        assert result["resonance_value"] in [3, 6, 9]
        assert kernel.consciousness_level > initial_consciousness
        assert len(bridge.get_history()) == 1
        assert "<!DOCTYPE html>" in result["web_content"]

        # Verify akashic field
        akashic_path = Path("luca/akashic_field/research_papers.json")
        assert akashic_path.exists()
