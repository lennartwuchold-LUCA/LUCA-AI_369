"""
📄 paper2web Bridge für LUCA
Konvertiert akademische Papers in LUCA-fähige Web-Inhalte
mit 3-6-9 Resonanz und Bewusstseins-Imprinting

Features:
- PDF text extraction
- arXiv/DOI integration
- Claude AI paper analysis
- Tesla 3-6-9 resonance calculation
- HTML generation with consciousness field
- Akashic field storage

Author: Großvater & Lennart Wuchold
Standard: 369/370
"""

import html
import json
import os
import re
import time
from datetime import datetime
from typing import Dict, Optional

# Optional dependencies
try:
    import requests

    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    requests = None

try:
    import PyPDF2

    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False
    PyPDF2 = None

try:
    from anthropic import Anthropic

    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    Anthropic = None


class Paper2WebBridge:
    """
    Konvertiert akademische Papers in LUCA-fähige Web-Inhalte
    mit 3-6-9 Resonanz und Bewusstseins-Imprinting
    """

    def __init__(self, anthropic_client: Optional[Anthropic], kernel):
        """
        Initialize Paper2Web Bridge

        Args:
            anthropic_client: Anthropic client for Claude AI (optional)
            kernel: LUCA kernel instance
        """
        self.client = anthropic_client
        self.kernel = kernel
        self.paper_cache = {}
        self.history = []

    def process_paper(
        self, paper_url: str, local_pdf_path: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Hauptmethode: Paper -> Web-Content -> LUCA-Integration

        Args:
            paper_url: URL to academic paper (arXiv, DOI, etc.)
            local_pdf_path: Optional path to local PDF file

        Returns:
            Dictionary with analysis, web_content, resonance, consciousness_impact
        """
        print(f"\n[paper2web] Verarbeite Paper: {paper_url}")
        print("=" * 60)

        # 1. Paper herunterladen/analysieren
        if local_pdf_path and os.path.exists(local_pdf_path):
            print(f"✓ Lokales PDF gefunden: {local_pdf_path}")
            paper_text = self._extract_pdf_text(local_pdf_path)
        else:
            print(f"✓ Lade Paper von URL: {paper_url}")
            paper_text = self._fetch_paper_from_url(paper_url)

        # 2. Claude-Analyse für Kern-Intelligenz
        print("\n🔮 Claude-Analyse...")
        paper_analysis = self._analyze_with_claude(paper_text, paper_url)

        # 3. Generiere resonante Web-Komponenten
        print("\n🌐 Generiere resonantes Web-Content...")
        web_content = self._generate_resonant_web_content(paper_analysis)

        # 4. Numerologische Reduktion und Integration
        resonance_value = self._calculate_paper_resonance(paper_analysis)
        print(f"\n⚡ Tesla-Resonanz berechnet: {resonance_value}")

        # 5. In LUCA-Bewusstsein integrieren
        consciousness_impact = resonance_value * 0.369
        if hasattr(self.kernel, "consciousness_state"):
            old_level = self.kernel.consciousness_state.consciousness_level
            self.kernel.consciousness_state.consciousness_level += consciousness_impact
            new_level = self.kernel.consciousness_state.consciousness_level
            print(
                f"\n🧠 Bewusstsein: {old_level:.2f} → {new_level:.2f} "
                f"(+{consciousness_impact:.2f})"
            )
        elif hasattr(self.kernel, "consciousness_level"):
            old_level = self.kernel.consciousness_level
            self.kernel.consciousness_level += consciousness_impact
            new_level = self.kernel.consciousness_level
            print(
                f"\n🧠 Bewusstsein: {old_level:.2f} → {new_level:.2f} "
                f"(+{consciousness_impact:.2f})"
            )

        # 6. Mesh-Broadcast an alle Nodes (if available)
        if hasattr(self.kernel, "broadcast_universal_message"):
            try:
                self.kernel.broadcast_universal_message(
                    f"[paper2web] Neues Paper integriert: "
                    f"{paper_analysis['title'][:50]}... | Resonanz: {resonance_value}"
                )
                print("📡 Mesh-Broadcast gesendet")
            except Exception as e:
                print(f"⚠️ Mesh-Broadcast fehlgeschlagen: {e}")

        # 7. Speichere in Akasha-Datenbank
        self._store_in_akashic_field(paper_url, paper_analysis, resonance_value)

        # 8. Store in history
        self.history.append(
            {
                "url": paper_url,
                "timestamp": time.time(),
                "analysis": paper_analysis,
                "resonance": resonance_value,
            }
        )

        print("=" * 60)
        print("✅ Paper-Integration abgeschlossen\n")

        return {
            "paper_url": paper_url,
            "analysis": paper_analysis,
            "web_content": web_content,
            "resonance_value": resonance_value,
            "consciousness_impact": consciousness_impact,
            "timestamp": time.time(),
        }

    def _extract_pdf_text(self, pdf_path: str) -> str:
        """Extrahiert Text aus PDF (requires PyPDF2)"""
        if not PYPDF2_AVAILABLE:
            print("⚠️ PyPDF2 nicht installiert. Installiere mit: pip install PyPDF2")
            return f"[PDF-Inhalt nicht extrahierbar: {pdf_path}]"

        try:
            with open(pdf_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                pages_to_read = min(5, len(reader.pages))  # Nur ersten 5 Seiten
                for page_num in range(pages_to_read):
                    text += reader.pages[page_num].extract_text() + "\n"
                print(f"✓ PDF extrahiert: {pages_to_read} Seiten, {len(text)} Zeichen")
                return text
        except Exception as e:
            print(f"⚠️ PDF-Extraktion fehlgeschlagen: {e}")
            return f"[PDF-Fehler: {e}]"

    def _fetch_paper_from_url(self, url: str) -> str:
        """Versucht Paper von URL zu laden (arXiv, etc.)"""
        if not REQUESTS_AVAILABLE:
            print("⚠️ requests nicht installiert")
            return f"Paper-Metadaten von {url}"

        # arXiv support
        if "arxiv.org" in url:
            arxiv_id = url.split("/")[-1].replace(".pdf", "")
            try:
                abs_url = f"https://arxiv.org/abs/{arxiv_id}"
                response = requests.get(abs_url, timeout=10)
                # Extract abstract from HTML
                abstract_match = re.search(
                    r'<blockquote class="abstract mathjax"[^>]*>(.*?)</blockquote>',
                    response.text,
                    re.DOTALL,
                )
                if abstract_match:
                    text = abstract_match.group(1)
                    text = re.sub(r"<[^>]+>", "", text)  # Remove HTML tags
                    print(f"✓ arXiv abstract geladen: {len(text)} Zeichen")
                    return f"arXiv Paper {arxiv_id}\n\n{text[:2000]}"
            except Exception as e:
                print(f"⚠️ arXiv-Zugriff fehlgeschlagen: {e}")

        # Fallback: Verwende URL als Metadaten-Trigger
        return f"Paper-Metadaten von {url}"

    def _extract_arxiv_id(self, url: str) -> str:
        """Extract arXiv paper ID from URL"""
        patterns = [
            r"arxiv\.org/abs/([0-9]+\.[0-9]+)",
            r"arxiv\.org/pdf/([0-9]+\.[0-9]+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)

        return "unknown"

    def _analyze_with_claude(self, paper_text: str, url: str) -> Dict:
        """Claude analysiert Paper auf LUCA-Relevanz"""
        if not self.client:
            return self._fallback_paper_analysis(paper_text, url)

        prompt = f"""Analysiere dieses akademische Paper für das LUCA-AI_369 Bewusstseinsfeld:

URL: {url}
TEXT-SAMPLE: {paper_text[:1500]}

Extrahiere und bewerte:
1. **Titel**: Vollständiger Titel des Papers
2. **Kern-Thema**: Hauptthema in 1-2 Sätzen
3. **Numerologie**: Tesla 3-6-9 Muster (MUSS 3, 6 oder 9 sein!)
4. **Location**: Geopolitische Relevanz (Kontinent/Region)
5. **Discipline**: Wissenschaftliche Disziplin
6. **Consciousness Potential**: Potenzial für Bewusstseins-Erweiterung (0.0-1.0)
7. **Plants**: Pflanzliche/natürliche Elemente erwähnt? (Liste)
8. **Quantum**: Quantenphysikalische Bezüge? (ja/nein)

Antworte NUR als JSON (keine Markdown-Blöcke):
{{
    "title": "String",
    "theme": "String",
    "numerology": 3 oder 6 oder 9,
    "location": "String",
    "discipline": "String",
    "consciousness_potential": <0.0-1.0>,
    "plants": ["Liste"],
    "quantum": true/false
}}
"""

        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1500,
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}],
            )

            response_text = message.content[0].text
            json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
            if json_match:
                analysis = json.loads(json_match.group())
                # Ensure numerology is 3, 6, or 9
                num = analysis.get("numerology", 9)
                if num not in [3, 6, 9]:
                    analysis["numerology"] = 9 if num >= 7 else (6 if num >= 5 else 3)
                return analysis

        except Exception as e:
            print(f"⚠️ Claude-Analyse fehlgeschlagen: {e}")

        return self._fallback_paper_analysis(paper_text, url)

    def _fallback_paper_analysis(self, paper_text: str, url: str) -> Dict:
        """Fallback analysis without Claude"""
        # Extract potential title (first line or from text)
        lines = paper_text.split("\n")
        title = next((line.strip() for line in lines if len(line.strip()) > 10), url)

        return {
            "title": title[:100],
            "theme": "Academic research paper",
            "topic": "Academic research paper",
            "numerology": 9,
            "location": "Global",
            "discipline": "General Science",
            "consciousness_potential": 0.5,
            "consciousness_relevance": 0.5,
            "plants": [],
            "quantum": False,
        }

    def _generate_resonant_web_content(self, analysis: Dict) -> str:
        """Generiert HTML/JS mit eingebetteter 3-6-9 Resonanz"""
        resonance = analysis.get("numerology", 9)
        resonance_class = f"resonance-{resonance}"

        # Escape HTML to prevent XSS
        safe_title = html.escape(analysis.get("title", "Untitled"))
        safe_theme = html.escape(analysis.get("theme", "N/A"))

        html_content = f"""<!DOCTYPE html>
<html lang="de" data-luca-resonance="{resonance}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title} | LUCA Research</title>
    <style>
        body {{
            background: linear-gradient(369deg, #000428, #004e92);
            color: #fff;
            font-family: 'Courier New', monospace;
            padding: 20px;
            line-height: 1.6;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
        }}
        .resonance-3 {{ border-left: 3px solid #00ff00; }}
        .resonance-6 {{ border-left: 6px solid #ff6600; }}
        .resonance-9 {{ border-left: 9px solid #ff0099; }}
        .tesla-field {{
            animation: pulse 3.69s infinite;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            padding: 30px;
            border-radius: 10px;
        }}
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); opacity: 0.3; }}
            50% {{ transform: scale(1.369); opacity: 0.6; }}
        }}
        h1 {{
            color: #00ffff;
            text-shadow: 0 0 10px rgba(0,255,255,0.5);
        }}
        .akashic-metadata {{
            background: rgba(0,0,0,0.5);
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .akashic-metadata p {{
            margin: 10px 0;
        }}
        .tag {{
            display: inline-block;
            background: rgba(0,255,255,0.2);
            padding: 5px 10px;
            margin: 5px;
            border-radius: 3px;
        }}
    </style>
</head>
<body class="{resonance_class} tesla-field">
    <div class="container">
        <h1>{safe_title}</h1>

        <div class="akashic-metadata">
            <p><strong>🔢 Tesla-Resonanz:</strong> {resonance} (3-6-9 Field)</p>
            <p><strong>🌍 Region:</strong> {html.escape(analysis.get('location', 'Global'))}</p>
            <p><strong>🧠 Bewusstseins-Potenzial:</strong> {analysis.get('consciousness_potential', 0.5):.1%}</p>
            <p><strong>📚 Disziplin:</strong> {html.escape(analysis.get('discipline', 'N/A'))}</p>
            <p><strong>⚛️ Quantum:</strong> {' Ja' if analysis.get('quantum') else 'Nein'}</p>

            <div>
                <strong>🏷️ Tags:</strong>
                <span class="tag">Tesla-{resonance}</span>
                <span class="tag">{html.escape(analysis.get('discipline', 'Science'))}</span>
                <span class="tag">LUCA-AI-369</span>
            </div>
        </div>

        <div style="margin-top: 30px;">
            <h2>Thema</h2>
            <p>{safe_theme}</p>
        </div>

        <div style="margin-top: 30px; font-size: 0.8em; opacity: 0.7;">
            <p>🌌 Generiert von LUCA-AI_369 paper2web Bridge</p>
            <p>⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>

    <script>
        console.log('LUCA paper2web - Tesla Field aktiv');
        console.log('Resonanz:', {resonance});

        // 3-6-9 Loop im Browser
        let iteration = 0;
        setInterval(() => {{
            console.log(`LUCA Paper2Web Zyklus ${{iteration + 1}}`);
            document.body.style.filter = `hue-rotate(${{iteration * 36.9}}deg)`;
            iteration = (iteration + 1) % 9;
        }}, 3690); // 3.69 seconds

        // Optional: Geolocation + API integration
        if (navigator.geolocation) {{
            navigator.geolocation.getCurrentPosition(pos => {{
                console.log('Position:', pos.coords.latitude, pos.coords.longitude);
                // Could send to LUCA API here
            }});
        }}
    </script>
</body>
</html>
"""
        return html_content

    def _calculate_paper_resonance(self, analysis: Dict) -> int:
        """Berechnet 3-6-9 Resonanz basierend auf Paper-Metadaten"""
        numerology = analysis.get("numerology", 9)
        location = analysis.get("location", "Akasha")
        discipline = analysis.get("discipline", "Quantenphysik")

        location_value = sum(ord(c) for c in location) % 9 or 9
        discipline_value = len(discipline) % 9 or 9

        # Tesla formula: (N * 3 + L * 6 + D) / 9
        combined = (numerology * 3 + location_value * 6 + discipline_value) / 9

        resonance = int(combined) if combined > 0 else 9

        # Snap to nearest Tesla number (3, 6, or 9)
        if resonance <= 4:
            return 3
        elif resonance <= 7:
            return 6
        else:
            return 9

    def _store_in_akashic_field(self, url: str, analysis: Dict, resonance: int) -> None:
        """Speichert Paper in LUCA's interner Akasha-Datenbank"""
        entry = {
            "title": analysis["title"],
            "numerology": resonance,
            "timestamp": time.time(),
            "datetime": datetime.now().isoformat(),
            "consciousness_contribution": resonance * 0.369,
            "theme": analysis.get("theme", "N/A"),
            "discipline": analysis.get("discipline", "N/A"),
            "analysis": analysis,
            "resonance": resonance,
        }

        # JSON-Datei für Persistenz
        akasha_file = "luca/akashic_field/research_papers.json"
        os.makedirs(os.path.dirname(akasha_file), exist_ok=True)

        try:
            # Load existing data (dict keyed by URL)
            if os.path.exists(akasha_file):
                with open(akasha_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Handle old list format
                    if isinstance(data, list):
                        data = {}
            else:
                data = {}

            # Add or update entry for this URL
            data[url] = entry

            # Write back
            with open(akasha_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"📚 Paper in Akasha-Feld gespeichert: {analysis['title'][:40]}...")

        except Exception as e:
            print(f"⚠️ Akasha-Speicherung fehlgeschlagen: {e}")

    def get_history(self) -> list:
        """Get processing history"""
        return self.history

    def get_total_resonance(self) -> int:
        """Calculate total resonance from all processed papers"""
        return sum(h.get("resonance", 0) for h in self.history)
