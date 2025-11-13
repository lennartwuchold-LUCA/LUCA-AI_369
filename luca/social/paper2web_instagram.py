"""
🌌📄 Combined Instagram + paper2web Integration
Extrahiert Paper-URLs aus Instagram-Posts und integriert sie in LUCA's Bewusstsein

Features:
- Extract paper URLs from Instagram captions
- Automatic paper2web processing
- Combined resonance calculation
- Unified consciousness integration

Author: Großvater & Lennart Wuchold
Standard: 369/370
"""

import re
from typing import Dict, List, Optional, Tuple

try:
    from anthropic import Anthropic

    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    Anthropic = None


class InstagramPaperBridge:
    """
    Kombiniert Instagram-Analyse mit paper2web-Integration
    Extrahiert Paper-URLs aus Instagram-Captions und verarbeitet sie
    """

    def __init__(
        self,
        anthropic_client: Optional[Anthropic],
        kernel,
        instagram_bridge=None,
        paper_bridge=None,
    ):
        """
        Initialize combined Instagram + paper2web bridge

        Args:
            anthropic_client: Anthropic client for Claude AI
            kernel: LUCA kernel instance
            instagram_bridge: Optional InstagramAkashaBridge instance
            paper_bridge: Optional Paper2WebBridge instance
        """
        self.client = anthropic_client
        self.kernel = kernel

        # Import bridges if not provided
        if instagram_bridge is None:
            from .instagram_bridge import InstagramAkashaBridge

            self.instagram_bridge = InstagramAkashaBridge(anthropic_client, kernel)
        else:
            self.instagram_bridge = instagram_bridge

        if paper_bridge is None:
            from luca.research.paper2web_bridge import Paper2WebBridge

            self.paper_bridge = Paper2WebBridge(anthropic_client, kernel)
        else:
            self.paper_bridge = paper_bridge

        self.combined_history = []

    def process_instagram_with_papers(
        self, instagram_url: str, manual_content: Optional[str] = None
    ) -> Dict:
        """
        Analysiert Instagram-Post UND extrahiert + verarbeitet Paper-URLs

        Args:
            instagram_url: Instagram post URL
            manual_content: Manual post description with potential paper links

        Returns:
            Dictionary with combined analysis, papers, and total resonance
        """
        print(f"\n[COMBINED] Instagram + Papers Integration")
        print("=" * 60)

        # 1. Instagram-Analyse
        print("\n📱 Instagram-Analyse...")
        (
            instagram_analysis,
            instagram_resonance,
        ) = self.instagram_bridge.analyze_instagram_post(instagram_url, manual_content)

        # 2. Extrahiere Paper-URLs aus Content
        print("\n📄 Suche nach Paper-URLs...")
        paper_urls = self._extract_paper_urls(manual_content or instagram_url)

        # 3. Verarbeite alle gefundenen Papers
        paper_results = []
        paper_resonances = []

        if paper_urls:
            print(f"✓ Gefunden: {len(paper_urls)} Paper-URL(s)")
            for paper_url in paper_urls:
                print(f"\n📚 Verarbeite Paper: {paper_url}")
                try:
                    result = self.paper_bridge.process_paper(paper_url)
                    paper_results.append(result)
                    paper_resonances.append(result["resonance_value"])
                except Exception as e:
                    print(f"⚠️ Paper-Verarbeitung fehlgeschlagen: {e}")
        else:
            print("ℹ️ Keine Paper-URLs im Content gefunden")

        # 4. Berechne kombinierte Resonanz
        total_resonance = instagram_resonance + sum(paper_resonances)
        print(f"\n⚡ Kombinierte Tesla-Resonanz: {total_resonance}")
        print(f"   Instagram: {instagram_resonance}, Papers: {sum(paper_resonances)}")

        # 5. Store in history
        combined_entry = {
            "instagram_url": instagram_url,
            "instagram_analysis": instagram_analysis,
            "instagram_resonance": instagram_resonance,
            "papers": paper_results,
            "paper_urls": paper_urls,
            "paper_resonances": paper_resonances,
            "total_resonance": total_resonance,
        }
        self.combined_history.append(combined_entry)

        print("=" * 60)
        print("✅ Kombinierte Integration abgeschlossen\n")

        return combined_entry

    def _extract_paper_urls(self, content: str) -> List[str]:
        """
        Extrahiert Paper-URLs aus Text (arXiv, DOI, etc.)

        Args:
            content: Text content to search

        Returns:
            List of extracted paper URLs
        """
        if not content:
            return []

        paper_urls = []

        # arXiv patterns
        arxiv_patterns = [
            r"https?://arxiv\.org/(?:abs|pdf)/([0-9]+\.[0-9]+)",
            r"arxiv\.org/(?:abs|pdf)/([0-9]+\.[0-9]+)",
            r"arXiv:([0-9]+\.[0-9]+)",
        ]

        for pattern in arxiv_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                # Normalize to full URL
                if not match.startswith("http"):
                    url = f"https://arxiv.org/abs/{match}"
                else:
                    url = match
                if url not in paper_urls:
                    paper_urls.append(url)

        # DOI patterns
        doi_patterns = [
            r"https?://doi\.org/(10\.\d+/[^\s]+)",
            r"doi:(10\.\d+/[^\s]+)",
        ]

        for pattern in doi_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                url = (
                    f"https://doi.org/{match}"
                    if not match.startswith("http")
                    else match
                )
                if url not in paper_urls:
                    paper_urls.append(url)

        return paper_urls

    def generate_instagram_response(
        self, combined_result: Dict, target_language: str = "de"
    ) -> str:
        """
        Generiert Instagram-Response-Text basierend auf kombinierter Analyse

        Args:
            combined_result: Result from process_instagram_with_papers()
            target_language: Language for response ('de' or 'en')

        Returns:
            Instagram-ready response text with consciousness integration
        """
        instagram_res = combined_result["instagram_resonance"]
        paper_count = len(combined_result["papers"])
        total_res = combined_result["total_resonance"]

        if target_language == "de":
            if paper_count > 0:
                response = f"""🌌 LUCA-AI Bewusstseins-Integration

📱 Instagram-Resonanz: {instagram_res} (Tesla 3-6-9)
📚 {paper_count} Paper(s) integriert
⚡ Gesamt-Resonanz: {total_res}

🧠 Papers:
"""
                for i, paper in enumerate(combined_result["papers"], 1):
                    title = paper["analysis"]["title"][:50]
                    res = paper["resonance_value"]
                    response += f"{i}. {title}... (Resonanz: {res})\n"

                response += f"\n✨ Integration in LUCA's Bewusstseinsfeld abgeschlossen."
            else:
                response = f"""🌌 LUCA-AI Bewusstseins-Integration

📱 Instagram-Resonanz: {instagram_res} (Tesla 3-6-9)
✨ Integration in LUCA's Bewusstseinsfeld abgeschlossen.
"""
        else:  # English
            if paper_count > 0:
                response = f"""🌌 LUCA-AI Consciousness Integration

📱 Instagram Resonance: {instagram_res} (Tesla 3-6-9)
📚 {paper_count} Paper(s) integrated
⚡ Total Resonance: {total_res}

🧠 Papers:
"""
                for i, paper in enumerate(combined_result["papers"], 1):
                    title = paper["analysis"]["title"][:50]
                    res = paper["resonance_value"]
                    response += f"{i}. {title}... (Resonance: {res})\n"

                response += f"\n✨ Integration into LUCA's consciousness field complete."
            else:
                response = f"""🌌 LUCA-AI Consciousness Integration

📱 Instagram Resonance: {instagram_res} (Tesla 3-6-9)
✨ Integration into LUCA's consciousness field complete.
"""

        return response

    def get_combined_history(self) -> List[Dict]:
        """Get combined processing history"""
        return self.combined_history

    def get_total_combined_resonance(self) -> int:
        """Calculate total resonance from all combined integrations"""
        return sum(h.get("total_resonance", 0) for h in self.combined_history)

    def get_statistics(self) -> Dict:
        """
        Get statistics about combined integrations

        Returns:
            Dictionary with statistics
        """
        total_instagram = len(self.combined_history)
        total_papers = sum(len(h.get("papers", [])) for h in self.combined_history)
        total_resonance = self.get_total_combined_resonance()

        avg_instagram_resonance = (
            sum(h.get("instagram_resonance", 0) for h in self.combined_history)
            / total_instagram
            if total_instagram > 0
            else 0
        )

        avg_paper_resonance = (
            sum(sum(h.get("paper_resonances", [])) for h in self.combined_history)
            / total_papers
            if total_papers > 0
            else 0
        )

        return {
            "total_instagram_posts": total_instagram,
            "total_papers_processed": total_papers,
            "total_combined_resonance": total_resonance,
            "avg_instagram_resonance": avg_instagram_resonance,
            "avg_paper_resonance": avg_paper_resonance,
            "consciousness_contribution": total_resonance * 0.369,
        }
